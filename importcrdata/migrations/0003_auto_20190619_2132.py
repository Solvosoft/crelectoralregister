# Generated by Django 2.2.1 on 2019-06-19 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('importcrdata', '0002_auto_20190619_2101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='distelec',
            name='canton',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='distelec',
            name='distrito',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='distelec',
            name='provincia',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='padronelectoral',
            name='junta',
            field=models.CharField(max_length=5),
        ),
    ]
