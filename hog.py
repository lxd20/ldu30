"""The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.


######################
# Phase 1: Simulator #
######################


def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 0.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN Question 1
    count = num_rolls
    total = 0
    can_add = True
    while count > 0:
        x = dice()
        if x == 1:
            can_add = False
        total = total + x
        count = count - 1
    if(can_add):
        return total
    else:
        return 0
    # END Question 1




def is_prime(total):
    x = 2
    if total == 1 or total ==0:
        return False
    while (x < total):
        if (total % x == 0):
            return False
        x = x+1
    return True


def next_prime(y):
    n = y+1
    while True:
        if is_prime(n):
            return n
        n = n+1


def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free bacon).

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.
    """
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN Question 2
    sum = 0
    if num_rolls ==0:
        x = opponent_score%10
        y = (opponent_score -x)//10
        sum = max(x,y)+1
    else:
        sum = roll_dice(num_rolls, dice)
    if is_prime(sum):
        sum = next_prime(sum)
    return sum


    # END Question 2


def select_dice(score, opponent_score):
    """Select six-sided dice unless the sum of SCORE and OPPONENT_SCORE is a
    multiple of 7, in which case select four-sided dice (Hog wild).
    """
    # BEGIN Question 3
    if (score+opponent_score) % 7 == 0:
        return four_sided
    else:
        return six_sided


    # END Question 3


def is_swap(score0, score1):
    """Returns whether the last two digits of SCORE0 and SCORE1 are reversed
    versions of each other, such as 19 and 91.
    """
    # BEGIN Question 4
    if(score0 < 10):
        x1 = 0
        y1 = score0
    else:
        n1 = score0%100
        y1 = n1%10
        x1 = (n1 -y1)/10

    if (score1<10):
        x2 = 0
        y2 = score1
    else:
        n2 = score1%100
        y2 = n2%10
        x2 = (n2 -y2)/10
    return x1 == y2 and y1 == x2



    # END Question 4


def other(who):
    """Return the other player, for a player WHO numbered 0 or 1.

    >>> other(0)
    >>> other(1)
    0
    """
    return 1 - who


def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):


    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first
    strategy1:  The strategy function for Player 1, who plays second
    score0   :  The starting score for Player 0
    score1   :  The starting score for Player 1
    """
    who = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    # BEGIN Question 5
    dice = six_sided
    while score0 < goal and score1 < goal:
        if who == 0:
            sum = take_turn(strategy0(score0,score1), score1, select_dice(score0, score1))
            if sum == 0:
                score1 += strategy0(score0,score1)
            else:
                score0 += sum
        else:
            sum = take_turn(strategy1(score1,score0), score0, select_dice(score0, score1))
            if sum == 0:
                score0 += strategy1(score1,score0)
            else:
                score1 += sum
        if is_swap(score0, score1):
            temp = score0
            score0 = score1
            score1 = temp
        who = other(who)

    # END Question 5
    return score0, score1


#######################
# Phase 2: Strategies #
#######################


def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n

    return strategy


# Experiments
def make_averaged(fn, num_samples=1000):


    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    >>> make_averaged(roll_dice, 1000)(2, dice)
    5.5

    In this last example, two different turn scenarios are averaged.
    - In the first, the player rolls a 3 then a 1, receiving a score of 0.
    - In the other, the player rolls a 5 and 6, scoring 11.
    Thus, the average value is 5.5.
    Note that the last example uses roll_dice so the hogtimus prime rule does
    not apply.
    """

    def func(*args):
        nonlocal num_samples
        total = 0
        x = num_samples
        while x > 0:
            result = fn(*args)
            total += result
            x -= 1
        return total / num_samples
    return func

def max_scoring_num_rolls(dice=six_sided, num_samples=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over NUM_SAMPLES times.
    Assume that dice always return positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    10
    """
    # BEGIN Question 7
    max_average = 0
    max_roll = 1
    x = 1
    while x <= 10:
        average = make_averaged(roll_dice, num_samples)
        n = average(x, dice)
        if n > max_average:
            max_average = n
            max_roll = x
        x += 1
    return max_roll

    # END Question 7



def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(5)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    if True:  # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Max scoring num rolls for four-sided dice:', four_sided_max)

    if False:  # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False:  # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if False:  # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    "*** You may add additional experiments as you wish ***"


# Strategies

def bacon_strategy(score, opponent_score, margin=8, num_rolls=5):
    """This strategy rolls 0 dice if that gives at least MARGIN points,
    and rolls NUM_ROLLS otherwise.
    """
    # BEGIN Question 8

    if (margin<=take_turn(0, opponent_score)):
        return 0
    else:
        return num_rolls

    # END Question 8


def swap_strategy(score, opponent_score, num_rolls=5):
    """This strategy rolls 0 dice when it results in a beneficial swap and
    rolls NUM_ROLLS otherwise.
    """
    # BEGIN Question 9
    test = score +take_turn(0, opponent_score)
    if is_swap(test, opponent_score):
        if (test < opponent_score):
            return 0
    return num_rolls

    # END Question 9


def play_strategy(num_rolls, score0, score1):
    sum = take_turn(num_rolls, score1, select_dice(score0, score1))
    if sum == 0:
        score1 += num_rolls
    else:
        score0 += sum
    if is_swap(score0, score1):
        temp = score0
        score0 = score1
        score1 = temp

    sum = take_turn(5, score0, select_dice(score0, score1))
    if sum == 0:
        score0 += num_rolls
    else:
        score1 += sum
    if is_swap(score0, score1):
        temp = score0
        score0 = score1
        score1 = temp

    return score0 - score1


def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.
    The code checks whether using swap_strategy or bacon_strategy can provide a score
    greater than 6 for a six_sided dice or 3 for a four_sided dice. If not, then I
    either roll 4 six_sided dices or 2 four_sided dices. I roll 0 if the sum of two total scores
    is a multiple of 7. I also roll 0 if the Goal_Score-score is at least 2 less than
    the value of the take_turn score. I roll 1 if the Goal_score-score is less than 2.
    """
    # BEGIN Question 10
    dice = select_dice(score, opponent_score)
    x = take_turn(0, opponent_score)
    if (score + x+opponent_score) % 7 == 0:
        return 0
    if (GOAL_SCORE-score) < 2:
        return 1
    if ((GOAL_SCORE-score) <= x+2) and (not is_swap(score + x, opponent_score)):
        return 0
    if dice == six_sided:
        if swap_strategy(score, opponent_score) == 0:
            swap_diff= opponent_score -(score+x)
            if swap_diff>6:
                return 0
        if not is_swap(score+x, opponent_score):
            return bacon_strategy(score,opponent_score,6,4)
        else:
            return 4

    else:
        if swap_strategy(score, opponent_score) == 0:
            swap_diff= opponent_score -(score+x)
            if swap_diff>3:
                return 0
        if not is_swap(score+x, opponent_score):
            return bacon_strategy(score,opponent_score,3,2)
        else:
            return 2

    # END Question 10


##########################
# Command Line Interface #
##########################


# Note: Functions in this section do not need to be changed. They use features
#       of Python not yet covered in the course.


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()

from hog import*
#counted_dice = make_test_dice(4,2,6)
#print(roll_dice(1, counted_dice))
