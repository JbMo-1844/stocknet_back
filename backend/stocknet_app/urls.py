from django.http import JsonResponse
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ItemViewSet,
    PurchaseViewSet,
    ProcurementRequestViewSet,
    DeliveryViewSet,
    InvoiceViewSet,
    PaymentViewSet,
    GoodsReceiptViewSet,
    TenderViewSet,
    BidViewSet,
    MenuEntryViewSet,
    ReleaseEntryViewSet,
    AuthViewSet,
    UserManagementViewSet,
    AuditLogViewSet,
)

router = DefaultRouter()
router.register(r'items', ItemViewSet)
router.register(r'purchases', PurchaseViewSet)
router.register(r'procurement/requests', ProcurementRequestViewSet, basename='procurement-requests')
router.register(r'procurement/deliveries', DeliveryViewSet, basename='procurement-deliveries')
router.register(r'procurement/invoices', InvoiceViewSet, basename='procurement-invoices')
router.register(r'procurement/payments', PaymentViewSet, basename='procurement-payments')
router.register(r'procurement/tenders', TenderViewSet, basename='procurement-tenders')
router.register(r'procurement/bids', BidViewSet, basename='procurement-bids')
router.register(r'procurement/receipts', GoodsReceiptViewSet, basename='procurement-receipts')
router.register(r'menus', MenuEntryViewSet)
router.register(r'releases', ReleaseEntryViewSet)
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'users', UserManagementViewSet, basename='users')
router.register(r'audit-logs', AuditLogViewSet, basename='audit-logs')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', AuthViewSet.as_view({'post': 'create'}), name='auth-register'),
    path('auth/login/', AuthViewSet.as_view({'post': 'login'}), name='auth-login'),
    path('health/', lambda request: JsonResponse({'status': 'ok'})),
]
