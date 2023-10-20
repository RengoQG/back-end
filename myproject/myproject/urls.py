"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Sistema import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.custom_login, name='custom_login'),
    path('dash/', views.panel, name='panel'),
    path('register/', views.register, name='registro'),
    path('api/stops/', views.datosCiudad, name='registro_paradas'),
    path('pasajeros/',views.pasajeros, name="pasajeros"),
    path('api/routes/<int:ruta_id>/add-stop/', views.agregar_parada_a_ruta, name='agregar_parada_a_ruta'),
    path('api/routes/<int:route_id>/stops/', views.consultar_paradas_en_ruta, name='consultar_paradas_en_ruta'),  
    path('rutas/', views.listar_rutas, name='listar_rutas'),
    path('rutasPa/', views.listar_rutas_pa, name='listar_rutas_pa'),
    path('api/routes/<int:ruta_id>/', views.detalle_ruta_j, name='detalle_rutas'),
    path('api/routes/', views.consultar_rutas_de_autobus, name='consultar_rutas'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

]
