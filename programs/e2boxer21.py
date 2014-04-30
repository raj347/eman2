#!/usr/bin/env python
#
# Author: Steven Ludtke 2014/04/27
# Copyright (c) 2014- Baylor College of Medicine


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

from EMAN2 import BoxingTools,gm_time_string,Transform, E2init, E2end, E2progress,db_open_dict,EMArgumentParser
from EMAN2db import db_check_dict
from EMAN2jsondb import *
from pyemtbx.boxertools import CoarsenedFlattenedImageCache,FLCFImageCache
from copy import deepcopy
from EMAN2 import *
from emboxerbase import *
import os

def main():
	progname = os.path.basename(sys.argv[0])
	usage = """prog [options] <image> <image2>....

	The even newer version of e2boxer. Complete rewrite. Incomplete.
	
	This program 
"""
	parser = EMArgumentParser(usage=usage,version=EMANVERSION)

	parser.add_pos_argument(name="micrographs",help="List the file to process with e2boxer here.", default="", guitype='filebox', browser="EMBoxesTable(withmodal=True,multiselect=True)",  row=0, col=0,rowspan=1, colspan=3, mode="boxing,extraction")
	parser.add_argument("--boxsize","-B",type=int,help="Box size in pixels",default=-1, guitype='intbox', row=2, col=0, rowspan=1, colspan=3, mode="boxing,extraction")
	parser.add_argument("--ptclsize","-P",type=int,help="Longest axis of particle in pixels",default=-1, guitype='intbox', row=2, col=0, rowspan=1, colspan=3, mode="boxing,extraction")
	parser.add_argument("--apix",type=float,help="Angstroms per pixel for all images",default=0, guitype='floatbox', row=4, col=0, rowspan=1, colspan=1, mode="autofit['self.pm().getAPIX()']")
	parser.add_argument("--voltage",type=float,help="Microscope voltage in KV",default=0, guitype='floatbox', row=4, col=1, rowspan=1, colspan=1, mode="autofit['self.pm().getVoltage()']")
	parser.add_argument("--cs",type=float,help="Microscope Cs (spherical aberation)",default=0, guitype='floatbox', row=5, col=0, rowspan=1, colspan=1, mode="autofit['self.pm().getCS()']")
	parser.add_argument("--ac",type=float,help="Amplitude contrast (percentage, default=10)",default=10, guitype='floatbox', row=5, col=1, rowspan=1, colspan=1, mode='autofit')
	parser.add_argument("--write_dbbox",action="store_true",help="Write coordinate file (eman1 dbbox) files",default=False, guitype='boolbox', row=3, col=0, rowspan=1, colspan=1, mode="extraction")
	parser.add_argument("--write_ptcls",action="store_true",help="Write particles to disk",default=False, guitype='boolbox', row=3, col=1, rowspan=1, colspan=1, mode="extraction[True]")
	parser.add_argument("--invert",action="store_true",help="If writing outputt inverts pixel intensities",default=False, guitype='boolbox', row=3, col=2, rowspan=1, colspan=1, mode="extraction")
	parser.add_argument("--ppid", type=int, help="Set the PID of the parent process, used for cross platform PPID",default=-1)
	parser.add_argument("--gui", action="store_true", default=True, help="Dummy option; used in older version of e2boxer")
	parser.add_argument("--verbose", "-v", dest="verbose", action="store", metavar="n", type=int, default=0, help="verbose level [0-9], higner number means higher level of verboseness")

	(options, args) = parser.parse_args()



if __name__ == "__main__":
	main()