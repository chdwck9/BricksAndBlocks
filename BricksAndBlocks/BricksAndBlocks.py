#Imports and setup
import os
import json
import cutie
import glob
import shutil
import sys
import re
from pathlib import Path
import git

class BricksAndBlocks(object):

		def __init__(self,a):
			#Change the working directory
			abspath = os.path.abspath(__file__)
			dname = os.path.dirname(abspath)
			os.chdir(dname)

			#Get some information about the destination directory
			srep = self.getOSSep()
			parentDir, name, defaultBricks = self.blockOrBrick(a)

			# Load the config file
			try :
				with open(os.path.join(sys.path[0],'config.json')) as json_file:
					conf = json.load(json_file)
			except :
				conf=None
				print("  Error: Config file either doesn't exist or is incorrectly formatted for JSON. Please try again.")

			if conf != None :
				templateDirectories = self.findTemplates(conf["TemplateDirectory"],srep)
				print("Reading templates from "+",".join(templateDirectories))
				print()
				#create a menu to pick what you want in your folder (mulitple choices accepted)
				blocks = self.userSelected(conf["Blocks"],"What blocks do you want configured?",ti=defaultBricks)
				print()
				print()
				#walk through the config file and create folders and/or copy files
				self.walkBlocks(blocks,srep,templateDirectories,parentDir,name)

		#Functions
		def getOSSep (self):
			if (os.name=="nt") :
				s="\\"
			else :
				s="/"
			return s

		def blockOrBrick(self,a) :
			if a[0] =="block":
				defaultBricks = [1]
				parentDir, name = self.getBlockPath(a[1])
			else :
				defaultBricks = []
				parentDir, name = self.getBrickPath(a[1])
			return parentDir, name, defaultBricks

		def getBlockPath(self,pd):
			name = str(input("What is the title of the block?: "))
			parentDir=pd.replace('/','|').replace('\\','|').rstrip('|')+'|'+name+'|'
			name = re.sub('[^a-zA-Z]+', '', re.sub('(\s)#\w+','',name)).lower()
			return parentDir, name

		def getBrickPath(self,pd):
			name = str(input("What is the title of the brick? (leave blank for default): "))
			if name == "": name = os.path.basename(pd)
			parentDir=pd.replace('/','|').replace('\\','|').rstrip('|')+'|'
			name = re.sub('[^a-zA-Z]+', '', re.sub('(\s)#\w+','',name)).lower()
			return parentDir, name

		def writeDir(self,d) :
			print("Creating directory: "+d)
			try: os.makedirs(d,exist_ok=True)
			except: print("  Note: Directory already exists")

		def copyBrick(self,f,t,n):
			try:
				for file in glob.glob(f+'*'):
					print(file)
					shutil.copy(re.sub(r'\[[\s\S]*\]',n,file), t)
			except: print('Couldn''t find the file you were looking for')

		def findTemplates(self,locs,s) :
			temps = []
			for i in locs:
				if os.path.isdir(i.replace('|',s)) : temps.append(i+'|')
			return(temps)

		def userSelected(self,c,cap,ind="Title",ti=[]):
			gdt=[cap]
			for i in c:
				gdt.append(i[ind])
			s = cutie.select_multiple(gdt,caption_indices=[0],ticked_indices=ti)
			bs = []
			for i in s:
				bs.append(c[i-1])
			return(bs)

		def walkBlocks(self,c,s,tp,p,n):
			for i in c:
				if "Structure" in i:
					for j in i["Structure"]:
						self.writeDir(re.sub(r'\[[\s\S]*\]',n,(p+j).replace("|",s)))
						# print(re.sub(r'\[[\s\S]*\]',n,(p+j).replace("|",s)))
				if "Bricks" in i: self.walkBricks(i["Bricks"],s,tp,p,n)
			# with open(((p+'.block').replace("|",s)), 'w') as outfile:
			# 	   json.dump(c, outfile)

		def walkBricks(self,c,s,tp,p,n):
			if len(c) > 0 :
				for i in c:
					t = re.sub(r'\[[\s\S]*\]',n,(p+i["to"]).replace('|.','').replace('|',s))
					if "run" in i:
						print("Attempting to run "+i["run"]+" in "+t)
						r = re.sub(r'\[[\s\S]*\]',n,i["run"])
						f = open("tmp.sh", "w")
						f.write("cd '"+t+"' && "+r)
						f.close()
						os.popen('tmp.sh')
					elif "git" in i:
						print("Attempting to clone "+i["git"]+" in "+t)
						git.Repo.clone_from(i["git"], t)
						# r = "git clone "+i["git"]
						# f = open("tmp.sh", "w")
						# f.write("cd '"+t+"' && "+r+" && pause")
						# f.close()
						# os.popen('tmp.sh')
					else :
						for temps in tp :
							f = (temps+i["name"]).replace('|',s)
							print("from "+f+"* to "+t)
							self.copyBrick(f,t,n)
