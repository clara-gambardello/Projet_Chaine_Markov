#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  6 17:37:32 2025

@author: Clara Gambardello
"""

# Import des packages 
import numpy as np
import matplotlib.pyplot as plt


# Chaine de Markov a temps continue

#Fonctions intermédiaire de la fonction finale 

  
def marche_alea (X, nb_pas) : 
    #On choisit un nombre aléatoire entre 1 et 4
    alea = np.random.choice([1, 2, 3, 4])
    
    #Selon le résultat le patient 0 marche
    
    for i in range(nb_pas):
        if alea==1 :
            X[0]+=1
        elif alea==2 :
            X[0]-=1
        elif alea==3:
            X[1]+=1
        else :
            X[1]-=1
    
    return X



def prochaine_action (stock_conta, lam, mu) :
     
    #On réinitialise le vecteur contenant les temps de guérison
    temps_deconta =[]
    conta_count = len(stock_conta)
    
    #Temps de contamination
    temps_conta = np.random.exponential(mu)
    
    #On calcule tous les temps de décontamination
    for i in range (conta_count): 
        temps_deconta.append(np.random.exponential(lam))
 
    #On calcule le minimum de tout ces temps sans le patient 0 (on le traite séparément)
    min_temps = min(temps_deconta[1:], default = np.Infinity)
    
    #Pour le patient 0
    temps_deconta_0 = temps_deconta[0]
    
    #On récupère le minimum de tout ces temps
    temps_action = min(temps_deconta_0, min_temps, temps_conta)
    
    
    #On établit la prochaine action en fonction de ce minimum
    if temps_action == temps_conta :
        action = "contamination"
        
    elif temps_action == temps_deconta_0 :
        action = "guerison_0"
        
    else:
        action ="guerison"
        
    
    return action, temps_action, temps_deconta



def contamination (X0, stock_conta, nb_pas) :
    
    #Calcule de la position du malade contaminant
    X0 = marche_alea(X0, nb_pas)
    
    #Stock dans un vecteur tous ces voisins qu'il contamine
    
    #Vérifier qu'on ne contamine pas deux fois la même personne
    if (X0[0]+1, X0[1]) not in stock_conta :
        stock_conta.append([X0[0]+1, X0[1]])
        
    if ([X0[0], X0[1]-1]) not in stock_conta :  
         stock_conta.append([X0[0], X0[1]-1])
         
    if ([X0[0]-1, X0[1]]) not in stock_conta :     
         stock_conta.append([X0[0]-1, X0[1]])
        
    if ([X0[0], X0[1]+1]) not in stock_conta :    
        stock_conta.append([X0[0], X0[1]+1])
   
    if (X0) not in stock_conta :
        stock_conta.append(X0)
    
    return stock_conta, X0
    

def guerison (temps_deconta, stock_conta) :
    
    #On sort du vecteurs des contaminés le malade guéri
    p_deconta = np.argmin(temps_deconta)
    stock_conta.pop(p_deconta)
    
    return stock_conta



def guerison_0 (stock_conta, lam, temps, nb_conta, X_fin, nb_pas, affichage) :
    
    #Adaptation de la taille des plans pour l'affichage 
    aff_plan = nb_pas*10
    
    #Réinitialisation des temps de décontamination, on enlève le patient 0
    temps_deconta=[]
    stock_conta.pop(0)
    
    
    #Configuration finale des contaminés quand le patient 0 guérit    
    # Séparer les coordonnées x et y
    if affichage :
        
        
        if(len(stock_conta)>0):
        
            #print(stock_conta)
            x, y = zip(*stock_conta)
        
            
            plt.scatter(x, y, label = "patients contaminés")
        plt.scatter(*X_fin, color="red", label = "Patient 0")
        plt.title("Configuration finale à la guérison du patient 0")
        plt.legend()
        plt.grid()
        plt.xticks(range(-aff_plan, aff_plan+1, nb_pas*2))
        plt.yticks(range(-aff_plan, aff_plan+1, 4))
        plt.show()
        plt.close()
    
    
    #Mise a jour du nombre de contaminé
    nb_conta.append(len(stock_conta))

    
    #Temps qu'on a encore des malades on continue
    while stock_conta != [] :
        
        #On retire progressivement des contaminés les malades guéris
        temps_deconta = []
        for i in range (len(stock_conta)): 
            temps_deconta.append(np.random.exponential(lam))


        min_temps = min(temps_deconta)
        
        #Actualisation du vecteur de temps
        temps.append(temps[-1]+min_temps)
        
        stock_conta.pop(np.argmin(temps_deconta))
        nb_conta.append(nb_conta[-1]-1)
    
    return stock_conta, temps, nb_conta
        



#Fonction finale 


def maladie (X_0, lam, mu, nb_pas=1, affichage=0) :
    
    X0 = X_0.copy()
    
    #Vecteurs des contaminés avec le pationt 0
    stock_conta =["patient_0"]
    
    #Historique nombre de contaminés 
    nb_conta = []

    #Contrôle des temps auquel il se passe quelque chose
    temps = [0] 

    #Initialisation de la variable action pour entrer dans la boucle
    action = "a venir"
    
    while ((action != "guerison_0") or (temps[-1]<20)) :
        
        #On détermine la prochaine action
        action, temps_action, temps_deconta = prochaine_action(stock_conta, lam, mu)
        #print(f"action is : {action}")
        
        #On conserve une trace du dernier rapport des contaminés 
        nb_conta.append(len(stock_conta))
        
        #On commence a traité les différentes possibilités selon "action"
        #On prend soin d'actualiser le vecteur de temps 
        temps.append(temps[-1]+temps_action)
        
        if action == "contamination" :
            stock_conta, X0 = contamination(X0, stock_conta, nb_pas)
    
        elif action == "guerison" :
            stock_conta = guerison(temps_deconta, stock_conta)
    
        elif action == "guerison_0" :
            stock_conta, temps, nb_conta = guerison_0 (stock_conta, lam, temps, nb_conta, X0, nb_pas, affichage)
            break
        
        else :
            print(f"Erreur : pas d'action renseigné : {action}")
            
    
    return temps, stock_conta,  nb_conta, temps[-1]
 

       
def simulation_temps_maladie (n, X0, lam, mu, nb_pas=1, affichage=False) :
   
    #Vecteur de simulation 
    temps_maladie = []
    
    #Autant de simulation que demandé
    for i in range (n) : 
        temps_simu, stock_conta_simu, nb_conta_simu, temps_fin_simu= maladie(X0, lam, mu, nb_pas, affichage)
        temps_maladie.append(temps_fin_simu)

    #Moyenne des temps de maladie 
    temps_moyen_extinc = np.mean(temps_maladie)
    
    
    return temps_moyen_extinc


#Pour les paramètres de random on considère l'inverse des valeurs utilisés (pays anglo-saxons)
#Déconramination
lam_fr = 2
#Contamination
mu_fr = 80


#En augmentant mu on augmente le temps d'extinction
lam = 1/lam_fr
mu = 1/mu_fr


pat0 = [0, 0]
n=1000
temps_1, stock_conta_1, nb_conta_1, temps_fin_1 = maladie(pat0, lam, mu, 3, affichage=True)

pat0 = [0, 0]
temps_moyen = simulation_temps_maladie (n, pat0, lam, mu, 3, affichage=False)

print(f"Le temps d'arrêt de la maladie avec lambda  = {1/lam} et mu = {1/mu} est : {temps_fin_1}")
plt.plot(temps_1, nb_conta_1)
plt.title("Nombre de contaminés en fonction du temps")
plt.xlabel("Temps")
plt.ylabel("nombre de contaminés")
plt.close()

print(f"Avec 1000 simulation et les paramètres précédent le temps moyen d'extinction de la maladie est de : {temps_moyen}")



#Graphiques pour le temps en fonction le quotient lambda/mu, lambda fixé

lamb = 30
vec_lam_simu = np.arange(1, 20, 1)
stock_simu = [simulation_temps_maladie (n, pat0, lamb, k, 1, False) for k in vec_lam_simu]
vec_ratio = [i/lamb for i in vec_lam_simu]

plt.plot(vec_ratio, stock_simu)
plt.xlabel("ratio")
plt.ylabel("Temps moyen décontamination")
plt.title(f"Temps moyen de décontamination en fonction de r = μ\λ pour lambda = {lamb}")
plt.show()
plt.close()


#Graphiques pour le temps en fonction le quotient lambda/mu, mu fixé

mu_tr = 30
vec_mu_simu = np.arange(1, 20, 1)
stock_simu = [simulation_temps_maladie (n, pat0, k, mu_tr, 1, False) for k in vec_mu_simu]
vec_ratio = [mu_tr/i for i in vec_mu_simu]

plt.plot(vec_ratio, stock_simu)
plt.xlabel("ratio")
plt.ylabel("Temps moyen décontamination")
plt.title(f"Temps moyen de décontamination en fonction de r = μ\λ pour mu = {mu_tr}")
plt.show()
plt.close()
