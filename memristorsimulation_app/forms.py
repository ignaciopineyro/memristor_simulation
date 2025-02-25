from django import forms


class ModelParametersForm(forms.Form):
    alpha = forms.FloatField(label="Alpha")
    beta = forms.FloatField(label="Beta")
    rinit = forms.FloatField(label="Rinit")
    roff = forms.FloatField(label="Roff")
    ron = forms.FloatField(label="Ron")
    vt = forms.FloatField(label="Vt")
