# Generated by Django 4.1.2 on 2022-11-27 03:46

from django.db import migrations, models
import myapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_alter_order_status_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='profile_pic',
            field=models.ImageField(null=True, upload_to='uploads/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='stock',
            field=models.PositiveIntegerField(default=100, validators=[myapp.models.validate_stock]),
        ),
    ]
