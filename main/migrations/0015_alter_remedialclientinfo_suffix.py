# Generated by Django 4.0.5 on 2022-09-05 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_alter_remedialclientinfo_suffix'),
    ]

    operations = [
        migrations.AlterField(
            model_name='remedialclientinfo',
            name='suffix',
            field=models.TextField(blank=True, error_messages={'invalid': 'Please enter only digits'}, max_length=4, null=True),
        ),
    ]