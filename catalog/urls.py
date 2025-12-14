from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import CatalogConfig
from catalog.views import ContactView, ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, \
    ProductDeleteView, unpublish_product, CategoryProductsView

app_name = CatalogConfig.name
urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('contacts/', ContactView.as_view(), name='contacts'),
    path('product/<int:pk>/', cache_page(60 * 15)(ProductDetailView.as_view()), name='product_detail'),
    path('product/create/', ProductCreateView.as_view(), name='product_create'),
    path('product/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('product/<int:pk>/unpublish/', unpublish_product, name='unpublish_product'),
    path('category/<slug:category_slug>/', CategoryProductsView.as_view(), name='category_products'),
]
