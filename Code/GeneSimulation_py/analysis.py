from engine import JHGEngine
from sklearn.preprocessing import normalize

import numpy as np

def computeGini(P):
    P.sort()
    # print(P)

    totalWealth = sum(P)
    wealth = 0
    area = 0
    for i in range(0,len(P)):
        newWealth = wealth + P[i]
        area = area + (1.0 / len(P)) * (((wealth + newWealth) / 2.0) / totalWealth)
        wealth = newWealth
        percentile = (i+1) / len(P)
        #print("wealth: " + str(wealth) + "; percentile: " + str(percentile))

    return (0.5 - area) / 0.5

def computeGini2(P):
    sum = 0.0
    m = 0.0
    for i in range(0, len(P)):
        m = m + P[i]
        for j in range(0, len(P)):
            sum = sum + abs(P[i] - P[j])
    m = m / len(P)

    return sum / (2 * len(P) * len(P) * m)

        

def computeGenOutcomes(genNum, v, numGames):
    engine = JHGEngine(0.2, 0.5, 1.3, 0.95, 1.6, 11, 100)
    socialWelfare = 0
    giniIndex = 0
    giniIndex2 = 0
    for i in range(0,20):
        fnombre = "../Results/theGameLogs_v" + str(v) + "_11/log_" + str(genNum) + "_" + str(i) + ".csv"
        engine.readGameFromFile(fnombre)
        socialWelfare = socialWelfare + sum(engine.P[engine.t])
        giniIndex = giniIndex + computeGini(engine.P[engine.t])
        giniIndex2 = giniIndex2 + computeGini2(engine.P[engine.t])

    return socialWelfare / (11 * numGames), giniIndex / numGames, giniIndex2 / numGames

def computeGeneralTrends():
    f = open("../Analysis/csvs/generalTrends11_all.csv", "w")
    f.write("Generation,Item,Value\n")
    smooth = 10

    for theSims in range(1,11):
        print()
        print("Evolutionary Simulation: " + str(theSims))
        socWel = []
        giniInd = []
        for g in range(0,200):
            sw, gini, gini2 = computeGenOutcomes(g, theSims, 20)
            print("   g" + str(g) + ": " + str(sw) + "; " + str(gini) + "; " + str(gini2))
            socWel.append(sw)
            giniInd.append(gini)
            
        f.write("1,socialWelfare," + str(socWel[0]) + "\n")
        f.write("1,giniIndex," + str(giniInd[0]) + "\n")
        for i in range(0, 200, smooth):
            lower = i
            denom = smooth
            if i == 0:
                lower = 1
                denom = smooth-1
            f.write(str(i+smooth) + ",socialWelfare," + str(sum(socWel[lower:(i+smooth)])/denom) + "\n")
            f.write(str(i+smooth) + ",giniIndex," + str(sum(giniInd[lower:(i+smooth)])/denom) + "\n")

    f.close()

    engine = JHGEngine(0.2, 0.5, 1.3, 0.95, 1.6, 11, 100)
    engine.readGameFromFile("../Results/theGameLogs_v1_11/log_0_0.csv")

    print("Total rounds: " + str(engine.t))
    socialWelfare = sum(engine.P[engine.t]) / 11
    print("average social welfare: " + str(socialWelfare))

    giniIndex = computeGini(engine.P[engine.t])
    print("Gini index: " + str(giniIndex))

    # P = [84, 1294, 714, 337, 63, 995, 236, 625, 12, 392, 1306]
    # P = [0, 0, 0, 0, 100]
    # P = [424.44931205999285,42.66352416160073,332.01933681955717,741.6423469879162,146.75847340984677,441.56472605597514,734.0063457819193,323.3641451759319,642.4633194981396,118.24673979887999]
    # P = [931.1412390586152,506.07433932745465,50.15958441957256,441.8697748325831,864.098194694786,349.9678429887779,59.971927870859005,334.3043664535227,826.5707513322909,567.0520084819152]
    # P = [1064.4737250434036,934.8002246346578,450.358809879163,306.21687933681386,196.32550506447495,2105.7403640818425,715.5237276795461,333.66253901127567,1883.9009628974786,294.4040759889461]
    # print(computeGini(P))
    # print(computeGini2(P))

def tokenTrends(genNum, v, gameNum):
    engine = JHGEngine(0.2, 0.5, 1.3, 0.95, 1.6, 11, 100)
    fnombre = "../Results/theGameLogs_v" + str(v) + "_11/log_" + str(genNum) + "_" + str(gameNum) + ".csv"
    engine.readGameFromFile(fnombre)

    kept = 0.0
    gave = 0.0
    stole = 0.0
    for t in range(1,41):                   # for each round
        for i in range(0,11):               # see how much each player kept, gave, and stole
            kept = kept + engine.T[t][i][i]
            gave = gave + (sum(engine.T[t][i].clip(0)) - engine.T[t][i][i]) 
            stole = stole + sum(np.negative(engine.T[t][i]).clip(0))

    percentKept = kept / (40 * 11)
    percentGave = gave / (40 * 11)
    percentStole = stole / (40 * 11)
    # print("percentKept in " + str(genNum) + "_v" + str(v) + "_" + str(gameNum) + ": " + str(percentKept)) 
    # print("percentGave in " + str(genNum) + "_v" + str(v) + "_" + str(gameNum) + ": " + str(percentGave)) 
    # print("percentStole in " + str(genNum) + "_v" + str(v) + "_" + str(gameNum) + ": " + str(percentStole)) 
    return percentKept, percentGave, percentStole

def computeTokenAllocations():
    f = open("../Analysis/csvs/generalTokenAllocs.csv", "w")
    f.write("Generation,simVersion,Proportion,Value\n")

    for simVersion in range(1,11):
        print("Simulation " + str(simVersion))
        for gen in range(0,200,5):
            keptSum = 0.0
            gaveSum = 0.0
            stoleSum = 0.0
            for i in range(0,20):
                kept,gave,stole = tokenTrends(gen, simVersion, i)
                keptSum = keptSum + kept
                gaveSum = gaveSum + gave
                stoleSum = stoleSum + stole
            f.write(str(gen+1) + "," + str(simVersion) + ",kept," + str(keptSum / 20) + "\n")
            f.write(str(gen+1) + "," + str(simVersion) + ",gave," + str(gaveSum / 20) + "\n")
            f.write(str(gen+1) + "," + str(simVersion) + ",stole," + str(stoleSum / 20) + "\n")

        # do it for the last generation
        gen = 199
        keptSum = 0.0
        gaveSum = 0.0
        stoleSum = 0.0
        for i in range(0,20):
            kept,gave,stole = tokenTrends(gen, simVersion, i)
            keptSum = keptSum + kept
            gaveSum = gaveSum + gave
            stoleSum = stoleSum + stole
        f.write(str(gen+1) + "," + str(simVersion) + ",Keep," + str(keptSum / 20) + "\n")
        f.write(str(gen+1) + "," + str(simVersion) + ",Give," + str(gaveSum / 20) + "\n")
        f.write(str(gen+1) + "," + str(simVersion) + ",Attack," + str(stoleSum / 20) + "\n")


    f.close()

def computeReciprocated(simVersion, genNum, gameNum):
    engine = JHGEngine(0.2, 0.5, 1.3, 0.95, 1.6, 11, 100)
    fnombre = "../Results/theGameLogs_v" + str(simVersion) + "_11/log_" + str(genNum) + "_" + str(gameNum) + ".csv"
    engine.readGameFromFile(fnombre)

    este = np.zeros((11, 11), dtype=float)
    for t in range(0,41):
        for i in range(0,11):
            for j in range(0,11):
                if i != j:
                    if (engine.T[t][i][j] >= 0.0):
                        este[i][j] += engine.T[t][i][j] * engine.P[t-1][i] * engine.C_g
                # else:
                    # este[t][i][j] = engine.T[t][i][j] * engine.P[t-1][i] * engine.C_s

    menos = np.zeros((11, 11), dtype=float)
    for i in range(0,11):
        for j in range(0,11):
            menos[i][j] = este[i][j] - este[j][i]
            if menos[i][j] < 0:
                menos[i][j] = 0


    # print(este)
    # print()
    # print(menos)
    # print()
    # print()
    sum_menos = sum(sum(menos))
    sum_este = sum(sum(este))
    # print(sum_menos)
    # print(sum_este)
    # print((sum_este - sum_menos) / sum_este)
                
    return (sum_este - sum_menos) / sum_este
                    
                
def adjacencyMatrices(simVersion, genNum, gameNum):
    engine = JHGEngine(0.2, 0.5, 1.3, 0.95, 1.6, 11, 100)
    fnombre = "../Results/theGameLogs_v" + str(simVersion) + "_11/log_" + str(genNum) + "_" + str(gameNum) + ".csv"
    engine.readGameFromFile(fnombre)
    engine2 = JHGEngine(0.2, 0.5, 1.3, 0.95, 1.6, 11, 100)
    for t in range(1,41):
        # print()
        # print(engine.P[t])
        # print(engine.T[t])
        engine2.apply_transaction(engine.T[t])
        # print(engine2.P[t])

    np.set_printoptions(formatter={'float': lambda x: "{0:0.1f}".format(x)})

    threshold = (1.0 / engine.N) * 1.0

    A = []
    Aeste = np.zeros((11, 11), dtype=float)
    A.append(Aeste)
    for t in range(1,41):
        # print()
        # print(t)
        # print(A)
        Aeste2 = normalize(engine2.I[t], axis=1, norm='l1')
        Aeste2[Aeste2 < threshold] = 0
        Aeste2[Aeste2 >= threshold] = 1
        np.fill_diagonal(Aeste2, 0.0)
        A.append(Aeste2)

        # print(A[t])
        
        # print()
        # print("Round: " + str(t))
        # print(engine2.I[t])
        # print()
        # print(Aeste)
        # print()
        # print(engine.P[t-1])

    return A
        
def averageNumFriends(A):
    return sum(sum(sum(A))) / (40*11)

def computeDegree():
    f = open("../Analysis/csvs/numFriends.csv", "w")
    f.write("simVersion,Generation,Friends\n")

    for simVersion in range(1,11):
        print("simVersion: " + str(simVersion))
        gen = 0
        theSum = 0.0
        for gm in range(0,20):
            A = adjacencyMatrices(simVersion, gen, gm)
            theSum = theSum + averageNumFriends(A)
        f.write(str(simVersion) + "," + str(gen) + "," + str(theSum / 20) + "\n")
        print("  " + str(gen+1) + ": " + str(theSum / 20))

        for gen in range(4,200,5):
            theSum = 0.0
            for gm in range(0,20):
                A = adjacencyMatrices(simVersion, gen, gm)
                theSum = theSum + averageNumFriends(A)
            f.write(str(simVersion) + "," + str(gen) + "," + str(theSum / 20) + "\n")
            print("  " + str(gen+1) + ": " + str(theSum / 20))


    f.close()

def overLaps(A, player_idx):
    yes = [0, 0]
    no = [0, 0]
    for j in range(0, 11):
        if j == player_idx:
            continue

        v = np.copy(A[j])
        v[player_idx] = 0
        if A[player_idx][j] == 1.0:  # computing yes's
            yes[1] = yes[1] + sum(v)
            yes[0] = yes[0] + np.dot(A[player_idx], v)
        else:
            no[1] = no[1] + sum(v)
            no[0] = no[0] + np.dot(A[player_idx], v)

    print(yes)
    print(no)

    return (yes[0] / yes[1]), (no[0] / no[1])



def computeFriendOverlap():
    A = adjacencyMatrices(4, 100, 0)
    print(A[20])

    for i in range(0,11):
        print()
        overLaps(A[20], i)

    


if __name__ == '__main__':
    # generalTrends()
    # computeTokenAllocations()

    # for g in range(0,20):
    #     print(computeReciprocated(1, 9, g))

    # computeDegree()
    computeFriendOverlap()

