
##TowerDefense

# Francois Therien
# Nicolas Paquette
# Caroline Emond
# Antoine Auger
# Mikael Korvat

from tkinter import *
import random

from _datetime import date
import MapCheckpoints


#test

class Vue():
    def __init__(self, parent, modele):
        self.modele = modele
        self.parent = parent
        self.root = Tk()
        self.root.title("towerDefense")
        #self.root.resizable(width=False, height=False)
        self.windowMenu()
        self.game = None
        self.gameCanvas = None
        self.gameFrame = None
        self.img = None
        self.gameInProg = False

    def windowMenu(self):
        self.menuFrame = Frame(self.root, bg="spring green3")

        self.welcomeLabel = Label(self.root, text="* WELCOME TO BOTANIK PANIK *",bg="spring green4", fg="dark goldenrod1", font=("system", 20),pady=20)

        self.welcomeLabel.pack(expand=True,fill=BOTH)

        buttonNewGame = Button(self.menuFrame, text="NEW GAME", command=self.gameWindow, bg="deep pink4", fg="pale violetred1",font=("system", 12),relief="raised")
        buttonOptions = Button(self.menuFrame, text="OPTIONS", command=self.options, bg="dark green", fg="lime green",font=("system", 12),relief="raised")
        buttonQuit = Button(self.menuFrame, text="QUITTER", command=self.quit, bg="DodgerBlue4", fg="DeepSkyBlue",font=("system", 12),relief="raised")

        buttonNewGame.grid(column=0, row=0, padx=200, pady=20)
        buttonOptions.grid(column=0, row=1, padx=200, pady=20)
        buttonQuit.grid(column=0, row=2, padx=200, pady=20)

        self.menuFrame.pack()

    def showGame(self):

        self.gameCanvas.delete(ALL)

        self.img = PhotoImage(file="assets/Map #1/grass/map1.1.png")

        self.gameCanvas.create_image(0, 0, image=self.img, anchor=NW)

        for i in self.modele.creepList:
            self.gameCanvas.create_image(i.posX-(i.width/2),i.posY-(i.height/2),image=i.zombie, anchor=NW)

    def gameWindow(self):
        self.menuFrame.pack_forget()
        self.welcomeLabel.pack_forget()
        self.game = Frame(self.root)
        #self.game.resizable(width=False, height=False)

        self.gameFrame = Frame(self.game, width=1600, height=800)
        self.gameCanvas = Canvas(self.gameFrame, width=1300, height=800)
        self.frameHUD = Frame(self.gameFrame, width=300, height=800)

        self.ressourceFrame = Frame(self.frameHUD, bg="blue", width=300, height=100)
        self.towerFrame = Frame(self.frameHUD, bg="red", width=300, height=600)
        self.upgradeFrame = Frame(self.frameHUD, bg="black", width=300, height=100)

        self.gameCanvas.grid(column=0, row=0)
        self.frameHUD.grid(column=1, row=0)

        self.ressourceFrame.grid(column=1, row=0)
        self.towerFrame.grid(column=1, row=1)
        self.upgradeFrame.grid(column=1, row=2)

        self.gameFrame.pack(expand=YES, fill=BOTH)
        self.game.pack()
        self.gameInProg = True
        self.parent.animate()

    def options(self):
        pass

    def quit(self):
        pass

    

class Creep1():
    def __init__(self, parent, posX, posY, currentCheckpoint):
        self.posX = posX
        self.posY = posY
        self.parent = parent
        self.currentCheckpoint = currentCheckpoint
        self.cibleX = self.currentCheckpoint.x
        self.cibleY = self.currentCheckpoint.y
        self.vitesse = random.randint(3,10)
        self.buffer = 5
        self.height = 105
        self.width = 67
        self.listImage = ["assets/zombies/zombie1.png", "assets/zombies/zombie2.png", "assets/zombies/zombie3.png","assets/zombies/zombie4.png","assets/zombies/zombie5.png","assets/zombies/zombie6.png"]
        self.zombie = PhotoImage(file=random.choice(self.listImage))
        self.reachedEnd = False

        self.moveHorizontal = True
        self.moveUp = False
        self.moveDown = False
        self.nextMoveHorizontal = False


    def move(self):
        if self.moveHorizontal:
            if self.posX <= self.cibleX:
                self.posX += self.vitesse
            else:
                self.updateTargetPosition()
        else:
            if self.moveUp:
                if self.posY >= self.cibleY:
                    self.posY -= self.vitesse
                else:
                    self.updateTargetPosition()
            if self.moveDown:
                if self.posY <= self.cibleY:
                    self.posY += self.vitesse
                else:
                    self.updateTargetPosition()
        print(self.posX, self.posY)
        print(self.cibleX, self.cibleY)
                  

    def updateTargetPosition(self):
        if (self.posX >= 1400 and self.posY >= 655):
            print("REACHED THE END!")
            self.reachedEnd = True
        else:
            self.currentCheckpoint = self.parent.getNextCheckpoint(self.currentCheckpoint)
            self.cibleX = self.currentCheckpoint.x
            self.cibleY = self.currentCheckpoint.y

            if self.posX >= self.cibleX:
                print("STOP")
                self.moveHorizontal = False
            
            if self.moveHorizontal == False and self.nextMoveHorizontal == False:
                if self.posY >= self.cibleY:
                    print("UP")
                    self.moveHorizontal = False
                    self.moveUp = True
                    self.moveDown = False
                    self.nextMoveHorizontal = True
                elif self.posY <= self.cibleY:
                    print("DOWN")
                    self.moveHorizontal = False
                    self.moveUp = False
                    self.moveDown = True
                    self.nextMoveHorizontal = True
            elif self.moveUp == False and self.moveDown == True or self.moveUp == True and self.moveDown == False and self.nextMoveHorizontal == True:
                    print("HORIZONTAL")
                    self.moveHorizontal = True
                    self.moveUp = False
                    self.moveDown = False
                    self.nextMoveHorizontal = False


class Checkpoint():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other, Checkpoint):
            return self.x == other.x and self.y == other.y
        return False


class Modele():
    def __init__(self, parent):
        self.parent = parent
        self.creepList = []
        self.checkpointList = MapCheckpoints.map[1]
        print(self.checkpointList)


    def createCreep(self):
        nbCreep = random.randint(5,10)
        for i in range(nbCreep):
            distanceX = random.randint(-500, 0)
            self.creepList.append(Creep1(self, distanceX, 630, self.checkpointList[0]))
        

    def creepMovement(self):
        for i in self.creepList:
            i.move()

    def getNextCheckpoint(self, currentCheckpoint):
        currentIndex = self.checkpointList.index(currentCheckpoint)
        checkpointList_len = len(self.checkpointList) - 1
        if currentIndex < checkpointList_len:
            return self.checkpointList[currentIndex+1]
        else:
            pass

    def deathCheck(self):
        for i in self.creepList:
            if i.reachedEnd:
                self.creepList.remove(i)
                del i
                
            #if shot  


    #Vérification si le joueur existe dans le fichier score.csv
    #TODO: Changer le nom des variables et mettre en argument le nom du joueur
    #TODO: Offrir au joueur la possibilité de refuser de continuer avec son profil si il veux recommencer?
    def getProfil(self, namePlayer):
        playerFound = False
        file = open("score.csv", "r")
        line=file.readlines()
        print(line)
        for player in line:
            currentPlayer = player.split(",")
            if currentPlayer[0].lower() == namePlayer.lower() and not playerFound:
                playerFound = True
                print("YEAH")
                self.nom = currentPlayer[0]
                self.niveau = currentPlayer[3]
                self.sagesse = currentPlayer[4]
        
        if not playerFound:
            self.nom = 0
            self.niveau = 0
            self.sagesse = 0

        file.close()


    #TODO: Changer le nom des variables
    def score(self):
        file = open("score.csv", "a")
        file.write(f"{self.nom},{str(date.today())},{str(self.point)},{str(self.level)},{str(self.sagesse)}")
        file.close()

    

    

class Controleur():
    def __init__(self):
        self.modele = Modele(self)
        self.vue = Vue(self, self.modele)
        self.creepWave()
        self.vue.root.after(10, self.animate)
        self.vue.root.mainloop()

    def creepWave(self):
        if len(self.modele.creepList) == 0:
            self.modele.createCreep()

    def animate(self):
        if self.vue.gameInProg == True:
            self.creepWave()
            self.modele.deathCheck()
            self.modele.creepMovement()
            self.vue.showGame()
            self.vue.root.after(10, self.animate)

   
        


if __name__ == '__main__':
    c = Controleur()
