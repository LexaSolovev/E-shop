from django import forms
from django.core.exceptions import ValidationError
from .models import Product


class ProductForm(forms.ModelForm):
    BANNED_WORDS = [
        'казино', 'криптовалюта', 'крипта',
        'биржа', 'дешево', 'бесплатно',
        'обман', 'полиция', 'радар'
    ]

    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        common_attrs = {
            'class': 'form-control mb-3',
            'style': 'background-color: #2b3035; color: #f8f9fa; border-color: #495057;'
        }

        self.fields['name'].widget.attrs.update({
            'placeholder': 'Введите название продукта',
            **common_attrs
        })

        self.fields['description'].widget.attrs.update({
            'placeholder': 'Подробное описание продукта',
            'rows': 3,
            **common_attrs
        })

        self.fields['price'].widget.attrs.update({
            'placeholder': '0.00',
            'min': '0.01',
            'step': '0.01',
            **common_attrs
        })

        self.fields['category'].widget.attrs.update(common_attrs)

        self.fields['image'].widget.attrs.update({
            **common_attrs
        })

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name', '').lower()
        description = cleaned_data.get('description', '').lower()

        for word in self.BANNED_WORDS:
            if word in name or word in description:
                raise ValidationError(
                    f'Использование запрещенного слова "{word}" не допускается!'
                )

        return cleaned_data

    def clean_price(self):
        price = self.cleaned_data['price']
        if price <= 0:
            raise ValidationError("Цена должна быть больше нуля!")
        return price