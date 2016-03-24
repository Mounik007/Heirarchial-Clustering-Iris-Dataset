# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 23:18:39 2015

@author: mounik
"""

import heapq
import math
import itertools
import sys
import csv

heapq.heap = []

def ComputeEucDistaceTwoPoints(lstCordFirstPoint, lstCordSecondPoint, posFirstPoint, posSecondPoint):
    distance = 0
    lstTempValues =[]
    for subIndex in range(len(lstCordFirstPoint)):
        diff = 0
        diff = float(lstCordFirstPoint[subIndex])-float(lstCordSecondPoint[subIndex])
        diff = diff*diff
        distance += diff
    finalDistance = math.sqrt(distance)
    lstTempValues.append(finalDistance)
    lstTempValues.append(posFirstPoint)
    lstTempValues.append(posSecondPoint)
    return lstTempValues

def ComputeHeirCluster(dictPositionInput, numberOfCluster):
    lstOmniList = []
    lstInputToHeap = []
    lstClusterList = []
    lstPresentValues = []
    dictClusters = {}
    dicChangePositionInput = {}
    dicChangePositionInput = dictPositionInput.copy()
    lstOmniList.append(list(dictPositionInput))
    for index in range(len(dictPositionInput)):
        for indexA in range(index+1, len(dictPositionInput)):
            lstInputToHeap.append(ComputeEucDistaceTwoPoints(dictPositionInput[str(index)], dictPositionInput[str(indexA)], index, indexA))
    
    for dictKeys in dictPositionInput.iterkeys():
        lstClusterList.append(dictKeys)
        
    lstClusterList =sorted(lstClusterList)
    for singItem in lstInputToHeap:
        heapq.heappush(heapq.heap, singItem)
    
    mergePassCounter =0
    """Two logics have been implemented, Uncomment the below while loop for a different logic, also comment the present uncommented while loop"""
    while(mergePassCounter < (len(dictPositionInput)-1)):
    #while(len(heapq.heap) > 0):
        heapItem = heapq.heappop(heapq.heap)
        itemAldreadyMerged = 0            
        clusterItemCountA = 0
        for clusterItemA in lstClusterList:
            if(clusterItemA == str(heapItem[1])):
                clusterItemCountA +=1
            
        clusterItemCountB = 0
        for clusterItemB in lstClusterList:
            if(clusterItemB == str(heapItem[2])):
                clusterItemCountB +=1
            
        if(clusterItemCountA ==1 and clusterItemCountB == 1):
            lstClusterList.remove(str(heapItem[1]))
            dicChangePositionInput.pop(str(heapItem[1]),None)
            lstClusterList.remove(str(heapItem[2]))
            dicChangePositionInput.pop(str(heapItem[2]),None)
            itemAldreadyMerged = 0
        else:
            itemAldreadyMerged =1
            
            
                    
        if(itemAldreadyMerged==0):
            lstTempClusList = []
            mergePassCounter += 1
            lstTwoDigits = []
            lstTwoDigits.append(str(heapItem[1]))
            lstTwoDigits.append(str(heapItem[2]))
            lstTempClusList.append(list(lstTwoDigits))
            lstTempClusList = list(itertools.chain(*lstTempClusList))
            lstTempClusList = [x for x in lstTempClusList if x != ',']
            lstTempClusList = sorted(lstTempClusList)
            dictClusters[mergePassCounter] = lstTempClusList
            """ Computation Of Centroid"""
            lstCentroidList = []
            lstCentroidCoordinates = []
            for element in lstTempClusList:
                lstElement=[]
                lstElement = element.split(',')
                for singItem in lstElement:
                    lstCentroidList.append(dictPositionInput[str(singItem)])
                
            for indexCord in range(len(lstCentroidList[0])):
                centroidSum=0
                for subIndA in range(len(lstCentroidList)):
                    centroidSum+= float(lstCentroidList[subIndA][indexCord])
                centroidValue = centroidSum/(len(lstCentroidList))
                lstCentroidCoordinates.append(centroidValue)
                
            """Computation Of New Distances In the Cluster with the new merged element"""            
            strInsertKeyDict = ','.join(lstTempClusList)
            dicChangePositionInput[strInsertKeyDict]= lstCentroidCoordinates
            lstDicChangePosition = []
            lstDicChangePosition = list(dicChangePositionInput)
            lstOmniList.append(lstDicChangePosition)
            lstPresentValues = []
            for key in dicChangePositionInput.iterkeys():
                if(dicChangePositionInput[strInsertKeyDict] != dicChangePositionInput[key]):
                    lstPresentValues.append(ComputeEucDistaceTwoPoints(dicChangePositionInput[strInsertKeyDict], dicChangePositionInput[key], strInsertKeyDict , str(key)))
            lstClusterList.append(strInsertKeyDict)
            lstClusterList = sorted(lstClusterList)
            for valueList in lstPresentValues:
                    heapq.heappush(heapq.heap, valueList)
           
    lstDesiredClusters =[]
    lstAlgoPairs = []
    if(len(lstOmniList)!= numberOfCluster):
        for subStr in lstOmniList[len(lstOmniList)-numberOfCluster]:
            lstTempSubStr = []
            lstTempSubStr = subStr.split(',')
            lstTempSubStr = sorted(lstTempSubStr, key = lambda x: int(x))
            lstDesiredClusters.append(lstTempSubStr)
            for pairSubA in range(len(lstTempSubStr)):
                for pairSubB in range(pairSubA+1,len(lstTempSubStr)):
                    lstTempAlgoPairs = []
                    lstTempAlgoPairs.append(int(lstTempSubStr[pairSubA]))
                    lstTempAlgoPairs.append(int(lstTempSubStr[pairSubB]))
                    lstAlgoPairs.append(lstTempAlgoPairs)
    
    else:
        for subStrZero in lstOmniList[len(lstOmniList)-numberOfCluster]:
            lstTempStrZero = []
            lstTempStrZero = subStrZero.split(',')
            lstTempSubStr = sorted(lstTempStrZero, key = lambda x: int(x))
            lstDesiredClusters.append(lstTempSubStr)
    
           
    return lstAlgoPairs, lstDesiredClusters      
            
                

if __name__=='__main__':
    lstInputData = []
    dictCalcPosition = {}
    dictPositionInput={}
    numberOfCluster = int(sys.argv[2])
    with open(sys.argv[1]) as tsvfile:
        tsvReader = csv.reader(tsvfile, delimiter="\n")
        for line in tsvReader:
            tempStr = (str(line)).replace("[", "").replace("]","").replace("'","")
            lstTempItem = tempStr.split(",")
            lstInputData.append(lstTempItem)
    
    for index in range(len(lstInputData)):
        lstTempInp = []
        if not lstInputData[index][4] in dictPositionInput:
            lstTempInp.append(index)
            dictPositionInput[str(lstInputData[index][4])] =lstTempInp 
        else:
            dictPositionInput[str(lstInputData[index][4])].append(index)
        
    lstGoldStandardPairs = []
    for keyPos in dictPositionInput:
        for keyIndexA in range(len(dictPositionInput[keyPos])):
            for keyIndexB in range(keyIndexA+1,len(dictPositionInput[keyPos])):
                lstTempGoldStd = []
                lstTempGoldStd.append(dictPositionInput[keyPos][keyIndexA])
                lstTempGoldStd.append(dictPositionInput[keyPos][keyIndexB])
                lstGoldStandardPairs.append(lstTempGoldStd)
    
    for item in lstInputData:
        del item[4]
    for ind in range(len(lstInputData)):
        ind1= str(ind)
        dictCalcPosition[str(ind)] = lstInputData[ind]
    
    if((len(dictCalcPosition) >= numberOfCluster) and (numberOfCluster != 0)):
        lstAlgoGeneratedPairs = []
        lstDesiredGeneratedCluster = []
        lstAlgoGeneratedPairs, lstDesiredGeneratedCluster = ComputeHeirCluster(dictCalcPosition,numberOfCluster)
    
        commonPairCounter = 0
        for algoPair in lstAlgoGeneratedPairs:
            for goldPair in lstGoldStandardPairs:
                if(algoPair == goldPair):
                    commonPairCounter += 1
        if(len(lstAlgoGeneratedPairs) !=0):
            precision = float(commonPairCounter)/float(len(lstAlgoGeneratedPairs))
        else:
            precision=0
        print(precision)
        if(len(lstGoldStandardPairs)!=0):
            recall = float(commonPairCounter)/float(len(lstGoldStandardPairs))
        else:
            recall = 0
        print(recall)  
        for desList in lstDesiredGeneratedCluster:
            print(desList)
    elif((len(dictCalcPosition) < numberOfCluster)):
        print("There are no clusters available as algorithm can perform a maximum of "+(str(len(dictCalcPosition)-1))+" merges. The maximum number of clusters available is "+str(len(dictCalcPosition)))
    
    elif(numberOfCluster == 0):
        print("There can be no zero cluster")