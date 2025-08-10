"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import path
from core.views import HorListView, FrutListView, VegetListView, GraListView, ProdDetailView, AddToCartView, CarrinhoView, RemoverDoCarrinhoView
from django.conf.urls.static import static
from accounts.views import register_view, login_view, logout_view, adicionar_endereco, listar_enderecos, editar_endereco, remover_endereco

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HorListView.as_view(),  name='lista_produtos'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login' ),
    path('logout/', logout_view, name='logout'),
    path('adicionar-endereco/', adicionar_endereco, name='adicionar_endereco'),
    path('endereço/', listar_enderecos, name='lista_de_enderecos'),
    path('enderecos/editar/<int:endereco_id>/', editar_endereco, name='editar_endereco'),
    path('enderecos/remover/<int:endereco_id>/', remover_endereco, name='remover_endereco'),
    path('Frutas/', FrutListView.as_view(), name='frutas'),
    path('vegetais/', VegetListView.as_view(), name='vegetais'),
    path('graos/', GraListView.as_view(), name='grao'),
    path('produto/<int:pk>/', ProdDetailView.as_view(), name='produto_detail'),
    path('adicionar_ao_carrinho/', AddToCartView.as_view() , name='adicionar_ao_carrinho' ),
    path('carrinho/', CarrinhoView.as_view(), name='carrinho'),
    path('remover_do_carrinho/', RemoverDoCarrinhoView.as_view(), name='remover_do_carrinho')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

