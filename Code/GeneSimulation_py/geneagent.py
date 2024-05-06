from baseagent import AbstractAgent
import random
import numpy as np
import heapq
import sys
import math

# np.set_printoptions(precision=2)
# np.set_printoptions(suppress=True)

class GeneAgent(AbstractAgent):

    def __init__(self, geneStr):
        super().__init__()
        self.whoami = "gene"
        if geneStr == "":
            # set up an agent with a random genotype
            self.genes = {
                "priorityRandom": np.random.randint(0,101),
                "priorityDefend": np.random.randint(0,101),
                "priorityPosDirRecip": np.random.randint(0,101),
                "priorityNegDirRecip": np.random.randint(0,101),
                "priorityFirstOrderGive": np.random.randint(0,101),
                "priorityIncreaseFriendship": np.random.randint(0,101),
                "priorityPosTriadicClosure": np.random.randint(0,101),
                "priorityNegTriadicClosure": np.random.randint(0,101),
                "priorityPillage": np.random.randint(0,101),
                "priorityWar": np.random.randint(0,101),
                "priorityJoinWar": np.random.randint(0,101),
                "posDirRecipBasis": np.random.randint(0,101),
                "negDirRecipBasis": np.random.randint(0,101),
                "firstOrderGiveBasis": np.random.randint(0,101),
                "visualTrait": np.random.randint(0,101),
                "visualHomophily": np.random.randint(0,101),
                "otherishDebtLimits": np.random.randint(0,101),
                "randomKeep": np.random.randint(0,101),
                "randomNeg": np.random.randint(0,101),
                "initialDefense": np.random.randint(0,101),
                "defensePropensity": np.random.randint(0,101),
                "defenseUpdate": np.random.randint(0,101),
                "negDirRecipMultiplier": np.random.randint(0,101),
                "firstOrderGiveTokens": np.random.randint(0,101),
                "firstOrderGiveMode": np.random.randint(0,101),
                "firstOrderGiveBesties": np.random.randint(0,101),
                "firstOrderGiveMax": np.random.randint(0,101),
                "posTriadicClosureTokens": np.random.randint(0,101),
                "posTriadicWealthMin": np.random.randint(0,101),
                "negTriadicAttackThreshold": np.random.randint(0,101),
                "pillageLow": 10,
                "pillageHigh": np.random.randint(0,101),
                "pillageFury": np.random.randint(0,101),
                "warHigh": np.random.randint(0,101),
                "warFury": np.random.randint(0,101),
                "warDelay": np.random.randint(0,101)
            }

        else:
            # read geneStr to set up the genotype
            words = geneStr.split("_")
            self.genes = {
                "priorityRandom": int(words[1]),
                "priorityDefend": int(words[2]),                
                "priorityPosDirRecip": int(words[3]), 
                "priorityNegDirRecip": int(words[4]),
                "priorityFirstOrderGive": int(words[5]),
                "priorityIncreaseFriendship": int(words[6]),
                "priorityPosTriadicClosure": int(words[7]),
                "priorityNegTriadicClosure": int(words[8]),
                "priorityPillage": int(words[9]),
                "priorityWar": int(words[10]),
                "priorityJoinWar": int(words[11]),
                "posDirRecipBasis": int(words[12]),
                "negDirRecipBasis": int(words[13]),
                "firstOrderGiveBasis": int(words[14]),
                "visualTrait": int(words[15]),
                "visualHomophily": int(words[16]),
                "otherishDebtLimits": int(words[17]),
                "randomKeep": int(words[18]),
                "randomNeg": int(words[19]),
                "initialDefense": int(words[20]),
                "defensePropensity": int(words[21]),
                "defenseUpdate": int(words[22]),
                "negDirRecipMultiplier": int(words[23]),
                "firstOrderGiveTokens": int(words[24]),
                "firstOrderGiveMode": int(words[25]),
                "firstOrderGiveBesties": int(words[26]),
                "firstOrderGiveMax": int(words[27]),
                "posTriadicClosureTokens": int(words[28]),
                "posTriadicWealthMin": int(words[29]),
                "negTriadicAttackThreshold": int(words[30]),
                "pillageLow": int(words[31]),
                "pillageHigh": int(words[32]),
                "pillageFury": int(words[33]),
                "warHigh": int(words[34]),
                "warFury": int(words[35]),
                "warDelay": int(words[36])
            }

        self.genes["pillageLow"] = 10

        # if np.random.randint(0,4) == 0:
        #     self.genes["visualTrait"] = 100

        self.count = 0
        self.rankFitness = 0.0
        self.popFitness = 0.0

        self.gameParams = {}

    def setGameParams(self, gameParams, visualTraits, _forcedRandom):
        self.gameParams = gameParams
        numPlayers = len(visualTraits)

        self.visualSimilarityScores = np.zeros((numPlayers, numPlayers), dtype=float)
        for i in range(0, numPlayers):
            for j in range(0, numPlayers):
                if i == j:
                    self.visualSimilarityScores[i][j] = 0
                else:
                    self.visualSimilarityScores[i][j] = self.getSimilarityScore(visualTraits[i], visualTraits[j])
                    self.visualSimilarityScores[j][i] = self.visualSimilarityScores[i][j]

        # print(visualTraits)
        # print(self.visualSimilarityScores)
        # print()

    def getSimilarityScore(self, vt1, vt2):
        diff = abs(vt1 - vt2)
        if diff >= 20:
            score = 0
        else:
            score = (20.0 - diff) / 20.0
    
        return score

    def mutate(self, mutateProb):
        for key in self.genes:
            numb = np.random.uniform(0,1)
            if (numb < mutateProb):
                self.genes[key] = np.random.randint(0,101)
    
    def splice(self, p):
        empieza = np.random.randint(0,len(self.genes))
        fin = np.random.randint(0, len(self.genes)-empieza) + (empieza + 1)
        c = 0
        for key in self.genes:
            if (c >= empieza) and (c < fin):
                self.genes[key] = p.genes[key]
            c = c + 1

    def getString(self):
        theStr = "genes"
        for key in self.genes:
            theStr = theStr + "_" + str(self.genes[key])

        return theStr

    def play_round(self, player_idx, round_num, received, popularities, influence, extra_data):
        numPlayers = len(popularities)
        numTokens = 2 * numPlayers
        heap = []

        # if player_idx >= 11:
        #     self.setWarrior()
        # elif (player_idx > 11):# and (player_idx < 11):
        #     self.setWarrior2()

        if round_num == 0:
            self.govPlayer = self.determineGovment(numPlayers, extra_data)

        self.computeUsefulQuantities(round_num, player_idx, numPlayers, received, popularities, influence)

        # print("player " + str(player_idx))

        # add the fail safe
        trans = self.createPotentialTransaction([player_idx], [numTokens])
        heapq.heappush(heap, (100, id(trans), trans))
        trans = self.createPotentialTransaction([player_idx], [numTokens])
        heapq.heappush(heap, (100, id(trans), trans))

        if round_num == 0:
            # print(self.getString())

            # Set specific parameters
            # if player_idx > 7:
            #     self.setPillagerParameters()
            # elif player_idx < 6:
            #     self.setGoodCitizenParameters()

            self.prevAllocations3 = np.zeros(numPlayers)
            self.prevAllocations2 = np.zeros(numPlayers)
            self.prevAllocations1 = np.zeros(numPlayers)

            # figure out what to do
            self.doRandomAllocations(player_idx, numPlayers, numTokens, heap)
            self.erectDefenses(round_num, player_idx, numPlayers, numTokens, received, popularities, heap)
        else:
            # if player_idx == 0:
            #     print("received: " + str(received * 2 * numPlayers))

            # if player_idx == 0:
            #     print()
            #     print("Round: " + str(round_num))
            #     print(self.friendshipChop)

            # figure out what to do
            self.doRandomAllocations(player_idx, numPlayers, numTokens, heap)
            self.erectDefenses(round_num, player_idx, numPlayers, numTokens, received, popularities, heap)
            self.doPosDirRecip(popularities, received, influence, player_idx, numPlayers, numTokens, heap)
            self.doNegDirRecip(popularities, influence, player_idx, numPlayers, numTokens, heap)
            self.firstOrderGive(popularities, player_idx, numPlayers, numTokens, heap)
            self.increaseFriendships(popularities, player_idx, numPlayers, numTokens, heap)
            self.triadicAction(popularities, influence, player_idx, numPlayers, numTokens, heap)
            self.pillageTheVillage(player_idx, numPlayers, numTokens, popularities, influence, heap)
            self.startWar(round_num, player_idx, numPlayers, numTokens, popularities, influence, heap)
            self.joinWar(round_num, player_idx, numPlayers, numTokens, popularities, influence, heap)
            

            # sys.exit(1)

        # if player_idx == 1:
        #     print()
        #     print(len(heap))
        #     for i in range(0,len(heap)):
        #         print(heap[i])

        transaction_vec = self.allocateTokens(player_idx, numPlayers, numTokens, popularities, heap)

        original = np.copy(transaction_vec)
        # if round_num > 2:
        #     transaction_vec = self.smoothTokenAllocation2Friends(player_idx, numPlayers, numTokens, transaction_vec)

        alocacion = np.linalg.norm(transaction_vec, ord=1)

        if abs(alocacion - numTokens) > 0.001:
            print(str(player_idx) + ": " + str(alocacion))
            print(transaction_vec)
            print(original)
            exit(1)

        # if player_idx == 1:
        # freedTokens, transaction_vec = self.pruneOtherishGivingDebtLimits(player_idx, numPlayers, numTokens, transaction_vec, popularities)
        # while freedTokens > 0:
        #     # print(freedTokens)
        #     transaction_vec = self.allocateTokens(numPlayers, freedTokens, transaction_vec, heap)
        #     freedTokens, transaction_vec = self.pruneOtherishGivingDebtLimits(player_idx, numPlayers, numTokens, transaction_vec, popularities)

        self.updateIndebtedness(round_num, player_idx, transaction_vec, popularities)

        self.prevPopularities = popularities
        self.prevInfluence = influence
        self.prevAllocations = transaction_vec

        self.prevAllocations3 = self.prevAllocations2
        self.prevAllocations2 = self.prevAllocations1
        self.prevAllocations1 = original


        # print(transaction_vec)

        if transaction_vec[player_idx] < 0:
            print(str(player_idx) + " is stealing from self!!!")

        return transaction_vec


    def determineGovment(self, numPlayers, extra_data):
        isGovment = np.zeros(numPlayers, dtype=int)
        taxes = {}
        for p_id, data in extra_data.items():
            if data is not None and data.get('is_government', False):
                isGovment[int(p_id)] = 1

        return isGovment


    # def get_my_taxes(self, extra_data):
    #     taxes = {}
    #     for p_id, data in extra_data.items():
    #         if data is not None and data.get('is_government', False):
    #             taxes[p_id] = data.get('taxes', 0.)
    #     return taxes


    # def findMyGroup(self, player_idx):
    #     for key in self.theGroups:
    #         if player_idx in self.theGroups[key]:
    #             return key
        
    #     print("my group not found")
    #     return -99999


    def computeUsefulQuantities(self, round_num, player_idx, numPlayers, received, popularities, influence):
        self.totalWelfare = sum(popularities)

        if round_num > 0:
            # update some values
            # if round_num == 1:
            #     self.receiving = received
            # else:
            #     c = self.genes["pillageReceivedUpdate"] / 100.0
            #     self.receiving = ((1-c) * self.receiving) + (c * received)

            for i in range(0, numPlayers):
                if i != player_idx:
                    if self.prevAllocations[i] < 0:
                        self.attacksWithMe += np.negative(np.negative(influence[:,i]).clip(0)) - np.negative(np.negative(self.prevInfluence[:,i]).clip(0))

            # make copies of the old
            self.infl_pos_prev = np.copy(self.infl_pos)
            self.infl_neg_prev = np.copy(self.infl_neg)

            self.infl_pos_sumrow_prev = np.copy(self.infl_pos_sumrow)
            self.infl_neg_sumrow_prev = np.copy(self.infl_neg_sumrow)

            self.infl_pos_sumcol_prev = np.copy(self.infl_pos_sumcol)
            self.infl_neg_sumcol_prev = np.copy(self.infl_neg_sumcol)
        else:
            # initialize some variables
            self.tally = np.zeros(numPlayers, dtype=float)
            self.expectedReturn = np.zeros(numPlayers, dtype=float)
            # self.receiving = np.zeros(numPlayers, dtype=float)
            self.attacksWithMe = np.zeros(numPlayers, dtype=float)

        # update
        self.infl_pos = np.positive(influence).clip(0)
        self.infl_neg = np.negative(influence).clip(0)

        self.infl_pos_sumrow = self.infl_pos.sum(axis=1)
        self.infl_neg_sumrow = self.infl_neg.sum(axis=1)

        self.infl_pos_sumcol = self.infl_pos.sum(axis=0)
        self.infl_neg_sumcol = self.infl_neg.sum(axis=0)

        if round_num > 0:
            # compute friendship
            distributionRatio = 1 - (np.sum(np.diag(self.infl_pos)[1:]) / np.sum(self.infl_pos))
            if distributionRatio == 0:
                distributionRatio = 0.001
            self.friendship = np.zeros((numPlayers, numPlayers), dtype=float)   # self.friendship[i][j] is the friendship that i shows toward j
            self.friendshipChop = np.zeros((numPlayers, numPlayers), dtype=float)
            self.collectiveStrength = np.zeros(numPlayers, dtype=float)

            minCollective = (self.genes["posTriadicWealthMin"] + 1.0) / 101.0
            # if player_idx == 0:
            #     print(minCollective)
            totalPop = self.totalWelfare    
            for i in range(0, numPlayers):
                if self.govPlayer[i] == 1:
                    continue

                mxtarg = self.infl_pos_sumcol[i] / (numPlayers * minCollective)
                mntarg = self.infl_pos_sumcol[i] / numPlayers

                # if player_idx == 0:
                #     print(str(mxtarg) + "; " + str(mntarg))

                for j in range(0, numPlayers):
                    if j == i:
                        self.friendship[j][i] = 1
                    elif influence[j][i] > mntarg:
                        if mxtarg == mntarg:
                            self.friendship[j][i] = influence[j][i] / mntarg
                        else:
                            self.friendship[j][i] = (influence[j][i] - mntarg) / (mxtarg - mntarg)

                    self.friendshipChop[j][i] = self.friendship[j][i]
                    if self.friendship[j][i] > 1.0:
                        self.friendshipChop[j][i] = 1.0

            # if player_idx == 0:
            #     print(self.friendshipChop[:,player_idx])
            self.fOverlap = np.zeros(numPlayers, dtype=float)
            for i in range(0, numPlayers):
                self.collectiveStrength[i] = np.dot(self.friendshipChop[:,i], popularities) / self.totalWelfare
                self.fOverlap[i] = self.friendOverLap(player_idx, i, numPlayers)

            # if player_idx == 0:
            #     print("\nFriendship")
            #     print(self.friendshipChop)
            #     print("\nOverlap")
            # print(self.fOverlap)                


    # what proportion of connection does other_idx have that player_idx also has
    def friendOverLap(self, player_idx, other_idx, numPlayers):

        # print("need to test modified friendOverLap()")

        # go through the columns of the influence matrix to see how much of what I received is the same as what the other receives
        total = 0.0
        mismo = 0.0
        for i in range(0, numPlayers):
            if self.govPlayer[i] == 1:
                continue

            if i == player_idx:
                continue

            # cantidadContenido = self.friendshipChop[i][player_idx] * self.infl_pos[i][other_idx]
            # mismo += cantidadContenido

            if self.isFriend(player_idx, i):
                mismo += self.infl_pos[i][other_idx]
            else:
                otherHasAdditional = self.infl_pos[i][other_idx] - self.infl_pos[i][player_idx]
                if otherHasAdditional < 0.0:
                    otherHasAdditional = 0.0

                mismo += self.infl_pos[i][other_idx] - otherHasAdditional

            total += self.infl_pos[i][other_idx]            

        if total > 0.0:
            overlap = mismo / total
            # if player_idx == 0:
            #     print(str(player_idx) + " shares " + str(mismo) + " out of " + str(total) + " with " + str(other_idx) + " -> " + str(overlap) + " overlap")
            return overlap

        return 1.0


    def allocateTokens(self, player_idx, numPlayers, numTokens, popularities, heap):
        allocations = np.zeros(numPlayers, dtype=float)
        tokensRemaining = numTokens

        while tokensRemaining > 0:
            if (tokensRemaining - int(tokensRemaining)) != 0:
                print(str(player_idx) + ": real-number token allocation: " + str(tokensRemaining))


            if len(heap) == 0:
                print(str(player_idx) + "heap ran out")
                break
                
            transaction = heapq.heappop(heap)[2]
            quien = transaction["who"][0]
            amount = transaction["quantity"][0]
            threshold = transaction["threshold"]

            # must have enough tokens to do it
            if tokensRemaining < threshold:
                # print("don't do it")
                continue

            # make sure we aren't allocating too many tokens
            if (abs(amount) > tokensRemaining):
                if amount < 0:
                    amount = -tokensRemaining
                else:
                    amount = tokensRemaining

            # for now, ignore case in which |quien| > 1
            if amount > 0 and quien != player_idx:
                amount = self.scaleBack(quien, amount)

            if ((amount > 0) and (allocations[quien] >= 0)) or ((amount < 0) and (allocations[quien] <= 0)):
                allocations[quien] += amount   

                tokensRemaining -= abs(amount)
            # else:
            #     print("discard: " + str(transaction))

                

        return allocations


    # def smoothTokenAllocation2Friends(self, player_idx, numPlayers, numTokens, transaction_vec):
        
    #     aves = (0.1 * self.prevAllocations3 + 0.2 * self.prevAllocations2 + 0.3 * self.prevAllocations1 + 0.4 * transaction_vec)
    #     tokens2Friends = 0
    #     friendAves = 0
    #     for i in range(0, numPlayers):
    #         if (self.govPlayer[i] == 1) or (player_idx == i):
    #             continue

    #         if self.isFriend(player_idx, i) and (transaction_vec[i] >= 0.0) and (self.prevAllocations3[i] >= 0) and (self.prevAllocations2[i] >= 0) and (self.prevAllocations1[i] >= 0):
    #             tokens2Friends += transaction_vec[i]
    #             friendAves += aves[i]

    #     if friendAves > 0.0:
    #         realNew = (tokens2Friends / friendAves) * aves

    #         # print("   " + str(tokens2Friends) + "; to 15: " + str(transaction_vec[15]))
    #         # print("   " + str(aves))
    #         # print("   " + str(friendAves))
    #         # print("   " + str(realNew))

    #         nuevoTrans = np.copy(transaction_vec)
    #         for i in range(0, numPlayers):
    #             if (self.govPlayer[i] == 1) or (player_idx == i):
    #                 continue

    #             if self.isFriend(player_idx, i) and (transaction_vec[i] >= 0.0) and (self.prevAllocations3[i] >= 0) and (self.prevAllocations2[i] >= 0) and (self.prevAllocations1[i] >= 0):
    #                 nuevoTrans[i] = realNew[i]
    #                 # print("     " + str(i))
            
    #         intNuevoTrans = nuevoTrans.astype(int)
    #         remNuevoTrans = nuevoTrans - intNuevoTrans

    #         if np.linalg.norm(intNuevoTrans, ord=1) > numTokens:
    #             return transaction_vec

    #         plyrs = list(range(0, numPlayers))
    #         while np.linalg.norm(intNuevoTrans, ord=1) < numTokens:
    #             if np.linalg.norm(remNuevoTrans, ord=1) == 0:
    #                 print("   " + str(transaction_vec))
    #                 print("   " + str(nuevoTrans))
    #                 print("   " + str(intNuevoTrans))
    #                 print("   " + str(remNuevoTrans))
    #                 print("no remainder: " + str(np.linalg.norm(intNuevoTrans, ord=1)))
    #                 print(intNuevoTrans)
    #                 exit(1)

    #             sel = random.choices(plyrs, weights=remNuevoTrans, k=1)
    #             intNuevoTrans[sel[0]] += 1
    #             remNuevoTrans[sel[0]] = 0.0


    #         # print("   " + str(intNuevoTrans))

    #         if (np.linalg.norm(intNuevoTrans, ord=1) != numTokens):
    #             print("   " + str(transaction_vec))
    #             print("   " + str(nuevoTrans))
    #             print("   " + str(intNuevoTrans))
    #             print("   " + str(remNuevoTrans))


    #         return intNuevoTrans

    #     else:
    #         return transaction_vec

    def createPotentialTransaction(self, quien, cantidad, threshold = 0):
        # if cantidad[0] < -1.0:
        #     print("  potential attack on " + str(quien[0]) + " of " + str(cantidad[0]))

        trans = {"who": quien, "quantity": cantidad, "threshold": threshold}
        return trans

    def convertPriority(self, _priority, dirImpact, player_idx, other_idx):
        impact = 0.0
        if self.genes["visualHomophily"] > 66:
            impact = dirImpact * ((self.visualSimilarityScores[player_idx][other_idx] * (self.genes["visualHomophily"] - 66)) / 3.3)
        elif self.genes["visualHomophily"] < 34:
            impact = -1.0 * dirImpact * ((self.visualSimilarityScores[player_idx][other_idx] * (34 - self.genes["visualHomophily"])) / 3.3)

        return _priority + impact

    def doRandomAllocations(self, player_idx, numPlayers, numTokens, heap):
        posneg = np.zeros(numPlayers, dtype=int)
        for i in range(0, numTokens):
            if np.random.randint(0,100) < self.genes["randomKeep"]:
                trans = self.createPotentialTransaction([player_idx], [1])
                heapq.heappush(heap, (-self.convertPriority(self.genes["priorityRandom"], 1.0, player_idx, player_idx), id(trans), trans))
                # heapq.heappush(heap, (-self.genes["priorityRandom"], id(trans), trans))
            else:
                sel = np.random.choice(np.setdiff1d(range(0,numPlayers), player_idx))
                while (sel == player_idx) or (sel < 0) or (self.govPlayer[sel] == 1):
                    # If i picked myself, something out of range, or a government player, pick again
                    sel = np.random.choice(np.setdiff1d(range(0,numPlayers), player_idx))

                if posneg[sel] == 0:
                    # decide whether to do it positive or negative
                    if np.random.randint(0,100) < self.genes["randomNeg"]:                        
                        posneg[sel] = -1
                    else:    
                        posneg[sel] = 1
                        # if self.infl_neg[sel][player_idx] > 0.0:
                        #     print("(RandomAllocation): " + str(player_idx) + " giving positively to " + str(sel) + " when " + str(self.infl_neg[sel][player_idx]))
                    trans = self.createPotentialTransaction([sel], [posneg[sel]])
                    heapq.heappush(heap, (-self.convertPriority(self.genes["priorityRandom"], posneg[sel], player_idx, sel), id(trans), trans))
                    # heapq.heappush(heap, (-self.genes["priorityRandom"], id(trans), trans))
                elif posneg[sel] > 0:
                    trans = self.createPotentialTransaction([sel], [1])
                    heapq.heappush(heap, (-self.convertPriority(self.genes["priorityRandom"], 1.0, player_idx, sel), id(trans), trans))
                    # heapq.heappush(heap, (-self.genes["priorityRandom"], id(trans), trans))
                else:
                    trans = self.createPotentialTransaction([sel], [-1])
                    heapq.heappush(heap, (-self.convertPriority(self.genes["priorityRandom"], -1.0, player_idx, sel), id(trans), trans))
                    # heapq.heappush(heap, (-self.genes["priorityRandom"], id(trans), trans))


    def erectDefenses(self, round_num, player_idx, numPlayers, numTokens, received, popularities, heap):
        if round_num == 0:
            self.underAttack = (self.genes["initialDefense"] / 100.0) * popularities[player_idx]
        else:
            totalAttack = np.dot(np.negative(received[1:numPlayers]).clip(0), popularities[1:numPlayers])
            dUpdate = self.genes["defenseUpdate"] / 100.0
            self.underAttack = (self.underAttack * (1.0 - dUpdate)) + (totalAttack * dUpdate)

        if popularities[player_idx] == 0:
            return

        caution = self.genes["defensePropensity"] / 50.0
        tokensNeeded = ((self.underAttack * caution) / popularities[player_idx]) * numTokens

        # if tokensNeeded < 0:
        #     print("self.underAttack: " + str(self.underAttack))
        #     print("tokensNeeded: " + str(tokensNeeded))
        
        trans = self.createPotentialTransaction([player_idx], [int(tokensNeeded + 0.5)])
        heapq.heappush(heap, (-self.genes["priorityDefend"], id(trans), trans))

        # print(str(player_idx) + ": " + str(tokensNeeded) + "; " + str(self.genes["priorityDefend"]))


    def doPosDirRecip(self, popularities, received, influence, player_idx, numPlayers, numTokens, heap):
        # update indebtedness
        self.tally += (received * numTokens) * self.prevPopularities
        self.tally[player_idx] = 0

        # if player_idx == 0:
        #     print(self.tally)

        if popularities[player_idx] <= 0:
            return

        # get elbase
        elbase = self.getBasis("posDirRecipBasis")

        # find out how many tokens player_idx owes each player
        v = []
        # owed = []
        for i in range(0, numPlayers):
            if self.govPlayer[i] == 1:
                continue

            if i != player_idx:
                if self.tally[i] > 0.0:
                    tokensOwed = self.tally[i] / popularities[player_idx]

                    if tokensOwed > numTokens:
                        tokensOwed = numTokens

                    # owed.append(tokensOwed)

                    # antes = tokensOwed
                    # if (tokensOwed > self.prevAllocations[i]):# and (not self.previousAttack):
                    #     tokensOwed = (tokensOwed + self.prevAllocations[i]) / 2.0

                    # if i == 15:
                    #     print("  tokensOwed = " + str(tokensOwed) + "; antes = " + str(antes))

                    # print(str(player_idx) + " owes " + str(i) + " " + str(tokensOwed) + " tokens")
                    if self.genes["posDirRecipBasis"] <= 33:
                        # sort based on debt
                        v.append((i, tokensOwed, tokensOwed, 0))
                    elif self.genes["posDirRecipBasis"] <= 66:
                        # sort based on influence
                        v.append((i, influence[i][player_idx], tokensOwed, 0))
                    else:
                        # sort based on popularity
                        v.append((i, popularities[i], tokensOwed, 0))
            #     else:
            #         owed.append(0)
            # else:
            #     owed.append(0)

        # vnp = np.asarray(owed)
        # print("   " + str(vnp))

        self.putInHeapByBasis(v, "priorityPosDirRecip", "posDirRecipBasis", elbase, 1.0, popularities, player_idx, heap)


    # I think this should be more based on "social class" -- should be more willing to retaliate against weaker individuals
    #  while less willing to retaliate against stronger individuals
    def doNegDirRecip(self, popularities, influence, player_idx, numPlayers, numTokens, heap):
        if popularities[player_idx] <= 0:
            return

        if self.genes["warHigh"] < 100.0:
            highPoint = self.collectiveStrength[player_idx] * (self.genes["warHigh"] / 50.0)
        else:
            highPoint = 99999999
        pillageLow = popularities[player_idx] * (self.genes["pillageLow"] / 50.0)

        # get elbase
        elbase = self.getBasis("negDirRecipBasis")

        multiplicador = self.genes["negDirRecipMultiplier"] / 33.0
        # c_should = ((self.genes["negDirRecipCShould"] + 1) / 101.0) * (self.gameParams["steal"] - 0.01) 
        c_should = self.gameParams["keep"]

        # find out how many tokens player_idx should take from each player
        ratioPredictedSteals = 1.0
        v = []
        for i in range(0, numPlayers):
            if self.govPlayer[i] == 1:
                continue

            if i != player_idx:
                if (influence[i][player_idx] < 0.0) and (-influence[i][player_idx] > (0.05 * popularities[player_idx])):
                    if (influence[i][player_idx] < influence[player_idx][i]) and (popularities[i] > 0.01):

                        predictedSteals = sum(np.negative(self.attacksWithMe).clip(0))
                        numer = predictedSteals + self.attacksWithMe[player_idx]
                        if numer > 0:
                            ratioPredictedSteals = predictedSteals / numer
                            if ratioPredictedSteals < 1.0:
                                ratioPredictedSteals = 1.0


                        theScore = (((influence[i][player_idx] - influence[player_idx][i]) * multiplicador) / popularities[player_idx]) * numTokens
                        tokens2Take = theScore - (self.isKeeping(i, numPlayers) * numTokens) * (popularities[i] / popularities[player_idx])

                        # how much does the player need to steal to have a sufficiently high impact?
                        keepingStrength = (self.isKeeping(i, numPlayers) * numTokens) * (popularities[i] / popularities[player_idx])
                        threshold = (keepingStrength * popularities[i] * self.gameParams["steal"]) / (popularities[player_idx] * (self.gameParams["steal"] - c_should))

                        if abs(tokens2Take) < threshold:
                            tokens2Take = -threshold

                        if abs(tokens2Take) > numTokens:
                            tokens2Take = numTokens

                        if (self.collectiveStrength[i] <= highPoint) and (popularities[i] > pillageLow):     # is positioned
                            if abs(tokens2Take) <= numTokens:
                                if self.genes["negDirRecipBasis"] <= 33:
                                    # sort based on the score
                                    # if player_idx == 13:
                                    #     print("sorting based on theScore")
                                    v.append((i, theScore, tokens2Take, threshold))
                                elif self.genes["negDirRecipBasis"] <= 66:
                                    # sort based on influence
                                    # if player_idx == 13:
                                    #     print("sorting based on influence")
                                    v.append((i, influence[i][player_idx], tokens2Take, threshold))
                                else:
                                    # sort based on popularity
                                    # if player_idx == 13:
                                    #     print("sorting based on popularity")
                                    v.append((i, popularities[i], tokens2Take, threshold))
                            # else:
                            #     if player_idx == 1:
                            #         print("retaliation unlikely to be successful")

        self.putInHeapByBasis(v, "priorityNegDirRecip", "negDirRecipBasis", elbase, 1.0, popularities, player_idx, heap)
        # if player_idx == 13:
        #     print("end doNegDirRecip")
        #     print()


    def updateIndebtedness(self, round_num, player_idx, transaction_vec, popularities):
        # update the tally of indebtedness
        self.tally *= (1.0 - self.gameParams["alpha"])  # forget the past somewhat
        self.tally -= np.positive(transaction_vec).clip(0) * popularities[player_idx]
        self.tally[player_idx] = 0

        # if round_num == 0:
        #     self.expectedReturn = transaction_vec * popularities[player_idx]
        # else:
        lmbda = 1.0 / (round_num + 1.0)
        if lmbda < self.gameParams["alpha"]:
            lmbda = self.gameParams["alpha"]
        self.expectedReturn = ((1-lmbda) * self.expectedReturn) + (lmbda * (transaction_vec * popularities[player_idx]))

        # if player_idx == 0:
        #     print()
        #     print("current round: " + str(round_num) + " (" + str(lmbda) + ")")
        #     print("giving: " + str(transaction_vec))
        #     print("expected: " + str(self.expectedReturn))
        #     print(self.tally)


    def getBasis(self, basisStr):
        if self.genes[basisStr] <= 33:
            elbase = 16
        elif self.genes[basisStr] <= 66:
            elbase = 50
        else:
            elbase = 83

        return elbase


    def putInHeapByBasis(self, v, priorityStr, basisStr, elbase, elLimit, popularities, player_idx, heap):
        sz = len(v)
        if sz > 0:
            v_sorted = sorted(v, key=lambda x: x[1], reverse=True)

            domainDiff = abs(v_sorted[0][1] - v_sorted[len(v)-1][1])

            hollerNuf = popularities[player_idx]
            mag = 0.0
            giving = 0.0
            for entry in v_sorted:
                mag += abs(entry[2])
                hollerNuf += popularities[entry[0]]
                if hollerNuf <= (elLimit * self.totalWelfare):
                    giving += abs(entry[2])

            if giving <= 0.0:
                return

            sc = mag / giving

            spread = ((self.genes[basisStr] - elbase) / 33.0) * 5.0

            hollerNuf = popularities[player_idx]
            for entry in v_sorted:

                if domainDiff == 0:
                    elpriority = self.genes[priorityStr]
                else:
                    elpriority = self.genes[priorityStr] - ((abs(entry[1] - v_sorted[0][1]) / domainDiff) * spread)

                if entry[2] > 0:
                    amnt = int((entry[2] * sc)+0.50)
                else:
                    amnt = int((entry[2] * sc)-0.50)

                if entry[3] > 0:
                    trans = self.createPotentialTransaction([entry[0]], [amnt], entry[3])
                    if amnt > 0:
                        heapq.heappush(heap, (-self.convertPriority(elpriority, 1.0, player_idx, entry[0]), id(trans), trans))
                    else:
                        heapq.heappush(heap, (-self.convertPriority(elpriority, -1.0, player_idx, entry[0]), id(trans), trans))
                else:
                    for i in range(0,abs(amnt)):
                        if amnt > 0:
                            trans = self.createPotentialTransaction([entry[0]], [1], entry[3])
                            heapq.heappush(heap, (-self.convertPriority(elpriority+(i*0.1), 1.0, player_idx, entry[0]), id(trans), trans))
                        else:
                            trans = self.createPotentialTransaction([entry[0]], [-1], entry[3])
                            heapq.heappush(heap, (-self.convertPriority(elpriority+(i*0.1), -1.0, player_idx, entry[0]), id(trans), trans))

                hollerNuf += popularities[entry[0]]
                if hollerNuf > (elLimit * self.totalWelfare):
                    break


    def isKeeping(self, other_idx, numPlayers):
        meAmount = 0.0
        totalAmount = 0.0
        for i in range(0, numPlayers):
            if self.govPlayer[i] == 1:
                continue

            if i != other_idx:
                if self.infl_neg[other_idx][i] > 0.0:
                    totalAmount += self.infl_neg[other_idx][i] / self.gameParams["steal"]
                    meAmount -= self.infl_neg[other_idx][i]
                else:
                    totalAmount += self.infl_pos[other_idx][i] / self.gameParams["give"]

        meAmount = (meAmount + self.infl_pos[other_idx][other_idx] - self.infl_neg[other_idx][other_idx]) / self.gameParams["keep"]
        totalAmount += meAmount

        # return meAmount
        if totalAmount > 0:
            return meAmount / totalAmount
        else:
            return 1.0


    def firstOrderGive(self, popularities, player_idx, numPlayers, numTokens, heap):
        if self.genes["firstOrderGiveTokens"] == 0:
            return

        profile = np.copy(self.infl_pos[:,player_idx])
        profile[player_idx] = 0.0

        poder = self.genes["firstOrderGiveBesties"] / 50.0
        if self.genes["firstOrderGiveMode"] < 50:
            compounding = np.ones(numPlayers, dtype=float)
            for i in range(0, numPlayers):
                if self.infl_pos[player_idx][i] == 0:
                    compounding[i] = 1.0
                else:
                    compounding[i] = self.infl_pos[i][player_idx] / self.infl_pos[player_idx][i]
            compounding = np.power(compounding, poder)
            profile *= compounding
        else:
            profile = np.power(profile, poder)

        sm = np.linalg.norm(profile, ord=1)
        if sm <= 0.0:
            return

        profile /= sm

        profile *= (self.genes["firstOrderGiveTokens"] / 100) * numTokens

        elbase = self.getBasis("firstOrderGiveBasis")

        v = []
        for i in range(0, numPlayers):
            if self.govPlayer[i] == 1:
                continue

            if profile[i] >= 0.50:
                v.append((i, self.friendship[i][player_idx], int(profile[i] + 0.5), 0))

        elLimit = self.genes["firstOrderGiveMax"] / 100.0

        self.putInHeapByBasis(v, "priorityFirstOrderGive", "firstOrderGiveBasis", elbase, elLimit, popularities, player_idx, heap)


    # New function created Dec 29, 2022
    def increaseFriendships(self, popularities, player_idx, numPlayers, numTokens, heap):
        if popularities[player_idx] <= 0:
            return

        # if player_idx == 0:
        #     print()
        #     print(self.friendship)

        minCollective = self.genes["posTriadicWealthMin"] / 100.0
        if self.collectiveStrength[player_idx] < minCollective:
            tokensRequerido = 2.0 / minCollective
            # if player_idx == 0:
            #     print("tokensRequerido: " + str(tokensRequerido) + " (based on " + str(minCollective) + ")")

            theSet = []
            theAmounts = []
            for i in range(0, numPlayers):
                if (self.govPlayer[i] == 1) or (popularities[i] == 0) or (i == player_idx):   # ADDED last condition on 12/27/2022
                    continue
            
                resourceCommitted = 1.0
                if self.infl_pos_sumrow[i] > 0.0:
                    resourceCommitted = self.infl_pos[i][player_idx] / self.infl_pos_sumrow[i]
    
                if (self.friendship[i][player_idx] > 0.0) and (self.friendship[i][player_idx] < 1.0) and (resourceCommitted < 0.9):
                    # if he is my friend and he has more to give, consider being a better friend to him
                    # current = 2.0 + self.friendship[player_idx][i] * (tokensRequerido - 2.0)
                    shortfall = tokensRequerido * (1 - self.friendship[player_idx][i])
                    # if player_idx == 0:
                    #     print(" player " + str(i))
                    #     print("  friendship: " + str(self.friendship[player_idx][i]))
                    #     print("  shortfall: " + str(shortfall))
                        # print("  current: " + str(current))

                    if shortfall >= 0.5:
                        theSet.append(i)
                        theAmounts.append(int(shortfall + 0.5))

            if len(theSet) > 0:
                ind = random.randint(0, len(theSet)-1)
                # if player_idx == 0:
                #     print(theSet)
                #     print(theAmounts)
                #     print("give " + str(theAmounts[ind]) + " to " + str(theSet[ind]))
                trans = self.createPotentialTransaction([theSet[ind]], [theAmounts[ind]])
                heapq.heappush(heap, (-self.convertPriority(self.genes["priorityIncreaseFriendship"], 1.0, player_idx, theSet[ind]), id(trans), trans))
            

    # def increaseFriendships(self, popularities, player_idx, numPlayers, numTokens, heap):
    #     if popularities[player_idx] <= 0:
    #         return

    #     # if player_idx == 0:
    #     #     print()
    #     #     print(self.friendship)

    #     minCollective = self.genes["posTriadicWealthMin"] / 100.0
    #     if self.collectiveStrength[player_idx] < minCollective:
    #         tokensRequerido = 2.0 / minCollective
    #         # if player_idx == 0:
    #         #     print("tokensRequerido: " + str(tokensRequerido) + " (based on " + str(minCollective) + ")")

    #         masCerca = -1
    #         numeroCerca = -1
    #         valorCerca = -1
    #         for i in range(0, numPlayers):
    #             if (self.govPlayer[i] == 1) or (popularities[i] == 0) or (i == player_idx):   # ADDED last condition on 12/27/2022
    #                 continue
            
    #             # compute the "shortfall": how much more do I need to give them for them to be a full friend (according to my estimates)
    #             if self.infl_pos_sumrow[i] > 0.0:
    #                 resourceCommitted = self.infl_pos[i][player_idx] / self.infl_pos_sumrow[i]
    #             else:
    #                 resourceCommitted = 1.0
    #             if (self.friendship[i][player_idx] > 0.0) and (resourceCommitted < 0.9):
    #                 # if he is my friend and he has more to give, consider being a better friend to him
    #                 current = 2.0 + self.friendship[player_idx][i] * (tokensRequerido - 2.0)
    #                 shortfall = tokensRequerido - current

    #                 if shortfall >= 0.5:
    #                     # if player_idx == 0:
    #                     #     print("consider giving more to " + str(i))
    #                     # if player_idx == 0:
    #                     #     print(str(player_idx) + " considers giving " + str(i) + " (fs: " + str(self.friendship[player_idx][i]) + ") " + str(shortfall) + " extra tokens")
    #                     amnt = int(shortfall + 0.5)
    #                     val = amnt #self.scaleBack(i, amnt)
    #                     if self.friendship[player_idx][i] > numeroCerca:
    #                         masCerca = i
    #                         numeroCerca = self.friendship[player_idx][i]
    #                         valorCerca = val

    #         if masCerca != -1:
    #             # if self.infl_neg[masCerca][player_idx] > 0.0:
    #             #     print("(increaseFriendship): " + str(player_idx) + " giving positively to " + str(masCerca) + " when " + str(self.infl_neg[masCerca][player_idx]))

    #             trans = self.createPotentialTransaction([masCerca], [valorCerca])
    #             heapq.heappush(heap, (-self.convertPriority(self.genes["priorityIncreaseFriendship"], 1.0, player_idx, masCerca), id(trans), trans))
    #             # heapq.heappush(heap, (-self.genes["priorityIncreaseFriendship"], id(trans), trans))
      
    #             # if player_idx == 0:
    #             #     print(str(player_idx) + " needs to give " + str(masCerca) + " " + str(valorCerca) + " extra tokens")
            

    def triadicAction(self, popularities, influence, player_idx, numPlayers, numTokens, heap):
        if popularities[player_idx] <= 0:
            return

        # new attempt
        M1 = influence - np.diag(np.diag(influence))
        M2 = np.dot(M1, M1)
        reactiveClosure = M2 - np.diag(np.diag(M2))

        # if player_idx == 1:
        #     print(M1)
        #     print()
        #     print(reactiveClosure)

        # compute difference between what is and what could be
        dff = np.zeros(numPlayers, dtype=float)
        for i in range(0, numPlayers):
            if self.govPlayer[i] == 1:
                continue

            if i == player_idx:
                dff[i] = 0.0
            elif reactiveClosure[i][player_idx] > 0.0:
                dff[i] = math.sqrt(reactiveClosure[i][player_idx]) - influence[i][player_idx]
            else:
                dff[i] = -math.sqrt(-reactiveClosure[i][player_idx]) - influence[i][player_idx]
        # if player_idx == 1:
        # print(dff)
        # print()

        # first, let's deal with the positive (only do something if I don't have enough friends)
        minCollective = self.genes["posTriadicWealthMin"] / 100.0
        if (self.collectiveStrength[player_idx] < minCollective) and (self.genes["posTriadicClosureTokens"] > 0):
            # print(str(player_idx) + " wants more collective strength: " + str(self.collectiveStrength[player_idx]) + " vs " + str(minCollective))
            
            # find the max of dff
            mxVal = 0
            mxInd = -1
            for i in range(0, numPlayers):
                if self.govPlayer[i] == 1:
                    continue

                if (dff[i] > mxVal) and (influence[i][player_idx] >= 0.0):
                    mxVal = dff[i]
                    mxInd = i

            if mxVal > 0.0:
                # figure out how many tokens it is going to take: curtail by posTriadicClosureTokens
                theSum = np.sum(self.infl_pos[:,player_idx])
                if theSum == 0.0:
                    nToks = numTokens
                else:
                    nToks = int(((mxVal / theSum) * numTokens) + 0.5)
                mToks = (self.genes["posTriadicClosureTokens"] / 100.0) * numTokens
                if nToks > mToks:
                    nToks = int(mToks)

                # if player_idx == 1:
                # print(str(player_idx) + ": give " + str(nToks) + " to " + str(mxInd))

                # make an entry into the heap

                if self.infl_neg[mxInd][player_idx] > 0.0:
                    print("(triadicAction): " + str(player_idx) + " giving positively to " + str(mxInd) + " when " + str(self.infl_neg[mxInd][player_idx]))

                trans = self.createPotentialTransaction([mxInd], [nToks])
                heapq.heappush(heap, (-self.convertPriority(self.genes["priorityPosTriadicClosure"], 1.0, player_idx, mxInd), id(trans), trans))
                # heapq.heappush(heap, (-self.genes["priorityPosTriadicClosure"], id(trans), trans))

        np.set_printoptions(precision=2)
        np.set_printoptions(linewidth=np.inf)
        np.set_printoptions(formatter={'float': lambda x: "{0:0.2f}".format(x)})

        # second, let's deal with the negative
        badMarks = np.zeros(numPlayers, dtype=float)
        worstInd = -1
        worstVal = 0
        for i in range(0,numPlayers):
            if (self.govPlayer[i] == 1) or (i == player_idx):
                continue

            if i != player_idx:
                badMarks[i] = np.dot(self.infl_neg[i], self.friendshipChop[:,player_idx])
                if badMarks[i] > 0:
                    badMarks[i] -= np.dot(self.infl_neg[:,i], self.friendshipChop[:,player_idx])

                if badMarks[i] > worstVal:
                    worstInd = i
                    worstVal = badMarks[worstInd]

        # if player_idx == 0:
        #     print(influence)
        #     print()
        #     print(self.infl_neg_sumrow)
        #     print(self.infl_neg_sumcol)
        #     print(badMarks)
        #     print(worstInd)
        #     print(worstVal)

        # print(" triadicAttack")

        # print(str(player_idx) + ": " + str(badMarks))
        # print("   " + str(self.friendshipChop[:,player_idx]))
        attackThreshold = self.genes["negTriadicAttackThreshold"] / 50.0
        myPopProp = popularities[player_idx] / sum(popularities)
        if (worstInd >= 0) and (popularities[worstInd] > 1.0):
            if not self.isFriend(player_idx, worstInd):
                guilt = 2.0 * (self.infl_neg_sumrow[worstInd] - self.infl_neg_sumcol[worstInd])

                # only retaliate if guilt is sufficiently high
                if (guilt / popularities[worstInd]) > 0.3:
                    propMyWeight = (guilt / (popularities[player_idx] * self.gameParams["alpha"])) / self.gameParams["steal"]
                    propMyWeight += (self.isKeeping(worstInd, numPlayers) * popularities[worstInd]) / popularities[player_idx]
                    # print(str(player_idx) + ": consider attacking " + str(worstInd) + " with " + str(propMyWeight) + " of my power")
                    # print("         given it's guilt is " + str(guilt))

                    
                    # account for attacks from others in my group
                    attackStrength = 0
                    # who was attacked by worstInd
                    for i in range(0,numPlayers):
                        if self.govPlayer[i] == 1:
                            continue

                        if self.infl_neg_sumcol[i] > 0:   # if being attacked by anyone -> blame it on worstInd
                            if self.collectiveStrength[i] > attackStrength:
                                attackStrength = self.collectiveStrength[i]

                    # # print("         attack strength is " + str(attackStrength))
                    if attackStrength > myPopProp:
                        myPart = (myPopProp / attackStrength) * propMyWeight
                        tokens2Take = int(myPart * numTokens + 0.5)

                        # print("         need to attack with " + str(myPart) + " proportion of my tokens")
                        if self.collectiveStrength[player_idx] > (self.collectiveStrength[worstInd] * attackThreshold):
                            trans = self.createPotentialTransaction([worstInd], [-tokens2Take])
                            heapq.heappush(heap, (-self.convertPriority(self.genes["priorityNegTriadicClosure"], -1.0, player_idx, worstInd), id(trans), trans))
                            # heapq.heappush(heap, (-self.genes["priorityNegTriadicClosure"], id(trans), trans))
                # else:
                #     print(str(player_idx) + " back off of " + str(worstInd) + " -- not guilty enough")


    def scaleBack(self, quien, amount):
        if self.govPlayer[quien] == 1:  # for now, don't scale back payments to the gov'ment
            return amount

        # consider scaling back if the other person is in debt to me and is expected to give me something
        if (self.tally[quien] < 0.0) and (self.expectedReturn[quien] > 0):
            debtLimit = self.genes["otherishDebtLimits"] / 10.0

            # scale back if there are debtLimits and if their debt exceeds the threshold
            if (-self.tally[quien]) > (self.expectedReturn[quien] * debtLimit):
                if debtLimit > 0:

                    backoffPerc = 1.0 - (((-self.tally[quien]) - (self.expectedReturn[quien] * debtLimit)) / (self.expectedReturn[quien] * debtLimit))
                    if backoffPerc < 0.0:
                        backoff = 0
                        # print("remove all " + str(amount - backoff) + " from " + str(quien) + "; " + str(backoff))
                    else:
                        backoff = int(backoffPerc * amount)
                        # print("remove some " + str(amount - backoff) + " from " + str(quien) + "; " + str(backoff))
                    
                    # if player_idx == 15:
                    

                    return backoff
                else:
                    return 0

        return amount
        


    def pillageTheVillage(self, player_idx, numPlayers, numTokens, popularities, influence, heap):
        if popularities[player_idx] <= 0.0:
            return

        # print()
        # print(" pillage")

        # compute expected defenses
        keepingStrength = []
        for i in range(0, numPlayers):
            if i != player_idx:
                keepingStrength_i = (self.isKeeping(i, numPlayers) * numTokens) #* (popularities[i] / popularities[player_idx])  # commented out on 12/30/2022
                keepingStrength.append(keepingStrength_i)
            else:
                keepingStrength.append(self.isKeeping(i, numPlayers) * numTokens)

        # print("keeping: " + str(keepingStrength))

        lowPoint = popularities[player_idx] * (self.genes["pillageLow"] / 50.0)
        if self.genes["pillageHigh"] < 100.0:
            highPoint = popularities[player_idx] * (self.genes["pillageHigh"] / 50.0)
        else:
            highPoint = 99999999

        numAttackTokens = int(numTokens * (self.genes["pillageFury"] / 100.0) + 0.5)
        if numAttackTokens <= 0:
            return

        # c_should = ((self.genes["pillageCShould"] + 1) / 101.0) * (self.gameParams["steal"] - 0.01) 
        c_should = self.gameParams["give"]   # default for now

        # ratioPredictedSteals = 1.0
        # predictedSteals = sum(np.negative(self.attacksWithMe).clip(0))
        # numer = predictedSteals + self.attacksWithMe[player_idx]
        # if numer > 0:
        #     ratioPredictedSteals = predictedSteals / numer
        #     if ratioPredictedSteals < 1:
        #         ratioPredictedSteals = 1.0
        
        # change on 12/29/2022 (modified from the above)
        ratioPredictedSteals = 1.0
        predictedSteals = sum(np.negative(self.attacksWithMe).clip(0))
        if self.attacksWithMe[player_idx] < 0:
            ratioPredictedSteals = predictedSteals / (-self.attacksWithMe[player_idx])

        # if player_idx == 0:
        #     print()
        #     print(influence)
        #     print()
        #     print(self.attacksWithMe)
        #     print("predictedSteals: " + str(predictedSteals))
        #     print("ratioPredictedSteals: " + str(ratioPredictedSteals))
        #     print("pillageFury: " + str(self.genes["pillageFury"]))
        #     print("numAttackTokens: " + str(numAttackTokens))


        attackPossibility = []
        for i in range(0, numPlayers):
            if self.govPlayer[i] == 1:
                continue

            if i != player_idx:
                if self.isPositioned(player_idx, i, popularities, lowPoint, highPoint) == True:
                    # print(str(i) + ": isPositioned = True")
                    if self.isFriend(player_idx, i) != True:
                        # print("   " + str(i) + ": isFriend = False")
                        # changing this on 12/30/2022
                        threshold = ((keepingStrength[i] / ratioPredictedSteals) * popularities[i] * self.gameParams["steal"]) / (popularities[player_idx] * (self.gameParams["steal"] - c_should))
                        # Compute how the threshold changes based on attacks by others (that tend to attack at the same time)

                        # gain = (popularities[player_idx] * numTokens) - (popularities[i] * keepingStrength[i] / ratioPredictedSteals)
                        # coefEst = (gain * self.gameParams["steal"]) / (numTokens * popularities[player_idx] * c_should)
                        # change on 12/29/2022
                        gain = (popularities[player_idx] * numAttackTokens) - (popularities[i] * keepingStrength[i] / ratioPredictedSteals)
                        coefEst = (gain * self.gameParams["steal"]) / (numAttackTokens * popularities[player_idx] * c_should)

                        # if player_idx == 0:
                        #     print("Player " + str(i))
                        #     print("  keepingStrength: " + str(keepingStrength[i]))
                        #     print("  gain: " + str(gain))
                        #     print("  coefEst: " + str(coefEst))
                        #     print("  threshold: " + str(threshold))

                        if (coefEst > 1.0):# and (numAttackTokens > threshold):
                            # print("      " + str(i) + ": coefEst = " + str(coefEst)) 
                            amnt = coefEst - 0.99
                            if influence[player_idx][i] < 0.0:
                                amnt *= 100
                            if len(attackPossibility) == 0:
                                attackPossibility = [(i, amnt, threshold)]
                            else:
                                attackPossibility.append((i, amnt, threshold))

        # if player_idx == 1:
        #     print(attackPossibility)
        # random selection
        if len(attackPossibility) > 0:

            mag = 0.0
            for i in range(0, len(attackPossibility)):
                mag += attackPossibility[i][1]
            num = np.random.uniform(0, 1.0)

            sumr = 0.0
            for i in range(0, len(attackPossibility)):
                sumr += (attackPossibility[i][1] / mag)

                if (num <= sumr):
                    thrshldTmp = attackPossibility[i][2] - ((ratioPredictedSteals - 1.0) * numAttackTokens)
                    if thrshldTmp < 0.0:
                        thrshldTmp = 0.0
                    # print(str(attackPossibility[i][2]) + " vs " + str(thrshldTmp))
                    # print(str(player_idx) + " pillage " + str(attackPossibility[i][0]) + " with " + str(numAttackTokens) + " tokens")
                    trans = self.createPotentialTransaction([attackPossibility[i][0]], [-numAttackTokens], thrshldTmp) #attackPossibility[i][2])
                    heapq.heappush(heap, (-self.convertPriority(self.genes["priorityPillage"], -1.0, player_idx, attackPossibility[i][0]), id(trans), trans))
                    # heapq.heappush(heap, (-self.genes["priorityPillage"], id(trans), trans))
                    break


    def isPositioned(self, player_idx, other_idx, popularities, lowPoint, highPoint):
        if (popularities[other_idx] >= lowPoint) and (popularities[other_idx] <= highPoint):
            return True
        
        return False


    def isFriend(self, player_idx, other_idx):
        if self.friendship[player_idx][other_idx] >= 0.1:
            return True
        
        return False


    def startWar(self, round_num, player_idx, numPlayers, numTokens, popularities, influence, heap):
        if popularities[player_idx] <= 0.0:
            return

        if round_num < (self.genes["warDelay"] / 10.0):
            # to early to start a war
            return

        keepingStrength = []
        for i in range(0, numPlayers):
            if i != player_idx:
                keepingStrength_i = (self.isKeeping(i, numPlayers) * numTokens) #* (popularities[i] / popularities[player_idx])  # commented out on 12/30/2022
                keepingStrength.append(keepingStrength_i)
            else:
                keepingStrength.append(self.isKeeping(i, numPlayers) * numTokens)

        # To attack a person out of the blue, five criteria should hold:
        #   1.  The player must have enough resources
        #   2.  The player shouldn't be my frined
        #   3.  The player shouldn't overlap with my friend group too much
        #   4.  The player's network of strength needs to be below the threshold ->
        #        the collective strength of it and each of its friends (not counting me) should be below the threshold
        #   5.  The player should be profitable to attack (not keeping too much)

        if self.genes["warHigh"] < 100.0:
            highPoint = self.collectiveStrength[player_idx] * (self.genes["warHigh"] / 50.0)
        else:
            highPoint = 99999999


        numAttackTokens = int(numTokens * (self.genes["warFury"] / 100.0) + 0.5)

        # c_should = ((self.genes["pillageCShould"] + 1) / 101.0) * (self.gameParams["steal"] - 0.01) 
        c_should = self.gameParams["give"]   # default for now

        # print("\n" + str(player_idx) + ": Should I start a war?")
        # print(" " + str(self.fOverlap))

        attackPossibility = []
        ratioPredictedSteals = 1.0
        for i in range(0, numPlayers):
            if self.govPlayer[i] == 1:
                continue

            if i != player_idx:
                # printf("need to reconsider the fOverlap threshold here")
                if (self.isFriend(player_idx, i) == False) and (self.fOverlap[i] < 0.4):    # points 2 and 3: is not my friend or there isn't too much of an overlapping friend group

                    mxCollectiveStrength = self.collectiveStrength[i]
                    for j in range(0, numPlayers):
                        if (self.govPlayer[j] == 1) or (j == player_idx) or (i == j) or (not self.isFriend(i, j)):
                            continue

                        if self.collectiveStrength[j] > mxCollectiveStrength:
                            mxCollectiveStrength = self.collectiveStrength[j]

                    # print("  positioned to attack " + str(i) + "? who has mxCollectiveStrength = " + str(mxCollectiveStrength) + "; (highPoint = " + str(highPoint) + "; pillageLow = " + str(self.genes["pillageLow"]) + ")")

                    pillageLow = popularities[player_idx] * (self.genes["pillageLow"] / 50.0)
                    if (mxCollectiveStrength <= highPoint) and (popularities[i] > pillageLow):     # points 1 and 4: the player has enough resources
                        threshold = (keepingStrength[i] * popularities[i] * self.gameParams["steal"]) / (popularities[player_idx] * (self.gameParams["steal"] - c_should))
                        predictedSteals = sum(np.negative(self.attacksWithMe).clip(0))
                        # numer = predictedSteals + self.attacksWithMe[player_idx]
                        # if numer > 0:
                        #     ratioPredictedSteals = predictedSteals / numer
                        #     if ratioPredictedSteals < 1:
                        #         ratioPredictedSteals = 1.0
                        # change on 12/30/2022 (modified from the above)
                        predictedSteals = sum(np.negative(self.attacksWithMe).clip(0))
                        if self.attacksWithMe[player_idx] < 0:
                            ratioPredictedSteals = predictedSteals / (-self.attacksWithMe[player_idx])

                        gain = (popularities[player_idx] * numTokens) - (popularities[i] * keepingStrength[i] / ratioPredictedSteals)
                        coefEst = (gain * self.gameParams["steal"]) / (numTokens * popularities[player_idx] * c_should)

                        # print("   consider starting group attack on " + str(i) + ": coefEst = " + str(coefEst) + "; threshold = " + str(threshold) + "; numAttackTokens = " + str(numAttackTokens))
                        if (coefEst > 1.0) and (numAttackTokens > threshold):       # point 5: it is profitable to attack the individual
                            amnt = coefEst - 0.99
                            if influence[player_idx][i] < 0.0:
                                amnt *= 100

                            # print("FRUITFUL: " + str(player_idx) + " to consider starting group attack on " + str(i) + " (" + str(numAttackTokens) + ")") 
                            # print("    Collective Strength: " + str(self.collectiveStrength[i]) + " vs " + str(mxCollectiveStrength))
                            # print("    Cap: " + str(highPoint)) 
                            if len(attackPossibility) == 0:
                                attackPossibility = [(i, amnt, threshold)]
                            else:
                                attackPossibility.append((i, amnt, threshold))

        if len(attackPossibility) > 0:

            mag = 0.0
            for i in range(0, len(attackPossibility)):
                mag += attackPossibility[i][1]
            num = np.random.uniform(0, 1.0)

            sumr = 0.0
            for i in range(0, len(attackPossibility)):
                sumr += (attackPossibility[i][1] / mag)

                if (num <= sumr):
                    thrshldTmp = attackPossibility[i][2] - ((ratioPredictedSteals - 1.0) * numAttackTokens)
                    if thrshldTmp < 0.0:
                        thrshldTmp = 0.0
                    # print(str(attackPossibility[i][2]) + " vs " + str(thrshldTmp))
                    # print(str(player_idx) + " pillage " + str(attackPossibility[i][0]) + " with " + str(numAttackTokens) + " tokens")
                    trans = self.createPotentialTransaction([attackPossibility[i][0]], [-numAttackTokens], thrshldTmp) #attackPossibility[i][2])
                    heapq.heappush(heap, (-self.convertPriority(self.genes["priorityWar"], -1.0, player_idx, attackPossibility[i][0]), id(trans), trans))
                    # heapq.heappush(heap, (-self.genes["priorityWar"], id(trans), trans))
                    break


    def joinWar(self, round_num, player_idx, numPlayers, numTokens, popularities, influence, heap):
        if popularities[player_idx] <= 0.0:
            return

        if round_num < (self.genes["warDelay"] / 10.0):
            # to early to join a war
            return
        
        # find the biggest new attack that involves one of my friends
        newAttacks = self.infl_neg - self.infl_neg_prev
        mx = 5.0
        preyInd = -1
        attackers = np.zeros(numPlayers)
        defenders = np.zeros(numPlayers)
        for i in range(0, numPlayers):
            if (self.govPlayer[i] == 1) or (i == player_idx) or self.isFriend(player_idx, i):
                continue

            friendAttacks_i = np.dot(self.friendshipChop[:,player_idx], newAttacks[:,i])
            if friendAttacks_i > mx:
                mx = friendAttacks_i
                preyInd = i
                attackers = np.zeros(numPlayers)
                defenders = np.zeros(numPlayers)
                for j in range(0, numPlayers):
                    if self.govPlayer[j] == 1:
                        continue
                    
                    if self.isFriend(player_idx, j) or (newAttacks[j][i] > 0.0):
                        attackers[j] = 1.0
                    
                    if self.isFriend(j, i):
                        defenders[j] = 1.0

        # print("Join War " + str(player_idx))
        # print(" " + str(self.fOverlap))
        # decide if want to join the war
        if preyInd != -1:
            totalPotentialAttack = np.dot(attackers, (popularities / self.totalWelfare))
            totalPotentialDefenders = np.dot(defenders, (popularities / self.totalWelfare))

            # print(" should I join the attack on " + str(preyInd))
            # print(" totalPotentialAttack = " + str(totalPotentialAttack))

            keepingStrength = []
            for i in range(0, numPlayers):
                if i != player_idx:
                    keepingStrength_i = (self.isKeeping(i, numPlayers) * numTokens) #* (popularities[i] / popularities[player_idx])  # commented out on 12/30/2022
                    keepingStrength.append(keepingStrength_i)
                else:
                    keepingStrength.append(self.isKeeping(i, numPlayers) * numTokens)

            c_should = self.gameParams["give"]   # default for now
            numAttackTokens = int(numTokens * (self.genes["warFury"] / 100.0) + 0.5)
            attackPossibility = []
            ratioPredictedSteals = 1.0

            # print(" totalPotentialDefenders = " + str(totalPotentialDefenders))

            warCaution = self.genes["warHigh"] / 50.0

            pillageLow = popularities[player_idx] * (self.genes["pillageLow"] / 50.0)
            if ((warCaution * totalPotentialDefenders) <= totalPotentialAttack) and (popularities[preyInd] > pillageLow):     # is positioned

                # print("   It is in the range")

                threshold = (keepingStrength[preyInd] * popularities[preyInd] * self.gameParams["steal"]) / (popularities[player_idx] * (self.gameParams["steal"] - c_should))
                # numer = predictedSteals + self.attacksWithMe[player_idx]
                # if numer > 0:
                #     ratioPredictedSteals = predictedSteals / numer
                #     if ratioPredictedSteals < 1:
                #         ratioPredictedSteals = 1.0
                # change on 12/30/2022 (modified from the above)
                predictedSteals = sum(np.negative(self.attacksWithMe).clip(0))
                if self.attacksWithMe[player_idx] < 0:
                    ratioPredictedSteals = predictedSteals / (-self.attacksWithMe[player_idx])

                gain = (popularities[player_idx] * numTokens) - (popularities[preyInd] * keepingStrength[preyInd] / ratioPredictedSteals)
                coefEst = (gain * self.gameParams["steal"]) / (numTokens * popularities[player_idx] * c_should)

                if (coefEst > 1.0) and (numAttackTokens > threshold):       # it is profitable to join the attack on this individual

                    otherSteals = 0.0
                    for i in range(0, numPlayers):
                        if (self.govPlayer[j] == 1) or (i == player_idx) or (i == preyInd):
                            continue

                        otherSteals += self.attacksWithMe[i]

                    bnd = ((popularities[preyInd] * (0.5 - 1.0 - self.gameParams["alpha"])) - (self.gameParams["alpha"] * otherSteals)) / (self.gameParams["alpha"] * popularities[player_idx])
                    bnd *= numTokens

                    # print("   attacksWithMe: " + str(self.attacksWithMe))
                    # print("   otherSteals: " + str(otherSteals))
                    # print("   bnd: " + str(bnd))

                    if (-numAttackTokens) < bnd:
                        # print("   -> cut back attack")
                        numAttackTokens = -int(bnd)

                    trans = self.createPotentialTransaction([preyInd], [-numAttackTokens], threshold) #attackPossibility[i][2])
                    heapq.heappush(heap, (-self.convertPriority(self.genes["priorityJoinWar"], -1.0, player_idx, preyInd), id(trans), trans))
                    # heapq.heappush(heap, (-self.genes["priorityJoinWar"], id(trans), trans))
    
            #     else:
            #         print("   No, it wouldn't be profitable")
            # else:
            #     print("   No, it isn't in the range")
