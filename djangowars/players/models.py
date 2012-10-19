from django.db import models
#importamos o modelo de usuario do Django para "extende-lo"
from django.contrib.auth.models import User
from django.db.models.signals import post_save

#importamos as armas e armaduras
from djangowars.itens.models import Arma, Armadura


# Create your models here.
class Player(models.Model):
    #fazendo o relacionamento entre o usuario Django e o player
    #Docs: https://docs.djangoproject.com/en/1.4/topics/auth/#storing-additional-information-about-users
    user = models.OneToOneField(User)
    
    #campos que definem o player do jogo
    carteira = models.FloatField(default=0) #dinheiro na mao
    banco = models.FloatField(default=0) #dinheiro no banco
    
    ataque = models.PositiveSmallIntegerField(default=10)
    defesa = models.PositiveSmallIntegerField(default=10)
    vida = models.PositiveSmallIntegerField(default=10)
    energia = models.PositiveSmallIntegerField(default=20) #energia para fazer roubos
    raiva = models.PositiveSmallIntegerField(default=5) #raiiva para atacar outros players
    
    hp = models.PositiveIntegerField(default=100) #hp = vida * 10
    energia_atual = models.PositiveIntegerField(default=20)
    raiva_atual = models.PositiveIntegerField(default=5)
    
    nivel = models.PositiveSmallIntegerField(default=1)
    experiencia = models.PositiveIntegerField(default=0)
    
    hp_update = models.DateTimeField(auto_now_add=True) # 1 de hp a cada 2 minutos
    energia_update = models.DateTimeField(auto_now_add=True) # 1 de energia a cada minuto
    raiva_update = models.DateTimeField(auto_now_add=True) # 1 de raiva a cada 5 minutos

    #relacionamentos
    armas = models.ManyToManyField(Arma)
    armaduras = models.ManyToManyField(Armadura)

    #itens ativos
    arma_ativa = models.ForeignKey(Arma, null=True, related_name="+")
    armadura_ativa = models.ForeignKey(Armadura, null=True, related_name="+")
    
    #pontos ao subir de nivel
    pontos = models.PositiveSmallIntegerField(default=0)
    
    
    #verifica se o player subiu de nivel
    def level_up(self):
        #definimos a quantidade de xp para cada nivel
        experiencia_necessaria = {1: 10, 2: 20, 3: 30, 4: 50, 5: 80,
                                  6: 130, 7: 210, 8: 340, 9: 480, 10: 630,
                                  11: 790, 12: 970, 13: 1200, 14: 1600, 15: 2000,
                                  16: 2500, 17: 3000, 18: 4000, 19: 5000, 20: 6000}
        
        if self.experiencia >= experiencia_necessaria[self.experiencia + 1]:
            self.nivel = self.nivel + 1 #sobe de nivel
            self.pontos = pontos + 5 #adiciona 5 pontos para o usuario distribuir
            self.hp = self.vida * 10 #recupera a vida
            self.energia_atual = self.energia #recupera a energia
            self.raiva_atual = self.raiva #recupera a raiva
            
            return True
        else:
            return False




# funcao que cria o player toda vez que um usuario for criado pelo Django.contrib.auth
def cria_user_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)

#configurando o signal que detecta quando um usuario eh criado
#ao detectar, executa a funcao acima (cria_user_payer) para termos o
# "perfil" do jogador ligado ao usuario
# vide documentacao: https://docs.djangoproject.com/en/1.4/topics/auth/#storing-additional-information-about-users
post_save.connect(cria_user_player, sender=User) # USER = importado na linha 3
