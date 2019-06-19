# Generated by Django 2.2.1 on 2019-06-19 20:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Distelec',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codele', models.CharField(max_length=6)),
                ('provincia', models.CharField(max_length=26)),
                ('canton', models.CharField(max_length=26)),
                ('distrito', models.CharField(max_length=26)),
            ],
        ),
        migrations.CreateModel(
            name='PadronElectoral',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cedula', models.CharField(max_length=9)),
                ('codele', models.CharField(max_length=6)),
                ('sexo', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(2)])),
                ('fechacaduc', models.CharField(max_length=8)),
                ('junta', models.CharField(max_length=5)),
                ('nombre_completo', models.CharField(max_length=90)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
