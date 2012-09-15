from django.db import models


class Arma(models.Model):
    poder = models.PositiveSmallIntegerField()
    compra = models.FloatField() # valor de compra
    venda = models.FloatField() # valor de venda
    secreta = models.BooleanField(default=False) #se a arma eh secreta ou disponivel na loja
    
    imagem = models.ImageField(upload_to="armas") #imagem do item
    
    #nome do item
    nome = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.nome


class Armadura(models.Model):
    poder = models.PositiveSmallIntegerField()
    compra = models.FloatField() # valor de compra
    venda = models.FloatField() # valor de venda
    secreta = models.BooleanField(default=False) #se a armadura eh secreta ou disponivel na loja
    
    imagem = models.ImageField(upload_to="armaduras") #imagem do item
    
    #nome do item
    nome = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.nome