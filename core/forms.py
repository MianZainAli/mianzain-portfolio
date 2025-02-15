from importlib.metadata import requires
from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'id': 'name', 'class': 'form-control', 'placeholder': 'Your Name', requires: True}),
            'email': forms.EmailInput(attrs={'id': 'email', 'class': 'form-control', 'placeholder': 'Your Email', requires: True}),
            'message': forms.Textarea(attrs={'id': 'message', 'class': 'form-control', 'placeholder': 'Your Message', 'rows': 5 , requires: True}),
        }
    
    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 2:
            raise forms.ValidationError('Name must be at least 2 characters long')
       
        if not name.replace(' ', '').isalpha():
            raise forms.ValidationError('Name should only contain alphabets and spaces')
        return name
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if '@' not in email:
            raise forms.ValidationError('Please enter a valid email address')
        return email
    
    def clean_message(self):
        message = self.cleaned_data['message']
        if len(message) < 10:
            raise forms.ValidationError('Message must be at least 10 characters long')
        if len(message) > 5000:
            raise forms.ValidationError('Message must be at most 5000 characters long')
        return message