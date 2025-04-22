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
        }
        ~GoodAgent() {}
        void playRound(int numPlayers, int numTokens, int playerIdx, int roundNum, double *received, double *popularities, double **influence, int *allocations) {
        //influence[i][j] player i has on player j
        //received[i] amount of tokens player i received (from me) last round
        //popularities[i] popularity of player i
        //allocations[i] amount of tokens player i will receive from me
            for (int i = 0; i < numPlayers; i++) {
                allocations[i] = 0; // give nothing to anyone by default
            }
            
            allocations[playerIdx] = numTokens; // keep everything, every round
        }
        void postContract(int playerIdx) {}
    private:
        bool isInitialized;
};
#endif