from individual import Individual, mutate, crossover
from custom_io import get_graph, get_number_of_medians
from random import sample, random
from copy import deepcopy
from math import ceil
from argparse import ArgumentParser


if __name__ == '__main__':
    parser = ArgumentParser(description='''Evolutionary Algorithm for
                                           the P-Median Problem''')
    parser.add_argument('inst', help='instance to be solved')
    parser.add_argument('popsize', type=int, help='population size')
    parser.add_argument('gener', type=int, help='number of generations')
    parser.add_argument('mutprob', type=float, help='probability of mutation')
    parser.add_argument('coprob', type=float, help='probability of crossover')
    parser.add_argument('tsize', type=int, help='tournament size')
    parser.add_argument('-e', '--elitism', type=float,
                        help='use of elitism')
    args = vars(parser.parse_args())
    for k, v in args.iteritems():
        print k + ': ' + str(v)

    G = get_graph(args['inst'])
    p = get_number_of_medians(args['inst'])
    nodes_ordered_by_demand = sorted(G.node.items(),
                                     key=lambda t: t[1]['demand'],
                                     reverse=True)

    pop = []
    for i in range(args['popsize']):
        individual = Individual(p, G)
        pop.append(individual)

    for i in range(args['gener']):
        scores = [(i.calculate_fitness(G, nodes_ordered_by_demand), i)
                  for i in pop]
        scores.sort()
        ranked = [i for (s, i) in scores]
        print scores[0][0]

        if args['elitism']:
            topelite = int(ceil(args['elitism'] * args['popsize']))
            new_pop = ranked[0:topelite]
        else:
            new_pop = []
        while len(new_pop) < args['popsize']:
            random_number = random()
            subpop = sample(pop, args['tsize'])
            if random_number < args['mutprob']:
                new_pop.append(mutate(subpop[0], G))
            elif random_number < args['coprob']:
                i1, i2 = crossover(subpop[0], subpop[1])
                new_pop.append(i1)
                new_pop.append(i2)
            else:
                new_pop.append(deepcopy(subpop[0]))
            if len(new_pop) > args['popsize']:
                new_pop.pop()
        pop = new_pop