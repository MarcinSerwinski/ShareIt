from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Institution(models.Model):
    institution_types = [(1, 'Fundacja'),
                         (2, 'Organizacja pozarządowa'),
                         (3, 'Zbiórka lokalna')]

    name = models.CharField(max_length=200)
    description = models.TextField(null=True)
    type = models.IntegerField(choices=institution_types, default=1)
    categories = models.ManyToManyField('Category')

    def __str__(self):
        return self.name



class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField('Category')
    institution = models.ForeignKey('Institution', on_delete=models.CASCADE)
    address = models.CharField(max_length=250)
    phone_number = models.CharField(max_length=30)
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=20)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)




    def __str__(self):
        return f"quantity: {self.quantity}, adres: {self.address}, phone: {self.phone_number}, city: {self.city},  " \
               f"zip-code: {self.zip_code}, pick_up_date: {self.pick_up_date}, pick_up_time: {self.pick_up_time}"
