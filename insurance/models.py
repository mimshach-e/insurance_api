from django.db import models
from django.urls import reverse


# Creating Customer Model.
class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Ordering by Name of Customer
    class Meta:
        ordering = ['name']


    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        """ Used by CreateView and UpdateView to redirect after a successful save,
and by templates to link to this customer's detail page."""
        
        return reverse('customer_app:customer_detail', kwargs={'pk': self.pk})



# Creating Policy Product
class PolicyProduct(models.Model):
    """Types of policies the company sells"""
    POLICY_TYPES = [
        ("life", "Life"),
        ("home", "Home"),
        ("health", "Health"),
        ("car", "Car"),
        ("travel", "Travel"),
        ("business", "Business"),
    ]

    name = models.CharField(max_length=100, unique=True)
    policy_type = models.CharField(max_length=20, choices=POLICY_TYPES)
    base_premium = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["policy_type", "name"]

    def __str__(self):
        return self.name


    # Creating Customer Policy
class CustomerPolicy(models.Model):
    """Specific policy a customer creates"""
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("active", "Active"),
        ("lapsed", "Lapsed"),
        ("canceled", "Cancelled"),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="policies")
    product = models.ForeignKey(PolicyProduct, on_delete=models.PROTECT, related_name="enrollments")
    policy_number = models.CharField(max_length=50, unique=True)
    actual_premium = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]


    def __str__(self):
        return f"{self.policy_number} - {self.customer.name} ({self.product.name})"


