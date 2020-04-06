# -*- coding: utf-8 -*-
# yumo
from mystruct import *
from drawhelp import *
from subdivision import *

PyramidPosList = [
	[0.0, 0.0, 0.0],
	[2.0, 0.0, 0.0],
	[2.0, 2.0, 0.0],
	[0.0, 2.0, 0.0],
	[1.0, 1.0, 2.0]
]

PyramidIndexList = [
	[4, 0, 1],
	[4, 1, 2],
	[4, 2, 3],
	[4, 3, 0],
	[0, 2, 1],
	[0, 3, 2]
]

# Pos and Index To TriList
def PosAndIndex2TriList(posList, indexList):
	triList = []
	for indexTuple in indexList:
		a, b, c = indexTuple
		posA = posList[a]
		posB = posList[b]
		posC = posList[c]
		triList.append([posA, posB, posC])
	return triList

def GetPyramidTriList():
	global PyramidPosList, PyramidIndexList
	return PosAndIndex2TriList(PyramidPosList, PyramidIndexList)

def GetPyramidXYZRange():
	return [
	[-0.5, 2.5],
	[-0.5, 2.5],
	[-0.5, 2.5]
	]

def GetPyramidSubdivideParam():
	global PyramidPosList, PyramidIndexList
	indexList = []
	for indexTuple in PyramidIndexList:
		a, b, c = indexTuple
		indexList.append(a)
		indexList.append(b)
		indexList.append(c)
	return indexList, PyramidPosList

if __name__ == '__main__':
	InitSystem()
	LoopSubdivide(0, *GetPyramidSubdivideParam())
	
	DrawTriList(GetPyramidTriList())
	Show(GetPyramidXYZRange())


