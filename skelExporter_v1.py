# ==================================== # 
# scriptName : skelExporter.py
# name : Mandl Cho
# updated : 2nd September 2018
# description : 
#   gets selected skeleton hierarchy 
#   and its transform nodess and 
#   writes it to a JSON file.    
# ==================================== #
import os
import re
import json
import pymel.core as pm 

keyBoneList = []

def exportBones(selBones=None,fileName=None):
    '''
    Exports List of Bones and its transforms to JSON
    '''
    global keyBoneList
    # first let's make sure a bone is selected 
    if not selBones:
        # look for the Dummy_Root bone
        selection = pm.ls(regex= '.+:Dummy_Root', type="joint")
        
        # once the Dummy_Root bone is found, cycle through it
        for eachBone in selection:
    		# and select the Dummy_Root, and all its children,
    	    pm.select(eachBone, hierarchy=True)
    		# and storing it into a listType. 
            selectedBones = pm.ls(selection=True)
            keyBoneList.append(eachBone)
                        
    # check if fileName is provided 
    if not fileName:
        # then bring up a file dialog
        basicFilter = "*.json"
        # and store whatever we selected in returnValue
        returnValue = pm.fileDialog2(dialogStyle=2, fm=0)
        if returnValue != None:
            file, ext = os.path.splitext(returnValue[0])
            # check if extension is not *.json, append it to filename
            if ext != ".json":
                fileName = file+".json"
            else:
                fileName = returnValue[0]
    print fileName

    
    # gather information about the bones
    boneName = pm.ls(selection=True)
    frameStart = pm.playbackOptions(q=True, min=True)
    frameEnd = pm.playbackOptions(q=True, max=True)
    for txform in boneName:
        outData = {
                    "BoneName":txform,
                    "transforms":{"matrix_world":{}}
                  }
    # loop over all the selected bones in the scene
    for i in range(len(keyBoneList)):
        # set the current frame
        outData["transforms"]["matrix_world"][str(i)]= pm.xform(str(keyBoneList), q=True, matrix=True)
    
    
    # store that data. 
    fout = open(fileName,"w")
    json.dumps(outData,fout,indent=2)
    fout.close()
    
    print "exported successfully to %s" % fileName
        
exportBones()