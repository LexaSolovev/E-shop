from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import home, product_detail

app_name = CatalogConfig.name
urlpatterns = [
    path('', home, name='home'),
    path('product/<int:pk>/', product_detail, name='product_detail'),
]
