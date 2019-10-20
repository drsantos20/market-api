# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.contrib.auth.admin import User


def create_user(apps, schema_editor):
    user = User()
    user.is_active = True
    user.is_user = True
    user.is_staff = True
    user.username = 'admin'
    user.email = 'admin@dc.com'
    user.set_password('password')
    user.save()


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.RunPython(create_user)
    ]
