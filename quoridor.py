#-------------Quoridor Phase 2-----------------#
"""
###########################
#Van V. Galstian          #
#                         #
#Cherif A. Seye           #
#                         #
#Rosalie Tremblay         #
########################### """
import random
import networkx as nx

class QuoridorError(Exception):
    """
    Erreur spécifique au jeu de Quoridor.
    """
    def __init__(self, *args, **kargs):
        Exception.__init__(self, *args, **kargs)

class Quoridor:
    """
    Classe pour encapsuler le jeu Quoridor.
    Attributes:
        état (dict): état du jeu tenu à jour.
    """

    def __init__(self, joueurs, murs = None):
        """Constructeur de la classe Quoridor.
        Initialise une partie de Quoridor avec les joueurs et les murs spécifiés,
        en s'assurant de faire une copie profonde de tout ce qui a besoin d'être copié.
        Args:
            joueurs (List): un itérable de deux joueurs dont le premier est toujours celui qui
                débute la partie. Un joueur est soit une chaîne de caractères soit un dictionnaire.
                Dans le cas d'une chaîne, il s'agit du nom du joueur. Selon le rang du joueur dans
                l'itérable, sa position est soit (5,1) soit (5,9), et chaque joueur peut
                initialement placer 10 murs. Dans le cas où l'argument est un dictionnaire,
                celui-ci doit contenir une clé 'nom' identifiant le joueur, une clé 'murs'
                spécifiant le nombre de murs qu'il peut encore placer, et une clé 'pos' qui
                spécifie sa position (x, y) actuelle. Notez que les positions peuvent être sous
                forme de tuple (x, y) ou de liste [x, y].
            murs (Dict, optionnel): Un dictionnaire contenant une clé 'horizontaux' associée à
                la liste des positions (x, y) des murs horizontaux, et une clé 'verticaux'
                associée à la liste des positions (x, y) des murs verticaux. Par défaut, il
                n'y a aucun mur placé sur le jeu. Notez que les positions peuvent être sous
                forme de tuple (x, y) ou de liste [x, y].
        Raises:
            QuoridorError: L'argument 'joueurs' n'est pas itérable.
            QuoridorError: L'itérable de joueurs en contient un nombre différent de deux.
            QuoridorError: Le nombre de murs qu'un joueur peut placer est plus grand que 10,
                            ou négatif.
            QuoridorError: La position d'un joueur est invalide.
            QuoridorError: L'argument 'murs' n'est pas un dictionnaire lorsque présent.
            QuoridorError: Le total des murs placés et plaçables n'est pas égal à 20.
            QuoridorError: La position d'un mur est invalide.
        """

        if '__iter__' not in dir(joueurs):
            raise QuoridorError("L'argument 'joueurs' n'est pas itérable")

        if len(joueurs) != 2:
            raise QuoridorError("L'itérable de joueurs en contient un nombre différent de deux")
        if isinstance(joueurs[0], str) and isinstance(joueurs[1], str):
            self.etat = {
                "joueurs": [
                    {"nom": joueurs[0], "murs": 10, "pos": (5, 1)},
                    {"nom": joueurs[1], "murs": 10, "pos": (5, 9)}
                ],
                "murs": {
                    "horizontaux": [],
                    "verticaux": []
                }
            }

        else:

            if (joueurs[0].get('murs')) > 10 or (joueurs[0].get('murs')) < 0:
                raise QuoridorError("Le nombre de murs qu'un joueur peut placer est\
                                    plus grand que 10, ou négatif.")
            if (joueurs[0].get('pos'))[0] not in range(1, 10)\
            or (joueurs[0].get('pos'))[1] not in range(1, 10)\
            or (joueurs[1].get('pos'))[0] not in range(1, 10)\
            or (joueurs[1].get('pos'))[1] not in range(1, 10)\
            or (joueurs[0].get('pos')) == (joueurs[1].get('pos')):
                raise QuoridorError("La position d'un joueur est invalide.")

            self.etat = {
                'joueurs':[{'nom' : joueurs[0]['nom'], 'murs' : joueurs[0]['murs'],
                'pos' : joueurs[0]['pos']},
                {'nom' : joueurs[1]['nom'],
                'murs' : joueurs[1]['murs'],
                'pos' : joueurs[1]['pos']}],
                'murs' : {
                    'horizontaux' : [],
                    'verticaux' : []
                }
            }

        if not isinstance(murs, dict) and murs is not None:
            raise QuoridorError("L'argument 'murs' n'est pas un dictionnaire lorsque présent.")

        if murs is not None:
            if not isinstance(murs, dict):
                raise QuoridorError("L'argument 'murs' n'est pas un dictionnaire lorsque présent.")
            self.etat["murs"]["horizontaux"] = murs["horizontaux"]
            self.etat["murs"]["verticaux"] = murs["verticaux"]

            if self.croisement_murs() or self.joueur_enferme() or self.verifier_pos_murs():
                self.etat["murs"]["horizontaux"] = []
                self.etat["murs"]["verticaux"] = []
                raise QuoridorError("Position des murs invalide")    

        murs_restants = self.etat['joueurs'][0]['murs'] + self.etat['joueurs'][1]['murs']
        murs_horizontaux = len(self.etat["murs"]["horizontaux"])
        murs_verticaux = len(self.etat["murs"]["verticaux"])
        if murs_restants + murs_horizontaux + murs_verticaux != 20:
            raise QuoridorError("Le total des murs placés et plaçables n'est pas égal à 20")

    def verifier_pos_murs(self):
        """
        Vérifie que les murs sont placés correctement.
        """
        for mur in self.etat["murs"]["horizontaux"]:
            if mur[0] > 8 or mur[0] < 2 or mur[1] > 9 or mur[1] < 2:
                return True
        for mur in self.etat["murs"]["verticaux"]:
            if mur[0] > 9 or mur[0] < 2 or mur[1] > 8 or mur[1] < 1:
                return True
        return False
    def __str__(self):
        """Représentation en art ascii de l'état actuel de la partie.
        Cette représentation est la même que celle du projet précédent.
        Returns:
            str: La chaîne de caractères de la représentation.
        """

        joueur1 = self.etat['joueurs'][0]['nom']
        joueur2 = self.etat['joueurs'][1]['nom']
        header = f'Légende: 1={joueur1}, 2={joueur2}\n' + ' ' * 3 + '-' * 35 + '\n'
        footer = ('-' * 2 + '|' + '-' * 35 + '\n' + ' ' * 2
                  + '|' + '  '.join([f' {i}' for i in range(1, 10)]))

        #création du damier vide
        rangees = ''
        for rangee in range(19, 2, -1):
            if rangee % 2 == 0:
                rangees += ' ' * 2 + '|' + ' ' * 35 + '|\n'
            else:
                rangees += f'{rangee // 2} ' + '|' + ' .  ' * 8 + ' . ' + '|\n'
        rangees = list(rangees)

        #ajout des joueurs
        rangees[-1 * (80 * (self.etat['joueurs'][0]['pos'][1] - 1)
                      + 40 - self.etat['joueurs'][0]['pos'][0] * 4)] = '1'
        rangees[-1 * (80 * (self.etat['joueurs'][1]['pos'][1] - 1)
                      + 40 - self.etat['joueurs'][1]['pos'][0] * 4)] = '2'

        #ajout des murs horizontaux
        for mur in self.etat['murs']['horizontaux']:
            rangees[-1 * (80 * (mur[1] - 1) + 1 - mur[0] * 4): - 1
                    * (80 * (mur[1] - 1) + 1 - mur[0] * 4) + 7] = ['-' for _ in range(7)]

        #ajout des murs verticaux
        for mur in self.etat['murs']['verticaux']:
            rangees[-1 * (80 * (mur[1] - 1) + 42 - mur[0] * 4)] = '|'
            rangees[-1 * (80 * (mur[1] - 1) + 82 - mur[0] * 4)] = '|'
            rangees[-1 * (80 * (mur[1] - 1) + 122 - mur[0] * 4)] = '|'

        return header + ''.join(rangees) + footer

    def déplacer_jeton(self, joueur, position):
        """Déplace un jeton.
        Pour le joueur spécifié, déplacer son jeton à la position spécifiée.
        Args:
            joueur (int): Un entier spécifiant le numéro du joueur (1 ou 2).
            position (Tuple[int, int]): Le tuple (x, y) de la position du jeton
            (1<=x<=9 et 1<=y<=9).
        Raises:
            QuoridorError: Le numéro du joueur est autre que 1 ou 2.
            QuoridorError: La position est invalide (en dehors du damier).
            QuoridorError: La position est invalide pour l'état actuel du jeu.
        """

        if joueur not in (1, 2):
            raise QuoridorError("Le numéro du joueur est autre que 1 ou 2")

        if int(position[0]) > 9 or int(position[0]) < 1 or int(position[1]) < 1 or int(position[1]) > 9:
            raise QuoridorError("QuoridorError: La position est invalide (en dehors du damier).")

        graphe = construire_graphe(
            [joueur['pos'] for joueur in self.etat['joueurs']],
            self.etat['murs']['horizontaux'],
            self.etat['murs']['verticaux'])
        print(graphe.successors(self.etat['joueurs'][joueur - 1]['pos']))
        if position in graphe.successors(self.etat['joueurs'][joueur - 1]['pos']):
            self.etat['joueurs'][joueur - 1]['pos'] = position

        else:
            raise QuoridorError("La position est invalide pour l'état actuel du jeu.")

    def état_partie(self):
        """Produire l'état actuel de la partie.
        Returns:
        Dict: Une copie de l'état actuel du jeu sous la forme d'un dictionnaire.
        Notez que les positions doivent être sous forme de tuple (x, y) uniquement.
        """

        return self.etat

    def jouer_coup(self, joueur):
        """Jouer un coup automatique pour un joueur.
        Pour le joueur spécifié, jouer automatiquement son meilleur coup pour l'état actuel
        de la partie. Ce coup est soit le déplacement de son jeton, soit le placement d'un
        mur horizontal ou vertical.
        Args:
            joueur (int): Un entier spécifiant le numéro du joueur (1 ou 2).
        Raises:
            QuoridorError: Le numéro du joueur est autre que 1 ou 2.
            QuoridorError: La partie est déjà terminée.
        Returns:
            Tuple[str, Tuple[int, int]]: Un tuple composé du type et de la position du coup joué.
        """
        goal1 = 'B1'
        goal2 = 'B2'
        if joueur == 2:
            goal1 = 'B2'
            goal2 = 'B1'

        graphe = construire_graphe(\
            [joueur['pos'] for joueur in self.etat['joueurs']],\
            self.etat['murs']['horizontaux'],\
            self.etat['murs']['verticaux'])
        shortest1 = nx.shortest_path(graphe, self.etat['joueurs'][joueur-1]['pos'], goal1)
        other = [0, 1]
        other.remove(joueur-1)
        shortest2 = nx.shortest_path(graphe, self.etat['joueurs'][other[0]]['pos'], goal2)
        choix = random.choice([1, 2, 3])
        if joueur not in (1, 2):
            raise QuoridorError('Le numéro du joueur est autre que 1 ou 2.')

        if self.partie_terminée() is not False:
            raise QuoridorError('La partie est déjà terminée.')

        if (len(shortest1) > len(shortest2)+2  or len(shortest2) < 3 or choix == 1)\
            and self.etat['joueurs'][joueur-1]['murs'] != 0:
            i = 1
            while i < len(shortest2):
                try:
                    if shortest2[i][0] == self.etat['joueurs'][other[0]]['pos'][0]:
                        self.placer_mur(joueur, (shortest2[i][0], shortest2[i][1]+1), 'horizontal')
                        return ('Placer mur horizontal', (shortest2[i][0], shortest2[i][1]+1))
                        break
                    elif shortest2[i][1] == self.etat['joueurs'][other[0]]['pos'][1]:
                        self.placer_mur(joueur, shortest2[i], 'vertical')
                        return ('Placer mur vertical', shortest2[i])
                        break
                except:
                    i += 1
        self.déplacer_jeton(joueur, shortest1[1])
        return ('Déplacer jeton', shortest1[1])

    def partie_terminée(self):
        """Déterminer si la partie est terminée.
        Returns:
            str/bool: Le nom du gagnant si la partie est terminée; False autrement.
        """
        if self.etat['joueurs'][0]['pos'][1] == 9:
            return self.etat['joueurs'][0]['nom']
        if self.etat['joueurs'][1]['pos'][1] == 1:
            return self.etat['joueurs'][1]['nom']
        return False

        def joueur_enferme(self):
            """
        Vérifie si un joueur est enfermé
        """
            graphe = construire_graphe([joueur['pos'] for joueur in self.etat['joueurs']],
                                       self.etat['murs']['horizontaux'],
                                       self.etat['murs']['verticaux'])

            if not (nx.has_path(graphe, self.etat['joueurs'][0]['pos'], 'B1')
                    and nx.has_path(graphe, self.etat['joueurs'][1]['pos'], 'B2')):
                return True
            return False    
            
    def croisement_murs(self):
            """
        Vérifie si deux murs se croisent
        """
            position_prise = []

            for mur in self.etat['murs']['horizontaux']:
                    position_prise.append(mur)
                    position_prise.append((mur[0] - 1, mur[1]))
                    position_prise.append((mur[0] + 1, mur[1]))
            for mur in self.etat['murs']['verticaux']:
                    position_prise.append((mur[0] - 1, mur[1] + 1))

            for mur in self.etat['murs']['horizontaux']:
                    position_prise.remove(mur)
                    if mur in position_prise:
                            return True
                    position_prise.append(mur)

            position_prise = []

            for mur in self.etat['murs']['verticaux']:
                    position_prise.append(mur)
                    position_prise.append((mur[0], mur[1] - 1))
                    position_prise.append((mur[0], mur[1] + 1))
            for mur in self.etat['murs']['horizontaux']:
                    position_prise.append((mur[0] + 1, mur[1] - 1))

            for mur in self.etat['murs']['verticaux']:
                    position_prise.remove(mur)
                    if mur in position_prise:
                            return True
                    position_prise.append(mur)

            return False


    def placer_mur(self, joueur, position, orientation):
        """Placer un mur.
        Pour le joueur spécifié, placer un mur à la position spécifiée.
        Args:
            joueur (int): le numéro du joueur (1 ou 2).
            position (Tuple[int, int]): le tuple (x, y) de la position du mur.
            orientation (str): l'orientation du mur ('horizontal' ou 'vertical').
        Raises:
            QuoridorError: Le numéro du joueur est autre que 1 ou 2.
            QuoridorError: Un mur occupe déjà cette position.
            QuoridorError: La position est invalide pour cette orientation.
            QuoridorError: Le joueur a déjà placé tous ses murs.
        """
        orientation = orientation.replace('al', 'aux')
        graphe = construire_graphe(
            [joueur['pos'] for joueur in self.etat['joueurs']],
            self.etat['murs']['horizontaux'],
            self.etat['murs']['verticaux'])
        if joueur not in(1,2):
            raise QuoridorError('Le numéro du joueur est autre que 1 ou 2.')

        if self.etat['joueurs'][joueur-1]['murs'] == 0:
            raise QuoridorError('Le joueur a déjà placé tous ses murs.')

        if position in self.etat['murs']['verticaux']\
        or position in self.etat['murs']['horizontaux']:
            raise QuoridorError('Un mur occupe déjà cette position.')

        self.etat['murs'][orientation].append(position)
        new = self.etat
        self.etat['murs'][orientation].remove(position)
        if position[1] not in range(1, 9)\
        or position[0] not in range(1, 9)\
        or nx.has_path(graphe, new['joueurs'][0]['pos'], 'B1') is False\
        or nx.has_path(graphe, new['joueurs'][1]['pos'], 'B2') is False:
            raise QuoridorError('La position est invalide pour cette orientation.')

        self.etat = new
        self.etat['joueurs'][joueur-1]['murs'] -= 1
        return (orientation, position) 


def construire_graphe(joueurs, murs_horizontaux, murs_verticaux):
    """Construire un graphe de la grille.
    Crée le graphe des déplacements admissibles pour les joueurs.
    Vous n'avez pas à modifer cette fonction.
    Args:
    joueurs (List[Tuple]): une liste des positions (x,y) des joueurs.
    murs_horizontaux (List[Tuple]): une liste des positions (x,y) des murs horizontaux.
        murs_verticaux (List[Tuple]): une liste des positions (x,y) des murs verticaux.
    Returns:
        DiGraph: le graphe bidirectionnel (en networkX) des déplacements admissibles.
    """
    graphe = nx.DiGraph()

    # pour chaque colonne du damier
    for x in range(1, 10):
        # pour chaque ligne du damier
        for y in range(1, 10):
            # ajouter les arcs de tous les déplacements possibles pour cette tuile
            if x > 1:
                graphe.add_edge((x, y), (x-1, y))
            if x < 9:
                graphe.add_edge((x, y), (x+1, y))
            if y > 1:
                graphe.add_edge((x, y), (x, y-1))
            if y < 9:
                graphe.add_edge((x, y), (x, y+1))

    # retirer tous les arcs qui croisent les murs horizontaux
    for x, y in murs_horizontaux:
        graphe.remove_edge((x, y-1), (x, y))
        graphe.remove_edge((x, y), (x, y-1))
        graphe.remove_edge((x+1, y-1), (x+1, y))
        graphe.remove_edge((x+1, y), (x+1, y-1))

    # retirer tous les arcs qui croisent les murs verticaux
    for x, y in murs_verticaux:
        graphe.remove_edge((x-1, y), (x, y))
        graphe.remove_edge((x, y), (x-1, y))
        graphe.remove_edge((x-1, y+1), (x, y+1))
        graphe.remove_edge((x, y+1), (x-1, y+1))

    # s'assurer que les positions des joueurs sont bien des tuples (et non des listes)
    j1, j2 = tuple(joueurs[0]), tuple(joueurs[1])

    # traiter le cas des joueurs adjacents
    if j2 in graphe.successors(j1) or j1 in graphe.successors(j2):

        # retirer les liens entre les joueurs
        graphe.remove_edge(j1, j2)
        graphe.remove_edge(j2, j1)

        def ajouter_lien_sauteur(noeud, voisin):
            """
            :param noeud: noeud de départ du lien.
            :param voisin: voisin par dessus lequel il faut sauter.
            """
            saut = 2*voisin[0]-noeud[0], 2*voisin[1]-noeud[1]

            if saut in graphe.successors(voisin):
                # ajouter le saut en ligne droite
                graphe.add_edge(noeud, saut)

            else:
                # ajouter les sauts en diagonale
                for saut in graphe.successors(voisin):
                    graphe.add_edge(noeud, saut)

        ajouter_lien_sauteur(j1, j2)
        ajouter_lien_sauteur(j2, j1)

    # ajouter les destinations finales des joueurs
    for x in range(1, 10):
        graphe.add_edge((x, 9), 'B1')
        graphe.add_edge((x, 1), 'B2')

    return graphe
