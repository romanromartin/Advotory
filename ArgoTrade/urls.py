from django.contrib import admin
from django.urls import path
from argo import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('management/', views.managment, name='management'),
    path('cart/', views.cart, name='cart'),
    path('<id_category>', views.category, name='category'),
    path('<id_category>/<id_sub>', views.sub, name='sub'),


]
