import numpy as np
from matplotlib import pyplot as plt
from numba import jit
import numba as nb


@jit(nopython=True)
def walk(lattice, dim, center, limit, prob, lattice_r, r2, x, y):
    point = False
    l_radius = 0
    while(True):
        n = x+center
        m = y+center
        if n>dim-2 or m >dim-2 or n<2 or m <2:                 #check if outside the matrix
            break
        points = [(n, m+1), (n+1, m),(n, m-1),(n-1, m)]
        for p in points:  
            if (lattice[p[0], p[1]]) == limit:
                if np.random.rand() <= prob:    
                    lattice[n, m] +=1               
                    if lattice[n, m] == limit:
                        point = True
                        l_radius = np.sqrt(x*x+y*y) #update radius
                    break
                else:
                    break
        if point:
            break
        moves = np.array([[x, y+1], [x+1, y], [x, y-1], [x-1, y]])
        moves2 = []
        for move in moves:
            nn = move[0]+center
            mm = move[1]+center
            if nn>dim-2 or mm >dim-2 or nn<2 or mm <2:                 #check if  outside the matrix
                continue
            if lattice[nn, mm] != limit:
                moves2.append(move)
        if len(moves2) == 0:
            break
        i = int(np.random.rand()*len(moves2))
        new_p = moves2[i] #move
        x = new_p[0]
        y = new_p[1]
        if np.sqrt(x*x+y*y) >= lattice_r+r2:  #check if outside big circle
            break
    return l_radius



def run(lattice, dim, center, N, r1, r2, limit, prob, step):
    lattice_r = 0
    points = 0
    saved = False
    for _ in range(N):
        if not saved:
            l2 = np.where(lattice == limit, 1, 0)
            im = plt.imshow(l2, cmap='Greys', interpolation='nearest')  
            plt.axis("off")
            plt.title(f'{points}', loc="left", fontsize='medium')
            plt.savefig(f"inny\{points:05d}", bbox_inches = 'tight', dpi=288)  #musi byc dpi!
            saved = True
            print(points)
        #r = lattice_r+np.sqrt(np.random.rand())*r1
        r = np.sqrt(np.random.rand()*(2*lattice_r*r1+r1*r1) + lattice_r*lattice_r)   #losowanie między r sieci a r sieci + r1
        #r = np.sqrt(np.random.rand())*(lattice_r+r1)  #losowanie uniformly w kole r sieci + r1
        phi = np.random.rand()*2*np.pi
        x = int(r*np.cos(phi))
        y = int(r*np.sin(phi))
        if lattice[x+center, y+center] == limit:  ## may be out of bounds - dim / 40 ok
            continue
        l_radius = walk(lattice, dim, center, limit, prob, lattice_r, r2, x, y)
        if l_radius != 0:                                                           #jeśli został dodany punkt, to promień nie jest zerowy
            points+=1
            if points % step == 0:
                saved = False
        lattice_r = max(lattice_r, l_radius)

        
N=10000       
dim=400     
center = dim // 2
limit = 10
p=0.1

lattice = np.zeros((dim, dim))
lattice[center, center] = limit

run(lattice, dim, center, N, 10, 150, limit, p, 500)
