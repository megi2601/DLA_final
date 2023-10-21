import numpy as np
from matplotlib import pyplot as plt
from numba import jit
import numba as nb

N = 10000 #liczba cząstek wpuszczonych do sieci

r_r1 = 50
r1_r2 = 150
R = [r_r1, r1_r2]

#matirx 
dim = 250
center = dim // 2

limit = 10

def matrix_to_coords(n, m):
    return n-center, m-center

def coords_to_matrix(x, y):
    n = x+center
    m = y+center
    return n, m


def update_radius(x, y):
    R[0] = max(R[0], np.round(np.sqrt(x*x+y*y))+r_r1)
    R[1] = R[0]+r1_r2


def is_near_lattice(n, m, lattice):
    points = [(n, m+1), (n+1, m),(n, m-1),(n-1, m)]
    for p in points:   ##
        try:
            if (lattice[p[0], p[1]]) == 1:
                return True
        except IndexError:
            pass
    return False

                
def invalid_point(x, y, lattice, point_val):
    n, m = coords_to_matrix(x, y)
    if too_far(x, y):
        return True
    if n>dim-2 or m >dim-2 or n<2 or m <2:  #punkt poza macierzą lub na brzegu
        return True
    if lattice[n, m] ==point_val:   #punkt jest częścią sieci
        return True
    return False


def too_far(x, y):
    return np.sqrt(x*x+y*y) >= R[1]


def move(x, y, lattice, point_val):
    points = [(x, y+1), (x+1, y),(x, y-1),(x-1, y)]
    points = [p for p in points if lattice[p[0], p[1]]!=point_val]
    i = np.random.randint(len(points))                              #co jeśli wylosuje między 4 elementami
    return points[i][0], points[i][1]

def point_in_circle(radius):
    r = np.random.rand()*radius
    phi = np.random.rand()*2*np.pi
    x = r*np.cos(phi)
    y = r*np.sin(phi)
    return int(x), int(y)


def plot_lattice(lattice, points, point_val):
    l2 = np.where(lattice >= point_val, 1, 0)
    plt.imshow(l2)
    plt.savefig(f"C:\SymulacjeKomputerowe\lab3_DLA\gif2\{points:05d}")


# 
# def walk(x0, y0, lattice):
#     x = x0
#     y = y0
#     while True:
#         n, m = coords_to_matrix(x, y)
#         if is_near_lattice(n, m, lattice):
#             lattice[n, m] = 1
#             update_radius(x, y)
#             return True
#         x, y = move(x, y)
#         if invalid_point(x, y, lattice):
#             return False

#numba

# def x_pic(r):
#     r = np.random.rand()*r
#     phi = np.random.rand()*2*np.pi
#     return  r*np.cos(phi)


# def y_pic(r):
#     r = np.random.rand()*r
#     phi = np.random.rand()*2*np.pi
#     return  r*np.sin(phi)


# def ctm(x):
#     return x-center

# def ip(x, y, lattice):
#     while invalid_point(x, y, lattice):
#         x = x_pic(R[0])
#         y = y_pic(R[0])
#     return x, y


# def evolve_point(lattice):
#     x = x_pic(R[0])
#     y = y_pic(R[0])
#     x, y = ip(x, y)
#     return walk(x, y, lattice)
    

# def walk(x, y, lattice):
#     while True:
#         n = ctm(x)
#         m = ctm(y)
#         if is_near_lattice(n, m, lattice):
#             lattice[n, m] = 1
#             update_radius(x, y)
#             return True
#         x, y = move(x, y)
#         if invalid_point(x, y, lattice):
#             return False

# #

def func_12(x, y, lattice, prob, point_val):
    n, m = coords_to_matrix(x, y)
    if np.random.rand() <= prob:
        lattice[n, m] = point_val
        update_radius(x, y)
        return True
    return False

def func_3(x, y, lattice, prob, point_val):
    n, m = coords_to_matrix(x, y)
    if np.random.rand <= prob:
        lattice[n, m] += 1
        if lattice[n, m] >= point_val:
            update_radius(x, y)
        return True
    return False

def count_to_points(lattice):
    return np.where(lattice >= limit, 1, 0)


# def evolve_point(lattice, func, probability, point_val):
#     x, y = point_in_circle(R[0])
#     while invalid_point(x, y, lattice):
#         x, y = point_in_circle(R[0])
#     while True:
#         n, m = coords_to_matrix(x, y)
#         if is_near_lattice(n, m, lattice):
#             # if np.random.rand >= p:
#             lattice[n, m] = 1
#             update_radius(x, y)
#             return True
#         x, y = move(x, y, lattice)
#         if invalid_point(x, y, lattice):
#             return False

def evolve_point(lattice, func, probability, point_val):
    x, y = point_in_circle(R[0])
    while invalid_point(x, y, lattice, point_val):
        x, y = point_in_circle(R[0])
    while True:
        n, m = coords_to_matrix(x, y)
        if is_near_lattice(n, m, lattice):
           b = func(x, y, lattice, probability, point_val)
           if b:
               return True
        x, y = move(x, y, lattice, point_val)
        if invalid_point(x, y, lattice, point_val):
            return False


def evolve(func, probability=1, point_val=1):
    lattice = np.zeros((dim, dim))
    lattice[center, center] = 1 #inicjacja sieci
    points = 1
    for _ in range(N):
        if evolve_point(lattice, func, probability, point_val):  #not counting points
            points+=1
        if points%50 ==1:
            plot_lattice(lattice, points, point_val)


evolve(func_12, 0.5, 1)

#250-300 dim 