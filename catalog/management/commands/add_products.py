import json
import os

from django.core.files import File
from django.core.management.base import BaseCommand
from catalog.models import Product,Category
from config import settings


class Command(BaseCommand):
    help = "Add test products to the database"

    def handle(self, *args, **options):
        # Очищаем существующие данные
        self.stdout.write(self.style.WARNING('Clearing existing data...'))

        # Удаляем все продукты
        Product.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('All products deleted'))

        # Удаляем все категории
        Category.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('All categories deleted'))

        # Путь к файлу фикстуры
        fixture_path = os.path.join(settings.BASE_DIR, 'catalog_fixture.json')

        try:
            with open(fixture_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('Fixture file not found'))
            return
        except json.JSONDecodeError:
            self.stdout.write(self.style.ERROR('Invalid JSON format'))
            return

        # Создаем категории
        categories = {}
        for item in data:
            if item['model'] == 'catalog.category':
                category = Category.objects.create(
                    pk=item['pk'],
                    name=item['fields']['name'],
                    slug=item['fields']['slug'],
                    description=item['fields']['description']
                )
                categories[item['pk']] = category
                self.stdout.write(self.style.SUCCESS(f'Created category: {category.name}'))

        # Создаем продукты
        for item in data:
            if item['model'] == 'catalog.product':
                fields = item['fields']

                # Получаем категорию
                category = categories.get(fields['category'])
                if not category:
                    self.stdout.write(self.style.ERROR(f'Category not found for product: {fields["name"]}'))
                    continue

                # Создаем продукт
                product = Product(
                    pk=item['pk'],
                    name=fields['name'],
                    description=fields['description'],
                    category=category,
                    price=fields['price'],
                    created_at=fields['created_at'],
                    updated_at=fields['updated_at']
                )

                # Обрабатываем изображение, если оно есть
                image_path = fields['image']
                if image_path:
                    full_image_path = os.path.join(settings.MEDIA_ROOT, image_path)
                    if os.path.exists(full_image_path):
                        with open(full_image_path, 'rb') as img:
                            product.image.save(os.path.basename(image_path), File(img), save=False)
                    else:
                        self.stdout.write(self.style.WARNING(f'Image not found: {full_image_path}'))

                product.save()
                self.stdout.write(self.style.SUCCESS(f'Created product: {product.name}'))

        self.stdout.write(self.style.SUCCESS('Successfully cleared and reloaded all products and categories'))


