# Generated by Django 2.2.5 on 2020-05-21 00:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mybasic_app', '0005_auto_20200516_2145'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='reviwer_list',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mybasic_app.Evaluateur'),
        ),
    ]
