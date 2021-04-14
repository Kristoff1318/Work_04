import math
from display import *
from matrix import *

def generate_steps(step):
    i = 0
    lt = []
    while (i <= 1):
        lt.append(i)
        i += step
    return lt
    
def add_circle( points, cx, cy, cz, r, step ):
    lt = generate_steps(step)
    l = len(lt)

    for t in range(l):
        u0 = 2 * math.pi * lt[t]
        x0 = cx + r * math.cos(u0)
        y0 = cy + r * math.sin(u0)

        v = 2 * math.pi * lt[(t+1) % l]
        x1 = cx + r * math.cos(v)
        y1 = cy + r * math.sin(v)

        add_edge(points, x0, y0, cz, x1, y1, cz)

def evaluate_x(t, a_x, b_x, c_x, d_x):
    return (a_x * t**3) + (b_x * t**2) + (c_x * t) + d_x

def evaluate_y(t, a_y, b_y, c_y, d_y):
    return (a_y * t**3) + (b_y * t**2) + (c_y * t) + d_y

def add_curve( points, x0, y0, x1, y1, x2, y2, x3, y3, step, curve_type ):
    lt = generate_steps(step)
    l = len(lt)

    if curve_type == 'bezier':
        a_x = -x0 + (3 * x1) - (3 * x2) + x3
        b_x = (3 * x0) - (6 * x1) + (3 * x2)
        c_x = -(3 * x0) + (3 * x1)
        d_x = x0

        a_y = -y0 + (3 * y1) - (3 * y2) + y3
        b_y = (3 * y0) - (6 * y1) + (3 * y2)
        c_y = -(3 * y0) + (3 * y1)
        d_y = y0

    if curve_type == 'hermite':
        a_x = (2 * x0) - (2 * x1) + x2 + x3
        b_x = -(3 * x0) + (3 * x1) - (2 * x2) - x3
        c_x = x2
        d_x = x0

        a_y = (2 * y0) - (2 * y1) + y2 + y3
        b_y = -(3 * y0) + (3 * y1) - (2 * y2) - y3
        c_y = y2
        d_y = y0

    for t in range(l - 1):
        u = lt[t]
        xc = evaluate_x(u, a_x, b_x, c_x, d_x)
        yc = evaluate_y(u, a_y, b_y, c_y, d_y)
        
        v = lt[t+1]
        xn = evaluate_x(v, a_x, b_x, c_x, d_x)
        yn = evaluate_y(v, a_y, b_y, c_y, d_y)
        
        add_edge(points, xc, yc, 0, xn, yn, 0)


def draw_lines( matrix, screen, color ):
    if len(matrix) < 2:
        print('Need at least 2 points to draw')
        return

    point = 0
    while point < len(matrix) - 1:
        draw_line( int(matrix[point][0]),
                   int(matrix[point][1]),
                   int(matrix[point+1][0]),
                   int(matrix[point+1][1]),
                   screen, color)    
        point+= 2
        
def add_edge( matrix, x0, y0, z0, x1, y1, z1 ):
    add_point(matrix, x0, y0, z0)
    add_point(matrix, x1, y1, z1)
    
def add_point( matrix, x, y, z=0 ):
    matrix.append( [x, y, z, 1] )
    



def draw_line( x0, y0, x1, y1, screen, color ):

    #swap points if going right -> left
    if x0 > x1:
        xt = x0
        yt = y0
        x0 = x1
        y0 = y1
        x1 = xt
        y1 = yt

    x = x0
    y = y0
    A = 2 * (y1 - y0)
    B = -2 * (x1 - x0)

    #octants 1 and 8
    if ( abs(x1-x0) >= abs(y1 - y0) ):

        #octant 1
        if A > 0:            
            d = A + B/2

            while x < x1:
                plot(screen, color, x, y)
                if d > 0:
                    y+= 1
                    d+= B
                x+= 1
                d+= A
            #end octant 1 while
            plot(screen, color, x1, y1)
        #end octant 1

        #octant 8
        else:
            d = A - B/2

            while x < x1:
                plot(screen, color, x, y)
                if d < 0:
                    y-= 1
                    d-= B
                x+= 1
                d+= A
            #end octant 8 while
            plot(screen, color, x1, y1)
        #end octant 8
    #end octants 1 and 8

    #octants 2 and 7
    else:
        #octant 2
        if A > 0:
            d = A/2 + B

            while y < y1:
                plot(screen, color, x, y)
                if d < 0:
                    x+= 1
                    d+= A
                y+= 1
                d+= B
            #end octant 2 while
            plot(screen, color, x1, y1)
        #end octant 2

        #octant 7
        else:
            d = A/2 - B;

            while y > y1:
                plot(screen, color, x, y)
                if d > 0:
                    x+= 1
                    d+= A
                y-= 1
                d-= B
            #end octant 7 while
            plot(screen, color, x1, y1)
        #end octant 7
    #end octants 2 and 7
#end draw_line
