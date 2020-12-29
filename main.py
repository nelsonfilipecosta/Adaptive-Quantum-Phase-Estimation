import numpy as np
import generate
import aqem
import de
import pso


#Global Parameters
G = 100
N = 25
N_ini = 10
R = 5

#Convergence Parameter
threshold = 0.02

#DE Parameters
F = 0.7
C = 0.8

#PSO Parameters
alpha = 0.7
beta = 0.8
w = 0.8
vmax = 0.2

#Gaussian Noise Parameters
mu = 0
sigma = 0.0

#Telegraph Noise Parameters
p = 0.0
delta = 0.0

#Visibility Parameter
visibility = 1.0

#Photon Loss Parameter
loss = 0.00

#Simulation
for i in range(N_ini,N):

  K = 10 * pow(i,2)
  P = 20 + 2 * (i//10 - 1)

  phi = generate.phi(K)
  input = generate.input(i)

  print("\n")
  print("Iteration:", i)
  print("\n")

  print("Differential Evolution", "\n")
  evo = de.evolution(K, i, P, G, R, threshold, F, C, phi, input, 0, 0, 0, 1)                                    #run the DE algorithm under the Clean Interferometer configuration
  #evo = de.evolution(K, i, P, G, R, threshold, F, C, phi, input, mu, sigma, loss, 1)                            #run the DE algorithm under the Gaussian Noise Interferometer configuration
  #evo = de.evolution(K, i, P, G, R, threshold, F, C, phi, input, p, delta, loss, 1)                             #run the DE algorithm under the Random Telegraph Noise Interferometer configuration
  #evo = de.evolution(K, i, P, G, R, threshold, F, C, phi, input, 0, 0, 0, visibility)                           #run the DE algorithm under the Visibility Noise Interferometer configuration
  
  print("Particle Swarm Optimization", "\n")
  opt = pso.optimization(K, i, P, G, R, threshold, alpha, beta, w, vmax, phi, input, 0, 0, 0, 1)                #run the PSO algorithm under the Clean Interferometer configuration
  #opt = pso.optimization(K, i, P, G, R, threshold, alpha, beta, w, vmax, phi, input, mu, sigma, loss, 1)        #run the PSO algorithm under the Gaussian Noise Interferometer configuration
  #opt = pso.optimization(K, i, P, G, R, threshold, alpha, beta, w, vmax, phi, input, p, delta, loss, 1)         #run the PSO algorithm under the Random Telegraph Noise Interferometer configuration
  #opt = pso.optimization(K, i, P, G, R, threshold, alpha, beta, w, vmax, phi, input, 0, 0, 0, visibility)       #run the PSO algorithm under the Visibility Noise Interferometer configuration

  print("Holevo Variance (HL):  ", np.log(1/i))
  print("Holevo Variance (SQL): ", np.log(np.sqrt(1/i)))
  print("Holevo Variance (DE):  ", np.log(aqem.simulate(K, i, R, phi, input, evo, 0, 0, 0, 1)))
  print("Holevo Variance (PSO): ", np.log(aqem.simulate(K, i, R, phi, input, opt, 0, 0, 0, 1)))