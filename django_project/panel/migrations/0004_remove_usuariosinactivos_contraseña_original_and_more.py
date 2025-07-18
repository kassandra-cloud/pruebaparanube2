# Generated by Django 4.2.4 on 2024-12-04 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0003_alter_usuarios_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuariosinactivos',
            name='contraseña_original',
        ),
        migrations.RemoveField(
            model_name='usuariosinactivos',
            name='fecha_inactivacion',
        ),
        migrations.AlterField(
            model_name='usuariosinactivos',
            name='apellido',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='usuariosinactivos',
            name='correo',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='usuariosinactivos',
            name='f_nac',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='usuariosinactivos',
            name='f_registro',
            field=models.DateTimeField(default='2023-01-01 00:00:00'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='usuariosinactivos',
            name='genero',
            field=models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino')], max_length=10),
        ),
        migrations.AlterField(
            model_name='usuariosinactivos',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='usuariosinactivos',
            name='nombre',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='usuariosinactivos',
            name='rut',
            field=models.CharField(max_length=12),
        ),
        migrations.AlterModelTable(
            name='usuariosinactivos',
            table=None,
        ),
    ]
