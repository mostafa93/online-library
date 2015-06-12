# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('OnlineBookLibrary', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='library_name',
            new_name='library',
        ),
        migrations.AlterField(
            model_name='library',
            name='library_owner',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
