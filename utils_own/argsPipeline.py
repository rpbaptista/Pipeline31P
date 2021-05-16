
class argPipeline():
    def __init__(self,alignAnat,
                align31P,createROI,
                createIndividualB1, applyB1Correction,
                computeStatistics, quantification,
                saveResults, BET):
        self.alignAnat = alignAnat
        self.align31P = align31P

        self.createROI = createROI
        self.createIndividualB1 = createIndividualB1
        self.applyB1Correction = applyB1Correction

        self.computeStatistics = computeStatistics
        self.quantification = quantification
        self.saveResults = saveResults
        self.BET = BET
