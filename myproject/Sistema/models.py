from django.db import models
from django.contrib.auth.models import Group
from django.contrib.auth.models import AbstractUser  # Importa AbstractUser para tu modelo personalizado
from django.contrib.auth.models import User  # Agrega importación de User
from django.contrib.auth.models import Permission
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import models



    # Puedes agregar validaciones personalizadas o personalizar el formulario aquí


class Ciudad(models.Model):
    nombre = models.CharField(max_length=255)  # Elimina el campo id personalizado

    def __str__(self):
        return self.nombre
    
class ParadaDeAutobus(models.Model):
    nombre = models.CharField(max_length=255)
    latitud = models.DecimalField(max_digits=9, decimal_places=6)
    longitud = models.DecimalField(max_digits=9, decimal_places=6)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
    
class RutaDeAutobus(models.Model):
    nombre = models.CharField(max_length=255)
    origen = models.CharField(max_length=255)
    destino = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre

class HorarioDeParada(models.Model):
    dia_de_la_semana = models.CharField(max_length=20)
    hora_de_llegada = models.TimeField()
    hora_de_salida = models.TimeField()
    parada_de_autobus = models.ForeignKey(ParadaDeAutobus, on_delete=models.CASCADE)
    ruta_de_autobus = models.ForeignKey(RutaDeAutobus, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.dia_de_la_semana} - {self.parada_de_autobus} - {self.ruta_de_autobus}'
    
class CustomUser(AbstractUser):
    # Añadir campos personalizados como nombre y rol
    nombre = models.CharField(max_length=255)
    rol = models.CharField(max_length=100)
    contrasena = models.CharField(max_length=100)

    # Cambiar el nombre de los campos relacionados
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name='customuser_set',
        related_query_name='user'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='customuser_set',
        related_query_name='user'
    )
    
class AsociacionParadaRuta(models.Model):
        parada = models.ForeignKey(ParadaDeAutobus, on_delete=models.CASCADE)
        ruta = models.ForeignKey(RutaDeAutobus, on_delete=models.CASCADE)

        def __str__(self):
            return f'{self.parada.nombre} - {self.ruta.nombre}'


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('nombre', 'rol')


<<<<<<< HEAD
=======
def consultar_paradas(request):
    paradas = ParadaDeAutobus.objects.all()

    if request.method == 'POST':
        route_id = request.POST.get('routeId')
        response = requests.get(f'https://tuapi.com/api/routes/{route_id}/stops/')
        paradas_en_ruta = response.json()
    else:
        paradas_en_ruta = []

    return render(request, 'consulta_paradas.html', {'paradas': paradas, 'paradas_en_ruta': paradas_en_ruta})
>>>>>>> e4a01bdea91c69e679961b4cf8a11597b0e8ac04

# Crear grupos (continuar usando esta parte)
#user_group, created = Group.objects.get_or_create(name='pasajero')
#admin_group, created = Group.objects.get_or_create(name='OperadorLogistico')
# Asignar usuarios a grupos (ejemplo)
#user = User.objects.get(username='Johan')
#admin_group  = Group.objects.get_or_create(name='OperadorLogistico')
#user.groups.add(admin_group)
#user.groups.add(user_group)  # Asigna el usuario al grupo de "Usuario"
#user.groups.add(admin_group)  # Asigna el usuario al grupo de "Administrador"
