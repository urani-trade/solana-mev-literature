"""This module supplies the main search forms for NISQ Algorithm zoo"""

from django import forms
from .utils import (get_algorithm_tuples,
                    get_computer_tuples,
                    get_qubit_type_tuples,
                    get_qubit_subtype_tuples)
from implementations.models import NISQImplementation



class ImplementationCreateForm(forms.ModelForm):
    # Field for the month of the NISQ Implementation
    month = forms.CharField(
        label="Month",
        widget=forms.TextInput(attrs={"type": "text",
                                      "autocomplete": "off",
                                      "class": "form-control zero-border-rad",
                                      "placeholder": "Month"})
    )

    # Field for the year of the NISQ Implementation
    year_int = forms.IntegerField(
        label="Year",
        widget=forms.NumberInput(attrs={"type": "number",
                                        "autocomplete": "off",
                                        "name": "year",
                                        "min": "1990",
                                        "max": "3035",
                                        "class": "form-control zero-border-rad",
                                        "id": "year",
                                        "placeholder": "Year"})
    )

    # Field for the reference URL of the NISQ Implementation
    reference_url = forms.URLField(
        label="Reference URL",
        required=False,
        widget=forms.URLInput(attrs={"type": "text",
                                     "autocomplete": "off",
                                     "class": "form-control zero-border-rad",
                                     "placeholder": "Reference URL"})
    )

    # Field for the qubit number of the NISQ Implementation
    qubit_number = forms.IntegerField(
        label="Number of Qubits",
        required=False,
        widget=forms.NumberInput(attrs={"autocomplete": "off",
                                        "type": "number",
                                        "name": "year",
                                        "min": "0",
                                        "class": "form-control zero-border-rad",
                                        "id": "qubit_number",
                                        "placeholder": "Number of Qubits",
                                        "required": "false"}))

    # Field for description of the NISQ Implementation
    description = forms.CharField(
        label="Description of Implementation",
        widget=forms.Textarea(attrs={'placeholder': "Description",
                                     'class': "form-control zero-border-rad",
                                     'id': "descriptionTextArea", 'rows': "3"})
    )

    # Field for the computer of the NISQ Implementation
    computer = forms.MultipleChoiceField(
        label='Computer(s)',
        required=False,
        choices=get_computer_tuples(),
        widget=forms.SelectMultiple(attrs={'multiple': 'true',
                                           'class': "form-control zero-border-rad",
                                           'id': "computerMultiSelect",
                                           'required': 'false'})
    )

    # Field for the algorithm of the NISQ Implementation
    algorithm = forms.MultipleChoiceField(
        label='Algorithm(s)',
        choices=get_algorithm_tuples(),
        required=False,
        widget=forms.SelectMultiple(attrs={'multiple': 'true',
                                           'class': "form-control zero-border-rad",
                                           'id': "algorithmMultiSelect",
                                           'required': 'false'})
    )

    # Field for the qubit type of the NISQ Implementation
    qubit_type = forms.MultipleChoiceField(
        label='Qubit Type(s)',
        required=False,
        choices=get_qubit_type_tuples(),
        widget=forms.SelectMultiple(attrs={'multiple': 'true',
                                           'class': "form-control zero-border-rad",
                                           'id': "qTypeMultiSelect",
                                           'required': 'false'})
    )

    # Field for the qubit subtype of the NISQ Implementation
    qubit_subtype = forms.MultipleChoiceField(
        label='Qubit Subtype(s)',
        required=False,
        choices=get_qubit_subtype_tuples(),
        widget=forms.SelectMultiple(attrs={'multiple': 'true',
                                           'class': "form-control zero-border-rad",
                                           'id': "qSubtypeMultiSelect",
                                           'required': 'false'})
    )

    new_computer = forms.CharField(
        label="Add Computer",
        required=False,
        widget=forms.TextInput(attrs={'type': "text",
                                      'autocomplete': 'off',
                                      'class': "form-control zero-border-rad",
                                      'placeholder': "Add new computer"})
    )

    new_algorithm = forms.CharField(
        label="Add Algorithm",
        required=False,
        widget=forms.TextInput(attrs={'type': "text",
                                      'autocomplete': 'off',
                                      'class': "form-control zero-border-rad",
                                      'placeholder': "Add new algorithm"})
    )

    new_qubit_type = forms.CharField(
        label="Add Qubit Type",
        required=False,
        widget=forms.TextInput(attrs={'type': "text",
                                      'autocomplete': 'off',
                                      'class': "form-control zero-border-rad",
                                      'placeholder': "Add new qubit type"}))

    new_qubit_subtype = forms.CharField(
        label="Add Qubit Subtype",
        required=False,
        widget=forms.TextInput(attrs={'type': "text",
                                      'autocomplete': 'off',
                                      'class':"form-control zero-border-rad",
                                      'placeholder':"Add new qubit subtype"})
    )
    class Meta:
        model = NISQImplementation
        db_table = 'nisqimplementation'
        fields = [
            'month',
            'year_int',
            'reference_url',
            'qubit_number',
            'description',
            'computer',
            'algorithm',
            'qubit_type',
            'qubit_subtype',
        ]

