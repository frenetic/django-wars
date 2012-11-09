from django.shortcuts import render_to_response # funcoes de renderizacao dos templates
from django.shortcuts import redirect # Funcao para executar um http-redirect


#pagina do hospital
def hospital(request):
    if not request.user.is_authenticated():
        return redirect('pagina_de_login')
    
    #da um refrash no hp, energia e raiva do player
    player = request.user.get_profile()
    player.refresh()
    player.save()
    
    return render_to_response("hospital.html", {"player": request.user.get_profile(),
                                                "vida": request.user.get_profile().vida * 10}) # para exibir o total de vida do usuario


#curar um numero qualquer
def curar(request, valor):
    if not request.user.is_authenticated():
        return redirect('pagina_de_login')
    
    player = request.user.get_profile()

    valor = int(valor) #o valor eh passado para a view como string, precisamos q ele seja integer

    #se for um valor menor que 11, cura
    #se nao for, ignora para nao "travar" o site com um mega loop
    if valor < 11:
        for i in range(valor):
            if player.carteira >= 100 and player.hp <= player.vida * 10:
                player.hp = player.hp + 1
                player.carteira = player.carteira - 100
            else:
                break

        #atualiza o jogador
        player.save()

    #retorna para a pagina do hospital
    return redirect(hospital)


#pagina para curar o quanto der
def curarx(request):
    if not request.user.is_authenticated():
        return redirect('pagina_de_login')
    
    player = request.user.get_profile()

    #verifica se o jogador esta full hp
    if player.hp == player.vida * 10:
        redirect(hospital)

    #enquanto o hp do jogador for menor que o maximo
    #e enquanto ele tiver dinheiro para pagar
    while player.hp < player.vida * 10 and player.carteira >= 100:
        player.hp = player.hp + 1
        player.carteira = player.carteira - 100

    #salva as alteracoes
    player.save()
    
    #volta para o hospital
    return redirect(hospital)