# Generated by Django 3.1.5 on 2021-01-17 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20210115_0208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='telegram_id',
            field=models.BigIntegerField(help_text='Telegram User ID', null=True, unique=True),
        ),
    ]
