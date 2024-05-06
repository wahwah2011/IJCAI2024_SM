#include <iostream>

int main() {
    for (int i = 0; i < 10; i++) {
        system("mkdir ../Results/theGenerations");
        system("mkdir ../Results/theGameLogs");
        system("python3 main.py evolve 100 200 20 11 40 0");
        char cmd[1024];
        sprintf(cmd, "mv ../Results/theGenerations ../Results/theGenerations_v%i_11", i+1);
        system(cmd);
        sprintf(cmd, "mv ../Results/theGameLogs ../Results/theGameLogs_v%i_11", i+1);
        system(cmd);
    }

    return 0;
}