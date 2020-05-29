from django.urls import path
from G__evaluation import views




urlpatterns = [
    #path('ListeFinal',views.Liste_choisi,name='ListeFinal'),
    #path('',views.division,name='enChoix'),
    path('Update',views.Update,name='Update'),


  #######"""++++++++++++

    #path('Comites',views.Comit,name='comites'),    #######  choix
    #path('specefic/<str:pk>/',views.Specefic ,name='specefic_comite'), #######  choix
    #path('Destr/<str:pk>/',views.Destribute,name='Destr'), #######  choix

 ###### ++++++++++++




    	]