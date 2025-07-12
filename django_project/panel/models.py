from django.db import models
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.hashers import make_password

# Función para calcular el dígito verificador
def calcular_dv(rut_numeros):
    suma = 0
    multiplicador = 2

    for digito in reversed(str(rut_numeros)):
        suma += int(digito) * multiplicador
        multiplicador = 2 if multiplicador == 7 else multiplicador + 1

    resto = suma % 11
    dv = 11 - resto

    if dv == 11:
        return "0"
    elif dv == 10:
        return "K"
    else:
        return str(dv)


class TipoUsuario(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    permisos = models.ManyToManyField(Permission, blank=True)  # Relación con permisos

    def __str__(self):
        return self.nombre
class Usuarios(models.Model):
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]

    rut = models.CharField(max_length=12, unique=True)  # Ej: "12345678-9"
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)  # Ej: "+56 9 12345678"
    contraseña = models.CharField(max_length=128)  # Contraseña encriptada
    f_nac = models.DateField(null=True, blank=True)
    genero = models.CharField(max_length=10, choices=GENERO_CHOICES)
    f_registro = models.DateTimeField(auto_now_add=True)
    grupos = models.ManyToManyField(Group, related_name="usuarios", blank=True)

    def save(self, *args, **kwargs):
        """
        Sobrescribe el método save para asegurarse de que las contraseñas estén encriptadas antes de guardar.
        """
        if not self.pk or not Usuarios.objects.filter(pk=self.pk, contraseña=self.contraseña).exists():
            self.contraseña = make_password(self.contraseña)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.rut}"

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ['nombre']
class UsuariosInactivos(models.Model):
    rut = models.CharField(max_length=12)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo = models.EmailField()
    contraseña = models.CharField(max_length=128)  # Solo guardar la contraseña encriptada
    telefono = models.CharField(max_length=15)
    f_nac = models.DateField(null=True, blank=True)
    f_registro = models.DateTimeField()
    genero = models.CharField(max_length=10, choices=[('M', 'Masculino'), ('F', 'Femenino')])

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.rut}"
class Paciente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    edad = models.PositiveIntegerField()
    estado = models.CharField(
        max_length=20,
        choices=[
            ('En espera', 'En espera'),
            ('En triaje', 'En triaje'),
            ('En consulta', 'En consulta'),
            ('Atendido', 'Atendido'),
        ],
        default='En espera'
    )
    tiempo_ingreso = models.DateTimeField(auto_now_add=True)
    tiempo_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.estado}"