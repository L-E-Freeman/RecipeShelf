# Generated by Django 3.2.4 on 2021-07-04 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_methodstep'),
    ]

    operations = [
        migrations.AlterField(
            model_name='methodstep',
            name='step',
            field=models.TextField(verbose_name=''),
        ),
    ]
