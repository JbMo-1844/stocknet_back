from django.db import models


class AuditLog(models.Model):
    actor = models.CharField(max_length=120, default='System')
    action = models.CharField(max_length=120)
    details = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.actor} - {self.action}"


class AuthAccount(models.Model):
    ROLE_CHOICES = [
        ('admin', 'admin'),
        ('procurement-officer', 'procurement-officer'),
        ('storekeeper', 'storekeeper'),
        ('stock-keeper', 'stock-keeper'),
    ]

    name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=200)
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='storekeeper')

    def __str__(self):
        return self.email


class Item(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)
    unit = models.CharField(max_length=50, default='kg')
    reorder_level = models.IntegerField(default=0)
    status = models.CharField(max_length=20, default='Healthy')

    class Meta:
        unique_together = ('name', 'category')

    def __str__(self):
        return self.name


class Purchase(models.Model):
    supplier = models.CharField(max_length=150)
    invoice = models.CharField(max_length=50, unique=True)
    item = models.CharField(max_length=100)
    quantity = models.CharField(max_length=50)
    amount = models.CharField(max_length=50)
    status = models.CharField(max_length=30, default='Pending')
    date = models.CharField(max_length=20)
    purchaser = models.CharField(max_length=100)
    note = models.TextField(blank=True)

    def __str__(self):
        return self.invoice


class ProcurementRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    department = models.CharField(max_length=120)
    justification = models.TextField()
    budget_estimate = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Pending')
    requested_items = models.JSONField(default=list)
    submitted_by = models.CharField(max_length=120, default='System')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.department} request #{self.id}"


class Delivery(models.Model):
    reference = models.CharField(max_length=100, unique=True)
    supplier = models.CharField(max_length=150)
    expected_on = models.CharField(max_length=20)
    status = models.CharField(max_length=30, default='Arriving')
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reference


class Invoice(models.Model):
    invoice_number = models.CharField(max_length=100, unique=True)
    supplier = models.CharField(max_length=150)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=30, default='Pending')
    due_date = models.CharField(max_length=20)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.invoice_number


class Payment(models.Model):
    payment_reference = models.CharField(max_length=100, unique=True)
    invoice_number = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=30, default='Pending')
    paid_on = models.CharField(max_length=20)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_reference


class Tender(models.Model):
    reference = models.CharField(max_length=100, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    specification = models.TextField(blank=True)
    closing_date = models.CharField(max_length=20)
    published = models.BooleanField(default=False)
    created_by = models.CharField(max_length=120, default='System')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reference


class Bid(models.Model):
    tender = models.ForeignKey(Tender, related_name='bids', on_delete=models.CASCADE)
    bidder_name = models.CharField(max_length=120)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    details = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bidder_name} - {self.tender.reference}"


class GoodsReceipt(models.Model):
    receipt_number = models.CharField(max_length=100, unique=True)
    purchase_order = models.CharField(max_length=100)
    received_on = models.CharField(max_length=20)
    status = models.CharField(max_length=30, default='Pending')
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.receipt_number


class MenuEntry(models.Model):
    day = models.CharField(max_length=20)
    cell = models.CharField(max_length=10)
    cell_leader = models.CharField(max_length=100)
    meal_type = models.CharField(max_length=20)
    meal_name = models.CharField(max_length=100)
    menu_items = models.JSONField(default=list)

    def __str__(self):
        return f"{self.day} - {self.meal_type}"


class ReleaseEntry(models.Model):
    day = models.CharField(max_length=20)
    meal_type = models.CharField(max_length=20)
    person_given = models.CharField(max_length=100)
    item = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)
    unit = models.CharField(max_length=50)
    note = models.TextField(blank=True)

    def __str__(self):
        return f"{self.item} - {self.day}"
