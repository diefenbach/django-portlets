# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='PortletAssignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content_id', models.PositiveIntegerField()),
                ('portlet_id', models.PositiveIntegerField()),
                ('position', models.PositiveSmallIntegerField(default=999, verbose_name='Position')),
                ('content_type', models.ForeignKey(related_name='pa_content', to='contenttypes.ContentType')),
                ('portlet_type', models.ForeignKey(related_name='pa_portlets', to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ['position'],
                'verbose_name_plural': 'Portlet assignments',
            },
        ),
        migrations.CreateModel(
            name='PortletBlocking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(related_name='pb_content', to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='PortletRegistration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(unique=True, max_length=30, verbose_name='Type')),
                ('name', models.CharField(unique=True, max_length=50, verbose_name='Name')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
            ],
            options={
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Slot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
            ],
        ),
        migrations.AddField(
            model_name='portletblocking',
            name='slot',
            field=models.ForeignKey(verbose_name='Slot', to='portlets.Slot'),
        ),
        migrations.AddField(
            model_name='portletassignment',
            name='slot',
            field=models.ForeignKey(verbose_name='Slot', to='portlets.Slot'),
        ),
        migrations.AlterUniqueTogether(
            name='portletblocking',
            unique_together=set([('slot', 'content_id', 'content_type')]),
        ),
    ]
