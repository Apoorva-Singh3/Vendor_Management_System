# Generated by Django 4.2.7 on 2023-11-29 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_management_app', '0002_alter_vendor_contact_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='acknowledgment_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='issue_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
