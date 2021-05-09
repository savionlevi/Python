from random import *


# rock paper scissors game
def rock_paper_scissors():
    print("ROCK, PAPER, SCISSORS")
    wins = 0
    losses = 0
    ties = 0
    running = True
    player_selection = ''
    list_of_outcome = {"wins": 0, "losses": 0, "ties": 0}
    while running:
        print(list_of_outcome["wins"], "Wins", list_of_outcome["losses"], "Losses", list_of_outcome["ties"], "Ties")
        print("Enter your move: (r)ock (p)aper (s)cissors (q)uit")
        player_selection = input()
        computer_pick = get_computer_pick()
        battle_result = ''
        if player_selection == 'r':
            print("ROCK versus...")
            print(computer_pick)
            battle_result = determine_victor('rock', computer_pick)
            print("result: ", battle_result)
        elif player_selection == 'p':
            print("PAPER versus...")
            print(computer_pick)
            battle_result = determine_victor('paper', computer_pick)
            print("result: ", battle_result)
        elif player_selection == 's':
            print("scissors versus...")
            print(computer_pick)
            battle_result = determine_victor('scissors', computer_pick)
            print("result: ", battle_result)
        elif player_selection == 'q':
            print('game ended !')
            running = False
        list_of_outcome = update_results(battle_result, list_of_outcome)


def get_computer_pick():
    """ Returns the selection the computer makes in the rock paper scissors game """
    list_of_options = ['rock', 'paper', 'scissors']
    return choice(list_of_options)


def determine_victor(player_choice, computer_choice):
    """ returns the result of the match. win = player won"""
    result = ''
    if player_choice == computer_choice:
        result = 'Tie'
    elif (player_choice == 'rock' and computer_choice == 'scissors') or (
            player_choice == 'paper' and computer_choice == 'rock') or (
            player_choice == 'scissors' and computer_choice == 'paper'):
        result = 'win'
    else:
        result = 'loss'
    return result


def update_results(battle_res, list_of_outcome):
    """ update the dictionary comtaining the results, win, loss, tie"""
    if battle_res == 'win':
        list_of_outcome['wins'] += 1
    elif battle_res == 'loss':
        list_of_outcome['losses'] += 1
    else:
        list_of_outcome['ties'] += 1
    return list_of_outcome


def print_results(outcome, dict):
    """ prints the outcome of the battels"""
    print(dict[outcome])


def main():
    rock_paper_scissors()


if __name__ == '__main__':
    main()
