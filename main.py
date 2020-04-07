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
	[1.0, 1.0, 2.0],
]

PyramidIndexList = [
	[4, 0, 1],
	[4, 1, 2],
	[4, 2, 3],
	[4, 3, 0],
	[0, 2, 1],
	[0, 3, 2]
]

CubePosList = [
	[0.0, 0.0, 0.0],
	[2.0, 0.0, 0.0],
	[2.0, 2.0, 0.0],
	[0.0, 2.0, 0.0],
	[0.0, 0.0, 2.0],
	[2.0, 0.0, 2.0],
	[2.0, 2.0, 2.0],
	[0.0, 2.0, 2.0],
]

CubeIndexList = [
	[0, 1, 2],
	[0, 2, 3],
	[5, 6, 2],
	[5, 2, 1],
	[6, 3, 2],
	[6, 7, 3],
	[7, 0, 3],
	[7, 4, 0],
	[4, 1, 0],
	[4, 5, 1],
	[4, 7, 6],
	[4, 6, 5],
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

def GetCubeTriList():
	global CubePosList, CubeIndexList
	return PosAndIndex2TriList(CubePosList, CubeIndexList)

def GetXYZRange():
	return [
	[-0.5, 2.5],
	[-0.5, 2.5],
	[-0.5, 2.5]
	]

def GetSubdivideParam(posList, indexList):
	resultList = []
	for indexTuple in indexList:
		a, b, c = indexTuple
		resultList.append(a)
		resultList.append(b)
		resultList.append(c)
	return resultList, posList

if __name__ == '__main__':
	InitSystem()
	#result = LoopSubdivide(3, *GetSubdivideParam(PyramidPosList, PyramidIndexList))
	#DrawTriList(result)
	
	result = LoopSubdivide(5, *GetSubdivideParam(CubePosList, CubeIndexList))
	DrawTriList(result)

	#DrawTriList(GetCubeTriList())
	#DrawTriList(GetPyramidTriList())
	Show(GetXYZRange())


