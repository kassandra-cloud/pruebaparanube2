from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Usuarios,UsuariosInactivos,Paciente
import secrets
import random
import string
import re  # Para validaciones con expresiones regulares
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.core.mail import send_mail
from django.http import JsonResponse
from django.contrib.auth.models import Group
from django.contrib.auth.hashers import make_password
#from .models import Usuario
from django.contrib.auth.hashers import check_password 
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import logout
from django.shortcuts import redirect
import logging
logger = logging.getLogger(__name__)
from django.core.mail import EmailMessage

def obtener_permisos_por_grupo(request, grupo_id):
    """
    Devuelve los permisos asociados a un grupo en formato JSON.
    """
    try:
        # Obtiene el grupo por su ID
        grupo = Group.objects.get(id=grupo_id)
        
        # Extrae los permisos del grupo
        permisos = grupo.permissions.values("id", "name")
        
        # Devuelve los permisos en formato JSON
        return JsonResponse({"success": True, "permisos": list(permisos)}, status=200)
    except Group.DoesNotExist:
        # Maneja el caso en que el grupo no existe
        return JsonResponse({"success": False, "error": "Grupo no encontrado."}, status=404)
def index(request):
    return render(request, "index.html")

def listar(request):
    orden = request.GET.get("orden", "nombre_asc")
    if orden == "nombre_asc":
        users = Usuarios.objects.all().order_by("nombre")
    elif orden == "nombre_desc":
        users = Usuarios.objects.all().order_by("-nombre")
    else:
        users = Usuarios.objects.all()

    users = users.prefetch_related("grupos")

    return render(request, "crud_usuarios/listar.html", {"usuarios": users, "orden": orden})
def agregar_grupo(request):
    if request.method == "POST":
        # Obtener datos del formulario
        nombre_grupo = request.POST.get("nombre")  # Nombre del grupo
        permisos_seleccionados = request.POST.getlist("permisos")  # Permisos seleccionados
        permisos_personalizados = request.POST.getlist("permisos_personalizados")  # Permisos personalizados

        # Verificar si el grupo ya existe
        if Group.objects.filter(name=nombre_grupo).exists():
            # Mostrar advertencia de grupo ya existente
            messages.warning(request, f"El grupo '{nombre_grupo}' ya existe. Intenta con otro nombre.")
            return redirect('agregar_grupo')  # Redirigir para mostrar el mensaje

        # Crear el grupo
        grupo = Group.objects.create(name=nombre_grupo)

        # Procesar permisos personalizados
        for permiso_nombre in permisos_personalizados:
            permiso_nombre = permiso_nombre.strip()  # Elimina espacios innecesarios
            if permiso_nombre:  # Verifica que el nombre no esté vacío
                # Crear el permiso personalizado
                content_type = ContentType.objects.get_for_model(Group)  # Asociar al modelo Group
                nuevo_permiso, created = Permission.objects.get_or_create(
                    codename=permiso_nombre.lower().replace(" ", "_"),  # Crear un codename único
                    name=permiso_nombre,
                    content_type=content_type,
                )
                # Agregar el permiso al listado de permisos seleccionados
                permisos_seleccionados.append(nuevo_permiso.id)

        # Asignar los permisos seleccionados al grupo
        grupo.permissions.set(Permission.objects.filter(id__in=permisos_seleccionados))
        grupo.save()

        # Redirigir después de guardar
        return redirect('agregar')  # Redirige a la lista de grupos o a otra vista

    # Obtener permisos y grupos existentes para mostrar en la plantilla
    permisos = Permission.objects.all().order_by('name')
    return render(request, 'crud_grupo/agregar_grupo.html', {'permisos': permisos})

def generar_contrasena():
    # Incluye letras, números y caracteres especiales
    caracteres = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(caracteres) for _ in range(12))

def generar_password_ajax(request):
    if request.method == 'POST':  # Comprueba si el método HTTP es POST
        # Incluye letras, números y caracteres especiales
        caracteres = string.ascii_letters + string.digits + string.punctuation
        contraseña = ''.join(random.choices(caracteres, k=12))  # Genera una contraseña de 12 caracteres
        return JsonResponse({'contraseña': contraseña})  # Devuelve la contraseña en formato JSON
    return JsonResponse({'error': 'Método no permitido'}, status=405)  # Error para métodos no permitidos

def enviar_correo(correo, nombre, apellido, contraseña_generada):
    """Envía un correo con las credenciales del usuario."""
    asunto = "Detalles de tu nueva cuenta"
    mensaje = f"""
    Hola {nombre} {apellido},

    Tu cuenta ha sido creada exitosamente. Aquí están tus credenciales:

    Usuario: {correo}
    Contraseña: {contraseña_generada}

    Por favor, inicia sesión y cambia tu contraseña en cuanto te sea posible.

    Atentamente,
    Equipo del Hospital de Alto Hospicio
    """

    try:
        # Configuración del correo con codificación UTF-8
        email = EmailMessage(
            asunto,
            mensaje,
            'tu_correo@gmail.com',  # Dirección del remitente
            [correo],               # Destinatarios
        )
        email.content_subtype = "plain"  # Define el contenido como texto plano
        email.charset = "utf-8"          # Asegura la codificación UTF-8
        email.send()
    except Exception as e:
        raise Exception(f"Error al enviar el correo: {e}")

def agregar(request):
    error_message = None

    if request.method == "POST":
        # Capturar datos del formulario
        rut_numeros = request.POST.get("rut_numeros", "").strip()
        rut_dv = request.POST.get("rut_dv", "").strip().upper()
        nombre = request.POST.get("nombre", "").strip()
        apellido = request.POST.get("apellido", "").strip()
        correo = request.POST.get("correo", "").strip()
        telefono = request.POST.get("telefono", "").strip()
        f_nac = request.POST.get("f_nac", "").strip()
        genero = request.POST.get("genero", "").strip()
        grupo_ids = request.POST.getlist("grupos")
        contraseña_generada = generar_contrasena()

        # Validaciones
        if not rut_numeros or not rut_dv:
            error_message = "El RUT es obligatorio."
        elif not re.match(r"^\d+$", rut_numeros):
            error_message = "El RUT debe contener solo números."
        elif Usuarios.objects.filter(rut=f"{rut_numeros}-{rut_dv}").exists():
            error_message = f"El RUT {rut_numeros}-{rut_dv} ya está registrado."
        elif not nombre:
            error_message = "El nombre es obligatorio."
        elif not apellido:
            error_message = "El apellido es obligatorio."
        elif not correo:
            error_message = "El correo es obligatorio."
        elif not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", correo):
            error_message = "El correo no es válido."
        else:
            try:
                # Crear el usuario
                usuario = Usuarios.objects.create(
                    rut=f"{rut_numeros}-{rut_dv}",
                    nombre=nombre,
                    apellido=apellido,
                    correo=correo,
                    telefono=f"+56 9 {telefono}",
                    f_nac=f_nac or None,
                    genero=genero,
                    contraseña=make_password(contraseña_generada),
                )

                # Asociar grupos
                if grupo_ids:
                    grupos = Group.objects.filter(id__in=grupo_ids)
                    usuario.grupos.set(grupos)
                usuario.save()

                # Enviar correo con las credenciales
                enviar_correo(correo, nombre, apellido, contraseña_generada)

                # Mensaje de éxito
                messages.success(
                    request,
                    f"El usuario {nombre} {apellido} ha sido agregado correctamente. Las credenciales se han enviado al correo proporcionado."
                )
                return redirect("listar")
            except Exception as e:
                error_message = f"Hubo un error al agregar el usuario o enviar el correo: {e}"

    # Obtener lista de grupos
    grupos = Group.objects.all()
    return render(request, "crud_usuarios/agregar.html", {"error_message": error_message, "grupos": grupos})

def actualizar(request):
    error_message = None

    if request.method == 'POST':
        user_id = request.POST.get("id")
        user = get_object_or_404(Usuarios, id=user_id)

        nombre = request.POST.get("nombre").strip()
        apellido = request.POST.get("apellido").strip()

        # Validar nombre y apellido
        if not re.match("^[A-Za-zÀ-ÿ\s]+$", nombre):
            error_message = "El nombre solo puede contener letras y espacios."
        elif not re.match("^[A-Za-zÀ-ÿ\s]+$", apellido):
            error_message = "El apellido solo puede contener letras y espacios."
        else:
            telefono = request.POST.get("telefono").strip()
            telefono_completo = f"+56 9 {telefono}"  # Reconstruir el número completo

            if not re.match(r"^\+56 9 [0-9]{8}$", telefono_completo):
                error_message = "El teléfono debe tener el formato +56 9 XXXXXXXX, donde X son números."
            else:
                # Actualizar el usuario si no hay errores
                user.nombre = nombre
                user.apellido = apellido
                user.correo = request.POST.get("correo")
                user.telefono = telefono_completo
                user.f_nac = request.POST.get("f_nac")
                
                grupo_ids = request.POST.getlist("grupos")  # IDs de los grupos seleccionados
                if grupo_ids:
                    grupos = Group.objects.filter(id__in=grupo_ids)
                    user.grupos.set(grupos)  # Asignar los grupos al usuario
                user.save()

                # Agregar mensaje de éxito
                messages.success(request, f"El usuario {nombre} {apellido} ha sido actualizado correctamente.")
                return redirect('listar')

    user_id = request.GET.get("id")
    usuario = None
    telefono = ""
    if user_id:
        usuario = get_object_or_404(Usuarios, id=user_id)
        # Asignar solo los 8 dígitos del teléfono
        telefono = usuario.telefono[6:]  # Asumiendo que el formato es '+56 9 XXXXXXXX'

    # Cargar grupos para el formulario y asignar los grupos del usuario
    grupos = Group.objects.all()
    selected_grupos = usuario.grupos.values_list('id', flat=True)

    datos = {
        'usuario': usuario,
        'usuarios': Usuarios.objects.all(),
        'error_message': error_message,
        'telefono': telefono,  # Pasar solo los 8 dígitos del teléfono
        'grupos': grupos,
        'selected_grupos': selected_grupos,  # Listado de grupos seleccionados
    }
    return render(request, "crud_usuarios/actualizar.html", datos)

def eliminar(request, id):
    try:
        # Obtener el usuario que se desea inactivar
        usuario = get_object_or_404(Usuarios, id=id)

        # Mover los datos del usuario a la tabla `UsuariosInactivos`
        UsuariosInactivos.objects.create(
            rut=usuario.rut,
            nombre=usuario.nombre,
            apellido=usuario.apellido,
            correo=usuario.correo,
            contraseña=usuario.contraseña,  # Guardar solo la contraseña encriptada
            telefono=usuario.telefono,
            f_nac=usuario.f_nac,
            f_registro=usuario.f_registro,
            genero=usuario.genero,
        )

        # Eliminar al usuario de la tabla original
        usuario.delete()

        # Agregar mensaje de éxito
        messages.success(request, f"El usuario {usuario.nombre} {usuario.apellido} ha sido inactivado correctamente.")
        return redirect('listar')  # Redirige a la lista de usuarios después de inactivar

    except Exception as e:
        # Si ocurre un error, agregar un mensaje de error
        messages.error(request, f"Error al intentar inactivar el usuario: {e}")
        return redirect('listar')
    
def iniciar_admin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Verificamos si el nombre de usuario es el único permitido 
        if username == 'administrador':
            user = authenticate(request, username=username, password=password)

            if user is not None:  # Autenticación exitosa
                login(request, user)
                return redirect('index')  # Redirige al index
            else:
                messages.error(request, 'Credenciales incorrectas')
        else:
            messages.error(request, 'Usuario no autorizado')

    return render(request, 'login.html')
# Vista para cerrar sesión
def logout_admin(request):
    if request.user.is_authenticated:
        logout(request)
        logger.info("Redirigiendo al login después del logout")
        messages.success(request, "Has cerrado sesión correctamente.")
    else:
        messages.warning(request, "No estabas autenticado.")
    return redirect('/')


# Vista para la página principal (index)
def index(request):
    return render(request, 'index.html')


def editar_grupo(request, grupo_id):
    # Obtener el grupo que se desea editar
    grupo = get_object_or_404(Group, id=grupo_id)

    # Cargar permisos disponibles
    permisos = Permission.objects.all()

    if request.method == 'POST':
        # Actualizar nombre del grupo
        nuevo_nombre = request.POST.get('nombre')
        grupo.name = nuevo_nombre

        # Actualizar permisos seleccionados
        permisos_seleccionados = request.POST.getlist('permisos')
        grupo.permissions.set(permisos_seleccionados)

        # Guardar los cambios
        grupo.save()

        messages.success(request, 'Grupo actualizado con éxito.')
        return redirect('editar_grupo', grupo_id=grupo.id)

    # Renderizar la plantilla con datos del grupo
    context = {
        'grupo': grupo,
        'permisos': permisos,
        'permisos_grupo': grupo.permissions.all(),
    }
    return render(request, 'crud_grupo/editar_grupo.html', context)

def listar_grupos(request):
    grupos = Group.objects.all()
    return render(request, 'crud_grupo/listar_grupos.html', {'grupos': grupos})
def eliminar_grupo(request, grupo_id):
    grupo = get_object_or_404(Group, id=grupo_id)
    if request.method == "POST":
        grupo.delete()
        messages.success(request, "El grupo ha sido eliminado exitosamente.")
    return redirect('listar_grupos')  # Usa el nombre de la vista, no el archivo HTML
def listar_usuarios_inactivos(request):
    """
    Lista los usuarios inactivos desde la tabla UsuariosInactivos.
    """
    usuarios_inactivos = UsuariosInactivos.objects.all()
    return render(request, 'crud_usuarios/listarinactivos.html', {'usuarios_inactivos': usuarios_inactivos})
def reactivar_usuario(request, id):
    usuario_inactivo = get_object_or_404(UsuariosInactivos, id=id)
    Usuarios.objects.create(
        rut=usuario_inactivo.rut,
        nombre=usuario_inactivo.nombre,
        apellido=usuario_inactivo.apellido,
        correo=usuario_inactivo.correo,
        contraseña=usuario_inactivo.contraseña,
        telefono=usuario_inactivo.telefono,
        f_nac=usuario_inactivo.f_nac,
        genero=usuario_inactivo.genero,
        f_registro=usuario_inactivo.f_registro,
    )
    usuario_inactivo.delete()
    messages.success(request, f"El usuario {usuario_inactivo.nombre} {usuario_inactivo.apellido} ha sido reactivado.")
    return redirect('listar_usuarios_inactivos')
def obtener_flujo_pacientes(request):
    pacientes = Paciente.objects.all().order_by('tiempo_ingreso')
    data = [
        {
            'nombre': paciente.nombre,
            'apellido': paciente.apellido,
            'edad': paciente.edad,
            'estado': paciente.estado,
            'tiempo_ingreso': paciente.tiempo_ingreso.strftime('%Y-%m-%d %H:%M:%S'),
            'tiempo_actualizacion': paciente.tiempo_actualizacion.strftime('%Y-%m-%d %H:%M:%S'),
        }
        for paciente in pacientes
    ]
    return JsonResponse({'pacientes': data})

def monitoreo(request):
    # Lógica para la vista de monitoreo
    return render(request, 'crud_usuarios/monitoreo.html')

def monitoreo_desempeno(request):
    return render(request, 'monitoreodesempeno.html')

def api_monitoreo_desempeno(request):
    data = {
        "response_time": f"{random.randint(100, 150)}ms",
        "processing_speed": f"{random.randint(10, 15)} imágenes/s",
        "uptime": f"{round(99 + random.random(), 2)}%",
        "performance_chart": {
            "labels": ['Hace 5 min', 'Hace 4 min', 'Hace 3 min', 'Hace 2 min', 'Hace 1 min', 'Ahora'],
            "data": [random.randint(100, 150) for _ in range(6)]
        }
    }
    return JsonResponse(data)