# Author: Renata Porciuncula Baptista
# E-mail: renata.porciunculabaptista@cea.fr


# Loop differents subjects


from parameters.initialization import INITIALIZATION
from utils_own.argsPipeline import argPipeline
from main import run_pipeline 
from group_analysis import run_group

#subs = ['sub00_y','sub01_y','sub02_y','sub03_y']
subs = ['sub03_y']
#subs = [ 'sub00_y']
#rois = ['cortical_up','cortical_down', 'cortical_in']
rois = ['cortical_down']
only_group = False

if only_group == False:
    for sub in subs:
        args = argPipeline(alignAnat=0,
                        align31P=0,
                        createROI=0,
                        computeStatistics=1,
                        quantification=1, 
                        BET = True)
        firstRun = True

        for roi in rois:
            run_pipeline(sub,roi,args)
            if firstRun == True:
                firstRun = False
                args.alignAnat = 0
                args.align31P = 0

# Group analisis
for roi in rois:
    run_group(subs,roi)