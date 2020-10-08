
class argPipeline():
    def __init__(self,alignAnat,align31P,createROI,computeStatistics, BET):
        self.alignAnat = alignAnat
        self.align31P = align31P

        self.createROI = createROI
        self.computeStatistics = computeStatistics
        self.BET = BET
