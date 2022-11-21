from django import forms
from myapp.models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['client', 'product', 'num_units']
        labels = {'num_units': 'Quantity',
                  'client': 'Client Name'
                  }


class InterestForm(forms.Form):
    interested = forms.ChoiceField(widget=forms.RadioSelect, choices=[('1', 'Yes'), ('0', 'No')])
    quantity = forms.IntegerField(min_value=1, initial=1)
    comments = forms.CharField(widget=forms.Textarea, required=False, label='Additional Comments')
