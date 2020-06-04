from django.shortcuts import render,redirect
from mybasic_app.models import User
from mybasic_app.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from mybasic_app.models import (User, Evaluateur, Chercheur,
								Commite, Conferance, Article, Topic)
from mybasic_app.decorators import evaluteur_required
from django.views.decorators.csrf import requires_csrf_token


# hadi hiyaa li rahi t9l3naaa 
@requires_csrf_token
@login_required
def Update(request):
	if request.user.is_authenticated:
		if request.user.is_evaluteur:
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
	#nb_acl = All_Artcl.count()

	list_of_evl = list(All_Eval)
	#list_articl = list(All_Artcl)
	liste_of_commite = list(All_Comite)
	



	print('')
	print('///////////////*** les article par comite apre mth 1 + 2 ***/////////////////////')
	print('')

	for Conf in All_Conf:
		#for j in range(nb_cm):
			
			#if Conf.Commite == liste_of_commite[j]:
				
				#+++++++++++++++++++++++++++++++
		print('')
		print('////////*** Aplle de 3eme methode de choix ***/////')
		print('')


		# ++++++++++++++++++++++++++++++++++++++++++++++




		#evl_in_cm = liste_of_commite[j].evaluteur_list.all()
		evl_in_cm = Conf.Commite.evaluteur_list.all()
		#list_of_evl_iN_cm = list(evl_in_cm)   # hna nkhdeme dakhel fi kol commite b index t3 chaque eval
		Nbr_Artcl_in_Cm = 0
		Num_eval_in_Cm = 0

	 #####################################
	 ##################################
	 #############################


	
		qs = Article.objects.filter(Conferance = Conf)
		list_articl = list(qs)


		for a in evl_in_cm :
			a.count_pair_temporaire = 0
			a.save()


		clean = Choosing_map.objects.all() 
		for one in clean :
			one.satis = 0
			one.save()

		ar_num = qs.count()
		ev_nu = evl_in_cm.count()

		limit = ar_num // ev_nu

		if  ar_num % ev_nu != 0 :
			limit += 1

		#'EV = evals.filter(count_pair_temporaire__lte = limit )

		##############################################################################
		##############################################################################
		##############################################################################

	

		Destribute(request,Conf.Commite.pk,limit) #hadi  bach n3yte distrubue w nmdlhom par mth 

		evl_in_cm = Conf.Commite.evaluteur_list.all()
		list_of_evl_iN_cm = list(evl_in_cm) 
		



		Choisi_par_3 = Pair.objects.filter(comit = Conf.Commite)
		List_off_Choisi=list(Choisi_par_3)
													 
		Nbr_eval_in_Cm = len(list_of_evl_iN_cm)        # 4  evaluateurs dans chaque comite
		# si il n ya pas d'evaluateur !! on sort

	###########################  1. distribution article choisi    ##########""################"
		List_off_Choisi_par_3 = []
		for a in range(len(List_off_Choisi)):

			List_off_Choisi[a].evalu.artcl_a_corrige.add(List_off_Choisi[a].arti)  
			List_off_Choisi_par_3.append(List_off_Choisi[a].arti)
	#############################################################################################""


		# list_articl = sub(list_articl, List_off_Choisi_par_3) --> article non choisi 
		c = [x for x in list_articl if x not in List_off_Choisi_par_3]

		list_articl = c 


		nb_acl = len(list_articl)

                      
		print('limit    >>>>>>>>>> ',limit ,'>>>>>>>>>')
		print('evals    >>>>>>>>>> ',Nbr_eval_in_Cm ,'>>>>>>>>>')
		for art in range(nb_acl):    # article de comite non choisit  

			print('Chaque Confrence   >>>>>>>>>> ',nb_acl,'>>>>>>>>>' ,art)

			give = False

			while ((Num_eval_in_Cm != Nbr_eval_in_Cm ) & (not give)) :
				if list_of_evl_iN_cm[Num_eval_in_Cm].count_pair_temporaire < limit :
					list_of_evl_iN_cm[Num_eval_in_Cm].artcl_a_corrige.add(list_articl[art]) 

					give = True
					list_of_evl_iN_cm[Num_eval_in_Cm].count_pair_temporaire = list_of_evl_iN_cm[Num_eval_in_Cm].count_pair_temporaire + 1
					print('article ',list_articl[art].name ,'distribué a ',list_of_evl_iN_cm[Num_eval_in_Cm])

				Num_eval_in_Cm = Num_eval_in_Cm + 1
				
				if Num_eval_in_Cm == Nbr_eval_in_Cm :
					Num_eval_in_Cm = 0
			
	

		for a in evl_in_cm :
			a.count_pair_temporaire = 0
			a.save()



							 


		print('Chaque Confrence   >>>>>>>>>> Title = ',Conf.title ,'Et Nbr_eval =: ', Nbr_eval_in_Cm)    

	return render(request, 'Pour_Evaluaéé/mth_evluéé.html')
	
  

#///////////////////////////////////////////////////////////////////////////////////// 27/05/2020 
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
##########################################################
from django.db.models import Q
from G__evaluation.models import Pair,Choosing_map



@login_required
def Destribute(request , pk, limit):
	

	Choix_auncien = Pair.objects.filter(comit=pk)
	for choix in Choix_auncien :
		choix.delete()                  #pour evite les auncien choix et ecrase tjr active avec nvvv
										 #  w tani bch ykhdem b likhyrehom mchi yg3ode il ybdel 


	
	comit = Commite.objects.get( pk = pk )
	evals = comit.evaluteur_list.all() 
	
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
			 ##############################################################################  using "count_pair_temporaire"


			for S in EV :

				EEV = EEV.union(Evaluateur.objects.filter(pk = S , count_pair_temporaire__lt = limit ))

			EV = EEV.filter(count_pair_temporaire__lt = limit )

			 ##############################################################################
			 ##############################################################################
			 ##############################################################################



			if not (arti and EV) :  ################################### because there is nothing like a "do while" in django , i had to do a ( while true : if condition :break )
				break






 ####################################################################*##########
 ##############################################################################
 ##############################################################################


	



	clean = Choosing_map.objects.all() 
	for one in clean :
		one.satis = 0
		one.save()


	context = {}