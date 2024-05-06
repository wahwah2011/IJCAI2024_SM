

# ############################################################
# 
# Extra functions that might end up being useful
# 
# ############################################################

    # def determineAttackQuantities(self, player_idx):
    #     recipPos = self.infl_pos_sumrow[player_idx]
    #     recipNeg = self.infl_neg_sumrow[player_idx]
    #     myPoder = recipPos + recipNeg

    #     recipDenom = recipPos + recipNeg
    #     if recipDenom == 0:
    #         percentPoderUnderAttack = 0.0
    #     else
    #         percentPoderUnderAttack = recipNeg / recipPos



    # for now, just use the exponential sliding average of influence taken per round
    def predictAttacks(self, player_idx, received, popularities):
        numPlayers = len(popularities)
        numTokens = numPlayers * 2

        getting = (received * numTokens) * popularities
        if popularities[player_idx] <= 0.0:
            negVal = numTokens
        else:
            negVal = sum(np.negative(getting).clip(0)) / popularities[player_idx]

        if (self.attackRate < -1):
            return negVal
        else:
            rate = 0.8
            return (rate * self.attackRate) + ((1.0 - rate) * negVal)

    def initialAllocation(self, player_idx, numPlayers):
        pmfKeep = np.zeros(numPlayers, dtype=float)
        pmfKeep[player_idx] = 1.0

        pmfRandom = self.getPMFRandom(numPlayers, player_idx)

        w = self.genes["initialKeep"] / 100.0
        weights = [w, 1-w]
        thePMF = self.combinePMFs(weights, [pmfKeep, pmfRandom])

        return thePMF

    def getPMFRandom(self, numPlayers, player_idx):
        pmfRandom = np.zeros(numPlayers, dtype=float)
        p = self.genes["probRandGroup"] / 100.0
        for i in range(1, numPlayers):
            if i != player_idx:
                if i in self.theGroups[self.myGroup]:
                    pmfRandom[i] = 1
                else:
                    pmfRandom[i] = 1 - p

                if np.random.randint(0,100) < self.genes["probRandSteal"]:
                    pmfRandom[i] = -pmfRandom[i]

        pmfRandom = pmfRandom / np.linalg.norm(pmfRandom, ord=1)

        return pmfRandom

    def combinePMFs(self, weights, thePMFs):
        combinedPMF = weights[0] * thePMFs[0]
        for i in range(1, len(thePMFs)):
            combinedPMF += weights[i] * thePMFs[i]

        return combinedPMF

    def pruneTransactions(self, transaction_vec, popularities):
        # print(transaction_vec)

        propPop = self.genes["interactionCap"] / 100.0
        # print(propPop)
        popSum = sum(popularities)
        v = []
        for i in range(0, len(popularities)):
            v.append((i, transaction_vec[i]))
        
        vec_sorted = sorted(v, key=lambda x: x[1], reverse=True)
        # print(vec_sorted)
        
        val = 0
        curProp = 0.0
        for i in range(0, len(popularities)):
            if transaction_vec[vec_sorted[i][0]] > 0.0:
                if curProp > propPop:
                    transaction_vec[vec_sorted[i][0]] /= (curProp / (propPop + 0.000001))
                val += popularities[vec_sorted[i][0]]
                curProp = val / popSum

        # print(transaction_vec)

        # sys.exit(1)

        return transaction_vec


    def getDRecipPMF(self, player_idx, influence, popularities):
        posReceived = (influence.clip(0))
        negReceived = (np.negative(influence).clip(0))
        posReceived[player_idx] = negReceived[player_idx] = 0

        posInfl = posReceived * self.genes["recipPos"] * popularities
        negInfl = negReceived * self.genes["recipNeg"] * popularities

        distr = posInfl + negInfl

        co = (self.genes["besties"]+1) / 50.0
        poder = [co] * len(distr)
        distr = np.power(distr, poder)

        if (np.linalg.norm(distr, ord=1) == 0):
            distribucion = np.ones(len(influence), dtype=float)
            distribucion[0] = 0.0
            distribucion *= 1 / (len(influence) - 1)
        else:
            distribucion = distr / np.linalg.norm(distr, ord=1)

        for i in range(1,len(distribucion)):
            if influence[i] < 0.0:
                distribucion[i] = -distribucion[i]

        if True in np.isnan(distribucion):
            print("como?")

        return distribucion

    def computeAvailableRiches(self, attacker_idx, prey_idx, popularities):
        if (popularities[prey_idx] <= 0.0) or (popularities[attacker_idx] == 0):
            return 0.0

        numPlayers = len(popularities)

        projectedPreyWealth = popularities[prey_idx]
        worth = (projectedPreyWealth / self.gameParams["alpha"]) * 2 * numPlayers
        riches = worth / (self.gameParams["steal"] * popularities[attacker_idx])

        return riches

    def updatePropAttackMineEstimate(self, attacker, numPlayers):
        attackerRep = 0.0
        allRep = 0.0
        for i in range(1,numPlayers):
            if self.infl_neg[attacker][i] > 0.0:
                attackerRep += self.infl_neg[attacker][i]
                allRep += self.infl_neg_sumcol[i]

        if allRep > 0:
            c = 0.1
            pAttack = c * (attackerRep / allRep) + (1-c) * self.propAttackMine
            return pAttack
        else:
            return self.propAttackMine        


