# Generated by Django 4.2.16 on 2025-01-22 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deathrr', '0009_alter_deceasedentry_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deceasedentry',
            name='last_modified_by',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]
