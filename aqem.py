import numpy as np
import random


def interferometer(phi, cphi, mu, sigma):

    '''Clean and Gaussian Noise Interferometer. This function returns the output configuration of the photon after interacting with the clean or the Gaussian noise interferometer.'''

    cphi = cphi + np.random.normal(mu, sigma, 1)[0]

    return 1/2 * np.matrix([[-np.exp(1j*cphi) + np.exp(1j*phi), np.exp(1j*cphi) + np.exp(1j*phi)],
                            [-np.exp(1j*cphi) - np.exp(1j*phi), np.exp(1j*cphi) - np.exp(1j*phi)]])


def telegraph_interferometer(phi, cphi, p, delta):

    '''Random Telegraph Noise Interferometer. This function returns the output configuration of the photon after interacting with the Random Telegraph noise interferometer.'''

    aux = random.uniform(0, 1)

    if aux > p:
        cphi = cphi

    else:
        cphi = cphi + delta

    return 1/2 * np.matrix([[-np.exp(1j*cphi) + np.exp(1j*phi), np.exp(1j*cphi) + np.exp(1j*phi)],
                            [-np.exp(1j*cphi) - np.exp(1j*phi), np.exp(1j*cphi) - np.exp(1j*phi)]])


def visibility_interferometer(phi, cphi, input, visibility):

    '''Visibility Noise Interferometer. This function returns the output configuration of the photon after interacting with the Visibility noise interferometer.'''
    
    output = np.array([0. for i in range(2)])

    if input[0] == 1:      
        output[0] = np.sqrt(1/2 + 1/2 * visibility * np.cos(phi-cphi))
        output[1] = np.sqrt(1/2 - 1/2 * visibility * np.cos(phi-cphi))
        
    else:
        output[0] = np.sqrt(1/2 - 1/2 * visibility * np.cos(phi-cphi))
        output[1] = np.sqrt(1/2 + 1/2 * visibility * np.cos(phi-cphi))

    return output


def simulate(K, N, R, phi, input, policy, mu, sigma, loss, visibility):

    '''Adaptive Quantum Phase Estimation scheme. This function returns the 'variance' of the estimation process.'''

    variance = 0

    for k in range(R):
    
        cphi = [0 for x in range(K)]

        for i in range(K):

            for j in range(N):

                temp = random.uniform(0,1)

                if temp < loss:

                    output = -1

                    cphi[i] = cphi[i] 

                else:
                    
                    out = np.matmul(interferometer(phi[i], cphi[i], mu, sigma), input[j])                   #compute the interaction of the photons with the Clean and Gaussian Noise interferometer
                    #out = np.matmul(telegraph_interferometer(phi[i], cphi[i], mu, sigma), input[j])         #compute the interaction of the photons with the Random Telegraph Noise interferometer
                    #out = visibility_interferometer(phi[i], cphi[i], input[j], visibility)                  #compute the interaction of the photons with the Visibility interferometer

                    aux = random.uniform(0, 1)

                    if aux < abs(out[0])**2:
                        output = 0
                
                    else:
                        output = 1

                    if j < N:

                        cphi[i] = cphi[i] + pow(-1, output) * policy[j]

                        if cphi[i] < 0:
                            a = abs(cphi[i])
                            b = a // (2*np.pi) + 1
                            cphi[i] = 2*b*np.pi - a

                        if cphi[i] >= 2*np.pi:
                            a = cphi[i]
                            b = a // (2*np.pi)
                            cphi[i] = a - 2*b*np.pi
           
        performance = 0

        theta = [(phi[k] - cphi[k]) for k in range(K)]
               
        for k in range(K):
            performance = performance + np.exp(1j*theta[k])

        performance = abs(performance) / K

        variance = variance + pow(performance, -2) - 1

    variance = variance / R

    return variance