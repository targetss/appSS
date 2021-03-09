from django.forms import ModelForm, TextInput, Select, Textarea, DateInput
from .models import ApplicationObject
from django import forms

class ApplicationObjectForm(ModelForm):
    class Meta:
        model = ApplicationObject
        exclude = [""]
        widgets = {
            "number_object": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Номер объекта'
            }),
            "urgency_application": Select(attrs={
                'class': 'custom-select mr-sm-2',
            }),
            "completion_date": DateInput(attrs={
                'class': 'form-control',
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
                'class': 'custom-select mr-sm-2'
            }),
            "comment": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Комментарий'
            }),
            "source_application": Select(attrs={
                'class': 'custom-select mr-sm-2'
            }),
            "initiator_of_the_application": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Инициатор заявки'
            }),
            "status_application": Select(attrs={
                'class': 'custom-select mr-sm-2'
            }),
            "type_of_problem": Select(attrs={
                'class': 'custom-select mr-sm-2'
            }),
            "technician": Select(attrs={
                'class': 'custom-select mr-sm-2'
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
    completion_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), required=False)
    completion_date_2 = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}), required=False)
    initiator = forms.CharField(widget=forms.TextInput(attrs={'type': 'text'}), required=False)

class Search(forms.Form):
    comment = forms.CharField()