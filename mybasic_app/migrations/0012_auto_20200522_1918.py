# Generated by Django 2.2.5 on 2020-05-22 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mybasic_app', '0011_auto_20200522_0034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commite',
            name='evaluteur_list',
            field=models.ManyToManyField(blank=True, null=True, to='mybasic_app.Evaluateur'),
        ),
        migrations.AlterField(
            model_name='evaluateur',
            name='artcl_a_corrige',
            field=models.ManyToManyField(blank=True, null=True, to='mybasic_app.Article'),
        ),
    ]
