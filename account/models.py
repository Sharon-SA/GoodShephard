from django.db import models
from django.conf import settings
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, blank=False, null=False, default='a')
    last_name = models.CharField(max_length=50, blank=False, null=False, default='a')
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=20, blank=False, null=False)
    address = models.CharField(max_length=100, blank=False, null=False)
    city = models.CharField(max_length=50, blank=False, null=False)
    state = models.CharField(max_length=2, blank=False, null=False)
    zip = models.CharField(max_length=5, blank=False, null=False)
    phone = models.CharField(max_length=10, blank=False, null=False)

    def __str__(self):
        return f'Profile for user {self.user.username}'


class Client(models.Model):
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)
    date_of_birth = models.DateField(blank=False, null=False)
    gender = models.CharField(max_length=20, blank=False, null=False)
    address = models.CharField(max_length=100, blank=False, null=False)
    city = models.CharField(max_length=50, blank=False, null=False)
    state = models.CharField(max_length=2, blank=False, null=False)
    zip = models.CharField(max_length=5, blank=False, null=False)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    # username = models.CharField(max_length=50, blank=False, null=False)
    # password = models.CharField(max_length=50, blank=False, null=False)
    referred_by = models.CharField(max_length=1000)
    reffered_to = models.CharField(max_length=1000)
    created_date = models.DateTimeField(default=timezone.now)

    def created(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return self.first_name + " " + self.last_name


class Visit(models.Model):
    visit_note = models.CharField(max_length=2000)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)

    def created(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.created_date)


class Inventory(models.Model):
    UPScode = models.CharField(max_length=15)
    item_description = models.CharField(max_length=100)
    total_quantity = models.IntegerField(blank=True, null=False, default=0)
    created_date = models.DateTimeField(default=timezone.now)

    def created(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.item_description)


class Order(models.Model):
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    UPScode = models.ForeignKey(Inventory, on_delete=models.SET_NULL, blank=True, null=True, related_name='inventory_UPScode')
    item_description = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='inventory_item_description')
    request_quantity = models.IntegerField(blank=False, null=False)
    delivered_quantity = models.IntegerField(blank=False, null=False)
    date = models.DateTimeField(default=timezone.now)
    created_date = models.DateTimeField(default=timezone.now)

    def created(self):
        self.created_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.item_description)
