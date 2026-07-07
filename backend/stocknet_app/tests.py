from django.test import SimpleTestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from .serializers import ItemSerializer
from .views import build_menu_inventory_alerts
from .models import AuthAccount


class AuthEndpointTests(APITestCase):
    def test_register_and_login_work_with_backend(self):
        register_url = reverse('auth-register')
        response = self.client.post(register_url, {
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'secret123',
            'role': 'storekeeper',
        }, format='json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()['email'], 'test@example.com')
        self.assertEqual(AuthAccount.objects.count(), 1)

        login_url = reverse('auth-login')
        login_response = self.client.post(login_url, {
            'email': 'test@example.com',
            'password': 'secret123',
        }, format='json')

        self.assertEqual(login_response.status_code, 200)
        self.assertEqual(login_response.json()['email'], 'test@example.com')
        self.assertEqual(login_response.json()['role'], 'storekeeper')


class AdminEndpointsTests(APITestCase):
    def test_users_and_audit_logs_are_available(self):
        create_response = self.client.post(reverse('users-list'), {
            'name': 'Admin User',
            'email': 'admin@example.com',
            'password': 'secret123',
            'role': 'admin',
            'performed_by': 'System',
        }, format='json')

        self.assertEqual(create_response.status_code, 201)

        users_response = self.client.get(reverse('users-list'))
        self.assertEqual(users_response.status_code, 200)
        self.assertGreaterEqual(len(users_response.json()), 1)

        logs_response = self.client.get(reverse('audit-logs-list'))
        self.assertEqual(logs_response.status_code, 200)
        self.assertGreaterEqual(len(logs_response.json()), 1)


class ItemSerializerTests(SimpleTestCase):
    def test_negative_quantity_is_rejected(self):
        item = type(
            'ItemStub',
            (),
            {
                'id': 1,
                'name': 'Rice',
                'category': 'Staples',
                'quantity': 15,
                'unit': 'kg',
                'reorder_level': 10,
                'status': 'Healthy',
            },
        )()

        serializer = ItemSerializer(instance=item, data={'quantity': -5}, partial=True)

        self.assertFalse(serializer.is_valid())
        self.assertIn('You are trying to release that which is not available.', serializer.errors['quantity'])


class AlertGenerationTests(SimpleTestCase):
    def test_missing_or_low_inventory_items_are_reported_for_menus(self):
        inventory_items = [
            type('ItemStub', (), {'name': 'Rice', 'quantity': 3})(),
            type('ItemStub', (), {'name': 'Beans', 'quantity': 10})(),
        ]
        menu_entries = [
            type('MenuStub', (), {'day': 'Monday', 'cell': 'A', 'meal_type': 'Breakfast', 'menu_items': [{'item': 'Rice', 'quantity': '5'}, {'item': 'Oil', 'quantity': '2'}]})(),
        ]

        alerts = build_menu_inventory_alerts(menu_entries, inventory_items)

        self.assertEqual(len(alerts), 2)
        self.assertEqual(alerts[0]['item'], 'Rice')
        self.assertEqual(alerts[0]['required_quantity'], 5)
        self.assertEqual(alerts[0]['available_quantity'], 3)
        self.assertEqual(alerts[1]['item'], 'Oil')
        self.assertEqual(alerts[1]['available_quantity'], 0)
