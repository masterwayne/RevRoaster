from django import forms

class URLForm(forms.Form):
	url = forms.CharField(label='Enter URL here', max_length=1000)
