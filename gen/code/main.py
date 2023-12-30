from lib import *

def logic(pv, dv, count, decision):
    player, dealer, deck = Hand(), Hand(), Deck()
    game = Game([player, pv], [dealer, dv], [deck, count], decision)
    if dv == "A": game.peak()

    if decision == "D" and game.on: double, split = True, False
    elif decision == "P" and game.on: double, split = False, True
    else: double, split = False, False

    while game.on:
        game.do_player()
    game.do_dealer()
    result = game.update_result()

    if split: 
        player2, dealer2, deck2 = Hand(), Hand(), Deck()
        game2 = Game([player2, pv], [dealer2, dv], [deck2, count], "H")
        game2.dealer = game.dealer
        while game2.on:
            game2.do_player()
        game2.do_dealer()
        result += game2.update_result()

    elif double:
        result *= 2

    return result

def to_file(pv, dv, count, decision, expected_value):
    dictionary = {"H":"hit", "S":"stand", "D":"double", "P":"split"}
    with open(f"./results/{dictionary[decision]}/{count}.csv", "r") as f:
        table = list(csv.reader(f))
    j = table[0].index(dv)
    for line in table:
        if line[0] == pv:
            i = table.index(line)
    table[i][j] = "{:.4f}".format(expected_value)
    with open(f"./results/{dictionary[decision]}/{count}.csv", "w") as f:
        csv.writer(f).writerows(table)

def main(pv, dv, count, decision):
    print(f"Starting {pv} vs. {dv} at {count} with {decision}")
    wins, draws, losses, total = 0, 0, 0, 100000
    for _ in range(0,total):
        result = logic(pv, dv, count, decision)
        if result > 0: wins += result
        elif result == 0: draws += result
        elif result < 0: losses -= result
    expected_value = (1 * wins/total) + (0 * draws/total) + (-1 * losses/total)
    to_file(pv, dv, count, decision, expected_value)
    print(f"Finished {pv} vs. {dv} at {count} with {decision}")