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

	# 1. 计算顶点是外部点还是内部点
	# 2. 计算顶点价
	for v in vertices:
		f = v.startFace
		while f and f != v.startFace:
			f = f.nextFace(v)
		v.boundary = (f == None)
		if not v.boundary and v.valence() <= 6:
			v.regular = True
		elif v.boundary and v.valence() <= 4:
			v.regular = True
		else:
			v.regular = False
	# print("#### vertices: ", vertices)

	# 开始阶段性循环
	for i in range(nLevels):
		newVertices = []
		newFaces = []

		# 创建下一级的空间
		for vertex in vertices:
			vertex.child = SDVertex(Point3())
			vertex.child.boundary = vertex.boundary
			vertex.child.regular = vertex.regular
			newVertices.append(vertex.child)
		for face in faces:
			# 把一个面分为4个子面
			for k in range(4):
				face.children[k] = SDFace()
				newFaces.append(face.children[k])

		# even 点, 更新他们的位置
		for vertex in vertices:
			if not vertex.boundary:
				if vertex.regular:
					vertex.child.p = weightOneRing(vertex, 1.0/16.0)
				else:
					vertex.child.p = weightOneRing(vertex, beta(vertex.valence()))
			else:
				vertex.child.p = weightBoundary(vertex, 1.0/8.0)

		# odd 点, 增加的新的点
		edgeVerts = [] # 这个节点比较难搞, 因为不能做key
		for face in faces:
			for k in range(3):
				# 每一条边, 生成一个 odd 点
				edge = SDEdge(face.v[k], face.v[NEXT(k)])
				vertex = None
				for edgeKey,vertexValue in edgeVerts:
					if edge == edgeKey:
						vertex = vertexValue
						break
				if not vertex:
					vertex = SDVertex(Point3())
					newVertices.append(vertex)
					# 按照这种算法, 新的 odd 点的 顶点价 都是 6
					vertex.regular = True
					# 边界点的判断, 只需要知道, 当前face 对该点的一面，是否为空
					vertex.boundary = (face.f[k] == None)
					# startFace 是 3个 odd 点 共同生成的 面, 也就是位于中心的, 最后一个面
					vertex.startFace = face.children[3]

					# 计算位置
					if vertex.boundary:
						# 如果是边界点, 直接取中点
						vertex.p = 0.5 * edge.v[0].p
						vertex.p += 0.5 * edge.v[1].p
					else:
						vertex.p = (3.0/8.0) * edge.v[0].p
						vertex.p += (3.0/8.0) * edge.v[1].p
						# 加上对面顶点的因素
						vertex.p += (1.0/8.0) * face.otherVert(edge.v[0], edge.v[1]).p
						vertex.p += (1.0/8.0) * face.f[k].otherVert(edge.v[0], edge.v[1]).p

					# 表示这条边已经处理过, 生成了新的顶点
					edgeVerts.append([edge, vertex])

		# 更新新建的点的 三角形关系和点面关系
		
		# 处理 even 点的点面关系
		for vertex in vertices:
			vertNum = vertex.startFace.vnum(vertex)
			vertex.child.startFace = vertex.startFace.children[vertNum]

		# 更新 面面关系
		for face in faces:
			for j in range(3):
				face.children[3].f[j] = face.children[NEXT(j)]
				face.children[j].f[NEXT(j)] = face.children[3]

				# 更新相邻父三角形
				f2 = face.f[j]
				face.children[j].f[j] = f2.children[f2.vnum(face.v[j])] if f2 else None
				f2 = face.f[PREV(j)]
				face.children[j].f[PREV(j)] = f2.children[f2.vnum(face.v[j])] if f2 else None

		# 更新 子面 链接到 新生成点的关系
		for face in faces:
			for j in range(3):
				# even 点
				face.children[j].v[j] = face.v[j].child
				# odd 点
				vertex = None
				edge = SDEdge(face.v[j], face.v[NEXT(j)])
				for edgeKey,vertexValue in edgeVerts:
					if edge == edgeKey:
						vertex = vertexValue
						break
				if not vertex:
					print("######### 子面 链接到 新生成点的关系 出错")
				face.children[j].v[NEXT(j)] = vertex
				face.children[NEXT(j)].v[j] = vertex
				face.children[3].v[j] = vertex

		# 迭代更新
		vertices = newVertices
		faces = newFaces

	# print("#### faces: ", faces)
	# print("#### vertices: ", vertices)
	
	# 低纬度的曲面细分效果, 不使用求极限效果会更好
	if nLevels <= 2:
		return [face.getTriPos() for face in faces]
	

	# 为了不让顶点无限的细分下去, 这里给出了一个极限的规则
	pLimit = []
	for vertex in vertices:
		p_point = None
		if vertex.boundary:
			p_point = weightBoundary(vertex, 1.0/5.0)
		else:
			p_point = weightOneRing(vertex, loopGamma(vertex.valence()))
		pLimit.append(p_point)

	for index in range(len(vertices)):
		vertices[index].p = pLimit[index]

	return [face.getTriPos() for face in faces]
	