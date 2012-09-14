from django.db import models
#importamos o modelo de usuario do Django para "extende-lo"
from django.contrib.auth.models import User
from django.db.models.signals import post_save

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


# funcao que cria o player toda vez que um usuario for criado pelo Django.contrib.auth
def cria_user_player(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)

#configurando o signal que detecta quando um usuario eh criado
#ao detectar, executa a funcao acima (cria_user_payer) para termos o
# "perfil" do jogador ligado ao usuario
# vide documentacao: https://docs.djangoproject.com/en/1.4/topics/auth/#storing-additional-information-about-users
post_save.connect(cria_user_player, sender=User) # USER = importado na linha 3
