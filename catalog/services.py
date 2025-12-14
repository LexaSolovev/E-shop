from .models import Product
from django.core.cache import cache

def get_products_by_category(category_slug=None):
    """
    Функция получает список продуктов по категории, если категория не задана, получаем весь список продуктов.
    Используется кэширование по ключу "products_list_by_category_slug".
    Если категория не задана ключ = "products_list_by_None"
    """
    products_list = cache.get(f"products_list_by_{category_slug}")
    if products_list is None:
        if category_slug is not None:
            products_list = Product.objects.filter(category__slug=category_slug)
        else:
            products_list = Product.objects.all()

        cache.set(f"products_list_by_{category_slug}", products_list, 60 * 15)
    return products_list

if __name__ == "__main__":
    print(get_products_by_category(None))