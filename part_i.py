"""
The player is given a d20 with an initial value of 1.
There will be 100 rounds.
Each round, the player may either roll the d20 or take the current value of the d20.
How should the player play this game? How much will the player earn on average?
"""

import matplotlib.pyplot as plt
import numpy as np
import random


def sim():
    total_num_rounds = 100
    face_value = 1

    rolls = list(random.randint(1, 20) for _ in range(100))
    rolls[0] = 1

    returns = list()
    for round, face_value in enumerate(rolls):
        returns.append(face_value * (total_num_rounds - round))

    round = returns.index(max(returns))

    return round, rolls[round]

def monte_carlo():
    d = dict()
    for _ in range(10000):
        game_round, face_value = sim()
        if game_round not in d:
            d[game_round] = list()
        d[game_round].append(face_value)

    return d

def get_rounds(d: dict):
    rounds = list()
    for i in range(100):
        face_values = list(0 for _ in range(21))
        if i in d:
            for j in d[i]:
                face_values[j] += 1
        rounds.append(face_values)
    
    # remove rounds with no maximums
    cleaned_rounds = list(rounds)
    for i in range(1, len(rounds)):
        if sum(rounds[i]) == 0:
            cleaned_rounds.remove(rounds[i])
    
    return cleaned_rounds

def heatmap(rounds: list[list]):
    # rotate arrays
    y = list()
    for i in range(21):
        x = list(j[i] for j in rounds)
        y.append(x)

    # find y-axis limit
    for i in range(1, len(y)):
        if sum(y[i]) != 0:
            ylim = i
            break

    matrix = np.array(y)
    plt.imshow(matrix)
    plt.ylim(ylim, 20.5)
    plt.yticks(np.arange(ylim+1, 21))
    plt.xticks(np.arange(0, len(y[0]), 10), labels=np.arange(1, len(y[0])+1, 10))
    plt.colorbar(shrink=0.5)
    plt.show()

def graph_face_value(rounds: list[list]):
    x = list()
    y = list()
    for r in rounds:
        for face_value in range(1, 21):
            if sum(r) == 0:
                break
            if sum(r[face_value:]) / sum(r) < 0.99:
                x.append(rounds.index(r))
                y.append(face_value)
                break
    y_avg = np.mean(y)
    y_avg = y[np.abs(y - y_avg).argmin()]
    plt.axhline(y=y_avg)
    plt.scatter(x, y)
    plt.show()

def graph_game_round(d: dict):
    x = list()
    y = list()
    for i in d:
        x.append(i)
        y.append(len(d[i]))
    y_avg = np.mean(y)
    x_avg = x[np.abs(y - y_avg).argmin()]
    plt.axvline(x=x_avg)
    plt.scatter(x, y)
    plt.show()

def graph_returns():
    total_returns = list()
    n_sum = 210
    for n in range(1, 21):
        accepted_sides = 21 - n
        rolls = 20 / accepted_sides
        remaining_rounds = 100 - rolls
        avg = n_sum / accepted_sides
        n_sum -= n

        total_returns.append(avg * remaining_rounds)
    plt.plot(total_returns)
    plt.xticks(np.arange(0, 20, 1), labels=np.arange(1, 21, 1))
    plt.show()

# the player wants to maximize value early
# and simply take for the remaining rounds
def get_answers():
    max_return = 100
    n_sum = 210
    for n in range(1, 21):
        accepted_sides = 21 - n
        rolls = 20 / accepted_sides
        remaining_rounds = 100 - rolls
        avg = n_sum / accepted_sides
        n_sum -= n

        total = avg * remaining_rounds
        if total <= max_return:
            return n - 1, max_return
        max_return = total

def main():
    d = monte_carlo()
    rounds = get_rounds(d=d)
    heatmap(rounds=rounds)
    graph_face_value(rounds=rounds)
    graph_game_round(d=d)
    graph_returns()

    min_accepted_face_value, avg_earnings = get_answers()
    print(f"The player should roll until the d20 shows {min_accepted_face_value} or above")
    print(f"The player's average earnings would be {avg_earnings}")


if __name__ == '__main__':
    main()
