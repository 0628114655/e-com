# Generated by Django 5.0.7 on 2024-08-04 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
