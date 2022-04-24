# Generated by Django 4.0.3 on 2022-04-17 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='名前')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='生年月日')),
            ],
        ),
    ]