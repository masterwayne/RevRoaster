from django.shortcuts import render
from django.http import HttpResponseRedirect
# Create your views here.
from .forms import URLForm
import sentiment_mod as s

def home(request):
    # if this is a POST request we need to process the form data
	if request.method == 'POST':
		form = URLForm(request.POST)
		if form.is_valid():
			url = form.cleaned_data['url']
			print(url)
			return render(request, 'revroaster/searchpage2.html')
	else:
		form = URLForm()

	return render(request, 'revroaster/searchpage.html', {'form': form})
