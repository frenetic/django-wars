# Create your views here.
from django.shortcuts import render # funcoes de renderizacao dos templates
from django.shortcuts import redirect # Funcao para executar um http-redirect

from django.contrib.auth.forms import UserCreationForm # Formulario de criacao de usuarios
from django.contrib.auth.forms import AuthenticationForm # Formulario de autenticacao de usuarios
from django.contrib.auth import login # funcao que salva o usuario na sessao




# pagina de cadastro de jogador
def registrar(request):
    # Se dados forem passados via POST
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        
        if form.is_valid(): # se o formulario for valido
            form.save() # cria um novo usuario a partir dos dados enviados 
            return redirect(logar) # redireciona para a tela de login
        else:
            # mostra novamente o formulario de cadastro com os erros do formulario atual
            return render(request, "registrar.html", {"form": form})
    
    # se nenhuma informacao for passada, exibe a pagina de cadastro com o formulario
    return render(request, "registrar.html", {"form": UserCreationForm() })


# pagina de login do jogador
def logar(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST) # Veja a documentacao desta funcao
        
        if form.is_valid():
            #se o formulario for valido significa que o Django conseguiu encontrar o usuario no banco de dados
            #agora, basta logar o usuario e ser feliz.
            login(request, form.get_user())
            return redirect("pagina_de_crimes") # redireciona o usuario logado para a pagina inicial
        else:
            return render(request, "logar.html", {"form": form})
    
    #se nenhuma informacao for passada, exibe a pagina de login com o formulario
    return render(request, "logar.html", {"form": AuthenticationForm()})