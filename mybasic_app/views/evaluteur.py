from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from ..decorators import evaluteur_required
from ..forms import  EvaluteurSignUpForm,From_Edite_Profile
from ..models import  User,Evaluateur,Article,Conferance,Commite

from django.http import HttpResponseRedirect, HttpResponse





class EvaluteurSignUpView(CreateView):
    model = User
    form_class = EvaluteurSignUpForm
    template_name = 'registration/signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'evaluteur'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        #if Evaluteur.Code_Eval =="makani" :
        user = form.save()
        login(self.request, user)
        return redirect('evaluteur:dashboardeval')         # hadi dashboard en genralle ga33
        #else :
            #return HttpResponseRedirect(reverse('homme'))






@login_required
@evaluteur_required
def profil_eval(request):
	return render(request,'Templevaluteur/Dachboardeval.html')




@login_required
@evaluteur_required
def ToContact(request):
    return render(request,'Templevaluteur/contactAs_evaluteur.html')




@login_required
@evaluteur_required
def Usereval(request):
    return render(request,'Templevaluteur/ProfileEval.html')





@login_required
@evaluteur_required
def evaluéé(request):
    return render(request,'Templevaluteur/evaluation.html')


@login_required
@evaluteur_required
def AccedeauDoc(request):
    return render(request,'Templevaluteur/docs/documentation.html')




####################
@method_decorator([login_required, evaluteur_required], name='dispatch')
class Edit_Myprofil_As_Eval(UpdateView):
    template_name = 'Templevaluteur/Eval_edite_myprofile.html'
    model = User
    form_class = From_Edite_Profile
    
    def get_success_url(self):
        return reverse_lazy('evaluteur:Profile')
     



#+++++++++++++++++++++++++++++++++++++
@method_decorator([login_required, evaluteur_required], name='dispatch')
class Liste_All_Artcl(ListView):
    model = Article
    template_name = 'Templevaluteur/All_Artcles.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nbrArctl'] = Article.objects.all().count()
        return context




@method_decorator([login_required, evaluteur_required], name='dispatch')
class Liste_All_Confrence(ListView):
    model = Conferance
    template_name = 'Templevaluteur/All_Conf.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nbrConf'] = Conferance.objects.all().count()
        return context        



@method_decorator([login_required, evaluteur_required], name='dispatch')
class All_Etat_Du_Cherchr(ListView):
    model = User
    template_name = 'Templevaluteur/All_chercheur.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nbrchrch'] = User.objects.filter(is_chercheur=True).count()
        return context        




@method_decorator([login_required, evaluteur_required], name='dispatch')
class All_Commite(ListView):
    model = Commite
    template_name = 'Templevaluteur/All_Commite.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nbrCommite'] = Commite.objects.all().count()
        return context        







@login_required
@evaluteur_required
def Info_T(request):
    return render(request,'Templevaluteur/info_Ttt.html')





#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
############################################### choix


from ..forms import ChoosingForm      
from G__evaluation.models import Pair,Choosing_map        
from django import forms                                                 


@login_required
@evaluteur_required
def Specefic(request , pk):

    conf = Conferance.objects.get(Commite = pk)
    comit = Commite.objects.get( pk = pk )
    qs_articles = Article.objects.filter(Conferance = conf)

    address = ChoosingForm(conf)


    if request.method == 'POST':

                address = ChoosingForm(conf , request.POST )
                
                if address.is_valid():
                    Choix_auncien = Choosing_map.objects.filter(evalu__user=request.user ,comit=pk)
                    for choix in Choix_auncien :
                        choix.delete()           # pour evite les auncien choix et ecrase tjr active avec nvvv
                        
                    
                    address = address.save(commit=False)
                    address.evalu = Evaluateur.objects.get(user = request.user)
                    address.comit = comit
                    address.save()
                    return redirect('evaluteur:Mes_article_Final')


    context = { 'articles' : qs_articles ,
                'add' : address 
               }

    return render(request,'Templevaluteur/single_comite.html' , context)



@login_required
@evaluteur_required
def Mon_Commite(request ):
    evalu = Evaluateur.objects.get(user = request.user)
    comits = Commite.objects.filter( evaluteur_list= evalu )
    context = { 'comits' : comits }

    return render(request,'Templevaluteur/selected_comite.html' , context)




@login_required
@evaluteur_required
def final(request ): # hna rahi final mli li bghaahhhom brk mchi final pcq mth 1 + 2 9adeere tzidehe des artcl
    evalu = Evaluateur.objects.get(user = request.user)
    comits = Commite.objects.filter( evaluteur_list= evalu )
    paral = Pair.objects.filter( evalu = evalu )
    arts = Article.objects.filter(pair__evalu = evalu)

    data = {}

    for comit in comits :

            for par in paral :

                if (par.comit == comit):

                    data[par.arti] = par.comit


    context = { 'comits' : comits , 'listd' : data , 'evalu':evalu }

    return render(request,'Templevaluteur/Mes_artcl_a_Corrige.html' , context)

