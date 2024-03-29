# Generated by Django 2.2.2 on 2019-06-13 08:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce_api', '0002_sellers_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sellers',
            name='seller_address',
            field=models.TextField(default='', null=True),
        ),
        migrations.AlterField(
            model_name='sellers',
            name='user',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
