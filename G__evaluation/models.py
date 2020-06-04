from django.db import models
from mybasic_app.models import Evaluateur,Article,Commite
#+++++++++++++++++++ 27/05/2020
#######  choix
############################################### should be in G__evaluateur  


class Pair(models.Model):
    evalu = models.ForeignKey(Evaluateur ,null=True,  on_delete=models.CASCADE)
    arti = models.ForeignKey(Article ,null=True,  on_delete=models.CASCADE)
    comit = models.ForeignKey(Commite ,null=True,  on_delete=models.CASCADE)


    def __str__(self):
        return self.evalu.user.username


class Choosing_map(models.Model):
    comit = models.ForeignKey(Commite ,null=True,  on_delete=models.CASCADE)
    evalu = models.ForeignKey(Evaluateur ,null=True,  on_delete=models.CASCADE)
    satis = models.PositiveIntegerField(default=0)

    # by the way it's fucking useless that way , rather then the whole packet of Article objects i want something like a queryset 
    
    # also i should check the case when two fields map to the same article ( a repeat ) probalbly i can add conditions the prevents that 
    art1 = models.ForeignKey(Article ,null=True,  on_delete=models.CASCADE , related_name='art1')
    art2 = models.ForeignKey(Article ,null=True,  on_delete=models.CASCADE , related_name='art2')
    art3 = models.ForeignKey(Article ,null=True,  on_delete=models.CASCADE , related_name='art3')



    def __str__(self):
        return self.evalu.user.username

    def save(self, *args, **kwargs):
        if self.art1==self.art2 or self.art1==self.art3 or self.art2 == self.art3:
          return #any person can only be a mum or a dad, not both   # ++++++  erreur
        else:
          super(Choosing_map, self).save(*args, **kwargs)


