# Generated by Django 2.2.5 on 2020-05-21 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mybasic_app', '0007_auto_20200521_0205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='reviwer_list',
            field=models.ManyToManyField(null=True, to='mybasic_app.Evaluateur'),
        ),
    ]