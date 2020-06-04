from django.shortcuts import render , render_to_response,redirect,get_object_or_404
from django.http import HttpResponseRedirect
from Notification.models import Notification
from django.contrib.auth.decorators import login_required
from mybasic_app.decorators import evaluteur_required
from django.urls import reverse_lazy,reverse
from django.views.generic import ListView, CreateView, UpdateView, RedirectView, DetailView, DeleteView, TemplateView
from .forms import NotifieéForm
from mybasic_app.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin


@method_decorator([login_required, staff_member_required], name='dispatch')
class NotificationCreateView(SuccessMessageMixin,CreateView):
		template_name = "Notifie/creat_Notifie.html"
		form_class = NotifieéForm   
		success_message = "  Create  successfully ! "

		def form_valid(self, form):
			 return super(NotificationCreateView, self).form_valid(form)

		def get_success_url(self):
				return reverse_lazy('List_Notifeé')





@method_decorator([login_required, staff_member_required], name='dispatch')
class NotificationList(ListView):
	 context_object_name ='Notification_detail_Makani_CF_'
	 template_name = 'Notifie/liste_D_notification.html'
	 model = Notification        
	 paginate_by = 4

	 def get_context_data(self, **kwargs):
	 	context = super().get_context_data(**kwargs)
	 	context['Nbr_Notification_eval'] = Notification.objects.filter(user__is_evaluteur=True).count()
	 	context['Nbr_Notification_chr'] = Notification.objects.filter(user__is_chercheur=True).count()
	 	return context



@method_decorator([login_required, staff_member_required], name='dispatch')
class NotificationDetailView(DetailView):
		template_name = 'Notifie/detaille_Notifieé.html'
		model = Notification







@method_decorator([login_required, staff_member_required], name='dispatch')
class NotificationDeleteView(SuccessMessageMixin,DeleteView):
		model = Notification
		template_name = 'Notifie/Confirmation_delete_notifiee.html'
		success_url = reverse_lazy("List_Notifeé")
	

		
		def form_valid(self, form):       
				return super(NotificationDeleteView, self).form_valid(form)





@login_required
def Show_notification(request,pk):
	user=request.user
	n = Notification.objects.get(id=pk)
	return render_to_response('Notifie/notification.html',{'notification':n,'user':user})





@login_required
def Mark_Etat_D_notification (request,pk):
		n = Notification.objects.get(id=pk)
		n.As_viewed = True # c bon rah chafehe 
		n.save()
		messages.success(request,"successfully Mark as read : "+ str(n.title)+ " !!!, From @Makani-CF- ")

		if request.user.is_authenticated:
			if request.user.is_evaluteur:
				return redirect('evaluteur:dashboardeval')

			if request.user.is_chercheur:
				return redirect('chercheur:dashboardchrch')

			#if request.user.is_superuser:
				#return redirect('/MakaniAdmin')


