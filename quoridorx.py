import turtle
from quoridor import Quoridor
from math import ceil


class QuoridorX(Quoridor):
    """Cette classe permet de jouer en mode graphique"""
    def __init__(self, joueurs, murs=None):
        super().__init__(joueurs, murs)
        self.coups = []
    
    def déplacer(self):
        def coordonnées(self, x, y):
            self.j1.goto(ceil(((x -(12.5))/25))*25, ceil((y - (12.5))/25)*25)
            return (x, y)

    #turtle.onscreenclick(coordonnées)
    
    def afficher(self):
        d = 50
        self.window = turtle.Screen()
        self.window.title('Quoridor')
        self.window.setup(width=400, height=400)
        self.window.bgcolor('black')

        self.coup = self.window.textinput('Coup', 'Que voulez-vous faire?')
        if self.coup in ('d', 'déplacement'):
            self.position = self.window.textinput('Coup', 'À quelle position?')
        elif self.coup in ('m', 'mur'):
            self.orientation = self.window.textinput('Coup', 'Dans quelle orientation?')
            self.position = self.window.textinput('Coup', 'À quelle position?')
            
        crayon = turtle.Turtle()
        crayon.color('white')
        crayon.speed(0)
        crayon.penup()
        crayon.goto(180-4.5*d, 50+4.5*d)
        crayon.write('QUORIDOR PHASE 3')
        crayon.right(90)
        for i in range(10): #colonnes
            crayon.penup()
            crayon.goto((i-4.5)*d, 4.5*d)
            crayon.pendown()
            crayon.forward(9*d)
        crayon.left(90)
        crayon.penup()
        crayon.goto(-4.5*d, 4.5*d)
        crayon.pendown()
        crayon.forward(9*d)
        for i in reversed(range(1, 10)): #rangées
            crayon.penup()
            crayon.home()
            crayon.goto(-4.5*d, 4.5*d-(10-i)*d)
            crayon.back(d/2)
            crayon.write('{}'.format(i))
            crayon.forward(d/2)
            crayon.pendown()
            crayon.forward(9*d)
        crayon.penup()
        crayon.goto((d/2)-4.5*d, (4.5-9.5)*d)
        for i in range(1, 10): #chiffres du bas
            crayon.write('{}'.format(i))
            crayon.forward(d)

        #positionner les joueurs
        self.j1 = turtle.Turtle()
        self.j2 = turtle.Turtle()

        self.j1.color('red')
        self.j1.penup()
        self.j1.left(90)

        self.j2.color('green')
        self.j2.penup()
        self.j2.right(90)

        self.j1.goto((self.etat['joueurs'][0]['pos'][0]-(10/2))*d, ((self.etat['joueurs'][0]['pos'][1]-(10/2))*d))       
        self.j2.goto((self.etat['joueurs'][1]['pos'][0]- (10/2))*d, ((self.etat['joueurs'][1]['pos'][1] -(10/2)))*d)

        crayon.width(4)

        for mur in self.etat['murs']['horizontaux']: #dessiner les murs horizontaux
            crayon.penup()
            crayon.goto(25*(mur[0]-1), -25*(9-mur[1]))
            crayon.pendown()
            crayon.forward(50)

        for mur in self.etat['murs']['verticaux']: #dessiner les murs verticaux
            crayon.penup()
            crayon.goto(25*(mur[0]-1), -25*(9-mur[1]))
            crayon.right(90)
            crayon.pendown()
            crayon.forward(50)

        self.update = self.window.update()
        turtle.done()
"""
d = 50
fen = turtle.Screen()
fen.title('Quoridor')
fen.setup(width=400, height=400)
fen.bgcolor('black')
crayon = turtle.Turtle()
crayon.color('white')
crayon.speed(0)
crayon.penup()
crayon.goto(180-4.5*d, 50+4.5*d)
crayon.write('QUORIDOR PHASE 3')
crayon.right(90)
for i in range(10): #colonnes
    crayon.penup()
    crayon.goto((i-4.5)*d, 4.5*d)
    crayon.pendown()
    crayon.forward(9*d)
crayon.left(90)
crayon.penup()
crayon.goto(-4.5*d, 4.5*d)
crayon.pendown()
crayon.forward(9*d)
for i in reversed(range(1, 10)): #rangées
    crayon.penup()
    crayon.home()
    crayon.goto(-4.5*d, 4.5*d-(10-i)*d)
    crayon.back(d/2)
    crayon.write('{}'.format(i))
    crayon.forward(d/2)
    crayon.pendown()
    crayon.forward(9*d)
crayon.penup()
crayon.goto((d/2)-4.5*d, (4.5-9.5)*d)
for i in range(1, 10): #chiffres du bas
    crayon.write('{}'.format(i))
    crayon.forward(d)
turtle.mainloop()
"""