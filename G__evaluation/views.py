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
	

# ++++++++++++++++++++++++++++++++++++++++++++++
	Choisi_par_3 = Pair.objects.all()
	List_off_Choisi_par_3=list(Choisi_par_3)
	List_off_Artcl_Choix = []


	for a in range(len(List_off_Choisi_par_3)):         # hatite ga3 li khayroohom fi liste 
		List_off_Artcl_Choix.append(List_off_Choisi_par_3[a].arti)
		

	print('')
	print('///////////////*** les article par comite apre mth 1 + 2 ***/////////////////////')
	print('')

	for Conf in All_Conf:
		for j in range(nb_cm):
			
			if Conf.Commite == liste_of_commite[j]:
				
				#+++++++++++++++++++++++++++++++
				print('')
				print('////////*** Aplle de 3eme methode de choix ***/////')
				print('')

				Destribute(request,liste_of_commite[j].pk) #hadi  bach n3yte distrubue w nmdlhom par mth 3


				evl_in_cm = liste_of_commite[j].evaluteur_list.all()
				list_of_evl_iN_cm = list(evl_in_cm)   # hna nkhdeme dakhel fi kol commite b index t3 chaque eval
				Nbr_Artcl_in_Cm = 0
				Num_eval_in_Cm = 0
				

				print('')
				print('////*** Division __Commite > ',liste_of_commite[j] ,' ***////')
				print('')

															 
				Nbr_eval_in_Cm = len(list_of_evl_iN_cm)         # 4  evaluateurs dans chaque comite
				# si il n ya pas d'evaluateur !! on sort
				for art in range(nb_acl):     

					if  list_articl[art] not in  List_off_Artcl_Choix :     # le cas de pas choisi donc :   

						if list_articl[art].Conferance == Conf:
							Nbr_Artcl_in_Cm = Nbr_Artcl_in_Cm + 1
	
							if Num_eval_in_Cm == Nbr_eval_in_Cm :  
								Num_eval_in_Cm = 0
						
							if Num_eval_in_Cm != Nbr_eval_in_Cm :
								list_of_evl_iN_cm[Num_eval_in_Cm].artcl_a_corrige.add(list_articl[art])
								print('article ',list_articl[art].name ,'distribué a ',list_of_evl_iN_cm[Num_eval_in_Cm])

								Num_eval_in_Cm = Num_eval_in_Cm + 1


					else: #cas t3 li khayro c bn ta3tihomlhom 

						# hada zdetehe bch tmdelna nmbr article f cm nichan maybdach yzidena kol khatera t3 li khyrhom
						if list_articl[art].Conferance == Conf:
							Nbr_Artcl_in_Cm = Nbr_Artcl_in_Cm + 1 

						for a in range(len(List_off_Choisi_par_3)):
								if ((List_off_Choisi_par_3[a].arti==list_articl[art])
															 and (List_off_Choisi_par_3[a].comit== liste_of_commite[j])):

									List_off_Choisi_par_3[a].evalu.artcl_a_corrige.add(List_off_Choisi_par_3[a].arti)


				print('Chaque Confrence   >>>>>>>>>> Title = ',Conf.title ,' Nbr_arcl  = :', Nbr_Artcl_in_Cm ,'Et Nbr_eval =: ', Nbr_eval_in_Cm)	
		
	return render(request, 'Pour_Evaluaéé/mth_evluéé.html')
	
  

#///////////////////////////////////////////////////////////////////////////////////// 27/05/2020 
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
##########################################################
from django.db.models import Q
from G__evaluation.models import Pair,Choosing_map



@login_required
def Destribute(request , pk):
	conf = Conferance.objects.get(Commite = pk)
	comit = Commite.objects.get( pk = pk )
	evals = comit.evaluteur_list.all() 
	qs = Article.objects.filter(Conferance = conf)

	##############################################################################
	##############################################################################
	##############################################################################

	for a in evals :
		a.count_pair_temporaire = 0
		a.save()

	clean = Choosing_map.objects.all() 
	for one in clean :
		one.satis = 0
		one.save()

	ar_num = qs.count()
	ev_nu = evals.count()

	limit = ar_num // ev_nu

	if  ar_num % ev_nu != 0 :
		limit += 1

	#'EV = evals.filter(count_pair_temporaire__lte = limit )

	##############################################################################
	##############################################################################
	##############################################################################


	Choix_auncien = Pair.objects.filter(comit=pk)
	for choix in Choix_auncien :
		choix.delete()                  #pour evite les auncien choix et ecrase tjr active avec nvvv
		                                 #  w tani bch ykhdem b likhyrehom mchi yg3ode il ybdel 





   				







	##############################################################################
	##############################################################################
	##############################################################################

	cho = Choosing_map.objects.filter(comit = comit)
	arti= Article.objects.none()
	EEV = Evaluateur.objects.none()
	hell = Choosing_map.objects.none()

	cho_count = cho.count()
	for k in cho :

		EEV = EEV.union(Evaluateur.objects.filter(pk = k.evalu.pk , count_pair_temporaire__lt = limit ))

	EEV_count = EEV.count()

	EV = EEV.filter(count_pair_temporaire__lt = limit )

	EV_count = EV.count()


 ##############################################
 ############################################## for reduction por
 ##############################################

	for each in EV :
		hell = hell.union(cho.filter(evalu = each)).distinct()

	hell_count = hell.count()

	for k in hell :
			art1 = k.art1
			art2 = k.art2
			art3 = k.art3
		
			arti = Article.objects.filter( Q(pk = art1.pk) | Q(pk = art2.pk) | Q(pk = art3.pk) ).distinct()


 ##############################################
 ##############################################


	if cho :

		while True :

	         ######################################################################################
	          ######################################################################################     arrange the "choosing_maps" that match to "EV" and retreiving their "articles"
	           ######################################################################################
			hell = Choosing_map.objects.none()

			for each in EV :
				hell = hell.union(cho.filter(evalu = each)).distinct()


			for k in hell :
					art1 = k.art1
					art2 = k.art2
					art3 = k.art3
				
					arti = Article.objects.filter( Q(id__in = arti) & (Q(pk = art1.pk) | Q(pk = art2.pk) | Q(pk = art3.pk)) ).distinct()


			 ######################################################################################
			  ######################################################################################
			   ######################################################################################





			eev = hell.order_by('satis')

			indo = eev.first().satis
			bundle = eev.filter(satis = indo)

			for oz in bundle :

				ero1 = oz.art1
				ero2 = oz.art2
				ero3 = oz.art3
				if ero1 in arti :
						if oz.evalu in EV.all() :
							arti = arti.exclude(id =ero1.id)   ######################################################################################
							pair = Pair(comit = comit , evalu = oz.evalu , arti = ero1)
							pair.save()

							this = Evaluateur.objects.get( pk =oz.evalu )
							this.count_pair_temporaire += 1
							this.save()

							sample = Choosing_map.objects.filter(evalu = oz.evalu  , comit = comit ).first()
							sample.satis += 3
							sample.save()

							arti = arti.exclude(id =ero1.id)

							break

				elif ero2 in arti : 
						if oz.evalu in EV.all() :
							arti = arti.exclude(id =ero2.id)   ######################################################################################
							pair = Pair(comit = comit , evalu = oz.evalu   , arti = ero2)
							pair.save()

							this = Evaluateur.objects.get( pk =oz.evalu )
							this.count_pair_temporaire += 1
							this.save()

							sample = Choosing_map.objects.filter(evalu = oz.evalu  , comit = comit ).first()
							sample.satis += 2
							sample.save()

							arti = arti.exclude(id=ero2.id)

							break

				elif ero3 in arti :
						if oz.evalu in EV.all() :
							arti = arti.exclude(id =ero3.id)  ######################################################################################
							pair = Pair(comit = comit , evalu = oz.evalu   , arti = ero3)
							pair.save()

							this = Evaluateur.objects.get( pk =oz.evalu  )
							this.count_pair_temporaire += 1
							this.save()

							break

							sample = Choosing_map.objects.filter(evalu = oz.evalu , comit = comit ).first()
							sample.satis += 1
							sample.save()

							arti = arti.exclude(id =ero3.id)

							break


			 ##############################################################################
			 ##############################################################################  adjust the size of "EV" by making it smaller whenever an ev exceeds the set limit 
			 ##############################################################################	 using "count_pair_temporaire"


			for S in EV :

				EEV = EEV.union(Evaluateur.objects.filter(pk = S , count_pair_temporaire__lt = limit ))

			EV = EEV.filter(count_pair_temporaire__lt = limit )

			 ##############################################################################
			 ##############################################################################
			 ##############################################################################



			if not (arti and EV) :  ################################### because there is nothing like a "do while" in django , i had to do a ( while true : if condition :break )
				break






 ##############################################################################
 ##############################################################################
 ##############################################################################


	for a in evals :
		a.count_pair_temporaire = 0
		a.save()



	clean = Choosing_map.objects.all() 
	for one in clean :
		one.satis = 0
		one.save()


	context = {}
