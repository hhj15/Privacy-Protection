
import numpy as np
import math
import matplotlib.pyplot as plt


if __name__ == "__main__":
    
    base = './data/res/k'
    l2 = []
    l4 = []
    l6 = []
    l8 = []
    for l_div in range(2,11,1):
        direc2 = base+str(l_div)+'l2.npy'
        l2.append(list(np.load(direc2))[0][0])
    for l_div in range(4,11,1):
        direc4 = base+str(l_div)+'l4.npy'
        l4.append(list(np.load(direc4))[0][0])
    for l_div in range(6,11,1):
        direc6 = base+str(l_div)+'l6.npy'
        l6.append(list(np.load(direc6))[0][0])
    for l_div in range(8,11,1):
        direc8 = base+str(l_div)+'l8.npy'
        l8.append(list(np.load(direc8))[0][0])
    
    
    l1, = plt.plot(range(2,11,1),l2,'b.-')
    l2, = plt.plot(range(4,11,1),l4,'r.-')
    l3, = plt.plot(range(6,11,1),l6,'g.-')
    l4, = plt.plot(range(8,11,1),l8,'c.-')
#    l5, = plt.plot([16,32,64],l[2],'c>-')
    
    
    
    
    new_ticks = np.linspace(2, 11, 10)
    plt.xticks(new_ticks)
#    
#    l3, = plt.plot(range(2,7,1),l[0],'b.-')
#    l4, = plt.plot(range(3,7,1),l[1],'ro-')
#    l5, = plt.plot(range(4,7,1),l[2],'c>-')
#    l6, = plt.plot(range(6,11,1),l[3],'m,-')
#    l7, = plt.plot(range(7,11,1),l[4],'k*-')
    
    plt.legend(handles = [l1,l2,l3,l4,], labels = ['l=2','l=4','l=6','l=8',], loc = 'best')
    plt.xlabel('k')
    plt.ylabel('Average of Time Loss [h]')
    
    plt.savefig('test.png',dpi=500)
