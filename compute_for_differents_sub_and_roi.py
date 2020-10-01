# Loop differents subjects



from parameters.initialization import INITIALIZATION
from argsPipeline import argPipeline
from main import run_pipeline 

subs = ['sub01', 'sub02']
rois = ['cortical_up','cortical_down', 'cortical_in']
BET_option = [   1]
args = argPipeline(alignAnat=0,
                    align31P=0,
                    skulltrip=1,
                    warpMNI=1,
                    invwarpMNI=1,
                    createROI=1,
                    computeStatistics=1, 
                    BET = True)
for roi in rois:
    for sub in subs:
        for bet in BET_option:
            args.BET = bet
            run_pipeline(sub,roi,args)
