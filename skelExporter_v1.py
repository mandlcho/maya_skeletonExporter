# ==================================== # 
# scriptName : skelExporter.py
# name : Mandl Cho
# updated : 2nd September 2018
# description : 
#   gets selected skeleton hierarchy 
#   and its transform nodess and 
#   writes it to a JSON file.    
# ==================================== #

# pseudo code :
# get selection of bones in the scene. 
# select hierarchy of bones 
# get bone transforms
# select dir to save JSON
# write to JSON

import pymel.core as pm 
import json
import re
import os

boneList = []

def storeBones():
	global boneList
	# ensuring that no objects are selected
	pm.select(clear=True)
	# creating a pattern to look for our specified bone, selected   
	scnBones = pm.ls(regex= '.+:Dummy_Root', type="joint")
	# doing a check to see if we managed to get the Dummy_Root bone 
	for oRoot in scnBones:
		print oRoot
		# select the Dummy_Root, and all its children, and storing it into a variable
		storedBones = pm.select(oRoot, hierarchy=True)

	# storing selection to a variable
	stored = pm.ls(selection=True)
	boneList[:] = []
	for eachBone in stored:
		boneList.append(eachBone)
		print " %s has been added to list!" % eachBone	
	
	return boneList

def writejson():
	bonejson = {}
	selected_obj = pm.ls(sl=True, type='transform')

	basicFilter = "*.json"
	returnValue = pm.fileDialog2(dialogStyle=2, fm=0)
	if returnValue != None:
		file, ext = os.path.splitext(returnValue[0])
		if ext != ".json":
			fileName = file+".json"
		else:
			fileName = returnValue[0]

	for curr_obj in selected_obj:
		rotation = pm.xform(curr_obj,  query=True, rotation=True, worldSpace=False)
		rotation_worldspace = pm.xform(curr_obj,  query=True, rotation=True, worldSpace=True)
		translation = pm.xform(curr_obj, query=True, translation=True, worldSpace=False)
		translation_worldspace = pm.xform(curr_obj, query=True, translation=True, worldSpace=True)
		node = {
			'translation': str(round(translation[0],2)) + ',' + str(round(translation[1],2)) + ',' + str(round(translation[2],2)),
			'translation_worldspace': str(round(translation_worldspace[0],2)) + ',' + str(round(translation_worldspace[1],2)) + ',' + str(round(translation_worldspace[2],2)),
			'rotation': str(round(rotation[0],2)) + ',' + str(round(rotation[1],2)) + ',' + str(round(rotation[2],2)),
			'rotation_worldspace': str(round(rotation_worldspace[0],2)) + ',' + str(round(rotation_worldspace[1],2)) + ',' + str(round(rotation_worldspace[2],2)),
		}
		bonejson[str(curr_obj)] = node

		f = open(fileName, 'w')
		output_json = json.dump(bonejson, f, sort_keys=True, indent=4, separators=(',', ' : '))
		f.close()
	print output_json

storeBones()
writejson()
