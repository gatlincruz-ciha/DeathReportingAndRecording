# Generated by Django 4.2.16 on 2025-01-22 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deathrr', '0007_alter_deceasedentry_race'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deceasedentry',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='deceasedentry',
            name='last_modified_at',
        ),
        migrations.AlterField(
            model_name='deceasedentry',
            name='created_by',
            field=models.CharField(default='jill.sain@cherokeehospital.org', max_length=100),
        ),
    ]
