import numpy as np
import matplotlib.pyplot as plt
import init4

import functions4
import time



# Constants 
L = 1.0                                 # box size
N = 1300                # number of particles

r0 = 0.008                               # disk radius
v0 = 2.75                            # initial velocity magnitude
m0 = 0.001
zeta = 0.5

r = r0 * np.ones (N+1)
r[N] =  5*r0
m = m0 * np.ones(N+1)
m [ N] = 25*m0

t = 0
args = 200000
sigma = np.zeros((N+1 , N+1))

r_sum = r[:, np.newaxis] + r
sigma = r_sum



# Generate initial conditions
x , v = init4.init(r , L , N , v0)   

velocity = []
position = []
collision_event = []
velocity .append (np.round(np.sqrt(v[:, 0]**2 + v[:, 1]**2), decimals=6))



if __name__ == '__main__':
    start_time = time.time()
    position , velocity , collision_event, ratio = functions4.collision( x , v , N , L , r , sigma , zeta ,m , t , args , position, velocity , collision_event )
    end_time = time.time()
    print("Time taken on CPU: ", end_time - start_time)
    
# np.save('velocity.npy' , velocity)
# np.save('collision_event.npy', collision_event)
# np.save('position.npy' , position)



# Set the size of the plot
plt.figure(figsize=(8, 8))

# Set the aspect ratio of the plot to square
ax = plt.subplot(111, aspect='equal')
ax.set_aspect('equal', adjustable='box')
box = plt.Rectangle((0, 0), L , L , fill=False, linewidth=2)
ax.add_patch(box)
ax.set_xlim([- 0.1, L + 0.1])
ax.set_ylim([- 0.1, L + 0.1])
# Set the axis labels and title
plt.xlabel('x')
plt.ylabel('y')
plt.title('Particle Positions')

ax.grid(True, linestyle='--', linewidth=0.5)
for i in range(N+1):
    circle = plt.Circle((position[-1][i,0], position[-1][i,1]), r[i], color='b', fill=True)
    ax.add_artist(circle)

plt.show()

np.save('positionv2.75.npy' , position)












