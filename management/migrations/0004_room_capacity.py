# Generated by Django 4.2.17 on 2025-01-03 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0003_reservation'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='capacity',
            field=models.PositiveIntegerField(default=10),
            preserve_default=False,
        ),
    ]
