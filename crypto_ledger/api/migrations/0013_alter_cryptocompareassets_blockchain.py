# Generated by Django 4.2.1 on 2023-08-10 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_cryptocompareassets_blockchain_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cryptocompareassets',
            name='blockchain',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
