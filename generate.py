import numpy as np
import random


def phi(K):

    '''Generate unknown phase shifter angles. This function returns a string of K random 'phi' phase angles in the interval [0, 2pi[.'''

    return [random.uniform(0, 2*np.pi) for i in range(K)]


def input(N):

    '''Generate a standard input. This function returns a string of N 'input' photons in a random {0,1} configuration.'''

    input = np.array([np.matrix([[0],[0]]) for i in range(N)])

    for i in range(N):
        
        aux = random.randint(0,1)

        if aux == 0:
            input[i] = np.matrix([[1],[0]])
                
        else:
            input[i] = np.matrix([[0],[1]])

    return input


def policy(N):

    '''Generate policy. This function returns a string of N random 'policy' weights in the interval [0, 2pi[.'''

    return [random.uniform(0, 2*np.pi) for i in range(N)]