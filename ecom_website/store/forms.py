from django import forms
from .models import Shop, Product

class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ('title', 'description')

    # For styling input fields
    def __init__(self, *args, **kwargs) -> None:
        super(ShopForm, self).__init__(*args, **kwargs)

        class_attr = 'form-control'

        self.fields['title'].widget.attrs['class'] = class_attr
        self.fields['description'].widget.attrs['class'] = class_attr

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('title', 'description', 'price', 'image')

        class_attr = 'form-control'

        widgets = {
            'title': forms.TextInput(attrs={'class': class_attr}),
            'description': forms.TextInput(attrs={'class': class_attr}),
            'price': forms.NumberInput(attrs={'class': class_attr}),
            'image': forms.ClearableFileInput(attrs={'class': class_attr})
        }