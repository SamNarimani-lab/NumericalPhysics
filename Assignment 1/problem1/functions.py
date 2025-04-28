import numpy as np
from heapq import heappush, heappop

def dt_v (x , v , N , L , r):
    
    dt_w_v = np.zeros(N)
    mask_v_v_pos = v[:,0] > 0
    mask_v_v_neg = v[:,0] < 0
    mask_v_v_zero = v[:,0] == 0
    dt_w_v[mask_v_v_pos] = (L - r - x[:,0][mask_v_v_pos])/v[:,0][mask_v_v_pos]
    dt_w_v[mask_v_v_neg] = (r - x[:,0][mask_v_v_neg])/v[:,0][mask_v_v_neg]
    dt_w_v[mask_v_v_zero] = np.inf
    return dt_w_v
    
def dt_h (x , v , N , L , r):
    
    dt_w_h = np.zeros(N)
    mask_v_h_pos = v[:,1] > 0
    mask_v_h_neg = v[:,1] < 0
    mask_v_h_zero = v[:,1] == 0
    dt_w_h[mask_v_h_pos] = (L - r - x[:,1][mask_v_h_pos])/v[:,1][mask_v_h_pos]
    dt_w_h[mask_v_h_neg] = (r - x[:,1][mask_v_h_neg])/v[:,1][mask_v_h_neg]
    dt_w_h[mask_v_h_zero] = np.inf

    return dt_w_h
    
def dt_2_particles (x , v , N , sigma):
    
    dt_c = np.zeros((N , N))
    dx = x[:, np.newaxis, :] - x[np.newaxis, :, :]
    dv = v[:, np.newaxis, :] - v[np.newaxis, :, :]
    dr2 = np.sum(dx**2, axis=-1)
    dv2 = np.sum(dv**2, axis=-1)
    dot_product = np.sum(dv * dx, axis=-1)
    condition1 = np.greater(dot_product, 0)
    condition2 = np.less_equal((np.sum(dv * dx, axis=-1)**2) - (dv2 * (dr2 - sigma**2)), 0)
    dt_c = np.where(np.logical_or(condition1, condition2), np.inf, 
                    -(dot_product + np.sqrt((dot_product**2) - dv2 * (dr2 - sigma**2))) / dv2)  
    return dt_c

def x_prime(x , v , zeta , N , dt , sigma , m , event_type, event_index):
   v_prime = np.array ([[]])
   x_prime = np.zeros((N,2))
   if event_type == 'wall_v':
       v_prime = np.array ([-zeta * v [event_index ,0] ,  zeta * v[event_index ,1]])
       x_prime = x + dt* v
       v [event_index] = v_prime
   elif event_type == 'wall_h':
       v_prime  =  np.array ([zeta * v [event_index ,0] , -zeta * v[event_index ,1]])
       x_prime = x + dt* v
       v [event_index] = v_prime
   elif event_type =='to particles':
      i , j = event_index
      x_prime = x + dt* v
      dx_prime = x_prime[j] - x_prime[i]
      dv_prime = v[j] - v[i]
      R_2 = sigma**2
      alpha_j = (1 + zeta)* (m[i]/(m[i]+m[j]))*np.dot(dv_prime ,dx_prime) *dx_prime/R_2
      alpha_i = (1 + zeta)* (m[j]/(m[i]+m[j]))*np.dot(dv_prime ,dx_prime) *dx_prime/R_2
      v_prime_i = v[i] + alpha_i
      v_prime_j = v[j] - alpha_j
      v [i] = v_prime_i
      v [j] = v_prime_j
      

   else:
        raise ValueError(f"Invalid event type: {event_type}")

   return x_prime , v


def collision ( x , v , N , L , r , sigma , zeta ,m , t , args , position, velocity , collision_event ):
    for i in range(args): 
            dt_w_v = dt_v (x , v , N , L , r)
            dt_w_h = dt_h (x , v , N , L , r)
            dt_c = dt_2_particles (x , v , N , sigma)

            # Initialize the event queue as an empty list
            event_queue = []

            # add the event to the queue
            heappush(event_queue, (np.min(dt_w_v), 'wall_v', np.argmin(dt_w_v)))
            heappush(event_queue, (np.min(dt_w_h), 'wall_h', np.argmin(dt_w_h)))
            heappush(event_queue, (np.min(dt_c), 'to particles',
                                   np.unravel_index(np.argmin(dt_c, axis=None), dt_c.shape)))       
            # Retrieve the smallest event time from the event queue
            dt, event_type, event_index = heappop(event_queue)    
            x , v = x_prime (x , v , zeta , N , dt , sigma , m , event_type, event_index)
            t = t + dt
            collision_event . append ((t , event_type, event_index))
            velocity.append( np.round(np.sqrt(v[:, 0]**2 + v[:, 1]**2), decimals=6))
            position.append(x)
    return position , velocity , collision_event





