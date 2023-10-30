from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from .models import CustomUser, RutaDeAutobus
from django.contrib.auth import login
from django.contrib.auth import login

from .models import Ciudad 
from .models import AsociacionParadaRuta
# Asegúrate de importar tu modelo de Ciudad
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework import status
from .models import ParadaDeAutobus
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from .models import RutaDeAutobus  # Asegúrate de importar tu modelo de ruta
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response


#HTTP#####
@api_view(['POST'])
def custom_login2(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            custom_user = CustomUser.objects.get(username=username)
            if custom_user.check_password(password):
                login(request, custom_user, backend='django.contrib.auth.backends.ModelBackend')  # Añade el parámetro 'backend'
                
                if custom_user.rol == 'logistico':
                    # Devuelve un mensaje JSON personalizado con el nombre de usuario
                    message = f'Bienvenido {custom_user.username}, eres un operador logístico.'
                    return Response({'message': message}, status=status.HTTP_200_OK)
                else:
                    # Devuelve un mensaje JSON para otros roles
                    message = f'Bienvenido {custom_user.username}, eres un pasajero.' 
                    return Response({'message': message}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Nombre de usuario o contraseña incorrectos.'}, status=status.HTTP_401_UNAUTHORIZED)
        except CustomUser.DoesNotExist:
            return Response({'message': 'Nombre de usuario o contraseña incorrectos.'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({'message': 'Método no permitido'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def consultar_paradas_en_ruta2(request, route_id):
    try:
        user = request.user  # Obtén el usuario autenticado

        # Verifica que el usuario sea un operador logístico
        if user.rol != 'logistico':
            return Response({'message': 'No tienes permiso para realizar esta acción.'}, status=status.HTTP_403_FORBIDDEN)

        ruta = get_object_or_404(RutaDeAutobus, id=route_id)
        paradas = ParadaDeAutobus.objects.filter(asociacionparadaruta__ruta=ruta)

        # Crea una lista de paradas
        paradas_list = [{'nombre': parada.nombre, 'latitud': float(parada.latitud), 'longitud': float(parada.longitud)} for parada in paradas]

        return Response({'paradas': paradas_list}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'message': 'Error al consultar las paradas en la ruta.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
def register2(request):
    error_message = None
    success_message = None

    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        rol = request.data.get('rol')

        if username and password and rol:
            if CustomUser.objects.filter(username=username).exists():
                error_message = "El nombre de usuario ya está en uso."
            else:
                user = CustomUser(username=username, rol=rol)
                user.set_password(password)
                user.save()
                success_message = "Usuario registrado con éxito. Bienvenido."
                return JsonResponse({'message': success_message}, status=201)

        else:
            error_message = "No se pudieron procesar los datos. Asegúrate de incluir 'username', 'password' y 'rol' en tu solicitud."
            return JsonResponse({'error_message': error_message}, status=400)

    return JsonResponse({'error_message': error_message}, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Asegura que solo los usuarios autenticados puedan acceder
def datosCiudad2(request):
    if request.user.rol != 'logistico':
        return Response({'message': 'Acceso denegado. Debes ser un operador logístico.'}, status=403)

    nombre = request.data.get('nombre')
    latitud = request.data.get('latitud')
    longitud = request.data.get('longitud')
    ciudad_id = request.data.get('ciudad_id')

    message = None

    if not nombre or not latitud or not longitud:
        message = "Por favor, complete todos los campos obligatorios."

    if not message:
        try:
            nueva_parada = ParadaDeAutobus(nombre=nombre, latitud=latitud, longitud=longitud, ciudad_id=ciudad_id)
            nueva_parada.save()
            message = "Parada registrada con éxito."
        except Exception as e:
            message = "Error al registrar la parada: " + str(e)

    response_data = {'message': message}
    return JsonResponse(response_data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def agregar_parada_a_ruta2(request, ruta_id):
    try:
        # Verificar si el usuario es un "Operador Logístico"
        if request.user.rol != 'logistico':
            return JsonResponse({'message': 'No tienes permiso para realizar esta acción.'}, status=403)
        
        # Obtener la ruta
        ruta = get_object_or_404(RutaDeAutobus, id=ruta_id)

        # Obtener la parada asociada al request (puedes ajustar esto según tus necesidades)
        parada_id = request.data.get('parada_id')
        parada = get_object_or_404(ParadaDeAutobus, id=parada_id)

        # Verificar si la parada ya está asociada a la ruta
        if AsociacionParadaRuta.objects.filter(parada=parada, ruta=ruta).exists():
            return JsonResponse({'message': 'La parada ya está asociada a la ruta.'}, status=400)

        # Crear la asociación de la parada con la ruta
        asociacion = AsociacionParadaRuta(parada=parada, ruta=ruta)
        asociacion.save()
        
        return JsonResponse({'message': 'Parada asociada con éxito a la ruta.'}, status=200)

    except Exception as e:
        return JsonResponse({'message': 'Error al asociar la parada: ' + str(e)}, status=500)
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def consultar_paradas_en_ruta2(request):
    try:
        # Consulta todas las rutas
        rutas = RutaDeAutobus.objects.all()

        # Luego, puedes procesar las rutas y devolver la respuesta JSON
        rutas_data = []

        for ruta in rutas:
            rutas_data.append({
                'id': ruta.id,
                'nombre': ruta.nombre,
                'origen': ruta.origen,
                'destino': ruta.destino,
                # Agrega más campos según tus necesidades
            })

        return JsonResponse(rutas_data, safe=False)

    except Exception as e:
        return JsonResponse({'message': 'Error al consultar las rutas: ' + str(e)}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def detalle_ruta_2(request, ruta_id):
    try:
        try:
            ruta = RutaDeAutobus.objects.get(id=ruta_id)
        except RutaDeAutobus.DoesNotExist:
            return JsonResponse({'message': 'La ruta con el ID especificado no existe.'}, status=404)
       
        ruta = get_object_or_404(RutaDeAutobus, id=ruta_id)
        
        # Obtener las paradas asociadas a la ruta
        paradas = ParadaDeAutobus.objects.filter(asociacionparadaruta__ruta=ruta)

        # Supongamos que deseas devolver detalles específicos de la ruta en formato JSON,
        # junto con la lista de paradas asociadas.
        ruta_data = {
            'id': ruta.id,
            'nombre': ruta.nombre,
            'origen': ruta.origen,
            'destino': ruta.destino,
            # Agrega más campos de la ruta según tus necesidades
            'paradas': []  # Esto será una lista de paradas asociadas
        }

        # Agregar los detalles de las paradas asociadas a la ruta
        for parada in paradas:
            ruta_data['paradas'].append({
                'id': parada.id,
                'nombre': parada.nombre,
                'latitud': parada.latitud,
                'longitud': parada.longitud,
                # Agrega más campos de las paradas según tus necesidades
            })
    
        return JsonResponse(ruta_data, safe=False)
    except Exception as e:
        return JsonResponse({'message': 'Error al consultar los detalles de las rutas: ' + str(e)}, status=500)

########################


####Interfaz de usuario######
def inicioSesion(request):
    return render(request, 'Sistema/login.html')

#Interfaz de usuario
def custom_login(request):
    error_message = None

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Intenta autenticar en tu tabla personalizada
        try:
            custom_user = CustomUser.objects.get(username=username)
            if custom_user.check_password(password):
                login(request, custom_user)
                
                # Verifica el rol del usuario
                if custom_user.rol == 'logistico':
                    # Redirige a la vista del formulario de operador logístico
                    return redirect('/dash')
                else:
                    # Redirige a la vista del formulario para otros roles
                        return render(request, 'Sistema/pasajeros.html')
            else:
                error_message = "Nombre de usuario o contraseña incorrectos."
        except CustomUser.DoesNotExist:
            error_message = "Nombre de usuario o contraseña incorrectos."

    return render(request, 'Sistema/login.html', {'error_message': error_message})


    
def register(request):
    error_message = None
    success_message = None

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            rol = form.cleaned_data['rol']

            # Verifica si el nombre de usuario ya existe
            if CustomUser.objects.filter(username=username).exists():
                error_message = "El nombre de usuario ya está en uso."
            else:
                # Crear un nuevo usuario
                user = CustomUser(username=username, rol=rol)
                user.set_password(password)
                user.save()
                login(request, user)
                success_message = "Usuario registrado con éxito. Bienvenido."

        else:
            error_message = "No se pudo crear el usuario. Por favor, verifica los datos."

    else:
        form = CustomUserCreationForm()

    return render(request, 'Sistema/register.html', {'form': form, 'error_message': error_message, 'success_message': success_message})

#@login_required
@csrf_exempt
def datosCiudad(request):
    ciudades = Ciudad.objects.all()  
    message = None  

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        latitud = request.POST.get('latitud')
        longitud = request.POST.get('longitud')
        ciudad_id = request.POST.get('ciudad_id')

        if not nombre or not latitud or not longitud:
            message = "Por favor, complete todos los campos obligatorios."
        elif not latitud.isdigit() or not longitud.isdigit():
            message = "Las coordenadas deben ser valores numéricos."

        if not message:
            try:
                nueva_parada = ParadaDeAutobus(nombre=nombre, latitud=latitud, longitud=longitud, ciudad_id=ciudad_id)
                nueva_parada.save()
                message = "Parada registrada con éxito."
            except Exception as e:
                message = "Error al registrar la parada: " + str(e)

        # Verifica si la solicitud espera una respuesta JSON
        if 'application/json' in request.META.get('HTTP_ACCEPT'):
            # Construye una respuesta JSON
            response_data = {'message': message}
            return JsonResponse(response_data)
        else:
            # Respuesta HTML
            return render(request, 'Sistema/agregarParada.html', {'ciudades': ciudades, 'message': message})

    return render(request, 'Sistema/agregarParada.html', {'ciudades': ciudades, 'message': message})

def agregar_parada_a_ruta(request, ruta_id):
    error_message = None
    success_message = None
    ruta = get_object_or_404(RutaDeAutobus, id=ruta_id)
    paradas = ParadaDeAutobus.objects.all()
    if request.method == 'POST':
        parada_id = request.POST.get('parada_id')
        parada = get_object_or_404(ParadaDeAutobus, id=parada_id)

        try:
            asociacion = AsociacionParadaRuta(parada=parada, ruta=ruta)
            asociacion.save()
            success_message = 'Parada asociada con éxito a la ruta.'
        except Exception as e:
            messages.error(request, f'Error al asociar la parada: {e}')

        #return redirect('login')  # Puedes redirigir a la página de asociación.

    paradas_disponibles = ParadaDeAutobus.objects.exclude(asociacionparadaruta__ruta=ruta)
    return render(request, 'Sistema/asociar.html', {'ruta': ruta, 'paradas_disponibles': paradas_disponibles,'paradas': paradas, 'success_message': success_message})

def consultar_paradas(request):
    paradas = ParadaDeAutobus.objects.all()
    return render(request, 'Sistema/consultar_paradas.html', {'paradas': paradas})


def consultar_paradas_en_ruta(request, route_id):
    ruta = get_object_or_404(RutaDeAutobus, id=route_id)
    paradas = ParadaDeAutobus.objects.filter(asociacionparadaruta__ruta=ruta)
    
    return render(request, 'Sistema/consulta_paradas.html', {'paradas': paradas})




def consultar_rutas_de_autobus(request):
    rutas = RutaDeAutobus.objects.all()
    rutas_data = []

    for ruta in rutas:
        rutas_data.append({
            'id': ruta.id,
            'nombre': ruta.nombre,
            'origen': ruta.origen,
            'destino': ruta.destino,
            # Agrega más campos según tus necesidades
        })

    return JsonResponse(rutas_data, safe=False)

def detalle_ruta(request, ruta_id):
    ruta = get_object_or_404(RutaDeAutobus, id=ruta_id)
    return render(request, 'Sistema/detalle_ruta.html', {'ruta': ruta})

def detalle_ruta_j(request, ruta_id):
    ruta = get_object_or_404(RutaDeAutobus, id=ruta_id)
    
    # Supongamos que deseas devolver detalles específicos de la ruta en formato JSON.
    ruta_data = {
        'id': ruta.id,
        'nombre': ruta.nombre,
        'origen': ruta.origen,
        'destino': ruta.destino,
        # Agrega más campos según tus necesidades
    }
    
    return JsonResponse(ruta_data, safe=False)

def listar_rutas(request):
    rutas = RutaDeAutobus.objects.all()  # Obtiene todas las rutas de la base de datos
    return render(request, 'Sistema/rutas.html', {'rutas': rutas})


def listar_rutas_pa(request):
    rutas = RutaDeAutobus.objects.all()  # Obtiene todas las rutas de la base de datos
    return render(request, 'Sistema/rutasPa.html', {'rutas': rutas})


def pasajeros(request):
        return render(request, 'Sistema/pasajero.html')


def panel(request):
        return render(request, 'Sistema/dashAdmi.html')


    