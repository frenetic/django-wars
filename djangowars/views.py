# Create your views here.
from django.shortcuts import render_to_response, render
from django.shortcuts import redirect # Funcao para redirecionar o usuario
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import UserCreationForm # Formulario de criacao de usuarios
from django.contrib.auth.forms import AuthenticationForm # Formulario de autenticacao de usuarios
from django.contrib.auth import login # funcao que salva o usuario na sessao
from djangowars.itens.models import Arma, Armadura #importa as armas e armaduras


# pagina inicial do projeto django-wars
def index(request):
    return render_to_response("index.html")


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
            return redirect(crimes) # redireciona o usuario logado para a pagina inicial
        else:
            return render(request, "logar.html", {"form": form})
    
    #se nenhuma informacao for passada, exibe a pagina de login com o formulario
    return render(request, "logar.html", {"form": AuthenticationForm()})


# pagina que lista os crimes
def crimes(request):
    if not request.user.is_authenticated():
        return redirect(logar)
    return render_to_response("crimes.html", {"player": request.user.get_profile(),
                                              "vida": request.user.get_profile().vida * 10}) # para exibir o total de vida do usuario


# pagina da loja:
def loja(request):
    if not request.user.is_authenticated():
        return redirect(logar)

    armas = Arma.objects.filter(secreta=False).order_by('compra', '-venda')
    armaduras = Armadura.objects.filter(secreta=False).order_by('compra', '-venda')

    return render_to_response("loja.html", {"armas": armas,
                                            "armaduras": armaduras,
                                            "player": request.user.get_profile()})

#pagina de compra de armaduras
def comprar_armadura(request, item):
    if not request.user.is_authenticated():
        return redirect(logar)

    armadura = get_object_or_404(Armadura, pk=item)
    player = request.user.get_profile()

    if player.carteira >= armadura.compra:
        player.carteira = player.carteira - armadura.compra
        player.armaduras.add(armadura) #https://docs.djangoproject.com/en/1.4/ref/models/relations/
        player.save()

    return redirect(loja)

#pagina de venda de armaduras
def vender_armadura(request, item):
    if not request.user.is_authenticated():
        return redirect(logar)

    armadura = get_object_or_404(Armadura, pk=item)
    player = request.user.get_profile()

    if armadura in player.armaduras.all():
        player.carteira = player.carteira + armadura.venda
        player.armaduras.remove(armadura) #https://docs.djangoproject.com/en/1.4/ref/models/relations/

    return redirect(loja)
