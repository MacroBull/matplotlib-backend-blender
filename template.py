#! /usr/bin/python3
# -*- coding: utf-8 -*-
"""
Generated script for rendering.

"""


from math import *
import numpy as np
from numpy import *
import matplotlib as mpl

import bpy
import bgl, blf, mathutils
from bpy import ops, props, types, context, utils
from bpy import data as D
from bpy import context as C


ALPHA_DEFAULT = 0.7
COLOR_CYCLE = [eval(s.replace('#','0x')) for s in mpl.rcParams['axes.color_cycle']]
COLOR_CYCLE = [( (i&(0xff<<16))/(1<<24), (i&(0xff<<8))/(1<<16), (i&0xff)/(1<<8), ALPHA_DEFAULT) for i in COLOR_CYCLE]
COLOR_CYCLE_IDX = 0




def scatter_mball_XYZ(X, Y, Z):
	for x, y, z in np.array([X.flatten(), Y.flatten(), Z.flatten()]).T:
		ops.object.metaball_add(type = 'BALL', location = (x, y, z))

def scatter_icoSphere_XYZ(X, Y, Z,
	colors = None, sizes = None,
	name = 'scatter'):

	X, Y, Z = X.flatten(), Y.flatten(), Z.flatten()
	assert len(X) == len(Y) == len(Z)

	SUBDIV = log(1e4/len(X)+1)
	SIZE = np.linalg.norm([X.max()-X.min(), Y.max()-Y.min(), Z.max()-Z.min()]) / len(X)**(1/2.0) / 4
	print(SUBDIV, SIZE, np.linalg.norm([X.max()-X.min(), Y.max()-Y.min(), Z.max()-Z.min()]))

	global COLOR_CYCLE_IDX
	if colors is None: colors = np.repeat([COLOR_CYCLE[COLOR_CYCLE_IDX]], len(X), axis=0)
	assert len(X) == len(colors)
	COLOR_CYCLE_IDX += 1

	if sizes is None: sizes = np.ones(X.size)*SIZE
	assert len(X) == len(sizes)

	ops.mesh.primitive_ico_sphere_add(subdivisions = 3, size = SIZE)
	obj = C.object
	mesh = obj.data
	mesh.name = name + '_iconSphere'
	ops.object.delete(use_global=False)
	mat = bpy.data.materials.new(name)
	mat.use_object_color = True
	mesh.materials.append(mat)


	len_c = len(colors)
	for i, (x, y, z) in enumerate(np.array([X, Y, Z]).T):
		obj = D.objects.new(name, mesh)
		obj.location = (x, y, z)
		obj.color = colors[i]
#		obj.size = sizes[i]

		C.scene.objects.link(obj)

%(CODE_MAIN)s

#bpy.ops.curve.smooth()
#bpy.ops.curve.smooth_radius()
#bpy.ops.curve.vertex_add(location = (0,0,0))
#bpy.ops.mesh.beautify_fill()
#bpy.ops.mesh.primitive_circle_add()
#bpy.ops.mesh.primitive_cone_add()
#bpy.ops.mesh.primitive_cube_add()
#bpy.ops.mesh.primitive_grid_add()

