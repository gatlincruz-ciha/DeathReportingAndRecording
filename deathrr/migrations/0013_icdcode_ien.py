# Generated by Django 4.2.16 on 2025-01-24 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deathrr', '0012_alter_deceasedentry_dob'),
    ]

    operations = [
        migrations.AddField(
            model_name='icdcode',
            name='ien',
            field=models.IntegerField(default=1),
        ),
    ]
