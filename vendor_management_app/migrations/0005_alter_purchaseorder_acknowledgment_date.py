# Generated by Django 4.2.7 on 2023-11-29 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_management_app', '0004_alter_purchaseorder_acknowledgment_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='acknowledgment_date',
            field=models.DateTimeField(null=True),
        ),
    ]
