# Generated by Django 3.1.1 on 2020-09-14 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Scores',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('math', models.IntegerField()),
                ('english', models.IntegerField()),
                ('science', models.IntegerField()),
            ],
        ),
    ]
