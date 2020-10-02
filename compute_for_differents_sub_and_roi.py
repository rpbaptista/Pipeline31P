# Author: Renata Porciuncula Baptista
# E-mail: renata.porciunculabaptista@cea.fr


# Loop differents subjects


from parameters.initialization import INITIALIZATION
from argsPipeline import argPipeline
from main import run_pipeline 

subs = ['sub02']
rois = ['cortical_up','cortical_down', 'cortical_in']
BET_option = [ 1]
args = argPipeline(alignAnat=0,
                    align31P=0,
                    skulltrip=0,
                    warpMNI=0,      
                    invwarpMNI=0,
                    createROI=1,
                    computeStatistics=1, 
                    BET = True)

args_bck = args
for bet in BET_option:
    firstRun = True
    args = args_bck
    for roi in rois:
        for sub in subs:
            args.BET = bet
            run_pipeline(sub,roi,args)

            if firstRun == True:
                firstRun = False
                args.alignAnat = 0
                args.align31P = 0
                args.skulltrip = 0
                args.warpMNI = 0
                args.invwarpMNI = 0
