#ifndef GOODAGENT_H
#define GOODAGENT_H

#include <iostream>
#include <string>
#include <vector>
#include <set>
#include <sstream>
#include <fstream>

#include "AbstractAgent.h"

using namespace std;

class GoodAgent : public AbstractAgent {
public:
    GoodAgent() {
        cout << "GoodAgent" << endl;
        isInitialized = false;
        whoami = "good";
        reciprocityScore = nullptr;
        attackHistory = nullptr;
    }

    ~GoodAgent() {
        if (isInitialized) {
            delete[] reciprocityScore;
            delete[] attackHistory;
        }
    }

    void playRound(int numPlayers, int numTokens, int playerIdx, int roundNum, 
        double *received, double *popularities, double **influence, int *allocations) {
        cout << "GoodAgent playRound" << endl;
        if (!isInitialized) {
            initReciprocity(numPlayers);
        }

        playerIdx = playerIdx;
        fill_n(allocations, numPlayers, 0);
        allocations[playerIdx] = numTokens;

        povertyRelief(numPlayers, popularities, allocations);
        supportAttackVictims(numPlayers, received, allocations);
        maintainReciprocity(numPlayers, influence, allocations);
        progressiveRedistribution(numPlayers, popularities, allocations);

        allocations[playerIdx] = max(allocations[playerIdx], (int)(numTokens * 0.2));
        cout << "GoodAgent allocations: ";
        for (int i = 0; i < numPlayers; i++) {
            cout << allocations[i] << " ";
        }
        cout << "\nPLAYROUND FINISHED\n" << endl;
    }

    void postContract(int playerIdx) {}

private:
    bool isInitialized;
    double* reciprocityScore;
    double* attackHistory;
    const double POVERTY_THRESHOLD = 0.3;
    int playerIdx;

    void initReciprocity(int numPlayers) {
        reciprocityScore = new double[numPlayers];
        attackHistory = new double[numPlayers];
        fill_n(reciprocityScore, numPlayers, 0.0);
        fill_n(attackHistory, numPlayers, 0.0);
        isInitialized = true;
    }

    void povertyRelief(int numPlayers, double* popularities, int* allocations) {
        cout << "GoodAgent povertyRelief" << endl;
        double maxPop = *max_element(popularities, popularities + numPlayers);
        int reliefPool = (int)(allocations[playerIdx] * 0.15);
        for(int i=0; i<numPlayers; i++) {
            if (reliefPool > 0 && numPlayers > 0) {
                if(popularities[i] < POVERTY_THRESHOLD * maxPop) {
                    allocations[i] += reliefPool / numPlayers;
                }
            }
        }

        allocations[playerIdx] -= reliefPool;
        cout << "GoodAgent povertyRelief finished" << endl;
    }

    void supportAttackVictims(int numPlayers, double* received, int* allocations) {
        int compensationPool = 0;
        for(int i=0; i<numPlayers; i++) {
            if(received[i] < 0) {
                attackHistory[i] += abs(received[i]);
                compensationPool += (int)(abs(received[i]) * 0.5);
            }
        }
        
        allocations[playerIdx] -= compensationPool;
        for(int i=0; i<numPlayers; i++) {
            if(attackHistory[i] > 0) {
                allocations[i] += compensationPool / numPlayers;
            }
        }
    }

    void maintainReciprocity(int numPlayers, double** influence, int* allocations) {
        vector<pair<double,int>> reciprocityRankings;
        for(int i=0; i<numPlayers; i++) {
            reciprocityScore[i] = 0.9 * reciprocityScore[i] + 0.1 * influence[i][playerIdx];
            if(i != playerIdx) {
                reciprocityRankings.emplace_back(reciprocityScore[i], i);
            }
        }
        
        sort(reciprocityRankings.rbegin(), reciprocityRankings.rend());
        int reciprocityPool = (int)(allocations[playerIdx] * 0.1);
        for(int j=0; j<3 && j<reciprocityRankings.size(); j++) {
            allocations[reciprocityRankings[j].second] += reciprocityPool / 3;
        }
        allocations[playerIdx] -= reciprocityPool;
    }

    void progressiveRedistribution(int numPlayers, double* popularities, int* allocations) {
        vector<int> poorest = getPoorestAgents(numPlayers, popularities, 0.5);
        int redistribution = (int)(allocations[playerIdx] * 0.15);
        
        allocations[playerIdx] -= redistribution;
        for(int idx : poorest) {
            allocations[idx] += redistribution / poorest.size();
        }
    }

    vector<int> getPoorestAgents(int numPlayers, double* popularities, double percentile) {
        vector<pair<double,int>> rankings;
        for(int i=0; i<numPlayers; i++) {
            rankings.emplace_back(popularities[i], i);
        }
        sort(rankings.begin(), rankings.end());
        
        vector<int> result;
        for(int i=0; i<numPlayers*percentile; i++) {
            result.push_back(rankings[i].second);
        }
        return result;
    }
};

#endif
