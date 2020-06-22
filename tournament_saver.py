#!usr/bin/env python
"""
A command line program for multiple games between several bots.

For all the options run
python play.py -h
"""

from argparse import ArgumentParser
from api import State, util, engine
import random, time
import csv

def run_tournament(options):

	botnames = options.players.split(",")
	player1 = botnames[0]
	player2 = botnames[1]
	bots = []
	for botname in botnames:
		bots.append(util.load_player(botname))

	n = len(bots)
	wins = [0] * len(bots)
	matches = [(p1, p2) for p1 in range(n) for p2 in range(n) if p1 < p2]

	totalgames = (n*n - n)/2 * options.repeats
	playedgames = 0

	print('Playing {} games:'.format(int(totalgames)))

	output = []

	for a, b in matches:
		for r in range(options.repeats):

			if random.choice([True, False]):
				p = [a, b]
			else:
				p = [b, a]

			# Generate a state with a random seed
			state = State.generate(phase=int(options.phase))

			bot_1 = bots[p[0]]
			bot_2 = bots[p[1]]

			winner, score = engine.play(bot_1, bot_2, state, options.max_time*1000, verbose=options.verbose, fast=options.fast)

			if winner is not None:
				winner = p[winner - 1]
				#print(winner)
				#print(str(p))
				wins[winner] += score
			
			winner = bots[winner]

			if winner == bots[0]:
				winner = player1
			else:
				winner = player2
				
				
			print(str([r + 1, winner, score, wins[0], wins[1]]))

			output.append([r + 1, winner, score, wins[0], wins[1]])

			playedgames += 1
			print('Played {} out of {:.0f} games ({:.0f}%): {} \r'.format(playedgames, totalgames, playedgames/float(totalgames) * 100, wins))

	file_name = str(botnames[0]) + " vs " + str(botnames[1]) + " for " + str(options.repeats) + " games.csv"
			
	with open(file_name, mode='w') as out_file:
		
		file_writer = csv.writer(out_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		file_writer.writerow(['Game no.', 'Winner', 'Score', str(player1), str(player2)])

		for row in output:
			file_writer.writerow(row)

	print('Results:')
	for i in range(len(bots)):
		print('    bot {}: {} points'.format(bots[i], wins[i]))


if __name__ == "__main__":

	## Parse the command line options
	parser = ArgumentParser()

	parser.add_argument("-s", "--starting-phase",
						dest="phase",
						help="Which phase the game should start at.",
						default=1)

	parser.add_argument("-p", "--players",
						dest="players",
						help="Comma-separated list of player names (enclose with quotes).",
						default="rand,bully,rdeep")

	parser.add_argument("-r", "--repeats",
						dest="repeats",
						help="How many matches to play for each pair of bots",
						type=int, default=10)

	parser.add_argument("-t", "--max-time",
						dest="max_time",
						help="maximum amount of time allowed per turn in seconds (default: 5)",
						type=int, default=5)

	parser.add_argument("-f", "--fast",
						dest="fast",
						action="store_true",
						help="This option forgoes the engine's check of whether a bot is able to make a decision in the allotted time, so only use this option if you are sure that your bot is stable.")

	parser.add_argument("-v", "--verbose",
						dest="verbose",
						action="store_true",
						help="Print verbose information")

	options = parser.parse_args()

	run_tournament(options)
