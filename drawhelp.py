# -*- coding: utf-8 -*-
# yumo

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

g_Ax = None

def InitSystem():
	global g_Ax
	fig = plt.figure()
	g_Ax = fig.add_subplot(111, projection='3d')

def DrawTriList(triList):
	for tri in triList:
		g_Ax.add_collection3d(Poly3DCollection(tri, facecolors='cyan', linewidths=2, edgecolors='r', alpha=.25))
	#g_Ax.scatter(triList, triList, triList)

def Show(xyzrange):
	plt.xlim(xyzrange[0])
	plt.ylim(xyzrange[1])
	global g_Ax
	g_Ax.set_zlim3d(xyzrange[2][0], xyzrange[2][1])
	#plt.zlim(xyzrange[2])
	plt.show()

 