#!/usr/bin/env python

#
# Author: Jesus Galaz, 04/28/2012; last update 05/March/2013
# Copyright (c) 2011 Baylor College of Medicine
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

import os
from EMAN2 import *
from time import time
		 
import matplotlib
matplotlib.use('Agg')
		 
import matplotlib.pyplot as plt
import pylab
from pylab import *

import sys
import numpy		 
		 
def main():
	
	progname = os.path.basename(sys.argv[0])
	usage = """Tests cpu vs gpu speed on subtomogram alignment."""
			
	parser = EMArgumentParser(usage=usage,version=EMANVERSION)
	
	parser.add_argument("--cpu", action='store_true', help="Will test SPT alignment using CPU.",default=False)
	parser.add_argument("--gpu", action='store_true', help="Will test SPT alignment using GPU.",default=False)
	
	parser.add_argument("--test", action='store_true', help="Will run a quick tests using a few box sizes.",default=False)
	parser.add_argument("--medium", action='store_true', help="Will test boxsizes in multiples of 10 between 10 and 240.",default=False)
	parser.add_argument("--extensive", action='store_true', help="Will test EVERY box size between 12 and 256.",default=False)
	
	parser.add_argument("--ID", type=str, help="Tag files generated on a particular computer.",default='')
	parser.add_argument("--coarsestep", type=int, help="Step size for coarse alignment.",default=30)
	parser.add_argument("--finestep", type=int, help="Step size for fine alignment.",default=15)
	
	parser.add_argument("--ppid", type=int, help="Set the PID of the parent process, used for cross platform PPID",default=-1)
	parser.add_argument("--verbose", "-v", dest="verbose", action="store", metavar="n",type=int, default=0, help="verbose level [0-9], higner number means higher level of verboseness")
	parser.add_argument("--path",type=str,default=None,help="Directory to store results in. The default is a numbered series of directories containing the prefix 'sptsimjob'; for example, sptsimjob_02 will be the directory by default if 'sptsimjob_01' already exists.")
	parser.add_argument("--noplot", action='store_true', help="To run jobs on a cluster or other interfaces that don't support plotting, turn this option on.",default=False)
	
	parser.add_argument("--plotonly",type=str, help="""If you already have the time variation with boxsize (for a particular cpu or gpu) in a text file in rows of 'boxsize,time', 
												provide the txt file(s) separated by commas --plotonly=file1.txt,file2.txt,file3.txt etc...""", default=None)
	parser.add_argument("--singleplot",type=str, help="Provide the name of the .png file to plot all cpus and/or gpus provided through --plotonly, in a single .png file.", default='')
	
	parser.add_argument("--plotminima",action="store_true", help="Plot all cpus and/or gpus provided through --plotonly, in a single .png file.", default=False)
	parser.add_argument("--colorlessplot",action="store_true", help="Plot all cpus and/or gpus provided through --plotonly, in a single .png file.", default=False)
	
	global options
	
	(options, args) = parser.parse_args()
	
	
	#print "options are", options
	
	logger = E2init(sys.argv, options.ppid)
	
	'''
	Make the directory where to create the database where the results will be stored
	'''
	
	#if options.path and ("/" in options.path or "#" in options.path) :
	#	print "Path specifier should be the name of a subdirectory to use in the current directory. Neither '/' or '#' can be included. "
	#	sys.exit(1)
		
	#if options.path and options.path[:4].lower()!="bdb:": 
	#	options.path="bdb:"+options.path

	#if not options.path: 
	#	#options.path="bdb:"+numbered_path("sptavsa",True)
	#	options.path = "sptsim_01"
	
	
	if options.path and ("/" in options.path or "#" in options.path) :
		print "Path specifier should be the name of a subdirectory to use in the current directory. Neither '/' or '#' can be included. "
		sys.exit(1)

	if not options.path: 
		#options.path="bdb:"+numbered_path("sptavsa",True)
		options.path = "sptCudaTest_01"
	
	files=os.listdir(os.getcwd())
	print "right before while loop"
	while options.path in files:
		print "in while loop, options.path is", options.path
		#path = options.path
		if '_' not in options.path:
			print "I will add the number"
			options.path = options.path + '_00'
		else:
			jobtag=''
			components=options.path.split('_')
			if components[-1].isdigit():
				components[-1] = str(int(components[-1])+1).zfill(2)
			else:
				components.append('00')
						
			options.path = '_'.join(components)
			#options.path = path
			print "The new options.path is", options.path

	if options.path not in files:
		
		print "I will make the path", options.path
		os.system('mkdir ' + options.path)
	
	
	'''
	If options.plotonly is off (no files provided) you actually have to measure alignment time....
	'''
	if not options.plotonly:
		retcpu=[]
		retgpu=[]
		if options.ID:
			options.ID = options.ID + '_'
		
		'''
		Compute CPU alignment times and plot them
		'''
		if options.cpu:
			corg = 'CPU'

			retcpu=doit(corg,options)

			for i in range(len(retcpu)):
				step = retcpu[i][0]
				name = options.path + "/" + options.ID + "CS"+ str(step).zfill(2)  + "_FS" + str( float(step)/2.0 ).zfill(4) + '_CPU.png'
				cnums = numpy.array(retcpu[i][-1])
				sizes = numpy.array(retcpu[i][1])
				print "\n$$$$$$$\nThe step is", step
				print "\n\n"
				print "for which sizes to plot are", sizes
				print "and cnums to plot are", cnums
				print "\n"
				plotter(sizes,cnums,name,step,step/2)				
				plt.savefig(options.path + '/' + name)
				plt.clf()
				
				if options.plotminima:
					ret=minima(sizes,cnums)
					sizesmin=ret[0]
					cnumsmin=ret[1]
					namemin=name.replace('.png','_MIN.png')
					plotter(sizesmin,cnumsmin,namemin,step,step/2)
					plt.savefig(options.path + '/' + namemin)
					plt.clf()
						
		'''
		Compute GPU alignment times and plot them
		'''
		if options.gpu:
			corg = 'GPU'

			retgpu=doit(corg,options)

			for i in range(len(retgpu)):
				step = retgpu[i][0]
				name = options.path + "/" + options.ID + "CS"+str(step).zfill(2) + "_FS"+str( float(step)/2 ).zfill(4) + '_GPU.png'
				gnums = numpy.array(retgpu[i][-1])
				sizes = numpy.array(retgpu[i][1])
				print "\n$$$$$$$\nThe step is", step
				print "\n\n"
				print "for which sizes to plot are", sizes
				print "and gnums to plot are", gnums
				print '\n'
				plotter(sizes,gnums,name,step,step/2)
				plt.savefig(options.path + '/' + name)
				plt.clf()
	
				if options.plotminima:
					ret=minima(sizes,gnums)
					sizesmin=ret[0]
					gnumsmin=ret[1]
					namemin=name.replace('.png','_MIN.png')
					plotter(sizesmin,gnumsmin,namemin,step,step/2)
					plt.savefig(options.path + '/' + namemin)
					plt.clf()

		'''
		I you have both CPU and GPU times, compute the ratio and plot it
		'''
		if retcpu and retgpu:
			if len(retcpu) == len(retgpu):

				#steps=[]
				difs=[]
				for i in range(len(retgpu)):
					step = retgpu[i][0]
					name = options.path + "/" + options.ID + "CS"+str(step).zfill(2) + '_FS' + str( int(step)/2 ).zfill(2) + '_GPUvsCPU.png'
					gnums = numpy.array(retgpu[i][-1])
					cnums = numpy.array(retcpu[i][-1])
					sizes = numpy.array(retgpu[i][1])
					difs = cnums/gnums

					difsl = list(difs)
					for i in range(len(difsl)):
						difsl[i] = str(difsl[i]) + '\n'
					f = open(name.replace('.png','.txt'),'w')
					f.writelines(difsl)
					f.close()
		
					print "\n$$$$$$$\nThe step is", step
					print "\n\n"
					plotter(sizes,difs,name,step,step/2)
					plt.savefig(options.path + '/' + name)
					plt.clf()
		
					if options.plotminima:
						ret=minima(sizes,difs)
						sizesmin=ret[0]
						difsmin=ret[1]
						namemin=name.replace('.png','_MIN.png')
						plotter(sizesmin,difsmin,namemin,step,step/2)
						plt.savefig(options.path + '/' + namemin)
						plt.clf()
		
				#print "I should be plotting this"

			else:
				print "For some sick reason, you don't have the same number of data points for gpu and cpu, therefore, you cannot compare them, see", len(retgpu), len(retcpu)
				sys.exit()
		else:
			return()

	
	else:
		'''
		If options.plotonly received some files, parse them and plot them
		'''
		
		files=options.plotonly.split(',')
		print "Will plot these files", files
		
		values={}
		
		#k=0
		for F in files:
			print "Working with this file now", F
			name=os.path.basename(F).replace('.txt','.png')
			sizes=[]
			valuesforthisfile=[]
			
			f=open(F,'r')
			lines = f.readlines()
			f.close()
			
			for line in lines:
				#print "Line is\n", line
				size=line.split()[0]
				sizes.append(int(size))
				value=line.split()[-1].replace('\n','')
				valuesforthisfile.append(float(value))
				#print "Thus size, value are", size, value
			
			if options.plotminima:
				ret=minima(sizes,valuesforthisfile)
				sizesmin=ret[0]
				valuesmin=ret[1]
				namemin=name.replace('.png','_MIN.png')
				plotter(sizesmin,valuesmin,namemin)
				
				if options.singleplot:
					pass
				else:
					plt.savefig(options.path + '/' + namemin)
					plt.clf()
					
			else:
				plotter(sizes,valuesforthisfile,name)
				
				if options.singleplot:
					pass
				else:
					plt.savefig(options.path + '/' + name)
					plt.clf()
			
			#values.update({k:valuesforthisfile})
			#k+=1
		
		if options.singleplot:
			
			plt.savefig(options.path + '/' + options.singleplot)
			plt.clf()
			print "I have saved a single plot to", options.path + '/' + options.singleplot
			
	return()
	
'''
FUNCTION TO COMPUTE ALIGNMENT TIMES
'''
def doit(corg,options):
	c=os.getcwd()
	f=os.listdir(c)

	mults = [12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,35,36,40,42,44,45,48,49,50,52,54,56,60,64,65,66,70,72,75,77,78,80,81,84,88,91,96,98,100,104,112,120,128,136,144,152,160,168,176,184,192,200,208,216,224,232,240,248,256]

	if options.test:
		mults = [32,64,96,128]
		#steps = [30]

	if options.medium:
		mults=[]
		for i in xrange(1,25):
			mults.append(i*10)
		#steps = [30]

	if options.extensive:
		mults = []
		for i in xrange(12,257):
			mults.append(i)
		#steps=[10]
	
	computer = options.ID
	
	data = []
	
	coarsestep=options.coarsestep
	finestep=options.finestep
		
	#name = options.path + '/CS' + str(coarsestep).zfill(len(str(max(steps)))) + '_FS' + str(finestep) + '.txt'
	#if computer:
	name = options.path + '/' + computer + 'CS' + str(coarsestep).zfill(len(str(coarsestep))) + '_FS' + str(finestep) + '_' + corg + '.txt'
	
	txt = open(name,'w')
		
	times=[]
	for size in mults:
		t=t1=t2=t1h=t2h=t1m=t2m=t1s=t2s=t1tot=t2tot=0

		#a=EMData(argv[1])
		a=EMData(size,size,size)
		a=a.process('testimage.noise.gauss')
		#a=a.process("xform.scale",{'scale':1,'clip':size})
			
		#if 'gpu' not in corg:
		#	a.switchoffcuda()
	
		#a.to_one()
		aname = 'a_stack.hdf'
		a.write_image(options.path+ '/' + aname)

		b=EMData(size,size,size)
		b=b.process('testimage.noise.gauss')
		bname = 'b_stack.hdf'
		b.write_image(options.path+ '/' + bname)
			
		#if 'gpu' not in corg:
		#	b.switchoffcuda()
		#	print "\n\n\n !!!! I Have turned cuda OFF!!!\n\n\n"
	
		out = 'garbage.hdf'
			
		setcuda=''
		if corg=='gpu' or corg=='GPU':
			setcuda= 'export NOCUDAINIT=0 && '
			print "\n\n\n !!!! I Have turned cuda ON!!!\n\n\n"
		elif corg=='cpu' or corg=='CPU':
			setcuda = 'export NOCUDAINIT=1 && '
			print "\n\n\n !!!! I Have turned cuda OFF!!!\n\n\n"
		else:
			print "Something is wrong; you're supposed to select GPU or CPU. TERMINATING!"
			sys.exit()
							
		instruction1 = setcuda + '''cd ''' + options.path + ''' && e2spt_classaverage.py --input=''' + aname + ''' --output=''' + out + ''' --ref=''' + bname + ''' --iter=1 --npeakstorefine=1 -v 1 --mask=mask.sharp:outer_radius=-2 --preprocess=filter.lowpass.gauss:cutoff_freq=0.1:apix=1.0 --align=rotate_translate_3d:search=6:delta=''' + str(coarsestep) + ''':dphi=''' + str(coarsestep) + ''':verbose=1:sym=icos --parallel=thread:1 --ralign=refine_3d_grid:delta=''' + str(finestep) + ''':range=''' + str(coarsestep) + ''' --averager=mean.tomo --aligncmp=ccc.tomo --raligncmp=ccc.tomo --normproc=normalize.mask'''
		cmd = instruction1
		print "The instruction is", cmd
	
		#if 'gpu' in corg:
		#	a=test_image()
		#	a.do_fft_cuda()
			
		ta = time()
		os.system(cmd)
		tb = time()
			
		#t=eman2time()
		#print "The total alignment time was", t
			
		td = tb - ta
		print "BUt the real time is", td
		times.append(float(td))
		line2write= str(size) + ' ' + str(td)+'\n'
		txt.write(line2write)
	txt.close()
	
	data.append([coarsestep,mults,times])
	print "\n\nThe data to return is\n", data
	print "\n"
	return(data)


'''
FUNCTION TO PLOT RESULTS
'''
def plotter(xaxis,yaxis,name='',CS=0,FS=0):
	
	matplotlib.rc('xtick', labelsize=16) 
	matplotlib.rc('ytick', labelsize=16) 
	
	font = {'weight':'bold','size':16}
	matplotlib.rc('font', **font)
	
	pylab.rc("axes", linewidth=2.0)
	pylab.xlabel('X Axis', fontsize=16, fontweight='bold')
	pylab.ylabel('Y Axis', fontsize=16, fontweight='bold')
	print "BOLD IS ON!"
	
	mark=''
	if '_MIN.png' in name or '_min.png' in name:
		mark='o'
		
	if options.colorlessplot:
		plt.plot(xaxis, yaxis, linewidth=3, marker=mark,color = 'k')
	else:
		plt.plot(xaxis, yaxis, linewidth=3, marker=mark)

	labelfory='Time (s)'
	
	if name and CS and FS:
		tag='gpu speed gain factor'
		labelfory='CPU time / GPU time'
		if 'gpu' in name or 'GPU' in name and 'cpu' not in name and 'CPU' not in name:
			tag='gpu 3D alignment Time'
			labelfory='Time (s)'
		if 'cpu' in name or 'CPU' in name and 'gpu' not in name and 'GPU' not in name:
			tag='cpu 3D alignment Time'
			labelfory='Time (s)'
	
		stepslabel='\ncoarse step=' + str(CS) + ' : fine step=' + str(FS)
		plt.title(tag + ' VS box-size' + stepslabel)
	
	plt.ylabel(labelfory)
	plt.xlabel("Box side-length (pixels)")

	#plt.legend(['y = x', 'y = 2x', 'y = 3x', 'y = 4x'], loc='upper left')
	
	#a = plt.gca()
	#a.set_xlim(1,int(xaxis[-1]))
	#a.set_ylim(0,max(yaxis)+0.25*max(xaxis))
	#a.legend(stepslabel)
	
	#plt.xlim( (1,int(xaxis[-1]) ) )
	#plt.ylim( ( 0,max(yaxis)+0.25*max(yaxis) ) )
	
	#plt.savefig(name)
	#plt.clf()
	return()


'''
FUNCTION TO DETERMINE MINIMA to be plotted later, instead of plotting ALL values in alignment time plots
'''
def minima(sizes,vals):
	
	sizesmin=[sizes[0]]
	valsmin=[vals[0]]
	
	for i in xrange(0,len(vals) - 1 - 1 ):
		aux = 0 
		for j in xrange(i+1,len(vals) - 1 - 1 ):
			if vals[j]< vals[i]:
				aux=0
				#print "Because a downstream value is lower, I will break the loop, see", vals[j],vals[i]
				break
			else:
				aux=1
		if aux==1:
			sizesmin.append(sizes[i])
			valsmin.append(vals[i])
			#print "I have appended this box, value", sizes[i], vals[i]
	
	return(sizesmin,valsmin)

'''
def eman2time():

		f=open('.eman2log.txt','r')
		lines=f.readlines()
		last=lines[-1]
	
		t1=last.split()[1]
		print "\n\n\n@@@@@@@@@@@@@@@@@@@@@ The job started at time", t1

		t1h=int(t1.split(':')[0].replace('/',''))
		#print "The hours of time 1 are", t1h
		#print "Or that times 3600", t1h*3600
		t1m=int(t1.split(':')[1])
		#print "The minutes of time 1 are", t1m
		#print "Or that times 60", t1m*60

		t1s=int(t1.split(':')[2])
		#print "The seconds of time 1 are", t1s
				
		t1tot = t1h*3600 + t1m*60 + t1s
		print "\n\n******************************* Therefore, in seconds, this was the time of starting t1tot=%d, %d*3600 + %d*60 + %d" % (t1tot,t1h,t1m,t1s)
				
		t2=last.split()[3]
		print "\n\n\n@@@@@@@@@@@@@@@@@@@@The job finished at time", t2
			
		t2h=int(t2.split(':')[0].replace('/',''))
		print 't2h is', t2h
			
		t2m=int(t2.split(':')[1])
		print 't2m is', t2m
			
		t2s=int(t2.split(':')[2])
		print 't2s is', t2s

		t2tot = t2h*3600 + t2m*60 + t2s
		print "\n\n******************************* Therefore, in seconds, this was the time of finishing t2tot=%d, %d*3600 + %d*60 + %d\n\n" % (t2tot,t2h,t2m,t2s)
	
		t = t2tot - t1tot
	return(t)
'''

if '__main__' == __name__:
	main()
