#!/usr/bin/env python

#
# Author: Steven Ludtke, 03/06/2009 (sludtke@bcm.edu)
# Copyright (c) 2000-2006 Baylor College of Medicine
#
# This software is issued under a joint BSD/GNU license. You may use the
# source code in this file under either license. However, note that the
# complete EMAN2 and SPARX software packages have some GPL dependencies,
# so you are responsible for compliance with the licenses of these packages
# if you opt to use BSD licensing. The warranty disclaimer below holds
# in either instance.
#
# This complete copyright notice must be included in any revised version of the
# source code. Additional authorship citations may be added, but existing
# author citations must be preserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  2111-1307 USA
#
#

# e2parallel.py Steven Ludtke
# This program implements, via various options, the parallelism system for EMAN2

from EMAN2 import *
from EMAN2PAR import *
from optparse import OptionParser
from math import *
import time
import os
import sys
import socket

debug=False
logid=None

def main():
	global debug,logid
	progname = os.path.basename(sys.argv[0])
	commandlist=("dcserver","dcclient","dckill","dckillclients","servmon","rerunall","killall","precache")
	usage = """%prog [options] <command> ...
	
This program implements much of EMAN2's coarse-grained parallelism mechanism. There are several flavors available via
different options in this program. The simplest, and easiest to use is probably the client/server Distriuted Computing system.

<command> is one of: dcserver, dcclient, dckill, dcrerunall, precache, killall, killclients, servmon

run e2parallel.py servmon to run a GUI server monitor. This MUST run on the same machine in the same directory as the server.

client-server DC system:
run e2parallel.py dcserver on the machine containing your data and project files
run e2parallel.py dcclient on as many other machines as possible, pointing at the server machine

"""

	parser = OptionParser(usage=usage,version=EMANVERSION)

	parser.add_option("--server",type="string",help="Specifies host of the server to connect to",default="localhost")
	parser.add_option("--port",type="int",help="Specifies server port, default is automatic assignment",default=-1)
	parser.add_option("--verbose",type="int",help="debugging level (0-9) default=0)",default=0)
#	parser.add_option("--cpus",type="int",help="Number of CPUs/Cores for the clients to use on the local machine")
#	parser.add_option("--idleonly",action="store_true",help="Will only use CPUs on the local machine when idle",default=False)
	
	(options, args) = parser.parse_args()
	if len(args)<1 or args[0] not in commandlist: parser.error("command required: "+str(commandlist))

	if args[0]=="dcserver" :
		rundcserver(options.port,options.verbose)
		
	elif args[0]=="dcclient" :
		rundcclient(options.server,options.port,options.verbose)
		
	elif args[0]=="dckill" :
		killdcserver(options.server,options.port,options.verbose)
	
	elif args[0]=="dckillclients" :
		killdcclients(options.server,options.port,options.verbose)

	elif args[0]=="precache" :
		precache(args[1:])

	elif args[0]=="rerunall":
		rerunall()

	elif args[0]=="killall":
		killall()

	elif args[0]=="servmon" :
		runservmon()
		
def rundcserver(port,verbose):
	"""Launches a DCServer. If port is <1 or None, will autodetermine. Does not return."""
	import EMAN2db
	# The following was causing issues with the multithreaded parallelism server. Seems like we need to insure the server and the customer
	# are running on the same physical computer !!!
#	EMAN2db.BDB_CACHE_DISABLE=1	# this diables caching on the server so the customer knows it can freely write to local database files
	server=runEMDCServer(port,verbose)			# never returns

def killdcclients(server,port,verbose):
	import EMAN2db
	server=runEMDCServer(port,verbose,True)			# never returns


def rundcclient(host,port,verbose):
	"""Starts a DC client running, runs forever"""
#	while (1):
	client=EMDCTaskClient(host,port,verbose)
	client.run(onejob=False)
#	print "New client (%d alloced)"%EMData.totalalloc

def precache(files):
	"""Adds a list of filenames to the precaching queue. Precaching will occur before jobs are started."""
	q=EMTaskQueue()
	print len(files)," files queued for precaching" 
	q.precache["files"]=files
	

def rerunall():
	"""Requeues all active (incomplete) tasks"""
	q=EMTaskQueue()
	e=q.active.keys()
	e=[i for i in e if isinstance(i,int) and q.active[i]!=None]
	
	for i in e: q.task_rerun(i)
	
	print "Requeued %d tasks"%len(e)

def killall():
	"""Requeues all active (incomplete) tasks"""
	q=EMTaskQueue()
	e=q.active.keys()
	e=[i for i in e if isinstance(i,int) and q.active[i]!=None]
	
	for i in e: q.task_aborted(i)

	print "Killed %d tasks"%len(e)

def killdcserver(server,port,verbose):
	EMDCsendonecom(server,port,"QUIT")


# We import Qt even if we don't need it
try:
	from PyQt4 import QtCore, QtGui
	from PyQt4.QtCore import Qt
except:
	class dummy:
		"A dummy class for use when Qt not installed"
		def __init__(self,quiet=False):
			if not quiet :
				print "ERROR: Qt4 could not be imported, check your PyQt installation"
				import traceback
				traceback.print_exc()

	QtGui=dummy(True)
	QtGui.QWidget=dummy
	QtGui.QMainWindow=dummy
	QtCore=dummy(True)
	QtCore.QAbstractTableModel=dummy
	
def runservmon():
	import EMAN2db
	# we changed the meaning of the variable to disable writing to cache altogether, pap 9-01
	EMAN2db.BDB_CACHE_DISABLE=1

	queue=EMAN2db.EMTaskQueue(".",ro=True)

#	activedata=TaskData(queue.active)
#	completedata=TaskData(queue.complete)

	app = QtGui.QApplication([])
	window = GUIservmon()
	
#	ui.tableView.setModel(data)

	window.show()
	window.set_data(queue)
	
	app.exec_()
	
class GUIservmon(QtGui.QMainWindow):
	"""A DC server monitor GUI"""
	def __init__(self):
		QtGui.QWidget.__init__(self,None)

		self.cw=QtGui.QWidget()
		self.setCentralWidget(self.cw)
		self.vbl=QtGui.QVBoxLayout(self.cw)
		
		self.tabs = QtGui.QTabWidget()
		self.vbl.addWidget(self.tabs)
		self.tabs.setSizePolicy(QtGui.QSizePolicy.Preferred,QtGui.QSizePolicy.Expanding)
	
		self.activetab=QtGui.QWidget()
		self.vblat=QtGui.QVBoxLayout(self.activetab)
		self.actview=QtGui.QTableView()
		self.vblat.addWidget(self.actview)
		self.tabs.addTab(self.activetab,"Active")
		
		self.donetab=QtGui.QWidget()
		self.vbldt=QtGui.QVBoxLayout(self.donetab)
		self.doneview=QtGui.QTableView()
		self.vbldt.addWidget(self.doneview)
		self.tabs.addTab(self.donetab,"Complete")
		
		self.clienttab=QtGui.QWidget()
		self.vblct=QtGui.QVBoxLayout(self.clienttab)
		self.clientview=QtGui.QTableView()
		self.vblct.addWidget(self.clientview)
		self.tabs.addTab(self.clienttab,"Clients")
		
		self.startTimer(10000)
		
	def timerEvent(self,event):
		if self.tabs.currentIndex()==0 :
			self.actmodel.load()
			self.actview.setModel(None) 				# suboptimal, but a hack for now
			self.actview.setModel(self.actmodel)
			self.actview.resizeColumnsToContents()
		elif self.tabs.currentIndex()==1 :
			self.donemodel.load()
			self.doneview.setModel(None)
			self.doneview.setModel(self.donemodel)
			self.doneview.resizeColumnsToContents()
		
	def set_data(self,queue):
		"""This takes an EMTaskQueue object and displays it"""
		
		self.actmodel=TaskData(queue.active)
		self.actview.setModel(self.actmodel)
		self.donemodel=TaskData(queue.complete)
		self.doneview.setModel(self.donemodel)
		
		self.actmodel.load()
		self.donemodel.load()
		
#		self.vbl.addWidget(self.tabs)

class TaskData(QtCore.QAbstractTableModel):
	def __init__(self,target):
		QtCore.QAbstractTableModel.__init__(self)
		self.target=target
		self.nrows=0
		self.rows=[]

	def load(self):
		"""Updates the cached display from source"""
		keys=self.target.keys()
		keys.sort()
		keys=keys[:-2]
		self.nrows=len(keys)
		self.rows=[]
		for r in range(self.nrows):
			task=self.target[keys[r]]
			self.rows.append([self.col(task,i) for i in range(8)])
		
	def col(self,task,n):
		"""gets a single table entry"""
		if not isinstance(task,EMTask) : 
			print loc.row(),keys[loc.row()]
			print self.target[keys[loc.row()]]
			return QtCore.QVariant("???")
			
		if n==0 : ret=task.taskid
		elif n==1: 
			try: 
				if task.progtime==None or task.progtime[1]==-1 : ret = "-"
				elif task.progtime[1]==0 : ret= "#"
				elif task.progtime[1]<100 : ret= "#"*(1+task.progtime[1]/5)
				else : ret = "DONE"
				if task.progtime[0]-time.time()>300 : ret+=" ?"
			except: ret="?"
		elif n==2 : ret=task.command
		elif n==3 : ret=local_datetime(task.queuetime)
		elif n==4 : ret=local_datetime(task.starttime)
		elif n==5 : 
			try: ret=difftime(task.endtime-task.starttime)
			except: ret = "incomplete"
		elif n==6 : 
			ret=task.exechost
			if ret==None : ret=task.clientid
		elif n==7 :
			try:
				if   task.command=="e2classaverage.py" : ret= "Class %d"%task.class_idx
				elif task.command=="e2simmx.py" : ret= "Range: %d - %d : %d - %d"%(task.data["references"][2],task.data["references"][3],task.data["particles"][2],task.data["particles"][3])
				elif task.command=="e2project3d.py" : ret="Proj: %d - %d"%(min(task.data["indices"]),max(task.data["indices"]))
				else : ret = task.command
			except : ret = str(task)
			
		return QtCore.QVariant(str(ret))

	def data(self,loc,role):
		if not loc.isValid() or role != QtCore.Qt.DisplayRole : return QtCore.QVariant()
		try : return self.rows[loc.row()][loc.column()]
		except : return QtCore.QVariant("---")
		
	def rowCount(self,parent):
		if parent.isValid() : return 0
		return self.nrows

	def columnCount(self,parent):
		if parent.isValid() : return 0
		return 8


if __name__== "__main__":
	main()
	

	
