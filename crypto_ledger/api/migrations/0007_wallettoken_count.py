# Generated by Django 4.2.1 on 2023-08-04 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_wallettoken_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallettoken',
            name='count',
            field=models.IntegerField(default=0),
        ),
    ]
