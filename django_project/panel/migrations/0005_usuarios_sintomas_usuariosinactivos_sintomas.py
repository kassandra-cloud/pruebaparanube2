# Generated by Django 4.2.4 on 2024-12-09 01:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0004_remove_usuariosinactivos_contraseña_original_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuarios',
            name='sintomas',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='usuariosinactivos',
            name='sintomas',
            field=models.TextField(blank=True, null=True),
        ),
    ]
