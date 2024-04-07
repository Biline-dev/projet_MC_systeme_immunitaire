import subprocess
from concurrent.futures import ProcessPoolExecutor, wait, ALL_COMPLETED
import sys
import random
import csv
import time
import re

def traitement_ais():

    #Génération des paramètres aléatoires
    nbIndividus = random.randint(100,2500)
    pourcentageClone = random.randint(2,100)
    pourcentageNouveauxIndividus = random.randint(2,100)
    nbGenerations = random.randint(5000,10000)
    nbGenerationRemplacement = random.randint(5,int(nbGenerations-nbGenerations*0.5))
    typeMuteAc = random.randint(0,2)
    typeMeilleur = random.randint(0,1)

    #Création du string de la commande à exécuter
    commande = f"./ais {nbIndividus} {pourcentageClone} {pourcentageNouveauxIndividus} {nbGenerations} {nbGenerationRemplacement} {typeMuteAc} {typeMeilleur}"

    start_time = 0.0
    execution_time = 0.0

    # Début de l'enregistrement du temps
    start_time = time.time()

    #Lancement du programme ./ais avec des paramètres aléatoires
    resultat = subprocess.run(commande,shell=True,stdout=subprocess.PIPE,text=True)

    # Enregistrez le temps de fin
    end_time = time.time()

    execution_time = round(end_time - start_time,3)

    # Utilisation d'une expression régulière pour extraire le coût après la ligne spécifique
    # L'utilisation des parenthèse représente un groupe qui peut être extrait grâce à match.group()
    pattern = re.compile(r'\*\*\* Voici la meilleure solution trouvee \*\*\*\s+Cout:([0-9.]+)')
    match = pattern.search(resultat.stdout)

    if match:
        cout_meilleure_solution = float(match.group(1))
        with open("resultats.csv",'a') as csvfile:
                csvWriter = csv.writer(csvfile)
                csvWriter.writerow([nbIndividus,pourcentageClone,pourcentageNouveauxIndividus,nbGenerations,nbGenerationRemplacement,typeMuteAc,typeMeilleur,cout_meilleure_solution,execution_time])

    else:
        print("Aucun coût trouvé après la ligne spécifique.")
        exit(-1)

def main():

    default = 1
    if(len(sys.argv) > 1):
        default = int(sys.argv[1])
    else:
        print("Utilisation : python3 benchmark2.py [nombreProgramme]")
        exit(-1)

    with ProcessPoolExecutor() as executor:

        #Lance un nombre "i" de tâches en parallèle
        futures = [executor.submit(traitement_ais) for i in range(default)]
        #On attends la fin des tâches pour finir le programme
        wait(futures, return_when=ALL_COMPLETED)

        print("Toutes les tâches sont terminées")

if __name__ == "__main__":
    main()