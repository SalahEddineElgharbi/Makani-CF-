from django.shortcuts import render,redirect
from mybasic_app.models import User

from mybasic_app.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from mybasic_app.models import (User, Evaluateur, Chercheur,
								Commite, Conferance, Article, Topic)
from mybasic_app.decorators import evaluteur_required



# hadi hiyaa li rahi t9l3naaa 

@login_required
def Update(request):
	if request.user.is_authenticated:
		if request.user.is_evaluteur:
			division(request)
			return redirect('evaluteur:dashboardeval')

		if request.user.is_superuser:
			division(request)
			return redirect('/MakaniAdmin')

	else:
		return render(request, 'registration/login.html')





@login_required
def division(request):
	print('*****************************************************')
	print('*************************************************************')
	print('*************************************************************************')



	All_Conf = Conferance.objects.all()
	All_Eval = Evaluateur.objects.all()
	All_Comite = Commite.objects.all()
	All_Artcl = Article.objects.all()             #obj >>>>>   queryset  >>>> liste bch nkhdeme bien 



 	#+++++++++++++++++++++++++++++++++ evite problem de duplication et ecrasment ::
	for evll in All_Eval:
		evll.artcl_a_corrige.clear()
		
			

	nb_cf = All_Conf.count()
	nb_evl = All_Eval.count()
	nb_cm = All_Comite.count()
	nb_acl = All_Artcl.count()

	list_of_evl = list(All_Eval)
	list_articl = list(All_Artcl)
	liste_of_commite = list(All_Comite)
	
	i = 0
	l=0
	g=0
	s=0
	w=0
	a=0

  # ++++++++++++++++++++++++++++++++++++++++++++++
	Choisi_par_3 = Pair.objects.all()
	List_off_Choisi_par_3=list(Choisi_par_3)
	List_off_Artcl_Choix = []


	for a in range(len(List_off_Choisi_par_3)):         # hatite ga3 li khayroohom fi liste 
		List_off_Artcl_Choix.append(List_off_Choisi_par_3[a].arti)
		


	print('')
	print('///////////////*** les article par Sont comite apre mth 1 + 2 ***/////////////////////')
	print('')


	for Conf in All_Conf:

		for j in range(nb_cm):


			evl_in_cm=liste_of_commite[j].evaluteur_list.all()
			list_of_evl_iN_cm = list(evl_in_cm)   # hna nkhdeme dakhel fi kol commite b index t3 chaque eval
			
			if Conf.Commite == liste_of_commite[j]:

			

				#+++++++++++++++++++++++++++++++
				print('')
				print('////////*** Aplle de 3eme methode de choix ***/////')
				print('')

				Destribute(request,liste_of_commite[j].pk) #hadi  bach n3yte distrubue w nmdlhom par mth 3

				Nbr_eval_in_Cm = 0
				Nbr_Artcl_in_Cm = 0

				Nbr_eval_in_Cm =len(list_of_evl_iN_cm)
		
				print('')
				print('////*** Division __Commite > ',liste_of_commite[j] ,' ***////')
				print('')


				for art in range(nb_acl):
	
					if  list_articl[art] not in  List_off_Artcl_Choix :     # le cas de pas choisi donc :
				

							if list_articl[art].Conferance == Conf:
								Nbr_Artcl_in_Cm = Nbr_Artcl_in_Cm + 1 
												  
			
								Mx_index_D_evl_in_cm = len(list_of_evl_iN_cm) - 1 # hado (-1) bch nbda b index de liste ml zero
							

								if Nbr_Artcl_in_Cm <= Nbr_eval_in_Cm:
									s = Mx_index_D_evl_in_cm - g  
									if s>=0:			      
										list_of_evl_iN_cm[s].artcl_a_corrige.add(list_articl[art])
									
										g=g+1


								if Nbr_eval_in_Cm<Nbr_Artcl_in_Cm:                                             
									w = Mx_index_D_evl_in_cm - l  
									if w >=0:  
									   list_of_evl_iN_cm[w].artcl_a_corrige.add(list_articl[art])
									   
									   l = l + 1
									else :
										l=0
										w = Mx_index_D_evl_in_cm - l
										list_of_evl_iN_cm[w].artcl_a_corrige.add(list_articl[art])
										
										l = l + 1     # kyn riglage hna matnsahchee

					else: #cas t3 li khayro c bn ta3tihomlhom 

						# hada zdetehe bch tmdelna nmbr article f cm nichan maybdach yzidena kol khatera t3 li khyrhom
						if list_articl[art].Conferance == Conf:
							Nbr_Artcl_in_Cm = Nbr_Artcl_in_Cm + 1 

						for a in range(len(List_off_Choisi_par_3)):
								if ((List_off_Choisi_par_3[a].arti==list_articl[art])
															 and (List_off_Choisi_par_3[a].comit== liste_of_commite[j])):

									List_off_Choisi_par_3[a].evalu.artcl_a_corrige.add(List_off_Choisi_par_3[a].arti)
											

		  # pour reinsializeee les varrr pour novel comm
		g=0
		l=0

		print(' Confrence >>>>>> ',Conf,' Nbr_arcl = :', Nbr_Artcl_in_Cm ,'Et Nbr_eval =: ', Nbr_eval_in_Cm)






#///////////////////////////////////////////////////////////////////////////////////// 27/05/2020 
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
##########################################################
from django.db.models import Q
from G__evaluation.models import Pair,Choosing_map



@login_required
def Destribute(request , pk):
	conf = Conferance.objects.get(Commite = pk)
	comit = Commite.objects.get( pk = pk )
	evals = comit.evaluteur_list 
	qs = Article.objects.filter(Conferance = conf)


	Choix_auncien = Pair.objects.filter(comit=pk)
	for choix in Choix_auncien :
		choix.delete()                  #pour evite les auncien choix et ecrase tjr active avec nvvv
		                                 #  w tani bch ykhdem b likhyrehom mchi yg3ode il ybdel 



	for ar in qs :
	
		art1 = Choosing_map.objects.filter(art1 = ar)
		art2 = Choosing_map.objects.filter(art2 = ar)
		art3 = Choosing_map.objects.filter(art3 = ar)

		arts = Choosing_map.objects.filter( Q(art1 = ar) | Q(art2 = ar) | Q(art3 = ar) ).order_by('satis')

		if not arts :		
			continue

   				
		if arts.first().evalu in evals.all() :
			pair = Pair(comit = comit , evalu = arts.first().evalu , arti = ar)
			pair.save()


		if arts.first() in art1 :

			sample = Choosing_map.objects.filter(evalu = arts.first().evalu , comit = comit ).first()
			sample.satis += 3
			sample.save()


		if arts.first() in art2 :
			sample = Choosing_map.objects.filter(evalu = arts.first().evalu , comit = comit ).first()
			sample.satis += 2
			sample.save()

		if arts.first() in art3 :
			sample = Choosing_map.objects.filter(evalu = arts.first().evalu , comit = comit ).first()
			sample.satis += 1
			sample.save()


	clean = Choosing_map.objects.all() 
	for one in clean :
		one.satis = 0
		one.save()


	context = { }




