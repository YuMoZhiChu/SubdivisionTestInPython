# -*- coding: utf-8 -*-
# yumo

from mystruct import *

def LoopSubdivide(
	nLevels:int, # 曲面细分等级
	# nIndices:int, # 下标个数
	vertexIndices: list, # 下标数组
	# nVertices: int, # 顶点个数
	pointList: list # 顶点数组
	):
	vertices = []
	for point in pointList:
		vertices.append(
			SDVertex(Point3(*point))
			)

	nFace = int(len(vertexIndices) / 3)
	faces = []
	for i in range(nFace):
		faces.append(SDFace())

	vertexIndicesPointTo = 0
	for i in range(nFace):
		# 去除第i个面
		f = faces[i]
		for j in range(3):
			# 这是第 vertexIndecisPointTo 个 三角形 的 第 j 个点
			v = vertices[vertexIndices[vertexIndicesPointTo+j]]
			# 建立双边关系
			f.v[j] = v
			v.startFace = f
		vertexIndicesPointTo += 3

	edges = []
	for i in range(nFace):
		# f 是第i个面
		f = faces[i]
		# print(f)
		for edgeNum in range(3):
			# 这是第 edgeNum 条边
			# v0 - v1 构筑一条边
			v0 = edgeNum
			v1 = NEXT(edgeNum)
			e = SDEdge(f.v[v0], f.v[v1])
			findIndex = -1
			for edges_k in range(len(edges)):
				if e == edges[edges_k]:
					findIndex = edges_k
					break
			if findIndex == -1:			
				# 这是一条新的边
				e.f[0] = f # 它的0 对应 
				e.f0edgeNum = edgeNum # 表明 它是f0面的第 edgeNum 条边, 这边先记录下
				edges.append(e) # 加入新边
			else:
				# 如果这条边已经记录
				find_e = edges[findIndex]
				# print(find_e.f0edgeNum, f)
				# 这里不写注释了, 目的就是通过边, 建立面与面的关系
				find_e.f[0].f[find_e.f0edgeNum] = f
				f.f[edgeNum] = find_e.f[0]
				del edges[findIndex] # 把这条线排除

	# print("#### faces: ", faces)
	# print("#### vertices: ", vertices)
