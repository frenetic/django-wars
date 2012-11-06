# Create your views here.
from django.shortcuts import render_to_response # funcoes de renderizacao dos templates
from django.shortcuts import redirect # Funcao para executar um http-redirect
from django.shortcuts import get_object_or_404 # funcao para buscar um item no banco de dados. Se nao encontrar, retorna um http 404 - page not found

from djangowars.itens.models import Arma, Armadura #importa os modelos de armas e armaduras




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