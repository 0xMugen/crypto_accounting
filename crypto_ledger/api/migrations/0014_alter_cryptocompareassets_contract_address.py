# Generated by Django 4.2.1 on 2023-08-10 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_alter_cryptocompareassets_blockchain'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cryptocompareassets',
            name='contract_address',
            field=models.TextField(blank=True, null=True),
        ),
    ]