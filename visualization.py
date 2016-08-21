import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.patches import Rectangle

def visualization():
    inter_x = []
    inter_y = []
    plt.axes()
    

    f = open('inter.txt', 'r')
    for line in f:
        line = line.split()
        inter_x.append(int(line[1]))
        inter_y.append(int(line[2]))
    f.close()


    #intersections (x0, y0)
    for i in range(0, len(inter_x)):
        circle = plt.Circle((inter_x[i], inter_y[i]), 0.5, fc='b')
        plt.gca().add_patch(circle)
    plt.axis('scaled')

    f = open('ori.txt', 'r')
    for line in f:
        line = line.split()
        for i in line:
            street = plt.Line2D((inter_x[int(line[0])], inter_x[int(i)]), (inter_y[int(line[0])], inter_y[int(i)]), lw=3.0)
            plt.gca().add_line(street)
    f.close()


    f = open('ori.txt','r')
    for line in f:
        line = line.split()
        for i in line:
            if inter_x[int(line[0])] == inter_x[int(i)]:
                if inter_y[int(line[0])] > inter_y[int(i)]:
                    plt.gca().add_patch(Rectangle((inter_x[int(line[0])]-0.25,inter_y[int(line[0])]-1),0.5,0.5,fc='r'))
                if inter_y[int(line[0])] < inter_y[int(i)]:
                    plt.gca().add_patch(Rectangle((inter_x[int(line[0])]-0.25,inter_y[int(line[0])]+0.5),0.5,0.5,fc='r'))
            else:
                if inter_x[int(line[0])] > inter_x[int(i)]:
                    plt.gca().add_patch(Rectangle((inter_x[int(line[0])]-1,inter_y[int(line[0])]-0.25),0.5,0.5,fc='r'))
                if inter_x[int(line[0])] < inter_x[int(i)]:
                    plt.gca().add_patch(Rectangle((inter_x[int(line[0])]+0.5,inter_y[int(line[0])]-0.25),0.5,0.5,fc='r'))
    f.close()
    
    plt.show()


