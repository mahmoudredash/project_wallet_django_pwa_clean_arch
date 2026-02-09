from django.db import models
from django.contrib.auth.models import User

# Create your models here.

CATEGORIES =(
    ('income', 'Income'),
    ('expense', 'Expense')
)


class  Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=CATEGORIES)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


    def __str__(self):
        return self.name


class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField('Amount',max_digits=64, decimal_places=2)
    source = models.CharField(max_length=100)
    date_received = models.DateField('Date Received')

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField('Description', null=True , blank=True)

    date_created = models.DateTimeField('Date Created', auto_now_add=True)
    date_updated = models.DateTimeField('Date Updated', auto_now=True)

    def __str__(self):
        return f"{self.amount} From {self.source} by {self.user}"


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField('Amount',max_digits=64, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    date_incurred = models.DateField('Date Incurred')
    description = models.TextField('Description', null=True , blank=True)

    receipt_image = models.ImageField('Receipt Image', upload_to='receipts/', null=True, blank=True)

    date_created = models.DateTimeField('Date Created', auto_now_add=True)
    date_updated = models.DateTimeField('Date Updated', auto_now=True)

    def __str__(self):
        return f"{self.amount} on {self.date_incurred} for {self.category}"
