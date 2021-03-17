#Imports and setup
import os
import json
import cutie
import glob
import shutil
import sys
import re
from pathlib import Path

#Functions
def getOSSep ():
	if (os.name=="nt") :
		s="\\"
	else :
		s="/"
	return s

def blockOrBrick(a=None) :
	if a==None : a = [sys.argv[2],sys.argv[1]]
	if a[0] =="block":
		defaultBricks = [1]
		parentDir, name = getBlockPath(a[1])
	else :
		defaultBricks = []
		parentDir, name = getBrickPath(a[1])
	return parentDir, name, defaultBricks

def getBlockPath(pd):
	name = str(input("What is the title of the block?: "))
	parentDir=pd.replace('/','|').replace('\\','|').rstrip('|')+'|'+name+'|'
	name = re.sub('[^a-zA-Z]+', '', re.sub('(\s)#\w+','',name)).lower()
	return parentDir, name

def getBrickPath(pd):
	name = str(input("What is the title of the brick? (leave blank for default): "))
	if name == "": name = os.path.basename(pd)
	parentDir=pd.replace('/','|').replace('\\','|').rstrip('|')+'|'
	name = re.sub('[^a-zA-Z]+', '', re.sub('(\s)#\w+','',name)).lower()
	return parentDir, name

def writeDir(d) :
	print("Creating directory: "+d)
	try: os.makedirs(d,exist_ok=True)
	except: print("  Note: Directory already exists")

def copyBrick(f,t,n):
	try:
		for file in glob.glob(f+'*'):
		    print(file)
		    shutil.copy(re.sub(r'\[[\s\S]*\]',n,file), t)
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

def walkBlocks(c,s,tp,p,n):
	for i in c:
		if "Structure" in i:
			for j in i["Structure"]:
				writeDir(re.sub(r'\[[\s\S]*\]',n,(p+j).replace("|",s)))
				# print(re.sub(r'\[[\s\S]*\]',n,(p+j).replace("|",s)))
		if "Bricks" in i: walkBricks(i["Bricks"],s,tp,p,n)
	# with open(((p+'.block').replace("|",s)), 'w') as outfile:
	# 	   json.dump(c, outfile)

def walkBricks(c,s,tp,p,n):
	if len(c) > 0 :
		for i in c:
			t = re.sub(r'\[[\s\S]*\]',n,(p+i["to"]).replace('|.','').replace('|',s))
			if "run" in i:
				r = re.sub(r'\[[\s\S]*\]',n,i["run"])
				f = open("tmp.sh", "w")
				f.write("cd '"+t+"' && "+r)
				f.close()
				os.popen('tmp.sh')
				# os.remove('tmp.sh')
			else :
				f = (tp+i["name"]).replace('|',s)
				print("from: "+f+"*    to: "+t)
				copyBrick(f,t,n)

#Change the working directory
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

#Get some information about the destination directory
srep = getOSSep()
parentDir, name, defaultBricks = blockOrBrick()
# parentDir, name = block(["block",r"C:\Users\chdwck9\Temp\test"]) # dev
# parentDir, name = block(["brick",r"C:\Users\chdwck9\Temp\test"]) # dev
# print(parentDir, name) # dev


# Load the config file
try :
	with open(os.path.join(sys.path[0],'config.json')) as json_file:
		conf = json.load(json_file)
		templateDirectory = findTemplates(conf["TemplateDirectory"],srep)+'|'
		print("Reading templates from "+templateDirectory)
except :
	print("  Error: Config file either doesn't exist or is incorrectly formatted for JSON. Please try again.")
print()

#create a menu to pick what you want in your folder (mulitple choices accepted)
blocks = userSelected(conf["Blocks"],"What blocks do you want configured?",ti=defaultBricks)
print()
print()
# bricks = userSelected(conf["Bricks"],"What bricks do you want configured?",ind="name")

#walk through the config file and create folders and/or copy files
walkBlocks(blocks,srep,templateDirectory,parentDir,name)
# walkBricks(bricks,srep,templateDirectory,parentDir)