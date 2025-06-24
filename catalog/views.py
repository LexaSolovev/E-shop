from django.views.generic import ListView, DetailView, TemplateView
from .models import Product

class ContactView(TemplateView):
    template_name = 'contacts.html'


class ProductListView(ListView):
    model = Product
    template_name = 'index.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'
