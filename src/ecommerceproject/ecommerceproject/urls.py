
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/authentication/',include('api.v1.authentication.urls')),
    path('api/v1/admin_manage/',include('api.v1.admin_manage.urls')),
    path('api/v1/product_manage/',include('api.v1.product_manage.urls')),

]
