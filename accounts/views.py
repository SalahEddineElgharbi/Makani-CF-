from django.shortcuts import render,get_object_or_404, redirect
from django.db.models import ProtectedError
from django.http import HttpResponse

from django.urls import reverse_lazy,reverse
from django.views.generic import ListView, CreateView, UpdateView, RedirectView, DetailView, DeleteView, TemplateView

from .forms import EvalForm, CherForm,ConfForm, ComiteForm
from mybasic_app.models import User,Conferance,Article, Commite

from mybasic_app.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required





  # donc ydkol SSi ykon Admin
@method_decorator([login_required, staff_member_required], name='dispatch')
class HomePageView(TemplateView): 
    template_name= "accounts/dashboard.html"


#///////////////////partie evaluateur//////////////////////////////////
@method_decorator([login_required, staff_member_required], name='dispatch')
class evalList(ListView):
   template_name = 'accounts/liste_eval.html'
   model = User        
   paginate_by = 5

   def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    
    context['number'] = User.objects.filter(is_evaluteur=True).count()
 
    return context


#///////////////////////////////////////////////////////////////////////////////////////////////
@method_decorator([login_required, staff_member_required], name='dispatch')
class EvalCreateView(CreateView):
    template_name = "accounts/addUser.html"
    form_class = EvalForm
        
    def form_valid(self, form):
        
       return super(EvalCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('ges_eval')

#///////////////////////////////////////////////////////////////////////////////////////////////

@method_decorator([login_required, staff_member_required], name='dispatch')
class EvalUpdateView(UpdateView):
    template_name = 'accounts/edit_user.html'
    model = User
    form_class = EvalForm
    

    def get_success_url(self):
        return reverse_lazy('ges_eval')

#///////////////////////////////////////////////////////////////////////////////////////////////

@method_decorator([login_required, staff_member_required], name='dispatch')
class EvalDeleteView(DeleteView):
    model = User

    template_name = 'accounts/evaluateur_confirm_delete.html'

    def form_valid(self, form):       
        return super(EvalDeleteView, self).form_valid(form)
    def get_success_url(self):
        return reverse_lazy('ges_eval')





#///////////////////partie chercheur//////////////////////////////////

@method_decorator([login_required, staff_member_required], name='dispatch')
class cherList(ListView):
   template_name = 'accounts/liste_cher.html'
   model = User        
   paginate_by = 5

   def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['number'] = User.objects.filter(is_chercheur=True).count()
    return context

#///////////////////////////////////////////////////////////////////////////////////////////////

@method_decorator([login_required, staff_member_required], name='dispatch')
class CherCreateView(CreateView):
    template_name = "accounts/addUser.html"
    form_class = CherForm
        
    def form_valid(self, form):
        
        return super(CherCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('ges_cher')

#////////////////////////////////////////////////////////////////////////////////////////////////



@method_decorator([login_required, staff_member_required], name='dispatch')
class CherUpdateView(UpdateView):
    template_name = 'accounts/edit_user.html'
    model = User
    form_class = CherForm

    def get_success_url(self):
        return reverse_lazy('ges_cher')


#////////////////////////////////////////////////////////////////////////////////////////////////


@method_decorator([login_required, staff_member_required], name='dispatch')
class CherDeleteView(DeleteView):
    model = User
    template_name = 'accounts/chercheur_confirm_delete.html'

    def form_valid(self, form):
        
        return super(CherDeleteView, self).form_valid(form)
    def get_success_url(self):
        return reverse_lazy('ges_cher')


#################################################################################
###########################    t3 Gconf ############################################"""


@method_decorator([login_required, staff_member_required], name='dispatch')
class confList(ListView):
   template_name = 'gConf/list_Conf.html'
   model = Conferance        
   paginate_by = 5

   def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['number'] = Conferance.objects.all().count()
    return context
#///////////////////////////////////////////////////////////////////////////////////////////////
@method_decorator([login_required, staff_member_required], name='dispatch')
class ConfCreateView(CreateView):
    template_name = "gConf/add-conf.html"
    form_class = ConfForm
        
    def form_valid(self, form):
       return super(ConfCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('ges_conf')

#///////////////////////////////////////////////////////////////////////////////////////////////

@method_decorator([login_required, staff_member_required], name='dispatch')
class ConfUpdateView(UpdateView):
    template_name = 'gConf/edit_conf.html'
    model = Conferance
    form_class = ConfForm

    def get_success_url(self):
        return reverse_lazy('ges_conf')

#///////////////////////////////////////////////////////////////////////////////////////////////
@method_decorator([login_required, staff_member_required], name='dispatch')
class ConfDeleteView(DeleteView):
    template_name = 'gConf/conferance_confirm_delete.html'
    model = Conferance
    def form_valid(self, form):
        

        return super(ConfDeleteView, self).form_valid(form)
    def get_success_url(self):
        return reverse_lazy('ges_conf')

#///////////////////////////////////////////////////////////////////////////////////////////////

@method_decorator([login_required, staff_member_required], name='dispatch')
class ConfDetailView(DetailView):
    template_name = 'gConf/edit_conf.html'
    model = Conferance


#///////////////////////////////////////////////////////////////////////////
@method_decorator([login_required, staff_member_required], name='dispatch')
class Confmodifier(DetailView):
    template_name = 'gConf/modifier.html'
    model = Conferance



#//////////////////////////////////////////////////////////
@login_required
@staff_member_required
def ArticlList_Conf(request, pk):
    conferance = Conferance.objects.get(id = pk)
    articles= Article.objects.filter(Conferance = conferance)
    Nbr_Articl = articles.count()
    context = {'articles':articles, 'conferance':conferance, 'Nbr_Articl':Nbr_Articl}
    return render(request, 'gConf/Arctl_conf.html', context)




#///////////////////////////////////////////////////////////////////////////////////////////////
@method_decorator([login_required, staff_member_required], name='dispatch')
class ComiteCreateView(CreateView):
    template_name = "gConf/add_comite.html"
    form_class = ComiteForm  
    def form_valid(self, form):
       return super(ComiteCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('confCreate')




#//////////////////////////////////////////////////////////////////////////////////////////////
@method_decorator([login_required, staff_member_required], name='dispatch')
class ComiteUpdateView(UpdateView):
    template_name = 'gConf/edit_comite.html'
    model = Commite
    form_class = ComiteForm
    def get_success_url(self):
        return reverse('modifier',kwargs={'pk': self.object.pk})









############################################################################
############################################################################
############################################################################
# +++++++++++++++++++  Statistique rusalt with charJs and django  03/06/2020 ++++++++++++++++++++         
from mybasic_app.models import (User,Conferance,Article, Commite,
Evaluateur,Chercheur,Commite)
from django.http import JsonResponse




def StatistiQue_Data_evl_artcl(request):
    Eval_data = []
    evl =Evaluateur.objects.all()
    for e in evl :
        d=0
        d=e.artcl_a_corrige.all().count()
        Eval_data.append({e.user.username:d})
    return JsonResponse(Eval_data,safe=False)




def StatistiQue_Data_comite_eval(request):
    Comite_data = []
    Cm = Commite.objects.all()

    for c in Cm :
        d=0
        for i in c.evaluteur_list.all():
            d+=1
        Comite_data.append({c.Name:d})
    return JsonResponse(Comite_data,safe=False)



def StatistiQue_Data_articl_chrch(request):
    Artcl_Data = []
    Art = Article.objects.all()
    Chr=Chercheur.objects.all()
    for ch in Chr:
        d=0
        for c in Art:
            if c.author == ch :
                d+=1    
        Artcl_Data.append({ch.user.username:d})
        
    return JsonResponse(Artcl_Data,safe=False)






def StatistiQue_Data_Conf_topic(request):
    Conf_Data = []
    Conf_Data.append({"":""})
    Conf = Conferance.objects.all()

    for c in Conf :
        for i in c.topic.all():
            Conf_Data.append({c.title:i.title})
        
    return JsonResponse(Conf_Data,safe=False)






def StatistiQue_Data_articl_Confreance(request):
    Artcl_Data = []
    Art = Article.objects.all()
    Conf = Conferance.objects.all()
    for cf in Conf:
        d=0
        for c in Art:
            if c.Conferance == cf :
                d+=1    
        Artcl_Data.append({cf.title:d})
        
    return JsonResponse(Artcl_Data,safe=False)