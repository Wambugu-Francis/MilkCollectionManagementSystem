from django import forms
from .models import Farmer, MilkCollection

class FarmerForm(forms.ModelForm):
    class Meta:
        model = Farmer
        fields = ['first_name', 'last_name', 'phone_number', 'id_number', 'location', 'notes']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Last Name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '+254712345678'}),
            'id_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'ID Number'}),
            'location': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Location/Village'}),
            'notes': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Additional notes'}),
        }


class MilkCollectionForm(forms.ModelForm):
    class Meta:
        model = MilkCollection
        fields = ['farmer', 'quantity', 'collection_date', 'price_per_liter', 'notes']
        widgets = {
            'farmer': forms.Select(attrs={'class': 'form-input'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Quantity in liters', 'step': '0.01'}),
            'collection_date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'price_per_liter': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Price per liter', 'step': '0.01'}),
            'notes': forms.Textarea(attrs={'class': 'form-input', 'rows': 2, 'placeholder': 'Additional notes'}),
        }