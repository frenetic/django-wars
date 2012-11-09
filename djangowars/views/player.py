# Create your views here.
from django.shortcuts import render, render_to_response # funcoes de renderizacao dos templates
from django.shortcuts import redirect # Funcao para executar um http-redirect

from django.contrib.auth.forms import UserCreationForm # Formulario de criacao de usuarios
from django.contrib.auth.forms import AuthenticationForm # Formulario de autenticacao de usuarios
from django.contrib.auth import login # funcao que salva o usuario na sessao

from djangowars.players.models import Player




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


# pagina de stats do jogador
def stats(request):
    if not request.user.is_authenticated():
        return redirect('pagina_de_login')
    
    #da um refrash no hp, energia e raiva do player
    player = request.user.get_profile()
    player.refresh()
    player.save()
    
    return render_to_response("stats.html", {"player": player,
                                              "vida": player.vida * 10}) # para exibir o total de vida do usuario


# view que adiciona pontos aos stats do jogador
def adicionar(request, atributo):
    if not request.user.is_authenticated():
        return redirect('pagina_de_login')
    
    
    #pega o jogador logado
    player = request.user.get_profile()
    
    #verifica se o jogador ainda tem pontos para gastar
    if player.pontos > 0:
        #verifica o tipo do atributo para fazer a alteracao
        if atributo.lower() == "ataque":
            player.ataque = player.ataque + 1
            player.pontos = player.pontos - 1
        elif atributo.lower() == "defesa":
            player.defesa = player.defesa + 1
            player.pontos = player.pontos - 1
        elif atributo.lower() == "vida":
            player.vida = player.vida + 1
            player.pontos = player.pontos - 1
        elif atributo.lower() == "energia":
            player.energia = player.energia + 1
            player.pontos = player.pontos - 1
        elif atributo.lower() == "raiva":
            player.raiva = player.raiva + 1
            player.pontos = player.pontos - 1
        
        player.save()
    
    #volta para a pagina de stats
    return redirect(stats)


# pagina rank
def rank(request):
    if not request.user.is_authenticated():
        return redirect('pagina_de_login')
    
    #da um refrash no hp, energia e raiva do player
    jogador = request.user.get_profile()
    jogador.refresh()
    jogador.save()
    
    
    #pega a lista de 50 jogadores ordenado pelo xp
    rank = Player.objects.all().order_by("-experiencia")[:50]
    
    
    return render_to_response("rank.html", {"player": jogador,
                                              "vida": jogador.vida * 10,
                                              "rank": rank})