from django import forms
from .models import Shop

class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ('title', 'description')

    def __init__(self, *args, **kwargs) -> None:
        super(ShopForm, self).__init__(*args, **kwargs)

        class_attr = 'form-control'

        self.fields['title'].widget.attrs['class'] = class_attr
        self.fields['description'].widget.attrs['class'] = class_attr
