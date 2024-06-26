# Generated by Django 4.2.1 on 2023-08-10 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_walletssort_contract_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='cryptocompareassets',
            name='blockchain',
            field=models.CharField(blank=True, choices=[('BTC', 'Bitcoin'), ('ETH', 'Ethereum'), ('MATIC', 'Polygon')], max_length=8, null=True),
        ),
        migrations.AddField(
            model_name='cryptocompareassets',
            name='contract_address',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
