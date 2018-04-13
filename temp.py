# -*- coding: utf-8 -*-

#%matplotlib inline
import os, sys
import matplotlib
from matplotlib import cm
from matplotlib import pyplot as plt
import numpy as np

from matplotlib.patches import Circle, Wedge, Rectangle

def degree_range(n): 
    start = np.linspace(0,360,n+1, endpoint=True)[0:-1]
    end = np.linspace(0,360,n+1, endpoint=True)[1::]
    mid_points = start + ((end-start)/2.)
    return np.c_[start, end], mid_points

def rot_text(ang): 
    rotation = np.degrees(np.radians(ang) * np.pi / np.pi - np.radians(90))
    return rotation

with open('output.txt', 'r') as myfile:
    data=myfile.read()

if data == "Rock/Metal":
    x=1
elif data == "Folk/Country":
    x=2
elif data == "Electronic":
    x=3
elif data == "Jazz":
    x=4
elif data == "Reggae":
    x=5
elif data == "Pop":
    x=6
elif data == "Hip hop":
    x=7
elif data == "Instrumental":
    x=8    
myfile.close()
'''
with open('output.txt','r') as f:
    longest=max(f,key=len)
    
print(len(longest))
'''
def gauge(labels=['Rock/Metal','Folk/Country','Electronic','Jazz','Reggae','Pop','Hip hop','Instrumental'], \
          colors='jet_r', arrow=x, title='', fname=False): 
      
    N = len(labels)   
    if arrow > N: 
        raise Exception("\n\nThe category ({}) is greated than the length\nof the labels ({})".format(arrow, N))  
    if isinstance(colors, str):
        cmap = cm.get_cmap(colors, N)
        cmap = cmap(np.arange(N))
        colors = cmap[::-1,:].tolist()
    if isinstance(colors, list): 
        if len(colors) == N:
            colors = colors[::-1]
        else: 
            raise Exception("\n\nnumber of colors {} not equal to number of categories{}\n".format(len(colors), N))
    fig, ax = plt.subplots()
    ang_range, mid_points = degree_range(N)
    labels = labels[::-1]    
    patches = []
    for ang, c in zip(ang_range, colors): 
        patches.append(Wedge((0.,0.), .4, *ang, facecolor='w', lw=2))
        patches.append(Wedge((0.,0.), .4, *ang, width=0.10, facecolor=c, lw=2, alpha=0.5))  
    [ax.add_patch(p) for p in patches]

    for mid, lab in zip(mid_points, labels): 
        ax.text(0.35 * np.cos(np.radians(mid)), 0.35 * np.sin(np.radians(mid)), lab, \
            horizontalalignment='center', verticalalignment='center', fontsize=9, \
            fontweight='bold', rotation = rot_text(mid))
    ax.text(0, -0.05, title, horizontalalignment='center', \
         verticalalignment='center', fontsize=22, fontweight='bold')

    pos = mid_points[abs(arrow - N)]    
    ax.arrow(0, 0, 0.225 * np.cos(np.radians(pos)), 0.225 * np.sin(np.radians(pos)), \
                 width=0.04, head_width=0.09, head_length=0.1, fc='k', ec='k')   
    ax.add_patch(Circle((0, 0), radius=0.02, facecolor='k'))
    ax.add_patch(Circle((0, 0), radius=0.01, facecolor='w', zorder=11))
    ax.set_frame_on(True)
    ax.axes.set_xticks([])
    ax.axes.set_yticks([])
    ax.axis('equal')
    plt.tight_layout()
    fig.savefig("meter.png", dpi=200)
    plt.draw()  

gauge()
