# Generated by Django 2.0.4 on 2018-05-01 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20180415_1945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=20, unique=True, verbose_name='标签'),
        ),
    ]