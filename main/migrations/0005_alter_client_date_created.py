# Generated by Django 4.0.5 on 2022-08-08 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_client_date_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
