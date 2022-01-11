from django.db import models

# Create your models here.

class student(models.Model):
    cName = models.CharField(max_length=20, null=False)
    cSex = models.CharField(max_length=2, default='M', null=False)
    cBirthday = models.DateField(null=False)
    cEmail = models.EmailField(max_length=100, blank=True, default='')
    cPhone = models.CharField(max_length=50, blank=True, default='')
    cAddr = models.CharField(max_length=255, blank=True, default='')
    def __str__(self):
        return self.cName

class collection_table(models.Model):
    uName = models.CharField(max_length=500)
    book_Name = models.CharField(max_length=100)
    book_url = models.CharField(max_length=2000)
    book_Price = models.DecimalField(max_digits=12, decimal_places=3, default=0)
    book_Info = models.CharField(max_length=1000)
    lib = models.CharField(max_length=100, default="0")
    created_on = models.DateTimeField(auto_now_add=True)
