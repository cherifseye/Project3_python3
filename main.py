"""Ce module permet d'implémenter la boucle de jeu"""
import turtle
import argparse
import api
import quoridor
from quoridorx import QuoridorX



def analyser_commande():
    """permet d'analyser la commande entrée par le joueur"""

    parser = argparse.ArgumentParser(
        description = "Jeu Quoridor - Phase 3"
    )

    parser.add_argument(
        # Argument obligatoire servant à entrer l'idul du joueur
        'idul',  help='IDUL du joueur.', type = str
    )

    parser.add_argument(
        #Argument optionel
        '-a', '--automatique',
        help = 'Activer le mode automatique.', action = 'store_true'
    )
    parser.add_argument(
        #Argument optionel
        '-x', '--graphique',
        help = 'Activer le mode graphique.', action = 'store_true'
    )

    args = parser.parse_args()
    #retourne les arguments
    return args

if __name__ == "__main__":
    COMMANDE = analyser_commande()
    start = input('Débuter? ')

    if start == 'oui':
        dico = api.initialiser_partie(COMMANDE.idul)
        id_partie = dico[0]
        état = dico[1]
        état['joueurs'][0]['pos'] = (état['joueurs'][0]['pos'][0], état['joueurs'][0]['pos'][1])
        état['joueurs'][1]['pos'] = (état['joueurs'][1]['pos'][0], état['joueurs'][1]['pos'][1])

        partie = QuoridorX(état['joueurs'], état['murs'])

        def afficher_damier():
            if COMMANDE.graphique:
                partie.afficher()
            else:
                print(partie)

        if COMMANDE.automatique:
            afficher_damier()
            succes = False
            while succes != True:
                coup = partie.jouer_coup(1)
                print(coup)
                orientation = coup[0].split(' ')

                if 'Placer' in orientation:
                    nouveau = api.jouer_coup(id_partie,'M'+'{}'.format(orientation[2][0].upper()), coup[1])
                    print(nouveau)
                    nouveau['joueurs'][0]['pos'] = (
                        nouveau['joueurs'][0]['pos'][0], nouveau['joueurs'][0]['pos'][1])
                    nouveau['joueurs'][1]['pos'] = (
                        nouveau['joueurs'][1]['pos'][0], nouveau['joueurs'][1]['pos'][1])
                    partie.etat = nouveau
                    afficher_damier()
                else:
                    nouveau = api.jouer_coup(id_partie, 'D', coup[1])
                    print(nouveau)
                    nouveau['joueurs'][0]['pos'] = (nouveau['joueurs'][0]['pos'][0], nouveau['joueurs'][0]['pos'][1])
                    nouveau['joueurs'][1]['pos'] = (nouveau['joueurs'][1]['pos'][0], nouveau['joueurs'][1]['pos'][1])
                    partie.etat = nouveau
                    afficher_damier()

                if partie.partie_terminée():
                    print('Le gagnant est {}'.format(partie.partie_terminée()))
                    succes = True

        else:
            if COMMANDE.graphique:
                
                succes = False
                while succes == False:
                    partie.afficher()
                    try:
                        if partie.coup in  ('d', 'déplacement'):
                            pos = (int(partie.position[0]), int(partie.position[2]))
                            partie.déplacer_jeton(1, pos)
                            nouveau = api.jouer_coup(id_partie, 'D', pos)
                            nouveau['joueurs'][0]['pos'] = (nouveau['joueurs'][0]['pos'][0], nouveau['joueurs'][0]['pos'][1])
                            nouveau['joueurs'][1]['pos'] = (nouveau['joueurs'][1]['pos'][0], nouveau['joueurs'][1]['pos'][1])
                            partie.etat = nouveau

                        elif partie.coup in ('m', 'mur'):
                            pos = (int(partie.position[0]), int(partie.position[2]))
                            partie.placer_mur(1, pos, partie.orientation)
                            nouveau = api.jouer_coup(id_partie, 'M'+'{}'.format(partie.orientation[0].upper()), pos)
                            nouveau['joueurs'][0]['pos'] = (nouveau['joueurs'][0]['pos'][0], nouveau['joueurs'][0]['pos'][1])
                            nouveau['joueurs'][1]['pos'] = (nouveau['joueurs'][1]['pos'][0], nouveau['joueurs'][1]['pos'][1])
                            partie.etat = nouveau
                        elif partie.coup == 'rien':
                            break
                    except:
                        print("le coup n'est pas valide!")

                    if partie.partie_terminée():
                        succes = True
                        print(partie.partie_terminée())

            else:
                succes = False
                while succes != True:
                    try:
                        coup = input('Que voulez-vous faire?')
                        if coup in  ('d', 'déplacement'):
                            pos = input('Vers quelle position?').split(',')
                            pos = (int(pos[0]), int(pos[1]))
                            partie.déplacer_jeton(1, pos)
                            nouveau = api.jouer_coup(id_partie, 'D', pos)
                            nouveau['joueurs'][0]['pos'] = (nouveau['joueurs'][0]['pos'][0], nouveau['joueurs'][0]['pos'][1])
                            nouveau['joueurs'][1]['pos'] = (nouveau['joueurs'][1]['pos'][0], nouveau['joueurs'][1]['pos'][1])
                            partie.etat = nouveau
                            afficher_damier()

                        elif coup in ('m', 'mur'):
                            pos = input('À quelle position?').split(',')
                            pos = (int(pos[0]), int(pos[1]))
                            orientation = input('Dans quelle orientation?')
                            partie.placer_mur(1, pos, orientation)
                            afficher_damier()
                            nouveau = api.jouer_coup(id_partie, 'M'+'{}'.format(orientation[0].upper()), pos)
                            nouveau['joueurs'][0]['pos'] = (nouveau['joueurs'][0]['pos'][0], nouveau['joueurs'][0]['pos'][1])
                            nouveau['joueurs'][1]['pos'] = (nouveau['joueurs'][1]['pos'][0], nouveau['joueurs'][1]['pos'][1])
                            partie.etat = nouveau
                            afficher_damier()
                    except:
                        print("le coup n'est pas valide!")

                    if partie.partie_terminée():
                        succes = True
                        print(partie.partie_terminée())

    """ARGS = analyser_commande()
  initialiser_partie(ARGS.IDUL)
  if ARGS.parties:
    print(lister_parties(ARGS.IDUL))
  start = input('Débuter? ')
  if start == 'oui':
    tup = initialiser_partie(ARGS.IDUL)
    while running == True:
      afficher_damier_ascii(tup)
      coup = input('Quel coup jouer? ')
      ran = input('Choisissez la rangée de votre coup ')
      col = input('Choisissez la colonne de votre coup ')
      try:
        jouer_coup(partie[0], type_coup, (colonne, ligne))
      except StopIteration as win:
        print(win)
        running = False
      except RuntimeError as entrée_invalide:
        print(entrée_invalide)
        continue
      
      tup = jouer_coup(partie[0], type_coup, (colonne, ligne))
    else:
      print('Au revoir!')"""