# -*- coding: utf-8 -*-
# yumo

# import weakref # 按照原则来说, 应该用弱引用, 但这只是个demo


# 上下一个点的简写
NEXT = lambda i: (i+1)%3
PREV = lambda i: (i+2)%3

class Point3(object):
	"""xyz的顶点格式存储"""
	def __init__(self, _x=0, _y=0, _z=0):
		self.x = _x
		self.y = _y
		self.z = _z

	def __repr__(self):
		return "Point3 at %#x, (%f, %f, %f)"%(id(self), self.x, self.y, self.z)

	def __eq__(self, other):
		return self.x == other.x and \
		self.y == other.y and \
		self.z == other.z

	def __lt__(self, other):
		if self.x != other.x:
			return self.x < other.x
		if self.y != other.y:
			return self.y < other.y
		if self.z != other.z:
			return self.z < other.z
		return False

	def __mul__(self, single):
		return Point3(single * self.x, single * self.y, single * self.z)

	def __rmul__(self, single):
		return self * single

	def __iadd__(self, other):
		return Point3(self.x + other.x, self.y + other.y, self.z + other.z)

# a = Point3(0, -1, 2)
# b = Point3(0, 1, 3)
# print(min(a, b), max(a,b))
# print(a*3)
# a += b
# print(a)

class SDVertex(object):
	"""点结构"""
	def __init__(self, _p:Point3):
		# 自身点
		self.p = _p

		# 指向起点面
		self.startFace = None
		# 指向下一级别的子顶点
		self.child = None
		# 是否是平凡点
		self.regular = False
		# 是否是边界点
		self.boundary = False

	def __repr__(self):
		return "\nSDVertex at %#x, (%f, %f, %f) boundary:%d regular:%d valence:%d\n"%\
		(id(self), self.p.x, self.p.y, self.p.z, self.boundary, self.regular, self.valence())

	def __eq__(self, other):
		return self.p == other.p and \
		self.startFace == other.startFace and \
		self.child == other.child and \
		self.regular == other.regular and\
		self.boundary == other.boundary

	def __lt__(self, other):
		return Point3.__lt__(self.p, other.p)

	def valence(self) -> int:
		"""返回顶点价值"""
		f = self.startFace
		if not self.boundary:
			# 内部计算顶点价值, 每进过一个面 +1
			nf = 1
			f = f.nextFace(self)
			while f != self.startFace:
				nf += 1
				f = f.nextFace(self)
			return nf
		else:
			nf = 1
			f = f.nextFace(self)
			while f != None:
				nf += 1
			f = startFace
			f = f.prevFace(self)
			while f != None:
				nf += 1
			return nf + 1

	def oneRing(self) -> list:
		"""返回周围一圈的顶点值"""
		if not self.boundary:
			result = []
			f = self.startFace
			result.append(f.nextVert(self).p)
			f = f.nextFace(self)
			while f != self.startFace:
				result.append(f.nextVert(self).p)
				f = f.nextFace(self)
			return result
		else:
			result = []
			f = self.startFace
			f2 = f.nextFace(self)
			while f2 != None:
				f = f2
				f2 = f.nextFace(self)
			result.append(f.nextVert(self).p)
			# 往回数
			result.append(f.prevVert(self).p)
			f = f.prevFace(self)
			while f != None:
				result.append(f.prevVert(self).p)
				f = f.prevFace(self)
			return result

# a = Point3(0, -1, 2)
# b = Point3(0, 1, 3)
# A = SDVertex(a)
# B = SDVertex(b)
# print(min(A, B), max(A, B))

class SDFace(object):
	"""面结构"""
	def __init__(self):
		# 3个顶点
		self.v = [None, None, None]
		# 3个面
		self.f = [None, None, None]
		# 4个子面
		self.children = [None, None, None, None]

	def __repr__(self):
		return "\nSDFace at %#x, (%s, %s, %s) \n## f[0] id: %#x, f[1] id: %#x, f[2] id: %#x \n"%\
		(id(self), self.v[0], self.v[1], self.v[2], id(self.f[0]), id(self.f[1]), id(self.f[2]))

	def vnum(self, vert:SDVertex) -> int:
		"""查是第几个顶点"""
		for i in range(3):
			v = self.v[i]
			if v == vert:
				return i
		print("########### 这个点不存在于 面中", vert, self)
		return -1

	def nextFace(self, vert:SDVertex):
		return self.f[self.vnum(vert)]

	def prevFace(self, vert:SDVertex):
		return self.f[PREV(self.vnum(vert))]

	def nextVert(self, vert:SDVertex):
		return self.v[NEXT(self.vnum(vert))]

	def prevVert(self, vert:SDVertex):
		return self.v[PREV(self.vnum(vert))]

	def otherVert(self, v0:SDVertex, v1:SDVertex):
		for i in range(3):
			if self.v[i] != v0 and self.v[i] != v1:
				return self.v[i]
		print('########### 面调用 otherVert 出错')

	def getTriPos(self):
		return [
			[self.v[0].p.x, self.v[0].p.y, self.v[0].p.z],
			[self.v[1].p.x, self.v[1].p.y, self.v[1].p.z],
			[self.v[2].p.x, self.v[2].p.y, self.v[2].p.z],
		]

class SDEdge(object):
	"""边结构"""
	def __init__(self, v0:SDVertex, v1:SDVertex):
		_v0 = min(v0, v1)
		_v1 = max(v0, v1)
		self.v = [_v0, _v1]
		self.f = [None, None]
		self.f0edgeNum = -1 # 这条边是三角形的 第几条边

	def __lt__(self, other):
		if self.v[0] == other.v[0]:
			return self.v[1] < other.v[1]
		return self.v[0] < other.v[0]

	def __eq__(self, other):
		return self.v[0] == other.v[0] and self.v[1] == other.v[1]

def weightOneRing(vert:SDVertex, beta:float):
	valence = vert.valence()
	result = vert.oneRing()
	p = vert.p * (1 - valence * beta)
	for i in range(valence):
		p += result[i]*beta
	return p

def weightBoundary(vert:SDVertex, beta:float):
	valence = vert.valence()
	result = vert.oneRing()
	p = vert.p * (1 - 2 * beta)
	p += beta * result[0]
	p += beta * result[-1]
	return p 

def beta(valence:int):
	if valence == 3:
		return 3.0 / 16.0
	else:
		return 3.0 / 8.0 * valence

def loopGamma(valence:int):
	return 1.0 / (valence + 3.0 / (8.0 * beta(valence)));
