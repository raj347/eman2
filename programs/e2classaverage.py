#!/usr/bin/env python

#
# Author: David Woolford, 09/07/2007 (woolford@bcm.edu)
# Copyright (c) 2000-2007 Baylor College of Medicine
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

from EMAN2 import *
from optparse import OptionParser
from math import *
import os
import sys


def main():
	progname = os.path.basename(sys.argv[0])
	usage = """%prog [options] <input particles> <sim mx> <output>
	Produces class averages """
	parser = OptionParser(usage=usage,version=EMANVERSION)

	parser.add_option("--iter", type="int", help="The number of iterations to perform, default is 1 - this means the particles will only be averaged once (to the projection)", default=1)
	parser.add_option("--hard", type="float", help="The quality metric threshold. Default is off (0)", default=0.0)
	parser.add_option("--ref", type="string", help="the associated reference images to calculate the first quality metric from", default="")
	parser.add_option("--align",type="string",help="The name of an 'aligner' to use prior to comparing the images", default="rotate_translate")
	parser.add_option("--aligncmp",type="string",help="Name of the cmp to use in conjunction with the --align argument",default="dot")
	parser.add_option("--aliref",type="string",help="The name of an 'aligner' to use prior to comparing the images", default="rotate_translate")
	parser.add_option("--alirefcmp",type="string",help="Name of the cmp to use in conjunction with the --align argument",default="dot")
	parser.add_option("--averager",type="string",help="Name of averager to use",default="image")
	parser.add_option("--cmp",type="string",help="The name of a 'cmp' to be used in comparing the aligned images", default="dot:normalize=1")
	parser.add_option("--keepfrac",type="float",help="The fraction of particles in classes to keep, based on the quality metric generated by the --cmp argument. Default is 1.0",default=1.0)
	parser.add_option("--keepsig",type="float",help="The fraction of particles in classes to keep, based on the quality metric generated by the --cmp argument. Default is 1.0",default=1.0)
	parser.add_option("--verbose","-v",action="store_true",help="Verbose display during run",default=False)
	
	
	(options, args) = parser.parse_args()
		
	if len(args)<3 : parser.error("Input and output files required")

	# check to see if the image exists
	for i in range(0,2):
		if not os.path.exists(args[i]):
			parser.error("File %s does not exist" %args[i])
	
	if os.path.exists(args[2]):
		parser.error("File %s exists, will not write over, exiting" %args[2])
	
	num_sim =  EMUtil.get_image_count(args[1])
	if ( num_sim != 5 ):
		print "Error expecting the similarity image to contain 5 images, got %d - please generate the similarity matrix using e2classify.py" %num_sim
		exit(1)
	
	(num_proj, num_part ) = gimme_image_2dimensions(args[1]);
	
	if (options.ref != ""):
		if not os.path.exists(options.ref):
			parser.error("File %s does not exist" %options.ref)
			
		num_ref_check = EMUtil.get_image_count(options.ref)
		if ( num_proj != num_ref_check ):
			print "Error, the number of columns (%d) in the similarity image does not match the number of projections (%d) in the projection image." %(num_proj,num_ref_check)
			
	if (options.iter < 1 ):
		parser.error("iter must be greater than or equal to 1" %options.proj)
	
	options.align=parsemodopt(options.align)
	options.alicmp=parsemodopt(options.aligncmp)
	options.cmp=parsemodopt(options.cmp)
	
	num_part_check =  EMUtil.get_image_count(args[0])
	
	if ( num_part != num_part_check ):
		print "Error, the number of rows (%d) in the similarity image does not match the number of particles (%d) in the input image." %(num_part,num_part_check)
		exit(1)
		
	
	simmx = EMData()
	simmx.read_image(args[1], 0)
	alix = EMData()
	alix.read_image(args[1],1)
	aliy = EMData()
	aliy.read_image(args[1],2)
	aliaz = EMData()
	aliaz.read_image(args[1],3)
	projmx = EMData()
	projmx.read_image(args[1],4)

	# read as terminating index
	term_idx = get_first_zero_index(simmx)
	print term_idx;
	
	# initialize empyt arrays for storage
	classification = []
	classes = []
	for i in range(num_proj):
		classification.append([])
		classes.append([])
	
	# classification vector is comprised as follows:
	# columns denote projection number
	# each entry in a row contains (l,r) where l is the particle number and r is its weight
	for i in range(num_part):
		for j in range(term_idx):
			classification[int(projmx.get_value_at(j,i))].append((i,simmx.get_value_at(j,i)))
	
	(nx, ny) = gimme_image_2dimensions(args[0]);
	
	for it in range(1,options.iter+1):
		if options.verbose: 
			print "Averaging classes, iteration %d" %it
		
		ali_parms = []
		for i in range(num_proj):
			ali_parms.append([])
		
		#two temp EMData objects used at various locations below
		tmp1 = EMData()
		tmp2 = EMData()
		
		#first get ali params - alignment are stored in 4-length vectors in the following format
		# [quality score, alignment dx, alignment dy, alignment dazimuth]
		if (it == 1):
			# if i is 0 we use the alignment generated by e2simmx.py
			for i in range(num_proj):
				for j in range(len(classification[i])):
					idx = classification[i][j][0]
					
					ali = [0,alix.get_value_at(i,idx), aliy.get_value_at(i,idx), aliaz.get_value_at(i,idx)]
					
					if (options.ref != "" ):
						idx = classification[i][j][0]
						tmp1.read_image(options.ref, i)
						tmp2.read_image(args[0],idx)
						ali[0] = tmp1.cmp(options.cmp[0],tmp2,options.cmp[1])
					
					ali_parms[i].append(ali)
		else:
			# if i is greater than zero we do iterative alignment where the particles are aligned to the class average
			for i in range(num_proj):
				tmp1 = classes[i]
				tmp2 = EMData()
				for j in range(len(classification[i])):
					target.read_image(args[0], classification[i][j][0])
					ta=tmp1.align(options.align[0],tmp1,options.align[1],options.alicmp[0],options.alicmp[1])
					ali_parms[i].append([ta.cmp(options.cmp[0],tmp1,options.cmp[1]),ta.get_attr_default("align.dx",0),ta.get_attr_default("align.dy",0),ta.get_attr_default("align.az",0)])
		
		scores = []
		qual_scores = []
		for i in range(num_proj):
			qual_scores.append([])
			
		do_qual = True
		if ( it == 1 and options.ref == "" ):
			do_qual = False

		if do_qual:
			for i in range(num_proj):
				for j in range(len(classification[i])):
					qual_scores[i].append(ali_parms[i][j][0])
		
		for i in range(num_proj):
			a = Util.get_stats(qual_scores[i])
			b = Util.get_stats_cstyle(qual_scores[i])
			print "means %f %f"  %(a["mean"], b["mean"])
			print "std dev %f %f" %(a["std_dev"], b["std_dev"])
			print "skew %f %f" %(a["skewness"],b["skewness"])
			print "kurtosis %f %f" %(a["kurtosis"],b["kurtosis"])
			print "cs %f %f" %(a["cs"],b["cs"])
			print "qs %f %f" %(a["qs"],b["qs"])
			#print a["std_dev"]
			#print a["skewness"]
			#print a["kurtosis"]
		
		print num_proj
		for i in range(num_proj):
			if options.verbose: 
				print "%d/%d\r"%(i,num_proj),
				sys.stdout.flush()
	
			aparms=parsemodopt(options.averager)
			averager=Averagers.get(aparms[0], aparms[1])
		
			weight_sum = 0.0
			ptcl_repr = 0
			for j in range(len(classification[i])):
					weight_sum += classification[i][j][1]
					ptcl_repr += 1
					
					idx = classification[i][j][0]
					t3d = Transform3D(EULER_EMAN,ali_parms[i][j][3],0,0)
					t3d.set_posttrans(ali_parms[i][j][1], ali_parms[i][j][2])
					
					image = EMData()
					image.read_image(args[0], idx)
					image.rotate_translate(t3d)
					averager.add_image(image)
	
			
			if ( weight_sum != 0 ):
				averager.mult(1.0/weight_sum)
			
			if ( ptcl_repr != 0 ):
				classes[i] = averager.finish()
				classes[i].set_attr("ptcl_repr", ptcl_repr)
			else :
				tmp = EMData()
				tmp.set_size(nx,ny,1)
				tmp.to_zero()
				classes[i] = tmp
	
	
	if options.verbose: 
		print "Writing %s" %args[2]
	for i in range(num_proj):
		classes[i].write_image(args[2],-1)

	
def get_first_zero_index(simmx):
	num_proj = simmx.get_xsize()
	num_part = simmx.get_ysize()
	
	# get the first zero encountered in the first row
	first_zero_index = 0
	for i in range(num_proj):
		if (simmx.get_value_at(i,0)==0):
			first_zero_index = i
			break
	
	if ( first_zero_index == 0 ):
		print "Error, could not find any classification weights in the first image (first row)"
		exit(1)
		
	return first_zero_index

#def average_old:
	#for i in xrange(0,ysize):
		#max_score = simmx.get_value_at(0,i)
		#max_idx = 0
		#for j in xrange(1,xsize):
			#new_score = simmx.get_value_at(j,i)
			#if ( new_score < max_score ):
				#max_score = new_score
				#max_idx = j

		#classification.append(max_idx)
	
	#for idx in xrange(0,xsize):
		#average = EMData()
		#average.set_size(rxsize,rysize,1)
		#average.to_zero()
		#ptcl_repr = 0.0
		#for i in xrange(0,total_particle_images):
			#if ( classification[i] == idx ):
				#t3d = Transform3D(EULER_EMAN,aliaz.get_value_at(idx),0,0)
				#t3d.set_posttrans(alix.get_value_at(idx,i), aliy.get_value_at(idx,i))
				#image = EMData()
				#image.read_image(args[0], i)
				#image.rotate_translate(t3d)
				#average.add(image)
				#ptcl_repr += 1.0
		
		#if ( ptcl_repr != 0 ):
			#average.mult(1.0/ptcl_repr)
			
		#average.set_attr("ptcl_repr", ptcl_repr)
		#average.write_image("classes.img",-1)

if __name__ == "__main__":
    main()