#! /usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 30 23:35:12 2014
Project	:Python-Project
Version	:0.0.1
@author	:macrobull (http://github.com/macrobull)

"""
#blender  /home/macrobull/workspace/BlenderVis/scene.blend --python %f -f 0 -o /tmp/render_ -F PNG

import os
import numpy as np

CMD_VIEW = 'blender  /home/macrobull/workspace/BlenderVis/scene.blend --python %(OUTPUT)s -f 0 -o /tmp/render_ -F PNG'
OUTPUT = '/tmp/bv_gen.py'


class bvis():
	def __init__(self):
		self.CODE_MAIN = ''

	def _vars(self, *args):
		r = globals()
		r.update(self.__dict__)
		for d in args:
			r.update(d)
		return r

	def _render(self):
		self._genScript()
		print(os.popen(CMD_VIEW % globals()).read())

	def _genScript(self):
		fi = open('/home/macrobull/workspace/BlenderVis/template.py')
		code = fi.read() % self.__dict__
		fi.close()
		fo = open(OUTPUT, 'w')
		fo.write(code)
		fo.close()

	def plot(self, *args, **kwargs):
		print(args)

	def scatter(self, *args, **kwargs):
		kwargd = dict(
			colors = None, sizes = None,
			name = 'scatter'
			)
		kwargd.update(kwargs)
		if len(args) == 3:
			X, Y, Z = args


#		self.CODE_MAIN += 'scatter_mball_XYZ(%(X)r, %(Y)r, %(Z)r)' % self._vars(locals())
		self.CODE_MAIN += 'scatter_icoSphere_XYZ(%(X)r, %(Y)r, %(Z)r,\
			colors = %(colors)r, sizes = %(sizes)r,\
			name = %(name)r)\n' % self._vars(locals(), kwargd)




if __name__ == '__main__':

	from sklearn import datasets
	iris = datasets.load_iris()

	bv = bvis()
	x = iris.data[:, :3]
	x = x * 5
	y = iris.target
	for tar in range(3):
		x_s = x[np.where(y == tar)].T
#		print(x_s)
		bv.scatter(x_s[0], x_s[1], x_s[2], name = 'Iris_'+str(tar))

	bv._render()









