# Create your views here.
from django.shortcuts import render_to_response # funcoes de renderizacao dos templates
from django.shortcuts import redirect # Funcao para executar um http-redirect

from djangowars.players.models import Player # precisamos para listar os alvos





# pagina que lista os possiveis alvos
def alvos(request):
    if not request.user.is_authenticated():
        return redirect('pagina_de_login')
    
    #da um refrash no hp, energia e raiva do player
    jogador = request.user.get_profile()
    jogador.refresh()
    jogador.save()
    
    
    #pega os alvos
    # jogadores que estejam no range entre 60% e 140% da xp do jogador
    # nao pode ser o nosso jogador
    # nao pode ser um jogador com 0 de experiencia
    # pega apenas 10
    # quem me deu a dica de como aninhar varios filtros de forma elegante, de acordo com a PEP-8 foi o Renato Oliveira <http://www.labcodes.com.br/>
    alvos = Player.objects.filter(
        experiencia__gte = (jogador.experiencia * 0.6)
    ).filter(
        experiencia__lte = (jogador.experiencia * 1.4)
    ).exclude(
        id = jogador.id
    ).exclude(
        experiencia = 0
    )[:10]
    
    
    
    return render_to_response("alvos.html", {"player": jogador,
                                             "vida": jogador.vida * 10,
                                             "alvos": alvos})