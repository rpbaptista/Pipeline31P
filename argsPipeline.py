
class argPipeline():
    def __init__(self,alignAnat,align31P,skulltrip,warpMNI,invwarpMNI,createROI,computeStatistics, BET):
        self.alignAnat = alignAnat
        self.align31P = align31P
        self.skulltrip = skulltrip
        self.warpMNI = warpMNI
        self.invwarpMNI = invwarpMNI
        self.createROI = createROI
        self.computeStatistics = computeStatistics
        self.BET = BET
