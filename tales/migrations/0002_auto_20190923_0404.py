# Generated by Django 2.2.4 on 2019-09-23 03:04

from django.db import migrations
import djangoeditorwidgets.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tales', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=djangoeditorwidgets.fields.XMLField(blank=True, null=True),
        ),
    ]
