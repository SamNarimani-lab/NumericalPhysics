import numpy as np
import matplotlib.pyplot as plt
import init

import functions
import time
from scipy.stats import maxwell


# Constants 
L = 1.0                                 # box size
N = 2000                          # number of particles

r = 0.001                               # disk radius
v0 = 1                                # initial velocity magnitude
m0 = 0.001
zeta = 1.0 

r1 = r
r2 = r
sigma = r1 + r2
t = 0
args = 60000


m = np.empty(N)
m[:N//2] = m0
m[N//2:] = 4*m0  

# Generate initial conditions
x , v , theta = init.init(r, L, N ,v0)   
velocity = []
position = []
collision_event = []
velocity .append (np.round(np.sqrt(v[:, 0]**2 + v[:, 1]**2), decimals=6))


if __name__ == '__main__':
    start_time = time.time()
    position , velocity , collision_event = functions.collision(x, v, N, L, r, sigma, zeta, m, t, args, position, velocity, collision_event)
    end_time = time.time()
    print("Time taken on CPU: ", end_time - start_time)

count = 0
avg_particle = np.zeros (args)
collision_type = collision_event[: , 1]
for i in range (args):
    if collision_type [i] == 'to particles':
        count=count +1
        avg_particle[i] = count / N

np.save('velocity.npy' , velocity)
np.save('collision_event.npy', collision_event)
np.save('position.npy' , position)
np.save('mass.npy' , m)

