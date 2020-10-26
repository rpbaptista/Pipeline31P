# Author: Renata Porciuncula Baptista
# E-mail: renata.porciunculabaptista@cea.fr


# Loop differents subjects


from parameters.initialization import INITIALIZATION
from utils_own.argsPipeline import argPipeline
from main import run_pipeline 

subs = ['sub00_y','sub01_y','sub02_y','sub03_y']
#subs = [ 'sub03_y']
#rois = ['cortical_up','cortical_down', 'cortical_in']
rois = ['cortical_down']

args = argPipeline(alignAnat=0,
                    align31P=1,
                    createROI=0,
                    computeStatistics=0,
                    quantification=0, 
                    BET = True)

args_bck = args
firstRun = True
for sub in subs:
    args = args_bck
    firstRun = True

    for roi in rois:
        run_pipeline(sub,roi,args)
        if firstRun == True:
            firstRun = False
            args.alignAnat = 0
            args.align31P = 0
