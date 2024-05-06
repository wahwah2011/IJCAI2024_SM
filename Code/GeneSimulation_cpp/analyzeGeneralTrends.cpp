#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <map>

using namespace std;

#define MAX_PLAYERS     10

struct transactionAmounts {
    double CAB1steal, CAB1keep, CAB1give;
    double CAB3steal, CAB3keep, CAB3give;

    transactionAmounts() {
        CAB1steal = CAB1keep = CAB1give = CAB3steal = CAB3keep = CAB3give = 0;
    }
};

struct roiStructure {
    double growth[2][3][5];
    double powerExpended[2][3][5];

    roiStructure() {
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 4; j++) {
                growth[0][i][j] = growth[1][i][j] = 0.0;
                powerExpended[0][i][j] = powerExpended[1][i][j] = 0.0;
            }
        }
    }
};

struct gameTransactions {
    int CABSteal[3], CABKeep[3], CABGive[3];
    int HumanSteal[3], HumanKeep[3], HumanGive[3];

    gameTransactions() {
        for (int i = 0; i < 3; i++) {
            CABSteal[i] = CABKeep[i] = CABGive[i] = HumanSteal[i] = HumanKeep[i] = HumanGive[i] = 0;
        }
    }
};

struct RoundInfo {
    int numPlayers;
    int round;
    double alpha, beta, give, keep, steal;
    double popularities[MAX_PLAYERS];
    double transactions[MAX_PLAYERS][MAX_PLAYERS];
    double influences[MAX_PLAYERS][MAX_PLAYERS];
    string playerTypes[MAX_PLAYERS];
};

vector<string> parse(const string& s) {
    vector<string> tokens;
    string token;
    istringstream tokenStream(s);
    while (getline(tokenStream, token, ','))
        tokens.push_back(token);
    return tokens;
}


RoundInfo readRound(string line, int numPlayers) {
    RoundInfo rnd;
    vector<string> words = parse(line);

    rnd.numPlayers = numPlayers;
    rnd.round = stoi(words[0]);
    rnd.alpha = stof(words[1]);
    rnd.beta = stof(words[2]);
    rnd.give = stof(words[3]);
    rnd.keep = stof(words[4]);
    rnd.steal = stof(words[5]);

    for (int i = 0; i < numPlayers; i++) {
        rnd.popularities[i] = stof(words[i+6]);
    }

    int ind = 6 + numPlayers;
    for (int i = 0; i < numPlayers; i++) {
        for (int j = 0; j < numPlayers; j++) {
            rnd.transactions[i][j] = stof(words[ind]);
            ind ++;
        }
    }

    for (int i = 0; i < numPlayers; i++) {
        for (int j = 0; j < numPlayers; j++) {
            rnd.influences[i][j] = stof(words[ind]);
            ind ++;
        }
    }

    // // bring this back in if it is for the human-bot studies
    // for (int i = 0; i < numPlayers; i++) {
    //     rnd.playerTypes[i] = words[ind];
    //     ind ++;
    // }

    return rnd;
}

int getNumPlayers(string line) {
    vector<string> words = parse(line);
    int i = 6;
    while (words[i][0] == 'p') {
        i++;
    }

    return i - 6;
}

vector<RoundInfo> readGame(string fnombre) {
    cout << fnombre << endl;
    ifstream input(fnombre);

    if (!input) {
        cout << "Could not read file " << fnombre << endl;
        exit(-1);
    }

    vector<RoundInfo> v;

    string line;

    getline(input, line);  // read header
    int numPlayers = getNumPlayers(line);
    int c = 0;
    while (!input.eof()) {
        getline(input, line);
        // cout << c << ": " << line << " is it?" << endl;
        if (line.length() > 2) {
            v.push_back(readRound(line, numPlayers));
            c++;
        }

        // if (c == 1) {
        //     cout << "Types for game: " << fnombre << endl;
        //     for (int i = 0; i < 8; i++) {
        //         cout << "  " << v[c-1].playerTypes[i] << endl;
        //         // cout << "  " << v[0].playerTypes[i] << endl;
        //     }
        // }
    }

    input.close();

    return v;
}

double getSocialWelfare(double popularities[MAX_PLAYERS], int numPlayers) {
    double s = 0.0;
    for (int i = 0; i < numPlayers; i++) {
        s += popularities[i];
    }
    return s / numPlayers;
}

void logSamples(ofstream& output, int gen, string config) {
    for (int trial = 0; trial < 30; trial ++) {
        string fnombre = "../Results/RndGames_" + to_string(gen) + "_10_30_" + config + "/game_" + to_string(trial) + ".csv";
        vector<RoundInfo> v = readGame(fnombre);
        for (int i = 0; i <= 30; i+=5) {
            output << gen << "_" << config << "," << trial << "," << i << "," << getSocialWelfare(v[i].popularities, v[i].numPlayers) << endl;
        }
    }
}

void processWelfares(string fnombre, string code, string condition, ofstream &output) {
    vector<RoundInfo> hh1 = readGame(fnombre);
    // cout << "Types for game: " << fnombre << endl;
    // for (int i = 0; i < hh1[0].numPlayers; i++) {
    //     cout << "  " << hh1[0].playerTypes[i] << endl;
    //     cout << " 2" << hh1[0].playerTypes[i] << ": " << endl;
    // }
    // cout << "Final popularities are " << hh1[0].numPlayers << ": " << endl;
    for (int r = 0; r <= 21; r++) {
        for (int i = 0; i < hh1[0].numPlayers; i++) {
                output << code << "," << condition << "," << hh1[0].playerTypes[i] << "," << r << "," << hh1[r].popularities[i] << endl;
            // string tipo = hh1[0].playerTypes[i];
            // // double val = hh1[hh1.size()-1].popularities[i];
            // double val = hh1[20].popularities[i];
            // finalPop[tipo].push_back(val);
            // cout << "tipo: " << tipo << endl;
            // if (tipo == "Human")
            //     finalPop_Human.push_back(val); 
            // else if (tipo == "Bot")
            //     finalPop_Bot.push_back(val);
            // else {
            //     cout << "tipo2: " << tipo << endl;
            //     cout << "tipo " << tipo << " not found *************" << endl;
            // }
        }
    }
}

void getHumanBotWelfare() {
    // map<string, vector<double> > finalPop;
    // vector<double> finalPop_Bot;
    // vector<double> finalPop_Human;
    ofstream output("../Analysis/csvs/popularities.csv");
    output << "GameCode,Condition,Type,Round,Popularity" << endl;

    // Half and half
    processWelfares("../HumanBotStudy_csvs/half_human_bot/jhg_CXJR.csv", "CXJR", "Even", output);
    processWelfares("../HumanBotStudy_csvs/half_human_bot/jhg_MCZG.csv", "MCZG", "Even", output);
    processWelfares("../HumanBotStudy_csvs/half_human_bot/jhg_PSGN.csv", "PSGN", "Even", output);
    processWelfares("../HumanBotStudy_csvs/half_human_bot/jhg_VBLN.csv", "VBLN", "Even", output);
    processWelfares("../HumanBotStudy_csvs/half_human_bot/jhg_WQDS.csv", "WQDS", "Even", output);
    processWelfares("../HumanBotStudy_csvs/half_human_bot/jhg_XSVC.csv", "XSVC", "Even", output);

    // Majority bot
    processWelfares("../HumanBotStudy_csvs/majority_bot/jhg_GXVS.csv", "GXVS", "Bot Majority", output);
    processWelfares("../HumanBotStudy_csvs/majority_bot/jhg_HNCQ.csv", "HNCQ", "Bot Majority", output);
    processWelfares("../HumanBotStudy_csvs/majority_bot/jhg_SHFC.csv", "SHFC", "Bot Majority", output);
    processWelfares("../HumanBotStudy_csvs/majority_bot/jhg_TKRW.csv", "TKRW", "Bot Majority", output);
    processWelfares("../HumanBotStudy_csvs/majority_bot/jhg_WCJQ.csv", "WCJQ", "Bot Majority", output);
    processWelfares("../HumanBotStudy_csvs/majority_bot/jhg_WHRP.csv", "WHRP", "Bot Majority", output);

    // Majority human
    processWelfares("../HumanBotStudy_csvs/majority_human/jhg_GCVN.csv", "GCVN", "Human Majority", output);
    processWelfares("../HumanBotStudy_csvs/majority_human/jhg_GJFD.csv", "GJFD", "Human Majority", output);
    processWelfares("../HumanBotStudy_csvs/majority_human/jhg_TDGM.csv", "TDGM", "Human Majority", output);
    processWelfares("../HumanBotStudy_csvs/majority_human/jhg_WQJR.csv", "WGJQ", "Human Majority", output);
    processWelfares("../HumanBotStudy_csvs/majority_human/jhg_WRBV.csv", "WRBV", "Human Majority", output);
    processWelfares("../HumanBotStudy_csvs/majority_human/jhg_XTWS.csv", "XTWS", "Human Majority", output);

    output.close();

    // for (map<string, vector<double> >::iterator itr = finalPop.begin(); itr != finalPop.end(); itr++) {
    //     double mean = 0.0;
    //     cout << itr->first << ": ";
    //     for (int i = 0; i < itr->second.size(); i++) {    
    //         cout << itr->second[i] << " ";
    //         mean += itr->second[i];
    //     }
    //     cout << "\nmean of " << itr->first << ": " << (mean / itr->second.size()) << endl;
    // }
}

int getStanding(int index, int round, double popularities[MAX_PLAYERS], int numPlayers) {
    double m = 0;
    for (int i = 0; i < numPlayers; i++)
        m += popularities[i];
    m /= numPlayers;

    if (popularities[index] < (0.75 * m))
        return 0;
    else if (popularities[index] > (1.25 * m))
        return 2;

    return 1;
}

void processTokenAllocations(string fnombre, string code, ofstream &outputAllocations, ofstream &outputWho) {
    vector<RoundInfo> v = readGame(fnombre);

    for (int i = 0; i < v[0].numPlayers; i++) {
        int tokensKept = 0;
        int tokensGiven = 0, tokensGivenH = 0, tokensGivenB = 0;
        int tokensStolen = 0;
        for (int r = 1; r <= 21; r++) {
            tokensKept += v[r].transactions[i][i];
            int check = 0;
            for (int j = 0; j < v[0].numPlayers; j++) {
                check += abs(v[r].transactions[i][j]);
                if (i == j)
                    continue;

                if (v[r].transactions[i][j] < 0)
                    tokensStolen -= v[r].transactions[i][j];
                else {
                    tokensGiven += v[r].transactions[i][j];
                    if (v[r].playerTypes[j] == "Human")
                        tokensGivenH += v[r].transactions[i][j];
                    else
                        tokensGivenB += v[r].transactions[i][j];
                }
            }

            if ((check != 2 * v[0].numPlayers) && (r > 0)) {
                cout << "tokens check doesn't work: " << check << endl;
                exit(1);
            }
        }
        outputAllocations << code << "," << v[0].playerTypes[i] << ",Keeping," << (((double)tokensKept) / (42.0 * v[0].numPlayers)) << endl;
        outputAllocations << code << "," << v[0].playerTypes[i] << ",Giving," << (((double)tokensGiven) / (42.0 * v[0].numPlayers)) << endl;
        outputAllocations << code << "," << v[0].playerTypes[i] << ",Stealing," << (((double)tokensStolen) / (42.0 * v[0].numPlayers)) << endl;

        outputWho << code << "," << v[0].playerTypes[i] << ",given2Human," << tokensGivenH << endl;
        outputWho << code << "," << v[0].playerTypes[i] << ",given2Bot," << tokensGivenB << endl;
    }
}

gameTransactions processTokenAllocationsByClass(string fnombre) {
    vector<RoundInfo> v = readGame(fnombre);

    gameTransactions tAmounts;

    for (int i = 0; i < v[0].numPlayers; i++) {
        for (int r = 1; r <= 21; r++) {
            int status = getStanding(i, r, v[r].popularities, 8);

            if (v[r].playerTypes[i] == "Human")
                tAmounts.HumanKeep[status] += v[r].transactions[i][i];
            else
                tAmounts.CABKeep[status] += v[r].transactions[i][i];
            int check = 0;
            for (int j = 0; j < v[0].numPlayers; j++) {
                check += abs(v[r].transactions[i][j]);
                if (i == j)
                    continue;

                if (v[r].transactions[i][j] < 0) {
                    if (v[r].playerTypes[i] == "Human")
                        tAmounts.HumanSteal[status] -= v[r].transactions[i][j];
                    else
                        tAmounts.CABSteal[status] -= v[r].transactions[i][j];
                }
                else {
                    if (v[r].playerTypes[i] == "Human")
                        tAmounts.HumanGive[status] += v[r].transactions[i][j];
                    else
                        tAmounts.CABGive[status] += v[r].transactions[i][j];
                }
            }

            if ((check != 2 * v[0].numPlayers) && (r > 0)) {
                cout << "tokens check doesn't work: " << check << endl;
                exit(1);
            }
        }
        // outputAllocations << code << "," << v[0].playerTypes[i] << ",Keeping," << (((double)tokensKept) / (42.0 * v[0].numPlayers)) << endl;
        // outputAllocations << code << "," << v[0].playerTypes[i] << ",Giving," << (((double)tokensGiven) / (42.0 * v[0].numPlayers)) << endl;
        // outputAllocations << code << "," << v[0].playerTypes[i] << ",Stealing," << (((double)tokensStolen) / (42.0 * v[0].numPlayers)) << endl;

        // outputWho << code << "," << v[0].playerTypes[i] << ",given2Human," << tokensGivenH << endl;
        // outputWho << code << "," << v[0].playerTypes[i] << ",given2Bot," << tokensGivenB << endl;
    }

    return tAmounts;
}

void addAmounts(gameTransactions tAmounts, gameTransactions &totalAmounts) {
    for (int i = 0; i < 3; i++) {
        totalAmounts.HumanKeep[i] += tAmounts.HumanKeep[i];
        totalAmounts.HumanGive[i] += tAmounts.HumanGive[i];
        totalAmounts.HumanSteal[i] += tAmounts.HumanSteal[i];
        totalAmounts.CABKeep[i] += tAmounts.CABKeep[i];
        totalAmounts.CABGive[i] += tAmounts.CABGive[i];
        totalAmounts.CABSteal[i] += tAmounts.CABSteal[i];
    }
}

void processHumanBotAllocationsByClass() {
    gameTransactions totalAmounts;

    // Even
    gameTransactions tAmounts = processTokenAllocationsByClass("../HumanBotStudy_csvs/half_human_bot/jhg_CXJR.csv");
    addAmounts(tAmounts, totalAmounts);
    tAmounts = processTokenAllocationsByClass("../HumanBotStudy_csvs/half_human_bot/jhg_MCZG.csv");
    addAmounts(tAmounts, totalAmounts);
    tAmounts = processTokenAllocationsByClass("../HumanBotStudy_csvs/half_human_bot/jhg_PSGN.csv");
    addAmounts(tAmounts, totalAmounts);
    tAmounts = processTokenAllocationsByClass("../HumanBotStudy_csvs/half_human_bot/jhg_VBLN.csv");
    addAmounts(tAmounts, totalAmounts);
    tAmounts = processTokenAllocationsByClass("../HumanBotStudy_csvs/half_human_bot/jhg_WQDS.csv");
    addAmounts(tAmounts, totalAmounts);
    tAmounts = processTokenAllocationsByClass("../HumanBotStudy_csvs/half_human_bot/jhg_XSVC.csv");
    addAmounts(tAmounts, totalAmounts);

    // // Majority bot
    tAmounts = processTokenAllocationsByClass("../HumanBotStudy_csvs/majority_bot/jhg_GXVS.csv");
    addAmounts(tAmounts, totalAmounts);
    tAmounts = processTokenAllocationsByClass("../HumanBotStudy_csvs/majority_bot/jhg_HNCQ.csv");
    addAmounts(tAmounts, totalAmounts);
    tAmounts = processTokenAllocationsByClass("../HumanBotStudy_csvs/majority_bot/jhg_SHFC.csv");
    addAmounts(tAmounts, totalAmounts);
    tAmounts = processTokenAllocationsByClass("../HumanBotStudy_csvs/majority_bot/jhg_TKRW.csv");
    addAmounts(tAmounts, totalAmounts);
    tAmounts = processTokenAllocationsByClass("../HumanBotStudy_csvs/majority_bot/jhg_WCJQ.csv");
    addAmounts(tAmounts, totalAmounts);
    tAmounts = processTokenAllocationsByClass("../HumanBotStudy_csvs/majority_bot/jhg_WHRP.csv");
    addAmounts(tAmounts, totalAmounts);

    // // Majority human
    tAmounts = processTokenAllocationsByClass("../HumanBotStudy_csvs/majority_human/jhg_GCVN.csv");
    addAmounts(tAmounts, totalAmounts);
    tAmounts = processTokenAllocationsByClass("../HumanBotStudy_csvs/majority_human/jhg_GJFD.csv");
    addAmounts(tAmounts, totalAmounts);
    tAmounts = processTokenAllocationsByClass("../HumanBotStudy_csvs/majority_human/jhg_TDGM.csv");
    addAmounts(tAmounts, totalAmounts);
    tAmounts = processTokenAllocationsByClass("../HumanBotStudy_csvs/majority_human/jhg_WQJR.csv");
    addAmounts(tAmounts, totalAmounts);
    tAmounts = processTokenAllocationsByClass("../HumanBotStudy_csvs/majority_human/jhg_WRBV.csv");
    addAmounts(tAmounts, totalAmounts);
    tAmounts = processTokenAllocationsByClass("../HumanBotStudy_csvs/majority_human/jhg_XTWS.csv");
    addAmounts(tAmounts, totalAmounts);

    cout << "              Keep      Steal     Give" << endl;
    cout << "CAB poor:     " << totalAmounts.CABKeep[0] << "       " << totalAmounts.CABSteal[0] << "        " << totalAmounts.CABGive[0] << endl;
    cout << "CAB middle:   " << totalAmounts.CABKeep[1] << "       " << totalAmounts.CABSteal[1] << "        " << totalAmounts.CABGive[1] << endl;
    cout << "CAB rich:     " << totalAmounts.CABKeep[2] << "       " << totalAmounts.CABSteal[2] << "        " << totalAmounts.CABGive[2] << endl;
    cout << "Human poor:   " << totalAmounts.HumanKeep[0] << "       " << totalAmounts.HumanSteal[0] << "        " << totalAmounts.HumanGive[0] << endl;
    cout << "Human middle: " << totalAmounts.HumanKeep[1] << "       " << totalAmounts.HumanSteal[1] << "        " << totalAmounts.HumanGive[1] << endl;
    cout << "Human rich:   " << totalAmounts.HumanKeep[2] << "       " << totalAmounts.HumanSteal[2] << "        " << totalAmounts.HumanGive[2] << endl;
}

void processHumanBotAllocations() {
    ofstream output("../Analysis/csvs/allocations.csv");
    output << "GameCode,Type,Transaction,Proportion" << endl;

    ofstream outputWho("../Analysis/csvs/allocationsWho.csv");
    outputWho << "GameCode,Type,Who,Amount" << endl;

    processTokenAllocations("../HumanBotStudy_csvs/half_human_bot/jhg_CXJR.csv", "CXJR", output, outputWho);
    processTokenAllocations("../HumanBotStudy_csvs/half_human_bot/jhg_MCZG.csv", "MCZG", output, outputWho);
    processTokenAllocations("../HumanBotStudy_csvs/half_human_bot/jhg_PSGN.csv", "PSGN", output, outputWho);
    processTokenAllocations("../HumanBotStudy_csvs/half_human_bot/jhg_VBLN.csv", "VBLN", output, outputWho);
    processTokenAllocations("../HumanBotStudy_csvs/half_human_bot/jhg_WQDS.csv", "WQDS", output, outputWho);
    processTokenAllocations("../HumanBotStudy_csvs/half_human_bot/jhg_XSVC.csv", "XSVC", output, outputWho);

    // Majority bot
    processTokenAllocations("../HumanBotStudy_csvs/majority_bot/jhg_GXVS.csv", "GXVS", output, outputWho);
    processTokenAllocations("../HumanBotStudy_csvs/majority_bot/jhg_HNCQ.csv", "HNCQ", output, outputWho);
    processTokenAllocations("../HumanBotStudy_csvs/majority_bot/jhg_SHFC.csv", "SHFC", output, outputWho);
    processTokenAllocations("../HumanBotStudy_csvs/majority_bot/jhg_TKRW.csv", "TKRW", output, outputWho);
    processTokenAllocations("../HumanBotStudy_csvs/majority_bot/jhg_WCJQ.csv", "WCJQ", output, outputWho);
    processTokenAllocations("../HumanBotStudy_csvs/majority_bot/jhg_WHRP.csv", "WHRP", output, outputWho);

    // Majority human
    processTokenAllocations("../HumanBotStudy_csvs/majority_human/jhg_GCVN.csv", "GCVN", output, outputWho);
    processTokenAllocations("../HumanBotStudy_csvs/majority_human/jhg_GJFD.csv", "GJFD", output, outputWho);
    processTokenAllocations("../HumanBotStudy_csvs/majority_human/jhg_TDGM.csv", "TDGM", output, outputWho);
    processTokenAllocations("../HumanBotStudy_csvs/majority_human/jhg_WQJR.csv", "WGJQ", output, outputWho);
    processTokenAllocations("../HumanBotStudy_csvs/majority_human/jhg_WRBV.csv", "WRBV", output, outputWho);
    processTokenAllocations("../HumanBotStudy_csvs/majority_human/jhg_XTWS.csv", "XTWS", output, outputWho);


    output.close();
    outputWho.close();
}

void doFriends(string fnombre, string code, ofstream &output, ofstream &outputWho, ofstream &outputAmount) {
    vector<RoundInfo> v = readGame(fnombre);

    for (int r = 2; r <= 21; r++) {
        for (int i = 0; i < v[0].numPlayers; i++) {
            int numFriends = 0;
            for (int j = 0; j < v[0].numPlayers; j++) {
                if (i == j)
                    continue;
                

                if (((v[r-1].transactions[i][j] + v[r].transactions[i][j]) >= 2) && (((v[r-1].transactions[j][i] + v[r].transactions[j][i]) >= 2))) {
                    numFriends ++;
                }
            }

            output << code << "," << v[0].playerTypes[i] << "," << r << "," << numFriends << endl;
        }
    }

    for (int i = 0; i < v[0].numPlayers; i++) {
        int numBotFriends = 0;
        int numHumanFriends = 0;
        int totalBots = 0;
        int totalHumans = 0;
        for (int j = 0; j < v[0].numPlayers; j++) {
            for (int r = 2; r <= 21; r++) {
                if (i == j)
                    continue;
                
                if (((v[r-1].transactions[i][j] + v[r].transactions[i][j]) >= 2) && (((v[r-1].transactions[j][i] + v[r].transactions[j][i]) >= 2))) {
                    if (v[0].playerTypes[j] == "Bot")
                        numBotFriends ++;
                    else
                        numHumanFriends ++;
                }
                if (v[0].playerTypes[j] == "Bot")
                    totalBots ++;
                else
                    totalHumans ++;

            }
        }
        outputWho << code << "," << v[0].playerTypes[i] << ",Bots," << (((double)numBotFriends * 100.0) / totalBots) << endl;
        outputWho << code << "," << v[0].playerTypes[i] << ",Humans," << (((double)numHumanFriends * 100.0) / totalHumans) << endl;
    }

    for (int i = 0; i < v[0].numPlayers; i++) {
        int numBotFriends = 0;
        int numHumanFriends = 0;
        int botShare = 0;
        int humanShare = 0;
        for (int j = 0; j < v[0].numPlayers; j++) {
            for (int r = 2; r <= 21; r++) {
                if (i == j)
                    continue;
                
                if (((v[r-1].transactions[i][j] + v[r].transactions[i][j]) >= 2) && (((v[r-1].transactions[j][i] + v[r].transactions[j][i]) >= 2))) {
                    if (v[0].playerTypes[j] == "Bot") {
                        numBotFriends ++;
                        botShare += (v[r-1].transactions[i][j] + v[r].transactions[i][j]) / 2.0;// + (v[r-1].transactions[j][i] + v[r].transactions[j][i])) / 4.0;
                    }
                    else {
                        numHumanFriends ++;
                        humanShare += (v[r-1].transactions[i][j] + v[r].transactions[i][j]) / 2.0;//+ (v[r-1].transactions[j][i] + v[r].transactions[j][i])) / 4.0;
                    }
                }
            }
        }
        if (numBotFriends > 0)
            outputAmount << code << "," << v[0].playerTypes[i] << ",Bots," << (((double)botShare) / numBotFriends) << endl;
        if (numHumanFriends > 0)
            outputAmount << code << "," << v[0].playerTypes[i] << ",Humans," << (((double)humanShare) / numHumanFriends) << endl;
    }


}

void numberOfFriends() {
    ofstream output("../Analysis/csvs/amigos.csv");
    output << "GameCode,Type,Round,numFriends" << endl;

    ofstream outputWho("../Analysis/csvs/amigosWho.csv");
    outputWho << "GameCode,Type,Who,Percent" << endl;

    ofstream outputAmount("../Analysis/csvs/amigosStrength.csv");
    outputAmount << "GameCode,Type,Who,Amount" << endl;

    doFriends("../HumanBotStudy_csvs/half_human_bot/jhg_CXJR.csv", "CXJR", output, outputWho, outputAmount);
    doFriends("../HumanBotStudy_csvs/half_human_bot/jhg_MCZG.csv", "MCZG", output, outputWho, outputAmount);
    doFriends("../HumanBotStudy_csvs/half_human_bot/jhg_PSGN.csv", "PSGN", output, outputWho, outputAmount);
    doFriends("../HumanBotStudy_csvs/half_human_bot/jhg_VBLN.csv", "VBLN", output, outputWho, outputAmount);
    doFriends("../HumanBotStudy_csvs/half_human_bot/jhg_WQDS.csv", "WQDS", output, outputWho, outputAmount);
    doFriends("../HumanBotStudy_csvs/half_human_bot/jhg_XSVC.csv", "XSVC", output, outputWho, outputAmount);

    // Majority bot
    doFriends("../HumanBotStudy_csvs/majority_bot/jhg_GXVS.csv", "GXVS", output, outputWho, outputAmount);
    doFriends("../HumanBotStudy_csvs/majority_bot/jhg_HNCQ.csv", "HNCQ", output, outputWho, outputAmount);
    doFriends("../HumanBotStudy_csvs/majority_bot/jhg_SHFC.csv", "SHFC", output, outputWho, outputAmount);
    doFriends("../HumanBotStudy_csvs/majority_bot/jhg_TKRW.csv", "TKRW", output, outputWho, outputAmount);
    doFriends("../HumanBotStudy_csvs/majority_bot/jhg_WCJQ.csv", "WCJQ", output, outputWho, outputAmount);
    doFriends("../HumanBotStudy_csvs/majority_bot/jhg_WHRP.csv", "WHRP", output, outputWho, outputAmount);

    // Majority human
    doFriends("../HumanBotStudy_csvs/majority_human/jhg_GCVN.csv", "GCVN", output, outputWho, outputAmount);
    doFriends("../HumanBotStudy_csvs/majority_human/jhg_GJFD.csv", "GJFD", output, outputWho, outputAmount);
    doFriends("../HumanBotStudy_csvs/majority_human/jhg_TDGM.csv", "TDGM", output, outputWho, outputAmount);
    doFriends("../HumanBotStudy_csvs/majority_human/jhg_WQJR.csv", "WGJQ", output, outputWho, outputAmount);
    doFriends("../HumanBotStudy_csvs/majority_human/jhg_WRBV.csv", "WRBV", output, outputWho, outputAmount);
    doFriends("../HumanBotStudy_csvs/majority_human/jhg_XTWS.csv", "XTWS", output, outputWho, outputAmount);

    output.close();
    outputWho.close();
    outputAmount.close();
}

void thievesExample() {
    string fnombre = "../Results/Thieves/log_100.csv";
    vector<RoundInfo> v = readGame(fnombre);

    ofstream output("../Analysis/csvs/thiefExample_3_varied.csv");
    output << "Round,Agent,Type,Popularity" << endl;

    for (int i = 0; i <= 30; i++) {
        for (int j = 0; j < 10; j++) {
            if (j < 8)
                output << i << ",A" << j << ",CAB," << v[i].popularities[j] << endl;
            else
                output << i << ",A" << j << ",Thief," << v[i].popularities[j] << endl;
        }
    }

    output.close();
}

// def computeGini2(P):
//     sum = 0.0
//     m = 0.0
//     for i in range(0, len(P)):
//         m = m + P[i]
//         for j in range(0, len(P)):
//             sum = sum + abs(P[i] - P[j])
//     m = m / len(P)

//     return sum / (2 * len(P) * len(P) * m)


double computeGini(double P[MAX_PLAYERS], int numPlayers) {
    double sum = 0.0;
    double m = 0.0;
    for (int i = 0; i < numPlayers; i++) {
        m += P[i];
        for (int j = 0; j < numPlayers; j++) {
            sum += fabs(P[i] - P[j]);
        }
    }
    m /= numPlayers;

    return sum / (2.0 * numPlayers * numPlayers * m);

}

void computeWelfareGini(string fnombre, string gameCode, string condition, ofstream &output) {
    vector<RoundInfo> v = readGame(fnombre);

    double welfare = 0.0;
    for (int i = 0; i < 8; i++) {
        welfare += v[21].popularities[i];
    }
    welfare /= 8.0;

    output << gameCode << "," << condition << "," << welfare << "," << computeGini(v[21].popularities, 8) << endl;
}

void scatterPlotCSV() {

    ofstream output("../Analysis/csvs/welfare_gini_scatter.csv");
    output << "GameCode,Condition,Social Welfare,Gini Index" << endl;

    computeWelfareGini("../HumanBotStudy_csvs/half_human_bot/jhg_CXJR.csv", "CXJR", "Even", output);
    computeWelfareGini("../HumanBotStudy_csvs/half_human_bot/jhg_MCZG.csv", "MCZG", "Even", output);
    computeWelfareGini("../HumanBotStudy_csvs/half_human_bot/jhg_PSGN.csv", "PSGN", "Even", output);
    computeWelfareGini("../HumanBotStudy_csvs/half_human_bot/jhg_VBLN.csv", "VBLN", "Even", output);
    computeWelfareGini("../HumanBotStudy_csvs/half_human_bot/jhg_WQDS.csv", "WQDS", "Even", output);
    computeWelfareGini("../HumanBotStudy_csvs/half_human_bot/jhg_XSVC.csv", "XSVC", "Even", output);

    // Majority bot
    computeWelfareGini("../HumanBotStudy_csvs/majority_bot/jhg_GXVS.csv", "GXVS", "Bot Majority", output);
    computeWelfareGini("../HumanBotStudy_csvs/majority_bot/jhg_HNCQ.csv", "HNCQ", "Bot Majority", output);
    computeWelfareGini("../HumanBotStudy_csvs/majority_bot/jhg_SHFC.csv", "SHFC", "Bot Majority", output);
    computeWelfareGini("../HumanBotStudy_csvs/majority_bot/jhg_TKRW.csv", "TKRW", "Bot Majority", output);
    computeWelfareGini("../HumanBotStudy_csvs/majority_bot/jhg_WCJQ.csv", "WCJQ", "Bot Majority", output);
    computeWelfareGini("../HumanBotStudy_csvs/majority_bot/jhg_WHRP.csv", "WHRP", "Bot Majority", output);

    // Majority human
    computeWelfareGini("../HumanBotStudy_csvs/majority_human/jhg_GCVN.csv", "GCVN", "Human Majority", output);
    computeWelfareGini("../HumanBotStudy_csvs/majority_human/jhg_GJFD.csv", "GJFD", "Human Majority", output);
    computeWelfareGini("../HumanBotStudy_csvs/majority_human/jhg_TDGM.csv", "TDGM", "Human Majority", output);
    computeWelfareGini("../HumanBotStudy_csvs/majority_human/jhg_WQJR.csv", "WGJQ", "Human Majority", output);
    computeWelfareGini("../HumanBotStudy_csvs/majority_human/jhg_WRBV.csv", "WRBV", "Human Majority", output);
    computeWelfareGini("../HumanBotStudy_csvs/majority_human/jhg_XTWS.csv", "XTWS", "Human Majority", output);

    output.close();
}

transactionAmounts processCABAllocationType(string fnombre, transactionAmounts totals[4]) {
    vector<RoundInfo> v = readGame(fnombre);
    transactionAmounts t;

    for (int r = 1; r <= 30; r++) {
        for (int i = 0; i < 5; i++) {
            for (int j = 0; j < 10; j++) {
                if (i == j) {
                    // count += (int)(v[r].transactions[i][j] * 10 + 0.5);
                    t.CAB1keep += (int)(v[r].transactions[i][j] * 10 + 0.5);
                }
                else if (v[r].transactions[i][j] < 0) {
                    // count -= int(fabs(v[r].transactions[i][j]) * 10 + 0.5);
                    t.CAB1steal += (int)(fabs(v[r].transactions[i][j]) * 10 + 0.5);
                }
                else {
                    // cout += (int)(v[r].transactions[i][j] * 10 + 0.5);
                    t.CAB1give += (int)(v[r].transactions[i][j] * 10 + 0.5);
                }
            }
        }

        for (int i = 5; i < 10; i++) {
            int status = getStanding(i, r, v[r].popularities, 10);
            for (int j = 0; j < 10; j++) {
                if (i == j) {
                    t.CAB3keep += (int)(v[r].transactions[i][j] * 10 + 0.5);
                    totals[status].CAB3keep += (int)(v[r].transactions[i][j] * 10 + 0.5);
                }
                else if (v[r].transactions[i][j] < 0) {
                    t.CAB3steal += (int)(fabs(v[r].transactions[i][j]) * 10 + 0.5);
                    totals[status].CAB3steal += (int)(fabs(v[r].transactions[i][j]) * 10 + 0.5);
                }
                else {
                    t.CAB3give += (int)(v[r].transactions[i][j] * 10 + 0.5);
                    totals[status].CAB3give += (int)(v[r].transactions[i][j] * 10 + 0.5);
                }
            } 
        }
    }

    totals[3].CAB1steal += t.CAB1steal;
    totals[3].CAB1keep += t.CAB1keep;
    totals[3].CAB1give += t.CAB1give;
    totals[3].CAB3steal += t.CAB3steal;
    totals[3].CAB3keep += t.CAB3keep;
    totals[3].CAB3give += t.CAB3give;


    return t;
}

void processCABTokenAllocations() {
    transactionAmounts totals[4];

    for (int i = 0; i < 50; i++) {
        string fnombre = "../BestBots_CAB/equal/game_" + to_string(i) + ".csv";
        transactionAmounts t = processCABAllocationType(fnombre, totals);
        cout << "CAB1: " << t.CAB1steal << "; " << t.CAB1keep << "; " << t.CAB1give << endl;
        cout << "CAB3: " << t.CAB3steal << "; " << t.CAB3keep << "; " << t.CAB3give << endl << endl;;
        // int amount = t.CAB1steal + t.CAB1keep + t.CAB1give + t.CAB3steal + t.CAB3keep + t.CAB3give;
        // if (amount != 3000) {
        //     cout << "only got " << amount << " tokens in equal " << i << endl;
        //     exit(-1);
        // }

        fnombre = "../BestBots_CAB/highlow/game_" + to_string(i) + ".csv";
        t = processCABAllocationType(fnombre, totals);

        fnombre = "../BestBots_CAB/power/game_" + to_string(i) + ".csv";
        t = processCABAllocationType(fnombre, totals);

        fnombre = "../BestBots_CAB/random/game_" + to_string(i) + ".csv";
        t = processCABAllocationType(fnombre, totals);

        fnombre = "../BestBots_CAB/step/game_" + to_string(i) + ".csv";
        t = processCABAllocationType(fnombre, totals);

    }

    cout << "\nTotals:" << endl;
    cout << "CAB1: " << totals[3].CAB1steal << "; " << totals[3].CAB1keep << "; " << totals[3].CAB1give << endl;
    cout << "CAB3: " << totals[3].CAB3steal << "; " << totals[3].CAB3keep << "; " << totals[3].CAB3give << endl << endl;

    cout << "\n CAB 3 Class Totals:" << endl;
    cout << "CAB3: " << totals[0].CAB3steal << "; " << totals[0].CAB3keep << "; " << totals[0].CAB3give << endl << endl;
    cout << "CAB3: " << totals[1].CAB3steal << "; " << totals[1].CAB3keep << "; " << totals[1].CAB3give << endl << endl;
    cout << "CAB3: " << totals[2].CAB3steal << "; " << totals[2].CAB3keep << "; " << totals[2].CAB3give << endl << endl;
}

roiStructure computeROIbyClass(string fnombre) {
    vector<RoundInfo> v = readGame(fnombre);
    roiStructure roi;
    int playerStatus, playerType, otherStatus;
    double alpha = 0.2;

    for (int i = 0; i < v[0].numPlayers; i++) {
        for (int r = 2; r <= 21; r++) {
            playerStatus = getStanding(i, r, v[r].popularities, 8);
            if (v[r].playerTypes[i] == "Human")
                playerType = 0;
            else
                playerType = 1;

            roi.powerExpended[playerType][playerStatus][3] += ((v[r].transactions[i][i] * v[r-1].popularities[i]) * alpha) / 16.0;
            roi.growth[playerType][playerStatus][3] += (v[r].influences[i][i] - (v[r-1].influences[i][i] * (1-alpha)));

            int check = 0;
            for (int j = 0; j < v[0].numPlayers; j++) {
                check += abs(v[r].transactions[i][j]);
                if (i == j) 
                    continue;

                
                else if (v[r].transactions[i][j] < 0) {
                    roi.powerExpended[playerType][playerStatus][3] += ((abs(v[r].transactions[i][j]) * v[r-1].popularities[i]) * alpha / 16.0);
                }
                else {
                    otherStatus = getStanding(j, r, v[r].popularities, 8);
                    roi.powerExpended[playerType][playerStatus][otherStatus] += ((abs(v[r].transactions[i][j]) * v[r-1].popularities[i]) * alpha) / 16.0;
                    roi.growth[playerType][playerStatus][otherStatus] += (v[r].influences[j][i] - (v[r-1].influences[j][i] * (1-alpha)));
                }
            }

            if ((check != 2 * v[0].numPlayers) && (r > 0)) {
                cout << "tokens check doesn't work: " << check << endl;
                exit(1);
            }
        }
    }

    return roi;
}

void addROI(roiStructure temp, roiStructure &roi) {
    for (int k = 0; k < 2; k++) {
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 4; j++) {
                roi.growth[k][i][j] += temp.growth[k][i][j];
                roi.powerExpended[k][i][j] += temp.powerExpended[k][i][j];
            }
        }
    }
}

void getROIbyClass() {
    roiStructure roi;
    roiStructure roiTemp;
    roiTemp = computeROIbyClass("../HumanBotStudy_csvs/half_human_bot/jhg_CXJR.csv");
    addROI(roiTemp, roi);
    roiTemp = computeROIbyClass("../HumanBotStudy_csvs/half_human_bot/jhg_MCZG.csv");
    addROI(roiTemp, roi);
    roiTemp = computeROIbyClass("../HumanBotStudy_csvs/half_human_bot/jhg_PSGN.csv");
    addROI(roiTemp, roi);
    roiTemp = computeROIbyClass("../HumanBotStudy_csvs/half_human_bot/jhg_VBLN.csv");
    addROI(roiTemp, roi);
    roiTemp = computeROIbyClass("../HumanBotStudy_csvs/half_human_bot/jhg_WQDS.csv");
    addROI(roiTemp, roi);
    roiTemp = computeROIbyClass("../HumanBotStudy_csvs/half_human_bot/jhg_XSVC.csv");
    addROI(roiTemp, roi);

    roiTemp = computeROIbyClass("../HumanBotStudy_csvs/majority_bot/jhg_GXVS.csv");
    addROI(roiTemp, roi);
    roiTemp = computeROIbyClass("../HumanBotStudy_csvs/majority_bot/jhg_HNCQ.csv");
    addROI(roiTemp, roi);
    roiTemp = computeROIbyClass("../HumanBotStudy_csvs/majority_bot/jhg_SHFC.csv");
    addROI(roiTemp, roi);
    roiTemp = computeROIbyClass("../HumanBotStudy_csvs/majority_bot/jhg_TKRW.csv");
    addROI(roiTemp, roi);
    roiTemp = computeROIbyClass("../HumanBotStudy_csvs/majority_bot/jhg_WCJQ.csv");
    addROI(roiTemp, roi);
    roiTemp = computeROIbyClass("../HumanBotStudy_csvs/majority_bot/jhg_WHRP.csv");
    addROI(roiTemp, roi);

    roiTemp = computeROIbyClass("../HumanBotStudy_csvs/majority_human/jhg_GCVN.csv");
    addROI(roiTemp, roi);
    roiTemp = computeROIbyClass("../HumanBotStudy_csvs/majority_human/jhg_GJFD.csv");
    addROI(roiTemp, roi);
    roiTemp = computeROIbyClass("../HumanBotStudy_csvs/majority_human/jhg_TDGM.csv");
    addROI(roiTemp, roi);
    roiTemp = computeROIbyClass("../HumanBotStudy_csvs/majority_human/jhg_WQJR.csv");
    addROI(roiTemp, roi);
    roiTemp = computeROIbyClass("../HumanBotStudy_csvs/majority_human/jhg_WRBV.csv");
    addROI(roiTemp, roi);
    roiTemp = computeROIbyClass("../HumanBotStudy_csvs/majority_human/jhg_XTWS.csv");
    addROI(roiTemp, roi);

    // compute total
    for (int k = 0; k < 2; k++) {
        for (int i = 0; i < 3; i++) {
            roi.growth[k][i][4] = roi.powerExpended[k][i][4] = 0.0;
            for (int j = 0; j < 4; j++) {
                roi.growth[k][i][4] += roi.growth[k][i][j];
                roi.powerExpended[k][i][4] += roi.powerExpended[k][i][j];
            }
        }
    }


    cout << "Human ROI" << endl;
    cout << "          Poor         Middle       Rich        Self        Total" << endl;
    cout << "Poor:     " << (roi.growth[0][0][0] / roi.powerExpended[0][0][0]) << "    " << (roi.growth[0][0][1] / roi.powerExpended[0][0][1]) << "    " << (roi.growth[0][0][2] / roi.powerExpended[0][0][2]) << "    " << (roi.growth[0][0][3] / roi.powerExpended[0][0][3]) << "    " << (roi.growth[0][0][4] / roi.powerExpended[0][0][4])<< endl;
    cout << "Middle:   " << (roi.growth[0][1][0] / roi.powerExpended[0][1][0]) << "    " << (roi.growth[0][1][1] / roi.powerExpended[0][1][1]) << "    " << (roi.growth[0][1][2] / roi.powerExpended[0][1][2]) << "    " << (roi.growth[0][1][3] / roi.powerExpended[0][1][3]) << "    " << (roi.growth[0][1][4] / roi.powerExpended[0][1][4])<< endl;
    cout << "Rich:     " << (roi.growth[0][2][0] / roi.powerExpended[0][2][0]) << "    " << (roi.growth[0][2][1] / roi.powerExpended[0][2][1]) << "    " << (roi.growth[0][2][2] / roi.powerExpended[0][2][2]) << "    " << (roi.growth[0][2][3] / roi.powerExpended[0][2][3]) << "    " << (roi.growth[0][2][4] / roi.powerExpended[0][2][4])<< endl;

    cout << endl;
    cout << "CAB ROI" << endl;
    cout << "          Poor         Middle       Rich        Self        Total" << endl;
    cout << "Poor:     " << (roi.growth[1][0][0] / roi.powerExpended[1][0][0]) << "    " << (roi.growth[1][0][1] / roi.powerExpended[1][0][1]) << "    " << (roi.growth[1][0][2] / roi.powerExpended[1][0][2]) << "    " << (roi.growth[1][0][3] / roi.powerExpended[1][0][3]) << "    " << (roi.growth[1][0][4] / roi.powerExpended[1][0][4])<< endl;
    cout << "Middle:   " << (roi.growth[1][1][0] / roi.powerExpended[1][1][0]) << "    " << (roi.growth[1][1][1] / roi.powerExpended[1][1][1]) << "    " << (roi.growth[1][1][2] / roi.powerExpended[1][1][2]) << "    " << (roi.growth[1][1][3] / roi.powerExpended[1][1][3]) << "    " << (roi.growth[1][1][4] / roi.powerExpended[1][1][4])<< endl;
    cout << "Rich:     " << (roi.growth[1][2][0] / roi.powerExpended[1][2][0]) << "    " << (roi.growth[1][2][1] / roi.powerExpended[1][2][1]) << "    " << (roi.growth[1][2][2] / roi.powerExpended[1][2][2]) << "    " << (roi.growth[1][2][3] / roi.powerExpended[1][2][3]) << "    " << (roi.growth[1][2][4] / roi.powerExpended[1][2][4])<< endl;

    // cout << endl;
    // cout << "Human Expended" << endl;
    // cout << "          Poor         Middle       Rich        Self" << endl;
    // cout << "Poor:     " << (roi.powerExpended[0][0][0]) << "    " << (roi.powerExpended[0][0][1]) << "    " << (roi.powerExpended[0][0][2]) << "    " << (roi.powerExpended[0][0][3]) << endl;
    // cout << "Middle:   " << (roi.powerExpended[0][1][0]) << "    " << (roi.powerExpended[0][1][1]) << "    " << (roi.powerExpended[0][1][2]) << "    " << (roi.powerExpended[0][1][3]) << endl;
    // cout << "Rich:     " << (roi.powerExpended[0][2][0]) << "    " << (roi.powerExpended[0][2][1]) << "    " << (roi.powerExpended[0][2][2]) << "    " << (roi.powerExpended[0][2][3]) << endl;

    // cout << endl;
    // cout << "CAB Expended" << endl;
    // cout << "          Poor         Middle       Rich        Self" << endl;
    // cout << "Poor:     " << (roi.powerExpended[1][0][0]) << "    " << (roi.powerExpended[1][0][1]) << "    " << (roi.powerExpended[1][0][2]) << "    " << (roi.powerExpended[1][0][3]) << endl;
    // cout << "Middle:   " << (roi.powerExpended[1][1][0]) << "    " << (roi.powerExpended[1][1][1]) << "    " << (roi.powerExpended[1][1][2]) << "    " << (roi.powerExpended[1][1][3]) << endl;
    // cout << "Rich:     " << (roi.powerExpended[1][2][0]) << "    " << (roi.powerExpended[1][2][1]) << "    " << (roi.powerExpended[1][2][2]) << "    " << (roi.powerExpended[1][2][3]) << endl;

    // cout << endl;
    // cout << "Human Growth" << endl;
    // cout << "          Poor         Middle       Rich        Self" << endl;
    // cout << "Poor:     " << (roi.growth[0][0][0]) << "    " << (roi.growth[0][0][1]) << "    " << (roi.growth[0][0][2]) << "    " << (roi.growth[0][0][3]) << endl;
    // cout << "Middle:   " << (roi.growth[0][1][0]) << "    " << (roi.growth[0][1][1]) << "    " << (roi.growth[0][1][2]) << "    " << (roi.growth[0][1][3]) << endl;
    // cout << "Rich:     " << (roi.growth[0][2][0]) << "    " << (roi.growth[0][2][1]) << "    " << (roi.growth[0][2][2]) << "    " << (roi.growth[0][2][3]) << endl;

    // cout << endl;
    // cout << "CAB Growth" << endl;
    // cout << "          Poor         Middle       Rich        Self" << endl;
    // cout << "Poor:     " << (roi.growth[1][0][0]) << "    " << (roi.growth[1][0][1]) << "    " << (roi.growth[1][0][2]) << "    " << (roi.growth[1][0][3]) << endl;
    // cout << "Middle:   " << (roi.growth[1][1][0]) << "    " << (roi.growth[1][1][1]) << "    " << (roi.growth[1][1][2]) << "    " << (roi.growth[1][1][3]) << endl;
    // cout << "Rich:     " << (roi.growth[1][2][0]) << "    " << (roi.growth[1][2][1]) << "    " << (roi.growth[1][2][2]) << "    " << (roi.growth[1][2][3]) << endl;

}

void runCATs(string Folder, int gen) {
    char command[1024];
    
    for (int i = 0; i < 50; i++) {
        snprintf(command, 1024, "./jhgsim play %s/theGenerations 100 3 %i 8 30 rnd_agents equal 0 nodeterministic assassins2Config", Folder.c_str(), gen);
        system(command);

        snprintf(command, 1024, "cp ../Results/theGameLogs/log_1000_1000.csv %s/CATs/log_%i_%i.csv", Folder.c_str(), gen, i);
        cout << "command: " << command << endl;
        system(command);
    }
}

void runAgainstCATs() {
    for (int gen = 0; gen < 200; gen += 10) {
        runCATs("../Results_notseeded_noCATs", gen);
        runCATs("../Results_notseeded_CATs", gen);
        runCATs("../Results_seeded_noCATs", gen);
        runCATs("../Results_seeded_CATs", gen);
    }
    runCATs("../Results_notseeded_noCATs", 199);
    runCATs("../Results_notseeded_CATs", 199);
    runCATs("../Results_seeded_noCATs", 199);
    runCATs("../Results_seeded_CATs", 199);
}

void versesCATs(string Folder, int gen, ofstream &output, string seeding, string training) {
    double totPop = 0.0, totThiefPop;
    int totSurvived = 0;
    for (int i = 0; i < 50; i++) {
        string fnombre = Folder + "/log_" + to_string(gen) + "_" + to_string(i) + ".csv";
        vector<RoundInfo> v = readGame(fnombre);

        double avePop = 0.0;
        int survived = 0;
        for (int j = 0; j < 8; j++) {
            avePop += v[30].popularities[j];
            if (v[30].popularities[j] > 20.0)
                survived ++;
        }
        printf("avePop: %lf; survived: %i\n", avePop / 8.0, survived);
        totPop += avePop / 8.0;
        totSurvived += survived;

        totThiefPop += (v[30].popularities[8] + v[30].popularities[9]) / 2.0;

        output << gen << ",CABs," << seeding << "," << training << "," << (avePop / 8.0) << endl;
        output << gen << ",CATs," << seeding << "," << training << "," << ((v[30].popularities[8] + v[30].popularities[9]) / 2.0) << endl;
    }

    printf("totPop: %lf\n", totPop / 30.0);
    printf("totThiefPop: %lf\n", totThiefPop / 30.0);
    printf("totSurvived: %i\n", totSurvived);
    printf("totSurvived: %lf\n", totSurvived / (30.0 * 8.0));
}

void logVersesCATs() {
    ofstream output("../Analysis/csvs/vsCATs.csv");

    output << "generation,agents,seeding,training,average" << endl;

    for (int gen = 0; gen < 200; gen+=10) {
        versesCATs("../Results_notseeded_noCATs/CATs", gen, output, "notseeded", "noCATs");
        versesCATs("../Results_notseeded_CATs/CATs", gen, output, "notseeded", "CATs");
        versesCATs("../Results_seeded_noCATs/CATs", gen, output, "seeded", "noCATs");
        versesCATs("../Results_seeded_CATs/CATs", gen, output, "seeded", "CATs");
    }
    versesCATs("../Results_notseeded_noCATs/CATs", 199, output, "notseeded", "noCATs");
    versesCATs("../Results_notseeded_CATs/CATs", 199, output, "notseeded", "CATs");
    versesCATs("../Results_seeded_noCATs/CATs", 199, output, "seeded", "noCATs");
    versesCATs("../Results_seeded_CATs/CATs", 199, output, "seeded", "CATs");

    output.close();
}


int main(int argc, char *argv[]) {
    // ofstream output("../Analysis/csvs/trends.csv");
    // output << "Generation_Config,Trial,Round,SocialWelfare" << endl;

    // logSamples(output, 9, "equal");
    // logSamples(output, 9, "step");
    // logSamples(output, 49, "equal");
    // logSamples(output, 49, "step");

    // output.close();

    // getHumanBotWelfare();
    // processHumanBotAllocations();
    //numberOfFriends();

    // runAgainstCATs();

    logVersesCATs();

    // versesCATs("../Results_seeded_CATs/CATs", 199);

    // thievesExample();

    // scatterPlotCSV();

    // processCABTokenAllocations();

    // processHumanBotAllocationsByClass();

    // getROIbyClass();

 
    return 0;
}