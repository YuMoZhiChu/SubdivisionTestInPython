# -*- coding: utf-8 -*-
# yumo

# import weakref # 按照原则来说, 应该用弱引用, 但这只是个demo


# 上下一个点的简写
NEXT = lambda i: (i+1)%3
PREV = lambda i: (i+1)%3

class Point3(object):
	"""xyz的顶点格式存储"""
	def __init__(self, _x=0, _y=0, _z=0):
		self.x = _x
		self.y = _y
		self.z = _z

	def __eq__(self, other):
		return self.x == other.x and \
		self.y == other.y and \
		self.z == other.z

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

	def __eq__(self, other):
		return self.p == other.p and \
		self.startFace == other.startFace and \
		self.child == other.child and \
		self.regular == other.regular and\
		self.boundary == other.boundary

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

class SDFace(object):
	"""面结构"""
	def __init__(self):
		# 3个顶点
		self.v = [None, None, None]
		# 3个面
		self.f = [None, None, None]
		# 4个子面
		self.children = [None, None, None, None]

	def vnum(vert:SDVertex) -> int:
		"""查是第几个顶点"""
		for i in range(3):
			v = self.v[i]
			if v == vert:
				return i
		print("########### 这个点不存在于 面中", vert, self)
		return -1

	def nextFace(vert:SDVertex):
		return self.f[self.vnum(vert)]

	def prevFace(vert:SDVertex):
		return self.f[PREV(self.vnum(vert))]

	def nextVert(vert:SDVertex):
		return self.v[NEXT(self.vnum(vert))]

	def prevVert(vert:SDVertex):
		return self.v[PREV(self.vnum(vert))]
