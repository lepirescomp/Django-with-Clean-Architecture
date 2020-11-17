from django.db import models

# Create your models here.

class OrderLineORM(models.Model):
    reference = models.CharField(max_length=256, blank=True, null=True)
    sku = models.CharField(max_length=256, blank=True, null=True)
    qty = models.IntegerField(blank=True, null=True)

class BatchORM(models.Model):
    reference = models.CharField(max_length=256,blank=True, null=True)
    sku = models.CharField(max_length=256,blank=True, null=True)
    qty = models.IntegerField(blank=True, null=True)
    eta = models.DateTimeField(blank=True, null=True)

class AllocationsORM(models.Model):
    batch = models.ForeignKey("BatchORM", related_name="batch", on_delete=models.CASCADE, blank=True, null=True)
    order_line = models.ForeignKey("OrderLineORM", related_name="order_line", on_delete=models.CASCADE, blank=True, null=True)