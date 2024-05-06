from simulator import GameSimulator
from randomagent import RandomAgent
from geneagent3 import GeneAgent3
from humanagent import HumanAgent
from scriptagent import ScriptAgent
from govtagent import DummyGovtAgent

import numpy as np
import os
import sys

# import matplotlib.pyplot as plt
# plt.style.use('seaborn-whitegrid')

def loadPopulationFromFile(popSize, generationFolder, startIndex):
    fnombre = generationFolder + "/gen_" + str(startIndex) + ".csv"
    # print(fnombre)
    fp = open(fnombre, "r")
    if fp.closed:
        print(fnombre + " not found")
        quit()

    thePopulation = []

    for i in range(0,popSize):
        line = fp.readline()
        words = line.split(",")

        thePopulation.append(GeneAgent3(words[0]))
        thePopulation[i].count = float(words[1])
        thePopulation[i].rankFitness = float(words[2])
        thePopulation[i].popFitness = float(words[3])

    fp.close()

    return thePopulation

def getSocialWelfare(thePopulation):
    totalSum = 0.0
    totalCount = 0
    for i in range(0, len(thePopulation)):
        if thePopulation[i].count > 0:
            totalSum += thePopulation[i].popFitness * thePopulation[i].count
            totalCount += thePopulation[i].count

    # print(str(totalSum) + " / " + str(totalCount))

    return totalSum / totalCount


def homophilyCategories(thePopulation):
    countHomophilic = 0
    countNone = 0
    countHeterophilic = 0    
    for i in range(0, len(thePopulation)):
        if thePopulation[i].genes_long["homophily"] < 34:
            countHeterophilic = countHeterophilic + 1
        elif thePopulation[i].genes_long["homophily"] > 66:
            countHomophilic = countHomophilic + 1
        else:
            countNone = countNone + 1

    return [countHeterophilic / float(len(thePopulation)), countNone / float(len(thePopulation)), countHomophilic / float(len(thePopulation))]


def visualCategories(thePopulation):
    cuentas = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(0, len(thePopulation)):
        ind = int(thePopulation[i].genes["visualTrait"] / 10)
        if ind == 10:
            ind = 9
        cuentas[ind] = cuentas[ind] + 1

    for i in range(0, 10):
        cuentas[i] = cuentas[i] / float(len(thePopulation))

    return cuentas


def visualCategories2(thePopulation):
    cuentas = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(0, len(thePopulation)):
        ind = int(thePopulation[i].genes["visualTrait"] / 20)
        if ind == 5:
            ind = 4
        cuentas[ind] = cuentas[ind] + 1

    for i in range(0, 5):
        cuentas[i] = cuentas[i] / float(len(thePopulation))

    return cuentas


def logValues(theArgs, values, ventana, nombre):
    fnombre = "../Analysis/csvs/" + nombre + ".csv"
    output = open(fnombre, "w")

    strng = "Round,Item,Value"
    output.write(strng + "\n")

    for i in range(0,len(values),ventana):
        for j in range(4,len(theArgs)):
            val = 0
            c = 0
            for k in range(i-int(ventana/2),i+int(ventana/2)+1):
                val += values[k][j-4]
                c = c+1
            # print(c)
            output.write(str(i) + "," + theArgs[j] + "," + str(val/(c)) + "\n")

    output.close()


def appendValues(theArgs, values, ventana, nombre):
    fnombre = "../Analysis/csvs/" + nombre + ".csv"
    output = open(fnombre, "a")

    # print out first generation
    for j in range(4,len(theArgs)):
        output.write("1," + theArgs[j] + "," + str(values[0][j-4]) + "\n")

    for i in range(0,len(values),ventana):
        for j in range(4,len(theArgs)):
            val = 0
            c = 0
            for k in range(i,i+ventana):
                val += values[k][j-4]
                c = c+1
            # print(c)
            output.write(str(i+ventana) + "," + theArgs[j] + "," + str(val/(c)) + "\n")

    output.close()



# python3 plotGenes.py [generationFolder] [popSize] [maxGen] [list of things to track]
if __name__ == '__main__':
    num = 1
    if sys.argv[1][0:3] == "all":
        num = 10

    # set up the header
    fnombre = "../Analysis/csvs/out.csv"
    output = open(fnombre, "w")
    strng = "Generation,Item,Value\n"
    output.write(strng)
    output.close()

    smoother = 1

    for v in range(1,num+1):
        theFolder = sys.argv[1]
        if theFolder[0:3] == "all":
            theFolder = "../Results/theGenerations_v" + str(v) + "_11"

        popSize = int(sys.argv[2])
        maxGen = int(sys.argv[3])

        for t in range(0, maxGen):
            thePopulation = loadPopulationFromFile(popSize, theFolder, t)

            tracking = []
            for i in range(4, len(sys.argv)):
                if sys.argv[i] == "socialWelfare":
                    tracking.append(getSocialWelfare(thePopulation))
                else:        
                    sum = 0.0
                    for a in thePopulation:
                        sum += a.genes_long[sys.argv[i]]
                    tracking.append(sum / popSize)

            if t == 0:
                values = [tracking]
            else:
                values.append(tracking)

            if t == 0:
                homophily = [homophilyCategories(thePopulation)]
            else:
                homophily.append(homophilyCategories(thePopulation))

            # if t == 0:
            #     visual = [visualCategories2(thePopulation)]
            # else:
            #     visual.append(visualCategories2(thePopulation))
            

        appendValues(sys.argv, values, smoother, "out")
        # logValues(sys.argv, values, 1, "out")

        strngs = ["--", "--", "--", "--", "Heterophilic", "Unbiased", "Homophilic"]
        if num > 1:    
            appendValues(strngs, homophily, smoother, "homophily")
        else:
            logValues(strngs, homophily, smoother, "homophily")

        # # strngs = ["--", "--", "--", "--", "0-9", "10-19", "20-29", "30-39", "40-49", "50-59", "60-69", "70-79", "80-89", "90-100"]
        # strngs = ["--", "--", "--", "--", "0-19", "20-39", "40-59", "60-79", "80-100"]
        # logValues(strngs, visual, 1, "visualCounts")


    # fig = plt.figure()
    # ax = plt.axes()
    # x = np.linspace(1,400,400)
    # ax.plot(x, socWelfare)
    # plt.show()

