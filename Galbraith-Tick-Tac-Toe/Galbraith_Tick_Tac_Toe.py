import os
import time
#Game created by Ryan Galbraith using Microsoft Visual Studio and Windows 10. Running on any other OS might not work.

#Board_state tracks the current state of the Tic Tac Toe board and who marked what where. Letters rep Collums and Numbers rep Rows
board_state = {'A1':' ','A2':' ','A3':' ','B1':' ','B2':' ','B3':' ','C1':' ','C2':' ','C3':' '}
#A Board at the start of the game, blank. Made to quickly reset the board_state back to normal
starting_board_state = {'A1':' ','A2':' ','A3':' ','B1':' ','B2':' ','B3':' ','C1':' ','C2':' ','C3':' '}

#tracking wins==================
num_O_wins = 0 #number of times O has won
num_X_wins = 0 #number of times X has won
num_ties = 0   #number of times the game ended in a tie. Only happens in standard play

current_turn = 1    #tracks which turn it is. Odds, its Xs turn, Evens (or %2 == 0) is Os turn. Also tracks when to call a tie in standard play
                    #Gets increments in print_instructions

#tracking flags
quit_program = False            #Should the program try to quit?
in_game = False                 #Is a game in play? If not, we're still selecting a new game

standard_rules = True           #Is game a standard game or a non-standard (non-standard, players can clear a space taken by the other player instead of claim one for themselves)
bad_data = False                #Tracks to see if the last input was something the game can inturpert, or if its garbage.
bad_move_your_space = False     #Tracks to see if the last move was bad because player tried to claim a spot they already had.
bad_move_their_space = False    #Tracks to see if the last move was bad because player tried to claim a spot the other player already had while in standard play
winner_found = False            #Tracks to see if we currently have a winner for this game or not
tie_found = False               #Tracks to see if we reached a tie in this game or not
good_move = False               #Tracks to see if the last instruction while in a game was a good move or not

#DUBUG================================================================================================================

#This isn't used except to debug the vars. Prints out each var we track and what the type of varible it is.
def DEBUG_print_var():
    """Function is for debug, prints out the values of each varible"""
    print("num_O_wins is %s as a %s" % (str(num_O_wins), type(num_O_wins)))
    print("num_X_wins is %s as a %s" % (str(num_X_wins), type(num_X_wins)))
    print("num_ties is %s as a %s" % (str(num_ties), type(num_ties)))
    print("quit_program is %s as a %s" % (str(quit_program), type(quit_program)))
    print("in_game is %s as a %s" % (str(in_game), type(in_game)))
    print("current_turn is %s as a %s" % (str(current_turn), type(current_turn)))
    print("standard_rules is %s as a %s" % (str(standard_rules), type(standard_rules)))
    print("bad_data is %s as a %s" % (str(bad_data), type(bad_data)))
    print("bad_move_your_space is %s as a %s" % (str(bad_move_your_space), type(bad_move_your_space)))
    print("bad_move_their_space is %s as a %s" % (str(bad_move_their_space), type(bad_move_their_space)))
    print("winner_found is %s as a %s" % (str(winner_found), type(winner_found)))
    print("tie_found is %s as a %s" % (str(tie_found), type(tie_found)))
    print("good_move is %s as a %s" % (str(good_move), type(good_move)))

#PRINT COMMANDS======================================================================================================
#Print commands more or less are used together to display the current state of the board and what the user should do next

#Prints the horizontal line in the game board
def print_crossbar():
    """function prints the line between rows"""
    print("---||---|---|---")

#Prints the top of the game board showing the name of each column and the line dividing them from the game board
def print_topbar():
    """function prints the top of the game board"""
    print("   || A | B | C ")
    print("===||===|===|===")

#Prints the values of a row on the game board. It is passed which number the row is, and the values in columns A, B, and C.
def print_row(n, x, y, z):
    """Function takes the passed values, and prints one row of the board"""
    print(" %s || %s | %s | %s " % (n, x, y, z))

#Prints the instructions for the current player. Player_1 is who is suppose to move, and Player_2 is who they are playing aginst.
def print_player_move_instruction(player_1, player_2):
    """Function prints out the instructions of how to move for the player"""

    global standard_rules

    print("Player %s, please select a space to mark by entering a number (1-3) and a letter (A-C) followed by hitting Enter" % player_1)
    if(standard_rules):
        #print this only if the current game is playing with standard rules
        print("You can only pick an open spot")
    else:
        #print this only if the current game is player with non-standard rules
        print("Picking an empty spot marks it as yours, Picking a spot with a %s emptys it" % player_2)

#Game created by Ryan Galbraith using Microsoft Visual Studio and Windows 10. Running on any other OS might not work.

#Prints the current score, how often O has won, how often X has won and how often there has been a tie
def print_score():
    """Function prints the current scores"""

    global num_O_wins
    global num_X_wins
    global num_ties

    print("Player X has won %s times. Player O has won %s times." % (str(num_X_wins), str(num_O_wins)))
    print("There has been %s ties" % str(num_ties))

#Prints out the instructions of what the user is suppose to do next, or what state the game is in such as on a win.
def print_instructions(override = " "):
    """Function prints the current instructions for the player"""
    global quit_program
    global in_game
    global current_turn
    global standard_rules
    global bad_data
    global bad_move_your_space
    global bad_move_their_space
    global winner_found
    global tie_found
    global good_move

    current_player = " "
    other_player = " "

    #if current_turn is even, O is the current player. If odd, X is the current player.
    if(current_turn % 2 == 0):
        current_player = "O"
        other_player = "X"
    else:
        current_player = "X"
        other_player = "O"

    #if the override is still default, then this function should be able to figgure out the next line to show.
    if override == " ":
        #Find the instruction to print

        #If the game is quiting...
        if(quit_program):
            print("Quiting game. Thank-you for playing")

        #else, if a game is being played...
        elif(in_game):

            #..and the last command was a good move but didn't end the game..
            if(good_move and not winner_found and not tie_found):
                #..tell the next player what to do..
                print_player_move_instruction(other_player, current_player)
                #..and reset the flag and update the turn
                good_move = False
                current_turn += 1

            #..and the last command was worthless gibberish..
            elif(bad_data):
                #..tell the player what they did wrong and tell them what to do..
                print("That is not a recognized command.")
                print_player_move_instruction(current_player, other_player)
                #..and reset the flag
                bad_data = False

            #..and the last command was a move to try to take a space they already had..
            elif(bad_move_your_space):
                #..tell the player what they did wrong and tell them what to do..
                print("You can't mark that spot, you already own it")
                print_player_move_instruction(current_player, other_player) 
                #..and reset the flag
                bad_move_your_space = False

            #..and the last command was a move to try to take a space the other player has and it's a standard game..
            elif(bad_move_their_space):
                #..tell the player what they did wrong and tell them what to do..
                print("You can't mark that spot, the other player already owns it and this is a standard game")
                print_player_move_instruction(current_player, other_player)
                #..and reset the flag
                bad_move_their_space = False

                #Game created by Ryan Galbraith using Microsoft Visual Studio and Windows 10. Running on any other OS might not work.

            #..and the last command won the game. This is used in the win animation, so no instructions are given. Only the status. Also resets the good_move flag
            elif(winner_found):
                print("Player %s has won!!!!" % current_player)
                good_move = False

            #..and the last command tied the game. This is used in the tie animation, so no instructions are given. Only the status. Also resets the good_move flag
            elif(tie_found):
                print("No moves left, game is a tie")
                good_move = False
    
            #..and this is the first move of a new game. Tell the player what to do
            elif(current_turn == 1):
                print_player_move_instruction(current_player, other_player)

            #DEBUG DEBUG! ... and something went wrong, this is for the dev to find bad states while playing the game. Shouldn't ever show up.
            else:
                print("ERROR: CURRENT GAME STATE NOT EXPECTED! FIX ME!!!")

        #.. we aren't in a game currently..
        else:
            #..if the last command was garbage, let the user know..
            if(bad_data):
                print("That is not a recognized command.")
                bad_data = False
            #..instruct the user how to start a game..
            print("To start match pick either a standard game by typing 'S' or a non-standard game by typing 'N'. Then hit enter.")
            print("In a non-standard game you either pick an open space to claim as your own, or a space your opponent owns to clear it.")

        #.. and finaly let the player know how to end the game, but only if we're not in winner or tie animation or already quiting.
        if(not winner_found and not tie_found and not quit_program):
            print("You can type 'Q' or 'Quit' at any time to end program.")

    #something we didn't plan for needs to be told to the user, this lets us pass this function what that message needs to be and shows it.
    else:
        print(str(override))

#Updates the visuals: the board and it's state, the current score, and the instructions. Only thing I don't handle is the message on input.
def print_layout():
    """Function prints to the screen the current game board layout"""

    #!!!!!!!!!! This clears the command window. This was writen with Windows 10, this might not work on other systems !!!!!!!!!!!!!!!!!!!
    os.system('CLS')

    #Game created by Ryan Galbraith using Microsoft Visual Studio and Windows 10. Running on any other OS might not work.
    
    #Print the game board..
    print_topbar()
    print_row("1", board_state.get('A1'), board_state.get('B1'), board_state.get('C1'))
    print_crossbar()
    print_row("2", board_state.get('A2'), board_state.get('B2'), board_state.get('C2'))
    print_crossbar()
    print_row("3", board_state.get('A3'), board_state.get('B3'), board_state.get('C3'))

    #..then print the score and then print the current instructions..
    print("")
    print_score()
    print("")
    print_instructions()
    
# Normally called after a win or a tie. Resets the state of the board, the current turn and standard_rules.
def reset_board():
    """Function clears the board state, then copys the state of the starting board onto it"""
    global board_state
    global current_turn
    global standard_rules 

    #clear the board out completely then copy over the default state.
    board_state.clear()
    board_state = starting_board_state.copy()

    #then reset the other bools
    current_turn = 1
    standard_rules = True #Admitedly, this might not be needed as each game starts with user selecting this, but I like to know what state we're in as we start anew.

#Animation and End Game-----------------------------------------------------------------------------------------------------------------
#on a win or a tie we change the image to create an animation when a user wins or ties a game. We also track the score here

# Plays an animation showing off the winning move. X, Y, Z are the dictionary locations of that winning move.
def play_winner(x, y, z):
    """Function is called when a winner is found. Makes game board do winning flash"""
    global board_state
    global winner_found
    global num_O_wins
    global num_X_wins
    global in_game
    i = 5 #used in loop to create animation

    #Game created by Ryan Galbraith using Microsoft Visual Studio and Windows 10. Running on any other OS might not work.

    winning_player = board_state[x] #record who won, X or O

    #Add 1 to the score of the player who won.
    if(winning_player == "X"):
        num_X_wins += 1
    else:
        num_O_wins += 1

    #turn the winning spaces into " " and back to the winning player (X or O) i number of times
    while i >= 0:
        #Set the winning spaces into " "
        board_state[x] = " "
        board_state[y] = " "
        board_state[z] = " "
        #update the board
        print_layout()
        #wait a moment
        time.sleep(0.7)
        #Set the winning spaces into the winning team (X or O)
        board_state[x] = winning_player
        board_state[y] = winning_player
        board_state[z] = winning_player
        #Game created by Ryan Galbraith using Microsoft Visual Studio and Windows 10. Running on any other OS might not work.
        #update the board
        print_layout()
        #wait a moment
        time.sleep(0.7)
        #reduce the number of times you'll flip the values again by one
        i -= 1

    #update the flags saying we're not in game, we haven't found a winner, and reset the board to default
    in_game = False
    winner_found = False
    reset_board()


#A tie has been found. Play tie animation by setting all the spaces to "#" and then to " " and back again a few times before reseting the board for a new game
def call_tie():
    """Function is called when there are no moves left and no one won. Ends game and sets as a tie"""
    global num_ties
    global in_game
    global tie_found
    global board_state

    i = 5
    tie_found = True
    num_ties += 1


    #Game created by Ryan Galbraith using Microsoft Visual Studio and Windows 10. Running on any other OS might not work.
    while i >= 0:
        for key in board_state:
            board_state[key] = "#"
            #print("key is %s" % str(key))
        print_layout()
        time.sleep(0.7)
        for key in board_state:
            board_state[key] = " "
        print_layout()
        time.sleep(0.7)
        i -= 1


    tie_found = False
    in_game = False
    reset_board()

#GAME AND INPUT FUCTIONS---------------------------------------------------------------------------------------------------------------------------
#handles all the input and what that input means

#Check to see if we have a winning move. The argument is the most recent move. Check all the possible lines that argument is on.
def check_for_win(target):
    """Function checks the three spaces given and see if they are all the same. If they are, we have a winner, Return true and run win sequence. Else Return False"""
    global board_state
    global winner_found

    #For each check, run the play_winner fuction passing the spaces that are part of the winning move, and update the winner_found flag

    #We take the first letter in the string, which is the column. Attaching that to different numbers we can see if we have a column win
    if ((board_state[target[0]+"1"] == board_state[target[0]+"2"] == board_state[target[0]+"3"]) and (board_state[target[0]+"1"] != " ")):
        winner_found = True
        play_winner(target[0]+"1", target[0]+"2", target[0]+"3")
    #We take the second letter in the string, which is the row. Attaching that to different letters, we can see if we have a row win
    elif ((board_state["A"+target[1]] == board_state["B"+target[1]] == board_state["C"+target[1]]) and (board_state["A"+target[1]] != " ")):
        winner_found = True
        play_winner("A"+target[1], "B"+target[1], "C"+target[1])
    #Check to see if the target on a diagonal and if the center square is even claimed. If so, it's possible there is a diagonal.
    elif (target != "B1" and target != "B3" and target != "A2" and target != "C2" and board_state["B2"] != " "):
        #Check to see if Top-Left to Bottom-Right diagonal is a win
        if (board_state["A1"] == board_state["B2"] == board_state["C3"]):
            winner_found = True
            play_winner("A1", "B2", "C3")
        #Check to see if Top-Right to Bottom-Left diagonal is a win
        elif(board_state["A3"] == board_state["B2"] == board_state["C1"]):
            winner_found = True
            play_winner("A3", "B2", "C1")


#Player has made a move in a match. Figgure out what the move is. Argument is the location of the move the player inputed (expected that value has been set to upper case).
def player_move(loc):
    """Function is called when player makes a move, function then updates game state"""
    global board_state
    global current_turn
    global bad_move_your_space
    global bad_move_their_space
    global standard_rules
    global winner_found
    global good_move
    global in_game

    location = ""

    #We KNOW the loc is a key on the board_state, but the order of Number and Letter might be backwards.
    #first see if the value the player gave is a key in the board_state. 
    if(loc in board_state):
        location = loc
    #if its not, then the Number and Letter is backwards. As there are only two char in the string, reversing the string will produce a key
    else:
        location = loc[::-1]

    #First, if the current_turn is even, it was O's play
    if(current_turn % 2 == 0):
        #if location has an O in it, then the player picked a bad spot because they already own it. Update flag accordingly.
        if board_state[location] == "O":
            bad_move_your_space = True
        #else if location is blank, claim it for the player. Update flag and board for a good move.
        elif board_state[location] == " ":
            board_state[location] = "O"
            good_move = True
        #else if these aren't the standard rules, and we have a spot the other player has claimed (by process of elimination), then unclaim the spot and update board and flags.
        elif not standard_rules:
            board_state[location] = " "
            good_move = True
        #else we are playing with standard rules and this spot was claimed by the other player. Then this is a bad move. Update the flag accordingly.
        else:
            bad_move_their_space = True

    #..else, the current_turn is odd, meaning it was X's play
    else:
        #if location has an X in it, then the player picked a bad spot because they already own it. Update flag accordingly.
        if board_state[location] == "X":
            bad_move_your_space = True
        #else if location is blank, claim it for the player. Update flag and board for a good move.
        elif board_state[location] == " ":
            board_state[location] = "X"
            good_move = True
        #else if these aren't the standard rules, and we have a spot the other player has claimed (by process of elimination), then unclaim the spot and update board and flags.
        elif not standard_rules:
            board_state[location] = " "
            good_move = True
        #else we are playing with standard rules and this spot was claimed by the other player. Then this is a bad move. Update the flag accordingly.
        else:
            bad_move_their_space = True

    #if neither bad move flag has been set, then we should check to see if the player won or tied
    if((not bad_move_their_space) and (not bad_move_your_space)):
        #Check for win. If not a win, and a standard game and if current_turn is at the max number of moves, then statment is true.
        #if true, we have, and call for, a tie
        if((not check_for_win(location)) and (standard_rules) and (current_turn == 9)):
            call_tie()

#Ask for the user's input. Figgure out if its a valid command.            
def player_input():
    global quit_program
    global board_state
    global in_game
    global standard_rules
    global bad_data

    #Request input from the user. This is the only place a string is printed to screen outside a print command
    #we use .upper() to make the string given to us by the user so we don't have to do one check for upper and one for lower as case doesn't mater, only the letter used
    input_value = input("Enter command: ").upper()

    #See if the player asked to quit. If so, update the flag for quit
    if input_value == "Q" or input_value == "QUIT":
        quit_program = True

    #see if the input, forward or backwards is a key in board_state. If in game, the input was a valid game move. Ask player_move to sort out what move.
    elif((input_value in board_state or input_value[::-1] in board_state) and in_game):
        player_move(input_value)

    #else, if not in a game, user should be requesting a game
    elif(not in_game):

        #If user inputed an S, start up a standard_rules game
        if(input_value == "S"):
            standard_rules = True
            in_game = True

        #if user inputed an N, start up a non-standard_rules game
        elif(input_value == "N"):
            standard_rules = False
            in_game = True

#if what the user inputed hasn't triggered one of the above checks, its just bad data. Update the flag accordingly.
        else:
            bad_data = True
    else:
        bad_data = True

        

#this is the main game loop. It goes between updating the screen, and checking the player input over and over until we're told to quit. Just like a big boy game. :)
#Uncomment DEBUG_print_var() to track the values of the flags for testing and hunting bugs
def game_loop():
    """Function loops between accepting input and updating the board until quit_program is true"""
    while not quit_program:
        print_layout()
        #DEBUG_print_var()
        player_input()
    #update the layout one last time.
    print_layout()

game_loop()


#Game created by Ryan Galbraith using Microsoft Visual Studio and Windows 10. Running on any other OS might not work.