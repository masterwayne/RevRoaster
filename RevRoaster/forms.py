from django import forms

class URLForm(forms.Form):
	url = forms.CharField(label='Not here', max_length=1000)
