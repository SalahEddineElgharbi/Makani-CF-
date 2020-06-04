from django.urls import path,re_path
from Notification.views import( NotificationList,NotificationCreateView,NotificationDeleteView,
	NotificationDetailView,Show_notification,Mark_Etat_D_notification)


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++01/06/2020


urlpatterns = [  
 # ++++++++++ pour chercheur et evaluateur 
 	path('show/<int:pk>/',Show_notification,name='Show_notification'),
 	path('Mark_AsViews/<int:pk>/', Mark_Etat_D_notification,name='Mark_Etat_D_notification'),
# pour adminstration voir liste et .... les Notification  	
    path('List/', NotificationList.as_view(), name="List_Notifeé"),
    path('Create/', NotificationCreateView.as_view(), name="Creat_Notifeé"),
    path('<int:pk>/deletNotifieé/', NotificationDeleteView.as_view(), name="delete_Notiféé"), 
    path('detaill/<int:pk>', NotificationDetailView.as_view(), name="Detaille_Notifeé"), 


]
