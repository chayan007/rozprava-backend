from django import forms


class CaseForm(forms.Form):
    """Form class for case validation."""

    question = forms.CharField(max_length=500)
    description = forms.CharField(max_length=5000, required=False)
    category = forms.IntegerField(min_value=0, max_value=9)
    for_label = forms.CharField(max_length=300, required=False)
    against_label = forms.CharField(max_length=300, required=False)

