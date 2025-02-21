from django.db import models


class Request(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('finished', 'Finished'),
    ]
    TYPE_CHOICES = [
        ('center', 'Center'),
        ('customer', 'Customer'),
    ]
    SERVICE_CHOICES = [
        ('car', 'Car'),
        ('home', 'Home')
    ]
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=15)
    message = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')
    type = models.CharField(max_length=15, choices=TYPE_CHOICES, default='')
    service = models.CharField(max_length=15, choices=SERVICE_CHOICES, default='')

    def __str__(self):
        return f"{self.name} ({self.status})"


class Picture(models.Model):
    picture_title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/project_images/', max_length=200)

    class Meta:
        ordering = ["pk"]

    def __str__(self):
        return self.picture_title
