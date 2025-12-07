from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone


class Farmer(models.Model):
    objects = None
    phone_regex = RegexValidator(
        regex=r'^\+?254?\d{9,10}$',
        message="Phone number must be in format: '+254712345678' or '0712345678'"
    )

    farmer_id = models.CharField(max_length=20, unique=True, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(validators=[phone_regex], max_length=15, unique=True)
    id_number = models.CharField(max_length=20, unique=True)
    location = models.CharField(max_length=200)
    date_registered = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-date_registered']

    def save(self, *args, **kwargs):
        if not self.farmer_id:
            last_farmer = Farmer.objects.all().order_by('id').last()
            if last_farmer:
                last_id = int(last_farmer.farmer_id.split('-')[1])
                self.farmer_id = f'FMR-{str(last_id + 1).zfill(4)}'
            else:
                self.farmer_id = 'FMR-0001'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.farmer_id} - {self.first_name} {self.last_name}"

    def get_total_milk_collected(self):
        return self.collections.aggregate(models.Sum('quantity'))['quantity__sum'] or 0

    def get_collections_this_month(self):
        today = timezone.now()
        return self.collections.filter(
            collection_date__year=today.year,
            collection_date__month=today.month
        ).aggregate(models.Sum('quantity'))['quantity__sum'] or 0


class MilkCollection(models.Model):
    objects = None
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='collections')
    quantity = models.DecimalField(max_digits=10, decimal_places=2, help_text="Quantity in liters")
    collection_date = models.DateField(default=timezone.now)
    collection_time = models.TimeField(auto_now_add=True)
    price_per_liter = models.DecimalField(max_digits=10, decimal_places=2, default=50.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    sms_sent = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-collection_date', '-collection_time']
        unique_together = ['farmer', 'collection_date']

    def save(self, *args, **kwargs):
        self.total_amount = self.quantity * self.price_per_liter
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.farmer.farmer_id} - {self.quantity}L on {self.collection_date}"
