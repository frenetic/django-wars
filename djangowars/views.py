# Create your views here.
from django.shortcuts import render_to_response, render # funcoes de renderizacao dos templates
from django.shortcuts import redirect # Funcao para executar um http-redirect
from django.shortcuts import get_object_or_404 # funcao para buscar um item no banco de dados. Se nao encontrar, retorna um http 404 - page not found

from django.contrib.auth.forms import UserCreationForm # Formulario de criacao de usuarios
from django.contrib.auth.forms import AuthenticationForm # Formulario de autenticacao de usuarios
from django.contrib.auth import login # funcao que salva o usuario na sessao

from djangowars.itens.models import Arma, Armadura #importa os modelos de armas e armaduras
from random import randint # funcao para escolher um numero aleatorio




# pagina inicial do projeto django-wars
def index(request):
    return render_to_response("index.html")




###############################################################################
###              Paginas de interacao do usuario no sistema                 ###
###############################################################################

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




###############################################################################
###           Paginas de crimes (listagem e execucao dos crimes)            ###
###############################################################################

# pagina que lista os crimes
def crimes(request):
    if not request.user.is_authenticated():
        return redirect(logar)
    
    #da um refrash no hp, energia e raiva do player
    player = request.user.get_profile()
    player.refresh()
    player.save()
    
    return render_to_response("crimes.html", {"player": request.user.get_profile(),
                                              "vida": request.user.get_profile().vida * 10}) # para exibir o total de vida do usuario


# cometendo o crime de nivel 1
def cometer_crime1(request):
    if not request.user.is_authenticated():
        return redirect(logar)

    player = request.user.get_profile()

    if player.energia_atual < 1:
        return redirect(crimes)

    player.carteira = player.carteira + (11 * randint(0, player.ataque))
    player.energia_atual = player.energia_atual - 1
    
    #adiciona experiencia ao jogador
    player.experiencia = player.experiencia + 10
    
    #verifica se subiu de nivel
    player.level_up()
    
    player.save()
    return redirect(crimes)


# cometendo o crime de nivel 2
def cometer_crime2(request):
    if not request.user.is_authenticated():
        return redirect(logar)

    player = request.user.get_profile()

    if player.energia_atual < 2 or player.nivel < 2:
        return redirect(crimes)

    player.carteira = player.carteira + (21 * randint(0, player.ataque))
    player.energia_atual = player.energia_atual - 2
    player.save()
    return redirect(crimes)




###############################################################################
###                             Paginas da loja                             ###
###    Listagem de itens, acoes de compras e vendas de armas e armaduras    ###
###############################################################################

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
        player.save()

    return redirect(loja)


#pagina de compra de armas
def comprar_arma(request, item):
    if not request.user.is_authenticated():
        return redirect(logar)

    arma = get_object_or_404(Arma, pk=item)
    player = request.user.get_profile()

    if player.carteira >= arma.compra:
        player.carteira = player.carteira - arma.compra
        player.armas.add(arma) #https://docs.djangoproject.com/en/1.4/ref/models/relations/
        player.save()

    return redirect(loja)


#pagina de venda de armas
def vender_arma(request, item):
    if not request.user.is_authenticated():
        return redirect(logar)

    arma = get_object_or_404(Arma, pk=item)
    player = request.user.get_profile()

    if arma in player.armas.all():
        player.carteira = player.carteira + arma.venda
        player.armas.remove(arma) #https://docs.djangoproject.com/en/1.4/ref/models/relations/
        player.save()

    return redirect(loja)




###############################################################################
###                  Paginas do inventario do usuario                       ###
###                       listagem e troca de itens                         ###
###############################################################################

#pagina de inventario - lista os itens do usuario
def inventario(request):
    if not request.user.is_authenticated():
        return redirect(logar)

    return render_to_response("inventario.html", {"player": request.user.get_profile()})


#pagina para equipar uma armadura
def equipar_armadura(request, item):
    if not request.user.is_authenticated():
        return redirect(logar)
    
    #verifica se a armadura existe no banco de dados
    armadura = get_object_or_404(Armadura, pk=item)
    #recupera o usuario que esta logado
    player = request.user.get_profile()
    
    #antes de ativar a armadura, tem que ver se o usuario possui essa armadura
    if armadura in player.armaduras.all():
        #coloca a armadura como ativa
        player.armadura_ativa = armadura
        player.save() #salva a armadura
    
    #redireciona para a pagina do inventario
    return redirect(inventario)


#pagina para equipar uma arma
def equipar_arma(request, item):
    if not request.user.is_authenticated():
        return redirect(logar)
    
    #verifica se a arma existe no banco de dados
    arma = get_object_or_404(Arma, pk=item)
    #recupera o usuario que esta logado
    player = request.user.get_profile()
    
    #antes de ativar a arma, tem que ver se o usuario possui essa arma
    if arma in player.armas.all():
        #coloca a arma como ativa
        player.arma_ativa = arma
        player.save() #salva a arma
    
    #redireciona para a pagina do inventario
    return redirect(inventario)