# Generated by Django 4.2.1 on 2023-08-10 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_alter_ledgers_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactions',
            name='contract_address',
            field=models.CharField(blank=True, max_length=66, null=True),
        ),
        migrations.AddField(
            model_name='wallettoken',
            name='contract_address',
            field=models.CharField(blank=True, max_length=66, null=True),
        ),
    ]
