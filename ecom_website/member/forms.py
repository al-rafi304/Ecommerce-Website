from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Member

class RegisterForm(UserCreationForm):
    class Meta:
        model = Member
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'phone', 'dob', 'address')

    def __init__(self, *args, **kwargs) -> None:
        super(RegisterForm, self).__init__(*args, **kwargs)
        
        class_attr = 'form-control'

        # HTML class attributes
        self.fields['first_name'].widget.attrs['class'] = class_attr
        self.fields['last_name'].widget.attrs['class'] = class_attr
        self.fields['username'].widget.attrs['class'] = class_attr
        self.fields['email'].widget.attrs['class'] = class_attr
        self.fields['password1'].widget.attrs['class'] = class_attr
        self.fields['password2'].widget.attrs['class'] = class_attr
        self.fields['phone'].widget.attrs['class'] = class_attr
        self.fields['dob'].widget.attrs['class'] = class_attr
        self.fields['address'].widget.attrs['class'] = class_attr