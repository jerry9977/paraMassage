# Generated by Django 4.0.5 on 2022-09-21 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_alter_remedialclientinfo_suffix'),
    ]

    operations = [
        migrations.AddField(
            model_name='remedialmedicalhistory',
            name='remedial_treatment_plan',
            field=models.TextField(blank=True, null=True),
        ),
    ]
