# Generated by Django 2.2.3 on 2019-07-29 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_checker', '0002_auto_20190729_2049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='final_address',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='site',
            name='original_address',
            field=models.URLField(blank=True, null=True),
        ),
    ]