# Generated by Django 4.2.4 on 2023-08-21 12:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="address",
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="age",
            field=models.IntegerField(null=True),
        ),
    ]
