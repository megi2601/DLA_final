import numpy as np
from matplotlib import pyplot as plt

N = 1000

lattice_x = np.array([0])
lattice_y = np.array([0])
rmin = 30
rmax = 100
Rs = [rmin, rmax]


def update_radius(x, y):
    Rs[0] = max(Rs[0], np.round(np.sqrt(x*x+y*y))+rmin)
    Rs[1] = Rs[0]+rmax

def particle(lx, ly):
    x=0
    y=0
    while is_in_lattice(x, y, lx, ly):
        x = np.random.randint(-Rs[0], Rs[0])  #nie losuje z koła
        y = np.random.randint(-Rs[0], Rs[0])
    while(True):
        if is_near_lattice(x, y, lx, ly):
            lx = np.append(lx, x)
            ly = np.append(ly, y)
            update_radius(x, y)
            break
        x, y = move(x, y)
        if np.sqrt(x*x+y*y) >= Rs[1]:
            break
    return lx, ly


def is_near_lattice(x, y, lx, ly):
    points = [(x, y+1), (x+1, y),(x, y-1),(x-1, y)]
    for i in range(len(lx)):
        if (lx[i], ly[i]) in points:
            return True
    return False
                

def is_in_lattice(x, y, lx, ly):
    n = len(lx)
    for i in range(n):
        if lx[i] == x and ly[i] == y:
            return True
    return False

def move(x, y):
    points = [(x, y+1), (x+1, y),(x, y-1),(x-1, y)]
    i = np.random.randint(4)
    return points[i][0], points[i][1]


def plot_fractal(x, y):
    fig, ax = plt.subplots()
    ax.set_facecolor('black')

    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.tick_params(axis='both', which='both', length=0)
    plt.scatter(x, y, s=1, marker="o", lw=0, c="green")

    ax.set_xticks([])
    ax.set_yticks([])
    
    return fig, ax

a=0
for n in range(500):
    lattice_x, lattice_y = particle(lattice_x, lattice_y)
    if a%50 ==0:
        plt.scatter(lattice_x, lattice_y, marker='o', c='blue')
        plt.xlim([-20, 20])
        plt.ylim([-20, 20])
        plt.savefig("siec_w"+str(n))
    a+=1



print(lattice_x)
print(lattice_y)