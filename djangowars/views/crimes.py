# Create your views here.
from django.shortcuts import render_to_response # funcoes de renderizacao dos templates
from django.shortcuts import redirect # Funcao para executar um http-redirect

from random import randint # funcao para escolher um numero aleatorio




# pagina que lista os crimes
def crimes(request):
    if not request.user.is_authenticated():
        return redirect('pagina_de_login')
    
    #da um refrash no hp, energia e raiva do player
    player = request.user.get_profile()
    player.refresh()
    player.save()
    
    return render_to_response("crimes.html", {"player": request.user.get_profile(),
                                              "vida": request.user.get_profile().vida * 10}) # para exibir o total de vida do usuario


# cometendo o crime de nivel 1
def cometer_crime1(request):
    if not request.user.is_authenticated():
        return redirect('pagina_de_login')

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
        return redirect('pagina_de_login')

    player = request.user.get_profile()

    if player.energia_atual < 2 or player.nivel < 2:
        return redirect(crimes)

    player.carteira = player.carteira + (21 * randint(0, player.ataque))
    player.energia_atual = player.energia_atual - 2
    player.save()
    return redirect(crimes)