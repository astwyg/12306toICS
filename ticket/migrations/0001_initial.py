# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20, verbose_name=b'\xe5\xa7\x93\xe5\x90\x8d')),
                ('time', models.CharField(max_length=40, verbose_name=b'\xe5\xbc\x80\xe8\xbd\xa6\xe6\x97\xb6\xe9\x97\xb4')),
                ('dist', models.CharField(max_length=40, verbose_name=b'\xe4\xb9\x98\xe8\xbd\xa6\xe5\x8c\xba\xe9\x97\xb4')),
                ('no', models.CharField(max_length=10, verbose_name=b'\xe8\xbd\xa6\xe6\xac\xa1')),
                ('seat', models.CharField(max_length=20, verbose_name=b'\xe5\xba\xa7\xe4\xbd\x8d')),
                ('sender', models.CharField(max_length=50, verbose_name=b'\xe5\x8f\x91\xe4\xbf\xa1\xe9\x82\xae\xe7\xae\xb1')),
            ],
        ),
    ]
