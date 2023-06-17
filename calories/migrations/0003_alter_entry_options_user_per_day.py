# Generated by Django 4.1.4 on 2023-06-16 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calories', '0002_entry'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entry',
            options={'verbose_name_plural': 'Entries'},
        ),
        migrations.AddField(
            model_name='user',
            name='per_day',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=16),
        ),
    ]
