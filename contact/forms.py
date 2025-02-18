from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Contact

class ContactForm(forms.ModelForm):
    picture = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'accept': 'image/*',
                'class': 'form-control',
                'placeholder': 'Picture',
                }
            )
        )

    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'email', 'phone', 'description', 'category', 'picture']
        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'First Name',
                    'required': 'required',
                    'autofocus': 'autofocus'
                    },
                ),
                
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Last Name',
                    # 'required': 'required'
                    }
                ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Email',
                    # 'required': 'required'
                    }
                ),
            'phone': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Phone',
                    # 'required': 'required'
                    }
                ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Description',
                    }
                ),
            'category': forms.Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Escolha uma categoria',
                    }
                )
        }


    # Mais utilizada para validar conteúdo de mais de um campo ou erros em geral
    def clean(self):
        cleaned_data = super().clean()

        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        if first_name == last_name:
            msg = ValidationError(
                    'First Name and Last Name cannot be the same', 
                    code='required'
                    )
            
            self.add_error(
                'first_name', 
                msg   
                )
            self.add_error(
                'last_name', 
                msg
            )
        return super().clean()

    # Mais utilizada para validar conteúdo de um campo específico
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        print('passei aqui')
            
        if first_name == "ABC":
        # DESSA FORMA A VALIDAÇÃO PARA NESSE ERRO E RETORNA PARA O USUARIO
        #   raise ValidationError(
        #        'Não digite ABC neste campo', 
        #         code='required'
        #         )

        # DESSA FORMA A VALIDAÇÃO CONTINUA A VALIDAÇÃO ANTES DE RETORNAR PARA O USUARIO
            self.add_error(
                'first_name', 
                ValidationError(
                    'Nao digite ABC neste campo', 
                    code='required'
                    )
                )
            
        return first_name
    

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'First Name',
                'required': 'required',
                'autofocus': 'autofocus'
                }
            )
        )
    
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Last Name',
                'required': 'required'
                }
            )
        )
    
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Email',
                'required': 'required'
                }
            )
        )
    
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username', 
            'email', 'password1', 'password2'
            ]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if User.objects.filter(email=email).exists():
            self.add_error(
                'email', 
                ValidationError(
                    'Email already exists', 
                    code='invalid'
                    )
            )    
        return email
    
class RegisterUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        help_text='Required.',
        error_messages={
            'min_length': 'Please, add more than 2 letters.'
        }
    )
    last_name = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        help_text='Required.'
    )

    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False,
    )

    password2 = forms.CharField(
        label="Password 2",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text='Use the same password as before.',
        required=False,
    )

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email',
            'username',
        )

    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        user = super().save(commit=False)
        password = cleaned_data.get('password1')

        if password:
            user.set_password(password)

        if commit:
            user.save()

        return user

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 or password2:
            if password1 != password2:
                self.add_error(
                    'password2',
                    ValidationError('Senhas não batem')
                )

        return super().clean()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        current_email = self.instance.email

        if current_email != email:
            if User.objects.filter(email=email).exists():
                self.add_error(
                    'email',
                    ValidationError('Já existe este e-mail', code='invalid')
                )

        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if password1:
            try:
                password_validation.validate_password(password1)
            except ValidationError as errors:
                self.add_error(
                    'password1',
                    ValidationError(errors)
                )

        return password1
    