from django.forms import ModelForm
from django import forms


from Notification.models import Notification


class NotifieéForm(ModelForm):
	class Meta:
		model = Notification
		fields = '__all__'