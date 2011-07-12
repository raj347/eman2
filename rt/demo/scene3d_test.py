#!/usr/bin/env python

from PyQt4 import QtCore, QtGui, QtOpenGL
from emscene3d import EMScene3D, EMInspector3D, EMInspectorControlShape
from emshapeitem3d import *

from EMAN2 import *

class GLdemo(QtGui.QWidget):
	def __init__(self):
		QtGui.QWidget.__init__(self)
		self.widget = EMScene3D()
		#self.widget.camera.useprespective(50, 0.5)
#		self.cube1 = glCube(50.0)
		self.cube1 = EMCube(50.0)
		self.widget.addChild(self.cube1)    # Something to Render something..... an EMItem3D
		#self.widget.activatenode(cube1)
#		self.cube2 = glCube(50.0)
		self.cube2 = EMCube(50.0)
		self.widget.addChild(self.cube2)
		#self.widget.activatenode(cube2)
		
		self.sphere = EMSphere(50.0)
		self.widget.addChild(self.sphere)
		
		self.cylinder = EMCylinder(50, 300)
		self.widget.addChild(self.cylinder)

		self.inspector = EMInspector3D(self.widget)
		self.widget.setInspector(self.inspector)
		
		rootnode = self.inspector.addTreeNode("root node", self.widget)
		self.inspector.addTreeNode("cube1", self.cube1, rootnode)
		self.inspector.addTreeNode("cube2", self.cube2, rootnode)
		self.inspector.addTreeNode("sphere", self.sphere, rootnode)
		self.inspector.addTreeNode("cylinder", self.cylinder, rootnode)
		
		# QT stuff to display the widget
		vbox = QtGui.QVBoxLayout()
		vbox.addWidget(self.widget)
		self.setLayout(vbox)
		self.setGeometry(300, 300, 600, 600)
		self.setWindowTitle('BCM EM Viewer')
	
	def show_inspector(self):
		self.inspector.show()
		
if __name__ == "__main__":
	import sys
	app = QtGui.QApplication(sys.argv)
	window = GLdemo()
	window.show()
	window.show_inspector()
	app.exec_()