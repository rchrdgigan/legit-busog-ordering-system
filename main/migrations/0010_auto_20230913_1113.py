# Generated by Django 2.1.15 on 2023-09-13 03:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20230912_1010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productinfo',
            name='category',
            field=models.IntegerField(),
        ),
    ]
