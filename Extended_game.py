# coding: utf-8
# !/usr/bin/env python



""" The Extended game program implements medics and expanded army, it generates a 2 Player/Commander game that allows
the user to pick which player he wants to use first to build  his army. An army can consist of a maximum of 10 units
that can be purchased in the range of $1 to $3 per unit, a commander can chose how many units he wants to purchase (max
10). There are 5 types of units available, Archers ($1), Soldiers ($1), Knights ($1), Siege Equipment ($2) and Wizards
($3), where  Archers are good against Soldiers but are terrible against Knights. Soldiers are good against Knights but
can’t win against Archers. Knights beat Archers, but fall short against Soldiers. Siege Equipment win against everyone
except Knights and Wizards. Wizard can beat anything, but they can’t dodge Archer arrows. If a unit comes up against a
unit of the same type, both lose. After each round, the loser will be removed from the battle field and the fight
continues with the winner of the previous round and the next in line of army of the losing commander of previous round.
If the losing commander has enough balance after purchasing units (balance>0), then medic will be used to revive the
lost army unit, at the cost of $1 for each revival, and the unit is added to the back of the army.The game continues
until a commander is left with no army, the winner of the last round is declared the winner. If the last round ends in a
tie, the commander having an army remaining is declared winner. If both commanders have no army left, the battle is
declared draw."""

"""The following module is used to provide color and bold formatting to the output printed on screen. Reference in
documentation."""
from colorama import *

init()

''' The matrix denotes who wins over the other, where 0 denotes Archer, 1 denotes Soldier, 2 denotes Knight, 3 denotes
Siege Equipment, 4 denotes Wizard and 5 denotes a tie. Hence game_matrix[i][j] would denote who will win the match 
between i and j, ex: match between Archer(0) and Soldier(1) would be won by Archer(0)'''

game_matrix = [[5, 0, 2, 3, 0], [0, 5, 1, 3, 4], [2, 1, 5, 2, 4], [3, 3, 2, 5, 4], [0, 4, 4, 4, 5]]

''' The class commander is used to define and store the army and cash balance for each player. The functions are used 
to add and remove units in the army and update the cash balance.'''


class Commander:
    """ The init function initialises 3 variables,  1.To store the amount in $ available with the commander, 2.The army the
    commander has built, as a list, 3.A dictionary that holds the name of the unit corresponding to the number
    assigned to them, mostly used for screen display. """

    def __init__(self):
        self.cash_balance = 10
        self.army = []
        self.units = {0: 'Archer', 1: 'Soldier', 2: 'Knight', 3: 'Siege Equipment', 4: 'Wizard'}

    ''' The purchase_units function adds units to the commanders army until the cash balance is available, i.e., it 
    is greater than 0 or till the user wishes to add units, whichever is earlier. With each unit purchase, it reduces $1 
    from the commander's balance. In case the user enters a wrong input for a choice, it repeats the menu until they 
    enter a valid input, after indicating an error message.'''

    def purchase_units(self):
        choice = 1
        while choice == 1 and self.cash_balance > 0:
            print("")
            print("You may purchase one unit at a time, Archer, Soldier or Knight units cost $1,"
                  " Siege Equipment unit costs $2 and Wizard unit cost $3")
            print(Fore.RED + Style.BRIGHT + "Your Current balance is ", str(self.cash_balance) + Style.RESET_ALL)
            print("Units: \n 1.Archer\n 2.Soldier\n 3.Knight\n 4.Siege Equipment\n 5.Wizard")
            unit_chosen = input("Enter your choice (1/2/3/4/5): ")
            ''' Using if else conditions to ensure that the input from user is only numeric and either 1,2,3,4 or 5'''
            if unit_chosen.isnumeric():
                unit_chosen = int(unit_chosen)
                if (unit_chosen >= 1) and (unit_chosen <= 3):
                    self.cash_balance -= 1
                elif unit_chosen == 4:
                    self.cash_balance -= 2
                elif unit_chosen == 5:
                    self.cash_balance -= 3
                else:
                    print(Fore.RED + "Invalid choice!!" + Style.RESET_ALL)
                    continue
            else:
                print(Fore.RED + "Invalid choice!!" + Style.RESET_ALL)
                continue
            self.army.append(unit_chosen - 1)
            print(Fore.RED + Style.BRIGHT + "Your Current balance is ", str(self.cash_balance) + Style.RESET_ALL)
            if self.cash_balance == 0:
                print("You can't purchase any further units")
                break
            else:
                ''' Using if else conditions to ensure that the input from user is only numeric and either 1 or 2'''
                while True:
                    choice = input("Do you want to continue purchasing? 1.Yes  2.No (1/2):")
                    if choice.isnumeric():
                        choice = int(choice)
                        if choice == 1 or choice == 2:
                            break
                        else:
                            print(Fore.RED + "Invalid Choice!!" + Style.RESET_ALL)
                    else:
                        print(Fore.RED + "Invalid Choice!!" + Style.RESET_ALL)

    ''' The function remove_unit is used to remove the unit in the front of the army if it has been defeated, if and only
    if there are any units to remove, i.e., the length of the army list is greater than 0. After removing/ popping the
    unit, it checks if the commander has enough balance to use the medic, if balance is more than 0, then the lost unit 
    is revived and added to the back of his army at the cost of $1, i.e.,his balance reduces by 1. If balance is 
    insufficient, no action is taken. After this process, it returns the length of the list, if it is greater than 0, or
    else it returns -1, to indicate that the list does not have elements to pop.'''

    def remove_unit(self, name):
        flag = 0
        if len(self.army) > 0:
            removed_item = self.army.pop(0)
            if self.cash_balance > 0:
                print("Medic used to revive", self.units[removed_item])
                self.army.append(removed_item)
                self.cash_balance -= 1
                print(self.units[removed_item], " has been added to ", name, "army at the end")
                print(Fore.RED + Style.BRIGHT + "Available Balance is ", str(self.cash_balance) + Style.RESET_ALL)
            else:
                print("Not enough cash balance to revive")
            flag = 1
        if flag:
            return len(self.army)
        else:
            return -1


''' The combat function forms the main logic of the battle, it checks the front of the army for both the commanders with
the game_matrix constructed above to see who wins, based on the unit that wins, the remove_unit function is called for 
the losing commander, to remove the unit at the front of his army, the result is printed on the screen and the battle 
continues to the next round, until there are no more units left in any one of the commander's army, correspondingly, 
the other commander is declared the winner of the game, who happens to be the winner of the last round as well. In case
of a tie, in a battle round, units at the front of the army for both the commanders are removed, using remove_unit. If
there is a tie in the last round, it is resolved by determining which commander has units left in his army, if both 
commanders are stranded, with empty armies, the game is declared a tie.'''


def combat():
    flag = 1
    flag1 = 1
    winner = None
    while flag and flag1:
        print("\n------------------------------------")
        print(Fore.CYAN + Style.BRIGHT + player1.units[player1.army[0]], " VS ", player2.units[player2.army[0]] +
              Style.RESET_ALL)
        if player1.army[0] == game_matrix[player1.army[0]][player2.army[0]]:
            winner = "Player1"
            print(Fore.YELLOW + Style.BRIGHT + "Round Winner: ", winner + Style.RESET_ALL)
            flag = player2.remove_unit("player2")

        elif player2.army[0] == game_matrix[player1.army[0]][player2.army[0]]:
            winner = "Player2"
            print(Fore.YELLOW + Style.BRIGHT + "Round Winner: ", winner + Style.RESET_ALL)
            flag = player1.remove_unit("player1")

        elif game_matrix[player1.army[0]][player2.army[0]]:
            winner = "No One"
            print(Fore.YELLOW + Style.BRIGHT + "Round Winner: ", winner, "\nIt's a Tie" + Style.RESET_ALL)
            flag = player1.remove_unit("player1")
            flag1 = player2.remove_unit("player2")

    if winner == "No One":
        if (flag > 0) and flag1 == 0:
            winner = "Player1"
        elif (flag1 > 0) and flag == 0:
            winner = "Player2"
        else:
            winner = "No One Its a tie"
    print("")
    print(Fore.YELLOW + Style.BRIGHT + "Winner of the Combat is :", winner + Style.RESET_ALL)
    return 0


# Create 2 objects for the class commander for the 2 players of the game
player1 = Commander()
player2 = Commander()

'''Displays a menu for the 2 commanders to choose their armies. A choice is given to determine whether commander 1 wants
to pick first or commander 2, Based on their choice, the commander's purchase_units function is called followed by the
other commander. The menu repeats itself if the user entered any value other than 1 or 2, after displaying an error 
message. Once the units are picked the combat function is called and the game begins.'''

print("Welcome to combat game!")
while True:
    playerChoice = input("Choose Player:\n 1.Player1\n 2.Player2 \n (1/2): ")
    print("")
    ''' Using if else conditions to ensure that the input from user is only numeric and either 1 or 2'''
    # if user chose player 1 assign units for player1
    if playerChoice.isnumeric():
        playerChoice = int(playerChoice)
        if playerChoice == 1:
            print("Player", playerChoice, "Assign Units")
            player1.purchase_units()
            print("")
            print(Fore.CYAN + Style.BRIGHT + "Your army is " + Style.RESET_ALL)

            # print the army built using the units dictionary with its key as army elements
            for i in range(len(player1.army)):
                print(player1.units[player1.army[i]])

            # Now let player 2 assign their units
            print("")
            print("Player", playerChoice + 1, "Assign Units")
            player2.purchase_units()
            print("")
            print(Fore.CYAN + Style.BRIGHT + "Your army is " + Style.RESET_ALL)

            # print the army built using the units dictionary with its key as army elements
            for i in range(len(player2.army)):
                print(player2.units[player2.army[i]])
            break

        # if user chose player 2 assign units for player2
        elif playerChoice == 2:
            print("Player", playerChoice, "Assign Units")
            player2.purchase_units()
            print("")
            print(Fore.CYAN + Style.BRIGHT + "Your army is " + Style.RESET_ALL)

            # print the army built using the units dictionary with its key as army elements
            for i in range(len(player2.army)):
                print(player2.units[player2.army[i]])

            # Now let player 1 assign their units
            print("")
            print("Player", playerChoice - 1, "Assign Units")
            player1.purchase_units()
            print("")
            print(Fore.CYAN + Style.BRIGHT + "Your army is " + Style.RESET_ALL)

            # print the army built using the units dictionary with its key as army elements
            for i in range(len(player1.army)):
                print(player1.units[player1.army[i]])
            break
        else:
            print(Fore.RED + "Invalid Player!!" + Style.RESET_ALL)

    else:
        print(Fore.RED + "Invalid Player!!" + Style.RESET_ALL)

print("")
print("Game Begins!")

# call combat function
combat()
key = input("Press enter to exit!")
