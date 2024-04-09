"""
URL configuration for billgenerator project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from bill.views import ProductViewSet
from bill.views import *
router = DefaultRouter()
router.register(r'api', ProductViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('login/',login,name='login'),
    path('list/',show),
    path('update-product/<int:product_id>/', update_product, name='update_product'),  
    path('delete-product/<int:product_id>/',delete_product, name='delete_product'),  
    path('add-product/', add_product, name='add_product'),  
    path('bill-generator/', bill_generator, name='bill_generator'), 
    path('signup/', user_signup, name='signup'),     
]
