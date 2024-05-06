#include <iostream>
#include <stdio.h>

using namespace std;


// g++ playGamesFromGen.cpp -o genGames
//
// ./genGames [genFolder] [gen] [numPlayers] [numRounds] [initPop] [povertyLine] [numGames]
int main(int argc, char *argv[]) {
    if (argc != 8) {
        cout << "not the right number of parameters" << endl;
    }

    char cmd[1024], cmd2[1024], theDir[1024];
    
    // create the directory
    snprintf(theDir, 1024, "../Results/RndGames_%s_%s_%s_%s", argv[2], argv[3], argv[4], argv[5]);
    snprintf(cmd2, 1024, "mkdir %s", theDir);
    system(cmd2);

    snprintf(cmd, 1024, "./jhgsim play %s 70 3 %s %s %s rnd_agents %s %s noHuman noGovment", argv[1], argv[2], argv[3], argv[4], argv[5], argv[6]);
    for (int g = 0; g < atoi(argv[7]); g++) {
        system(cmd);
        snprintf(cmd2, 1024, "mv ../Results/theGameLogs/log_1000_1000.csv %s/game_%i.csv", theDir, g);
        system(cmd2);
    }

    return 0;
}