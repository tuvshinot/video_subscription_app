# Generated by Django 2.2.5 on 2019-09-04 18:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('memberships', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usermembership',
            old_name='membership_type',
            new_name='membership',
        ),
    ]