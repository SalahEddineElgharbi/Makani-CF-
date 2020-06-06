from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView,DetailView
from ..decorators import chercheur_required
from ..forms import ChercheurSignUpForm,From_Edite_Profile,ArticleForm,ConfForm
from ..models import User,Chercheur ,Article,Topic,Conferance,Comment

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from django.forms import inlineformset_factory
from django.core.files.storage import FileSystemStorage
from django.contrib.messages.views import SuccessMessageMixin



#+++++++++++++++++
from mybasic_app.filters import FilterClass




class ChercheurSignUpView(SuccessMessageMixin,CreateView):
	model = User
	form_class = ChercheurSignUpForm
	template_name = 'registration/signup.html'
	success_message = "You'r Profile was Create successfully"
	def get_context_data(self, **kwargs):
		kwargs['user_type'] = 'chercheur'

		return super().get_context_data(**kwargs)


	def form_valid(self ,form):
		user = form.save()
		login(self.request, user)
		return redirect('chercheur:dashboardchrch') 



####################
@method_decorator([login_required, chercheur_required], name='dispatch')
class Edit_Myprofil(SuccessMessageMixin,UpdateView):
	template_name = 'Templchercheur/edite_myprofil.html'
	model = User
	form_class = From_Edite_Profile
	success_message = "  %(username)s You'r Profile was Updated successfully"


	def get_success_url(self):
		return reverse_lazy('chercheur:Profile')
	 


@login_required
@chercheur_required
def AccedeauDoc_Aschrch(request):
	User = request.user
	chrch = Chercheur.objects.get(user=User) 
	articles = Article.objects.filter(author = chrch )
	context = {'articles': articles}
	messages.info(request,"Etat d'articles au se moment  , From @Makani-CF- ")
	return render(request, 'Templchercheur/docs/documentation.html',context)




# ++++++++++++++++++++++++ notification  1/06/2020
from Notification.models import Notification


@login_required
@chercheur_required
def profil_chrch(request):
    n=Notification.objects.filter(user=request.user,As_viewed=False)
    us=request.user
    return render(request, 'Templchercheur/profil_chrch.html',{'notifications':n})


@login_required
@chercheur_required
def ToContact(request):
	us = request.user
	messages.info(request," Hi  "+ str(us) + " if you have any problem or issus Contact ! , From @Makani-CF- ")
	return render(request, 'Templchercheur/contactAS_chrcheur.html')



@login_required
@chercheur_required
def Userchrch(request):
	us=request.user
	messages.info(request," Hi  "+ str(us) +" , From @Makani-CF- ")
	return render(request, 'Templchercheur/profile-page.html')


'''

@login_required
@chercheur_required
def AccedeauDoc_Aschrch(request):
	return render(request, 'Templchercheur/docs/documentation.html')
'''


#+++++++++++++++++++++++++++++++++++++++++++++     10/06/2020   +++++++++++++++++++++++++++++-

@login_required
@chercheur_required
def CreeArticle(request ):

	User = request.user
	formset = ArticleForm()   
	if request.method == 'POST':
		formset = ArticleForm(request.POST , request.FILES)
			   
		if formset.is_valid():
			 article = formset.save(commit=False)
			 article.date_posté
			 article.author = Chercheur.objects.get(user=User)
			 article.save()
			 messages.success(request,"Your Article was Created successfully !!!,From @Makani-CF- ")

			 return redirect('chercheur:tach_ARTCL')

	context = {'formset': formset }
	return render(request, 'Templchercheur/register-page.html' ,context)





@login_required
@chercheur_required
def Delete_list(request):
	User = request.user
	researcher = Chercheur.objects.get(user=User)
	articles = Article.objects.filter(author = researcher)
	myfilter=FilterClass(request.GET , queryset=articles)
	articles = myfilter.qs
	context = {'articles': articles ,'myfilter':myfilter}
	messages.warning(request,"Attention Si Clique L'article est supprimeé")
	return render(request, 'Templchercheur/Delete_List_Article.html' , context)





@login_required
@chercheur_required
def Delete(request , pk):
	User = request.user
	researcher = Chercheur.objects.get(user=User)
	article = Article.objects.filter(author = researcher).get(pk = pk)
	article.delete()
	messages.error(request,"Your Article was Deleted successfully, From @Makani-CF- ")

	return redirect('chercheur:list_delete_Article')




@login_required
@chercheur_required
def Update_detaille_list(request):
	User = request.user 
	researcher = Chercheur.objects.get(user=User)
	articles = Article.objects.filter(author = researcher)   ##++++++++++++++ chkon li dar hada aartcile
	comments = Comment.objects.filter(authorComment__chercheur=researcher)
	comments_All = Comment.objects.all()
	myfilter=FilterClass(request.GET , queryset=articles)
	articles = myfilter.qs
	context = {'articles': articles ,'myfilter':myfilter , 'comments':comments,'comments_All':comments_All}
	
	return render(request, 'Templchercheur/les_articl_Detailles.html' , context)




@login_required
@chercheur_required
def Update(request ,pk ):

	User = request.user
	researcher = Chercheur.objects.get(user=User) ##+++++++++++++++  chkon li dar hada aartcile
	article = Article.objects.filter(author = User.id ).get(pk = pk)
	formset = ArticleForm(instance = article)
	
	if request.method == 'POST':
		formset = ArticleForm(request.POST , request.FILES  ,instance = article)
   
		if formset.is_valid():
			 article = formset.save(commit=False)
			 article.date_posté
			 article.author = Chercheur.objects.get(user=User)
			 article.Conferance.name = formset.cleaned_data['Conferance']
			 article.save()
			 messages.success(request,"Your Article was Update successfully !!! , From @Makani-CF-")

			 return redirect('chercheur:tach_ARTCL')

	context = {'formset': formset}
	return render(request, 'Templchercheur/modifèè.html' ,context)





# +++++++++++++++++++++++++++++++++++ 2020/05/15   +++++++++++++++++++++++++++++
  
@login_required
@chercheur_required
def confList(request, pk):
    topic = Topic.objects.get(id = pk)
    conferances= Conferance.objects.filter(topic = topic)
    conf_count = conferances.count()
    context = {'topic':topic, 'conferances':conferances, 'conf_count':conf_count}
    

    return render(request, 'Templchercheur/All_Confernce.html', context)




@method_decorator([login_required, chercheur_required], name='dispatch')
class topicList(SuccessMessageMixin,ListView):
   template_name = 'Templchercheur/All_Topics.html'
   model = Topic        
   paginate_by = 5

   def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['number'] = Topic.objects.all().count()
    return context   




@method_decorator([login_required, chercheur_required], name='dispatch')
class ConfDetailView(DetailView):
    template_name = 'Templchercheur/Conf_Detailles.html'
    model = Conferance
    form_class = ConfForm






# ++++++++++++++++++++++++++++++  2020/06/05 ++++++++++++++++++++++++
from mybasic_app.forms import CommentForm
from mybasic_app.models import Comment,Chercheur,User
from django.shortcuts import get_object_or_404


  
@login_required
@chercheur_required
def add_comment_to_Article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    User = request.user
    if request.method == 'POST' :
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment = form.save(commit=False)
            Comment.article = article
            Comment.authorComment=User
            Comment.save()
            messages.success(request,"Your Comment was Create successfully !!! , From @Makani-CF-")

            return redirect('chercheur:tach_ARTCL')    #, pk=article.pk)
    else :
        form  = CommentForm()
    return render(request,'Commentaire/comment_form.html',{'form' : form})         





  
@login_required
@chercheur_required
def comment_approve(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.approve()
    messages.success(request,"Your Comment off \n"+  str(comment) +" \n was Approved successfully !!! , From @Makani-CF-")
    return redirect('chercheur:tach_ARTCL')




  
@login_required
@chercheur_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    article_pk =comment.article.pk
    comment.delete()
    messages.success(request,"Your Comment was Deleted  !!! , From @Makani-CF-")
    return redirect('chercheur:tach_ARTCL')

