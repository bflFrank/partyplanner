# Generated by Django 3.1.2 on 2020-12-20 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0004_auto_20201027_1020'),
    ]

    operations = [
        migrations.CreateModel(
            name='Party',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.IntegerField(choices=[(0, 'Sunday'), (1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday')])),
                ('start', models.TimeField()),
                ('end', models.TimeField()),
                ('persons', models.ManyToManyField(to='planner.Person')),
            ],
        ),
    ]
