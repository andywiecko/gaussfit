#!/bin/python
from scipy.optimize import curve_fit
import numpy as np
import os
import matplotlib.pyplot as plt

dataname = 'data.txt'
paraname = "".join(dataname.split('.')[:-1])+'.fit'
logname = "".join(dataname.split('.')[:-1])+'.log'

####################################################
# Load data and fitting parameters                 #
####################################################
if len(os.sys.argv)>1:
    dataname = os.sys.argv[1]
if len(os.sys.argv)>2:
    paraname = os.sys.argv[2]
data = np.genfromtxt(dataname)
para = np.genfromtxt(paraname,comments='#')
####################################################
# Global lists with data, fitting range            #
# and initial values                               #
####################################################
x, y = data[:,0], data[:,1]
guess, low, high = [], [], []
for i in range(0, len(para), 3):
    guess += para[i+0,:].tolist()
    low   += para[i+1,:].tolist()
    high  += para[i+2,:].tolist()
####################################################
# Some functions, which are used to calculate      #
# fit of data with multiple gausses and plot them  #
# in screen                                        #
####################################################
# Printing in column fitted param.                 #
####################################################
def print_popt(popt):
    print '#ctr amp wid'
    for i in range(len(popt)):
        print popt[i],
        if (i+1) % 3 == 0:
            print ''
####################################################
# Calc. y vals for all fitted gausses              #
####################################################
def func(x, *params):
    y = np.zeros_like(x)
    for i in range(0, len(params), 3):
        ctr = params[i]
        amp = params[i+1]
        wid = params[i+2]
        y = y + amp * np.exp( -((x - ctr)/wid)**2)
    return y
####################################################
# Calc. y vals for specific param.                 #
####################################################
def func_plt(x, ctr, amp, wid):
    y = np.zeros_like(x)
    y = y + amp * np.exp( -((x - ctr)/wid)**2)
    return y
####################################################
# Plot sub-gausses                                 #
####################################################
def subplot(x,popt):
    for i in range(0,len(popt),3):
        ctr = popt[i]
        amp = popt[i+1]
        wid = popt[i+2]
        fit_X = func_plt(x, ctr,amp,wid)
        plt.plot(X, fit_X,'--')
####################################################
# Generate X in density DX                         #
####################################################
def calcpoint(x):
    X = []
    XL = x[0]
    XR = x[-1]
    DX = 0.1
    for i in range(int((XR-XL)/DX)):
        X.append(XL+i*DX)
    return X
####################################################

####################################################
# fitting data
popt, pcov = curve_fit(func, x, y, p0=guess,bounds=(low,high))

f = open(logname, 'w')
f.write('#ctr amp wid\n')
for i in range(len(popt)):
    f.write(str(popt[i])+'\t')
    if (i+1) % 3 == 0:
        f.write('\n')
f.close()

# printing parameters
print_popt(popt)

# calculate line from fitted parameters
X = calcpoint(x)
fit = func(X, *popt)

# plot data
plt.plot(x, y)

# plot gausses sum
plt.plot(X, fit , 'r-',lw=2)

# plot sub-gauss
subplot(X,popt)

# plotting
plt.show()
####################################################
