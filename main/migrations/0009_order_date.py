# Generated by Django 2.1.15 on 2023-09-19 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_personinfo_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='date',
            field=models.DateTimeField(null=True),
        ),
    ]
