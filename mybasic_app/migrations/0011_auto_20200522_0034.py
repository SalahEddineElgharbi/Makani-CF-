# Generated by Django 2.2.5 on 2020-05-21 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mybasic_app', '0010_auto_20200522_0033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluateur',
            name='artcl_a_corrige',
            field=models.ManyToManyField(default='Article de Teste', to='mybasic_app.Article'),
        ),
    ]
