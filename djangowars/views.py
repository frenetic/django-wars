# Create your views here.
from django.shortcuts import render_to_response

# pagina inicial do projeto django-wars
def index(request):
    return render_to_response("index.html")
