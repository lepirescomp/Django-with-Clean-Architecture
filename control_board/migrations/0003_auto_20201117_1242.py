# Generated by Django 3.1.3 on 2020-11-17 12:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('control_board', '0002_auto_20201117_1240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batchorm',
            name='allocated',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order_lines', to='control_board.orderlineorm'),
        ),
        migrations.AlterField(
            model_name='batchorm',
            name='eta',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='batchorm',
            name='qty',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='batchorm',
            name='reference',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='batchorm',
            name='sku',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
