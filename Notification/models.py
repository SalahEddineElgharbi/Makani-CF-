from django.db import models
from learning_user import settings
from django.db.models.signals import post_save #Signal treee importan 
from django.dispatch import receiver



The_User = settings.AUTH_USER_MODEL

class Notification(models.Model):
	title = models.CharField(max_length=256)
	message = models.TextField()
	As_viewed  = models.BooleanField(default=False)
	user = models.ForeignKey(The_User,on_delete=models.CASCADE)
	created_on = models.DateTimeField(auto_now_add=True)
   
	def __str__(self):
		return "Notification To > "+str(self.user)

	class Meta:
		ordering = ['-created_on']





@receiver(post_save , sender=The_User)
def create_welcom_MSG(sender,**Kwargs):
	if Kwargs.get('created',False): # ida kante 1er fois t3he ysne3 compte
		Notification.objects.create(user=Kwargs.get('instance'),
	       title="Wecome to <<<< Makani-CF- site >>>>  ",
message='''
	       	\n
			This should be as clear as possible. This lets the visitor know 
			\n
			they’ve completed the required action and they can expect whatever it is they’ve signed up for.
				  \n \n  \n
			hnaaaaa nmdolehe chwyia t3 les regle wlaaa prsentatio 3la site t3naa 
			\n 
			   *** Thank By @MAKANI-CF-  *** 

''')
	  

