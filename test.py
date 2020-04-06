from mystruct import *

a = Point3(1,1,1)
b = Point3(2,2,2)
c = Point3(3,3,3)

V0 = SDVertex(a)
v1 = SDVertex(b)
V2 = SDVertex(c)

e = SDEdge(V0, v1)
e2 = SDEdge(v1, V0)
e3 = SDEdge(V0, V2)

print(e == e2)


l = [e, e3]

print(e2 in l)

print(l)

del l[1]
print(l)

