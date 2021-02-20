from django.forms import ModelForm, TextInput, Select, Textarea, DateInput
from .models import ApplicationObject
from django import forms

class ApplicationObjectForm(ModelForm):
    class Meta:
        model = ApplicationObject
        exclude = [""]
        widgets = {
            "number_object": TextInput(attrs={
                'class': 'form-control col-md-4',
                'placeholder': 'Номер объекта'
            }),
            "urgency_application": Select(attrs={
                'class': 'form-group col-sm-6',
            }),
            "completion_date": DateInput(attrs={
                'class': 'form-group',
                'type': 'date'
            }),
            "name_object": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Наименование объекта'
            }),
            "address_object": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Адрес объекта'
            }),
            "service_area": Select(attrs={
                'class': 'form-group col-sm-6'
            }),
            "comment": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Комментарий'
            }),
            "source_application": Select(attrs={
                'class': 'form-group col-sm-6'
            }),
            "initiator_of_the_application": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Инициатор заявки'
            }),
            "status_application": Select(attrs={
                'class': 'form-group col-sm-6'
            }),
            "type_of_problem": Select(attrs={
                'class': 'form-group col-sm-6'
            }),
        }

class SortForm(forms.Form):
    sort_form = forms.TypedChoiceField(
        label='Сортировать:', choices=[
            ('Северо-Запад', 'Северо-Запад'),
            ('Центр', 'Центр'),
            ('Область', 'Область'),
            ('Обслуживание', 'Обслуживание'),
            ('АМЗ', 'АМЗ'),
            ('ЧТЗ', 'ЧТЗ'),
            ('ЧМЗ', 'ЧМЗ'),
            ('Ленинский', 'Ленинский'),
            ('Сосновский', 'Сосновский'),
            ('Екб. + Свердловская область', 'Екб. + Свердловская область')
        ])
    completion_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
