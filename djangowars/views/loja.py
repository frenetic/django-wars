# Create your views here.
from django.shortcuts import render_to_response # funcoes de renderizacao dos templates
from django.shortcuts import redirect # Funcao para executar um http-redirect
from django.shortcuts import get_object_or_404 # funcao para buscar um item no banco de dados. Se nao encontrar, retorna um http 404 - page not found

from djangowars.itens.models import Arma, Armadura #importa os modelos de armas e armaduras




# pagina da loja:
def loja(request):
    if not request.user.is_authenticated():
        return redirect('pagina_de_login')

    armas = Arma.objects.filter(secreta=False).order_by('compra', '-venda')
    armaduras = Armadura.objects.filter(secreta=False).order_by('compra', '-venda')

    return render_to_response("loja.html", {"armas": armas,
                                            "armaduras": armaduras,
                                            "player": request.user.get_profile()})


#pagina de compra de armaduras
def comprar_armadura(request, item):
    if not request.user.is_authenticated():
        return redirect('pagina_de_login')

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
        return redirect('pagina_de_login')

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
        return redirect('pagina_de_login')

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
        return redirect('pagina_de_login')

    arma = get_object_or_404(Arma, pk=item)
    player = request.user.get_profile()

    if arma in player.armas.all():
        player.carteira = player.carteira + arma.venda
        player.armas.remove(arma) #https://docs.djangoproject.com/en/1.4/ref/models/relations/
        player.save()

    return redirect(loja)