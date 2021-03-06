#! /bin/env python
###################
# davide.gerbaudo@cern.ch clement.helsens@cern.ch, francesco.rubbo@cern.ch
###################
# usage:
# python runLinearityMC12.py 
###################

import sys, os
sys.path.append(os.getcwd()+'/fbu/')

from pyFBU import pyFBU
import computeAc
import linearity
import plot

import numpy as np

def Integral(array, up, down):
    nb=0
    print 'up=%f   down=%f'%(up,down)
    for i in array:
        if i>up or i<down:nb+=1
    return nb

#__________________________________________________________
if __name__ == "__main__":
    Dir = 'tests/linearity/'
    pyfbu = pyFBU()

    pyfbu.nMCMC    = 100000
    pyfbu.setnBurn = 1000
    pyfbu.setnThin = 10
    
    pyfbu.lower = 400000
    pyfbu.upper = 900000

    pyfbu.jsonMig = Dir+'data/mc12/migrations.json'
    pyfbu.jsonBkg = Dir+'data/mc12/background.json'

    #pyfbu.rndseed = 0

    pyfbu.verbose = False
    
    dataList = ['dataA6neg.json', 'dataA4neg.json', 'dataA2neg.json', 'dataA2pos.json', 'dataA4pos.json', 'dataA6pos.json']
    meanAc = []
    stdAc = []
    
    TestPassed = True

    for data in dataList:
        pyfbu.jsonData  = Dir+'data/mc12/'+data
        pyfbu.modelName = data.replace('.json','')
        pyfbu.run()
        trace = pyfbu.trace

        np.save('outputFile'+data.replace('.json',''),trace)

        AcList  = computeAc.computeAcList(trace)
        AcArray = np.array(AcList)
        meanAc.append(np.mean(AcArray))
        stdAc.append(np.std(AcArray))
        plot.plotarray(AcArray,'Ac_posterior_'+data.replace('.json',''))
        integral = Integral(AcArray,np.mean(AcArray)+3.*np.std(AcArray),np.mean(AcArray)-3.*np.std(AcArray))
        ratio = float(integral)/float(len(trace))
        if ratio>0.0027:
            print 'integral  %i     ratio  %f   -->> this is NOT ok, should be < 0.0027 (3sigmas)'%(integral, ratio)
            TestPassed = TestPassed*False


    meanAcArray = np.array(meanAc)
    stdAcArray  = np.array(stdAc)

    testflag = linearity.dolinearityplot(meanAcArray,stdAcArray)

    TestPassed = TestPassed*testflag

    if TestPassed: print 'TEST PASSED'
    else :         print 'TEST FAILED'
