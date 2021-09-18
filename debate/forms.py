from django import forms


class DebateForm(forms.Form):
    """Form class for debate validation."""

    is_posted_anonymously = forms.BooleanField(required=False)
    comment = forms.CharField(max_length=5000)
    inclination = forms.IntegerField(min_value=0, max_value=1)


class RebuttalForm(forms.Form):
    """Form class for rebuttal validation."""

    is_posted_anonymously = forms.BooleanField(required=False)
    inclination = forms.IntegerField(min_value=0, max_value=1)
    comment = forms.CharField(max_length=5000)
    debate_uuid = forms.CharField(max_length=255)
