import random
import copy

"""connect four module. Contains classes Grid, Play"""


class Grid:
    """Grid class: has properties matrix, has methods __init__, __str__, checkForWin, checkForDraw, dropPiece, simulateMoves, playSimulatedGames """
    def __init__(self):
        """__init__(): initialize a Grid """       
        self.matrix = []
        for i in range(6):
            self.matrix.append( [0,0,0,0,0,0,0] )

    def __str__(self):
        """__str__(): override the print method for a Grid """
        return str(self.matrix[0]) + '\n' + str(self.matrix[1]) + '\n' + str(self.matrix[2]) + '\n' + str(self.matrix[3]) + '\n' + str(self.matrix[4]) + '\n' + str(self.matrix[5]) + '\n'
        #return str(self.matrix)

    def checkForWin(self, player):
        """checkForWin(player): argument accepts a 1 or 2 to check for a win for the specified player """ 
        #check horizontal wins
        for r in range(6):
            for c in range(4):
                if self.matrix[r][c:c+4] == [player,player,player,player]:
                    return True

        #check vertical wins
        for c in range(7):
            for r in range(3):
                if self.matrix[r][c] == self.matrix[r+1][c] == self.matrix[r+2][c] == self.matrix[r+3][c] == player:
                    return True

        #check postiviely sloped diagonal wins
        for c in range(4):
            for r in range(3,6):
                if self.matrix[r][c] == self.matrix[r-1][c+1] == self.matrix[r-2][c+2] == self.matrix[r-3][c+3] == player:
                    return True          

        #check negatively sloped diagonal wins
        for c in range(4):
            for r in range(3):
                if self.matrix[r][c] == self.matrix[r+1][c+1] == self.matrix[r+2][c+2] == self.matrix[r+3][c+3] == player:
                    return True
                
        return False


    def checkForDraw(self):
        """checkForDraw(): check if the entire board is filled with pieces, a draw """ 
        for c in range(7):
            if self.matrix[0][c] == 0:
                return False
        return True




    def dropPiece(self, column, player):
        """dropPiece(column, player): specify the column (1 through 7) and the player (1 or 2) and the piece is dropped in that location """ 
        for i in range(5,-1,-1):
            if self.matrix[i][column-1] == 0:
                self.matrix[i][column-1] = player
                break


    def simulateMoves(self):
        """simulateMoves(): simulate many possible results from the current Grid position to determine the possible moves and their likelihood of a victory  """ 
        validColumns = []
        for c in range(7):
            if self.matrix[0][c] == 0:
                validColumns.append(c+1)
        #print('Valid columns are',str(validColumns))

        for c in validColumns:
            t1 = copy.deepcopy(self)
            t1.dropPiece(c, 1)
            if t1.checkForWin(1):
                print('\nCAN WIN ON NEXT MOVE - DROP PIECE IN COLUMN', c,'\n')
                return

        maxWinsColumn = 0
        maxWinsValue = 0
        for c in validColumns:
            #print('Checking column', c)

            #prior to simulation, check if the column is a DO NOT TOUCH column because it would result in sabotaging a victory
            t1 = copy.deepcopy(self)
            t1.dropPiece(c, 2)      #if player two drops first
            t1.dropPiece(c, 1)      #then player one drops next
            if t1.checkForWin(1):   #if that results in a player one win
                print('Column', c, '\t', 'DO NOT TOUCH, IT WOULD SABOTAGE A WIN')
            else:
                wins, losses, draws = self.playSimulatedGames(c, validColumns[:])
                numberOfSimulations = wins + losses + draws
                print('Column', c, '\t', 'Wins\t', wins, '\tLosses\t', losses, '\tDraws\t', draws)
                #print('Column', c, 'Wins', wins/numberOfSimulations, 'Losses', losses/numberOfSimulations, 'Draws', draws/numberOfSimulations)

                if wins > maxWinsValue:
                    maxWinsValue = wins
                    maxWinsColumn = c
        if maxWinsColumn != 0:
            print('The robot recommends dropping your piece in column', maxWinsColumn)
        else:
            print('Valid columns are', str(validColumns))
            for v in validColumns:
                a1 = copy.deepcopy(self)
                a1.dropPiece(v, 1)      #if player one drops in the column, will player two win next move?
                for w in validColumns:
                    b1 = copy.deepcopy(a1)
                    if b1.matrix[0][w-1] == 0:
                        b1.dropPiece(w, 2)  #drop a piece in the valid columns for player 2 and test for the win                
                        if b1.checkForWin(2):
                            print('Don\'t drop in column', v, 'because that will result in a loss next move')
                            break





                        
                        #else:
                            #print('You can drop in column', v, 'because that will not result in a loss next move')
            


            

    def playSimulatedGames(self, simColumn, validColumns):
        """playSimulatedGames(simColumn, validColumns): for a specified simColumn (1 through 7) and a list of columns that are currently available for a piece """ 
        numberOfSimulations = 100
        w=0
        l=0
        d=0
             
        for i in range(numberOfSimulations):
            myTurn = False
            #print('beginning of simulation', i+1, 'of', numberOfSimulations)
            simulationValidColumns = validColumns[:]
            s1 = copy.deepcopy(self)
            #print('Simulation starting with this board')
            #print(s1)
            s1.dropPiece(simColumn, 1)
            
            if s1.checkForDraw():
                d += 1
                #print(s1)
                break

            if s1.checkForWin(1):
                w += 1
                #print(s1)
                break

            if s1.matrix[0][simColumn-1] != 0:
                simulationValidColumns.remove(simColumn)    #if player one just finished the column, remove the column from play
        

            while True:
                if myTurn:
                    if s1.checkForDraw():
                        d += 1
                        #print(s1)
                        break

                    #random or AI
                    column = random.choice(simulationValidColumns)
                    
                    for c in simulationValidColumns:
                        w1 = copy.deepcopy(s1)
                        w1.dropPiece(c,1)
                        if w1.checkForWin(1):
                            column = c
                            break

                    #print('Column', column, 'chosen')
                    s1.dropPiece(column, 1)
                    if s1.checkForWin(1):
                        w += 1
                        #print(s1)
                        break
                    #revise simulationValidColumns
                    if s1.matrix[0][column-1] != 0:
                        simulationValidColumns.remove(column)
                    
                    myTurn = not myTurn
                    #print('\n\nPlayer 1 Done')
                    #print(s1)
                    #print('Valid columns are', simulationValidColumns, '\n\n')
                else:
                    if s1.checkForDraw():
                        d += 1
                        #print(s1)
                        break

                    #random or AI
                    column = random.choice(simulationValidColumns)
                    #print('Player 2 random choice is', column)
                    #print('The valid columns are:', simulationValidColumns)

                    #check if player 2 can win
                    for c in simulationValidColumns:
                        winGuaranteed = False
                        #print('Checking potential of column', c)
                        w1 = copy.deepcopy(s1)
                        #print('Board before drop')
                        #print(w1)
                        w1.dropPiece(c,2)
                        #print('Board after drop')
                        #print(w1)
                        if w1.checkForWin(2):
                            #print('Column', c, 'is a winner')
                            column = c
                            winGuaranteed = True
                            break

                    #check if player 2 can prevent a player 1 win - if player 1 drops in a certain column, will it produce a player 1 victory
                    if not winGuaranteed:
                        for c in simulationValidColumns:
                            d1 = copy.deepcopy(s1)
                            d1.dropPiece(c,1)
                            if d1.checkForWin(1):
                                column = c
                                break
                    

                    #print('the final decision for the oppoenent is column', column)
                    
                    #print('Column', column, 'chosen')
                    s1.dropPiece(column, 2)
                    if s1.checkForWin(2):
                        l += 1
                        #print(s1)
                        break

                    #revise simulationValidColumns
                    if s1.matrix[0][column-1] != 0:
                        simulationValidColumns.remove(column)
                    
                    myTurn = not myTurn
                    #print('\n\nPlayer 2 Done')
                    #print(s1)
                    #print('Valid columns are', simulationValidColumns, '\n\n')
                    
        #print('returning',w,l,d)
        return w, l, d

    

class Play:
    """Grid class: has no properties, has methods __init__, startGame """
    def __init__(self):
        """__init__(): initialize a Play object to start a game """ 
        pass


    def startGame(self):
        """startGame(): start a Connect 4 game """ 
        g1 = Grid()
        
        response = int(input('Who goes first?\nPlayer 1 (you) or Player 2 (opponent)?\nEnter 1 or 2\n'))
        if response == 1:
            myTurn = True
        else:
            myTurn = False

        #print(myTurn)

        while True:
            if myTurn:
                #is a move possible or is it a draw
                if g1.checkForDraw():
                    print("Draw")
                    break
                
                #run simulation and produce report
                g1.simulateMoves()

                #choose column to play
                while True:
                    column = int(input('Which column will you play?  Enter 1-7\n'))
                    if column>7 or column<1:
                        print('Invalid column, try again.')
                    else:
                        break

                #figure out row that piece falls down to
                g1.dropPiece(column, 1)
                    
                #print grid
                print(g1)

      
                #check for win - if so then break
                if g1.checkForWin(1):
                    print("Player 1 Wins")
                    break



                #switch turns
                myTurn = not myTurn

            else:
                
                #is a move possible or is it a draw
                if g1.checkForDraw():
                    print("Draw")
                    break
                
                #where did opponent go
                while True:                
                    column = int(input('Where did opponent play?  Enter 1-7\n'))
                    if column>7 or column<1:
                        print('Invalid column, try again.')
                    else:
                        break                    

                #figure out row that piece falls down to
                g1.dropPiece(column, 2)             

                #print Grid
                print(g1)

                #check for win - if so then break
                if g1.checkForWin(2):
                    print("Player 2 Wins")
                    break
                
                #switch turns
                myTurn = not myTurn

        



        
if __name__ == '__main__':
    pass

    #g1 = Grid()
    #print(g1)
    #g1.checkForWin(1)

    p1 = Play()
    p1.startGame()

    

#How to use:
#1 - run this module in standalone mode to play a connect 4 game

#2 - import this module from another module with the following code
##import connectfour
##
##p1 = connectfour.Play()
##p1.startGame()








#robot is telling me to go somewhere that results in my opponent blocking me - build in defense
    #implement a check for a DON'T GO COLUMN
#DONE#if my play results in a win - I should see 100% wins#check for a win before simulation
#DONE#improve gametime display of information
#DONE#don't allow 3 in a row by me if it's an easy block #if there are 2 horizontal for me, try to get a 3rd horizontal with blanks on either side - if opponent has 2 horizontal, plug the third#the solution to this is for Player 2 to check for player 1 being one move away from victory, then player 2 must drop there

#4.0
#if there are 2 columns left and both are don't drop - it recommends column 0
#if there are 2 columns left and one results in a 0 wins (a loss) - look for this situation
#I think this is done#the robot is focusing too much on offense that it forgets to check danger first! - check one-move danger then go ahead

#ready for sharing - just note that whoever goes first has a disadvantage
