#! /usr/local/bin/python3

# -*- coding: utf-8 -*-
"""
Created on Thu Nov 28 15:47:12 2019

@author: chdwck9
"""

#Imports and setup
import os
import json
import cutie
import glob
import shutil
import sys

#Functions
def getOSSep ():
	if (os.name=="nt") :
		s="\\"
	else :
		s="/"
	return s

def getBlockPath():
	if os.path.isfile(".block") :
		parentDir = dname
	else :
		if len(sys.argv)>1 or not os.path.isfile(sys.argv[1]):
			parentDir=sys.argv[1]
			parentDir=parentDir.replace('/','|').replace('\\','|').rstrip('|')
		else : parentDir="C:|Users|chdwck9|Temp" #change this to dynamically take arguments (len(sys.argv) > 1)
		name = str(input("What is the title of the project/directory?: "))
		parentDir=parentDir+'|'+name+'|'
	return parentDir

def writeDir(d) :
	print("Creating directory: "+d)
	try: os.makedirs(d,exist_ok=True)
	except: print("  Note: Directory already exists")

def copyBrick(f,t):
	try:
		for file in glob.glob(f+'*'):
		    print(file)
		    shutil.copy(file, t)
	except: print('Couldn''t find the file you were looking for')

def findTemplates(locs,s) :
	for i in locs:
		if os.path.isdir(i.replace('|',s)) : break
	return(i)

def userSelected(c,cap,ind="Title",ti=[]):
	gdt=[cap]
	for i in c:
		gdt.append(i[ind])
	s = cutie.select_multiple(gdt,caption_indices=[0],ticked_indices=ti)
	bs = []
	for i in s:
		bs.append(c[i-1])
	return(bs)

def walkBlocks(c,s,tp,p):
	for i in c:
		for j in i["Structure"]:
			writeDir((p+j).replace("|",s))
		if "Bricks" in i: walkBricks(i["Bricks"],s,tp,p)
	with open(((p+'.block').replace("|",s)), 'w') as outfile:
		   json.dump(c, outfile)

def walkBricks(c,s,tp,p):
	if len(c) > 0 :
		for i in c:
			f = (tp+i["name"]).replace('|',s)
			t = (p+i["to"]).replace('|.','').replace('|',s)
			print("from: "+f+"*    to: "+t)
			copyBrick(f,t)

#Change the working directory
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#Get some information about the destination directory
srep = getOSSep()
parentDir = getBlockPath()
print(parentDir)

#Load the config file
try :
	with open(os.path.join(sys.path[0],'config.json')) as json_file:
		conf = json.load(json_file)
		templateDirectory = findTemplates(conf["TemplateDirectory"],srep)+'|'
		print("Reading templates from "+templateDirectory)
except :
	print("  Error: Config file either doesn't exist or is incorrectly formatted for JSON. Please try again.")
print()

#create a menu to pick what you want in your folder (mulitple choices accepted)
blocks = userSelected(conf["Blocks"],"What blocks do you want configured?",ti=[1])
print()
print()
# bricks = userSelected(conf["Bricks"],"What bricks do you want configured?",ind="name")

#walk through the config file and create folders and/or copy files
walkBlocks(blocks,srep,templateDirectory,parentDir)
# walkBricks(bricks,srep,templateDirectory,parentDir)