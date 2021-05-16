# Author: Renata Porciuncula Baptista
# E-mail: renata.porciunculabaptista@cea.fr


# Loop differents subjects


from parameters.initialization import INITIALIZATION
from utils_own.argsPipeline import argPipeline
from main import run_pipeline, run_saveResults 
from group_analysis import run_group

subs = ['sub01_y','sub02_y','sub03_y']#
#subs = ['sub01_o']
#subs = [ 'sub00_y']#
#rois = ['cortical_up','cortical_down', 'cortical_in']
rois = ['cortical_up_1','cortical_up_2',
        'cortical_down_1', 'cortical_down_2']

#rois = ['wm', 'gm'] 
#rois = ['occ_pole']
only_group = False
applyB1Correction = 1


if only_group == False:
    for sub in subs:
        args = argPipeline(alignAnat=0,
                        align31P=0,
                        createROI=0,
                        createIndividualB1=0,
                        applyB1Correction = applyB1Correction,
                        computeStatistics=0,
                        quantification=0,
                        saveResults=1, 
                        BET = True) 
        firstRun = True

        for roi in rois:
            run_pipeline(sub,roi,args)
            if firstRun == True:
                firstRun = False
                args.alignAnat = 0
                args.align31P = 0

run_saveResults(sub, rois, args)

# Group analisis
for roi in rois:
    run_group(subs,roi, applyB1Correction)