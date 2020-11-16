from django.db import models

# Create your models here.

class OrderLineORM(models.Model):
    reference = models.CharField(max_length=256)
    sku = models.CharField(max_length=256)
    qty = models.IntegerField()

class BatchORM(models.Model):
    reference = models.CharField(max_length=256)
    sku = models.CharField(max_length=256)
    qty = models.IntegerField()
    eta = models.DateTimeField()
    allocated = models.ForeignKey("OrderLineORM", related_name="order_lines", on_delete=models.CASCADE)