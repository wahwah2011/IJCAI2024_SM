#include <iostream>
#include <fstream>
#include <string>
#include <vector>

using namespace std;

struct genePair {
    genePair(string _theGene, double _fitness) {
        theGenes = _theGene;
        fitness = _fitness;
        visualTrait = -1;
    }

    string theGenes;
    double fitness;
    int visualTrait;
};

struct less_than_genePair {
    inline bool operator() (const genePair& struct1, const genePair& struct2) {
        return (struct1.fitness > struct2.fitness);
    }
};

struct Generacion {
    Generacion(string nombre) {
        // cout << nombre << endl;
        ifstream input(nombre);
        if (!input) {
            cout << "file " << nombre << " not found" << endl;
            exit(1);
        }

        for (int i = 0; i < 100; i++) {
            string line;
            getline(input, line);
            // cout << line << endl;
            vector<string> words = splitString(line, ",");
            genePair gp(words[0], stod(words[3]));
            gpool.push_back(gp);

            vector<string> genewords = splitString(gpool[gpool.size()-1].theGenes, "_");
            gpool[gpool.size()-1].visualTrait = stoi(genewords[15]);
        }

        input.close();

        sort(gpool.begin(), gpool.end(), less_than_genePair());
    }

    vector<string> splitString(string line, string delimiter) {
        vector<string> palabras;
        string token;
        int posStart = 0;
        int posEnd = line.find(delimiter, posStart);
        while (posEnd != string::npos) {
            token = line.substr(posStart, posEnd - posStart);
            posStart = posEnd + 1;
            palabras.push_back(token);
            posEnd = line.find(delimiter, posStart);
        }

        palabras.push_back(line.substr(posStart));

        return palabras;
    }

    vector<genePair> gpool;

};

void doTestHomophily(int simVersion, int generation, int numSamps, ofstream &f) {
    cout << "Results for " << simVersion << "-" << generation << endl;

    Generacion g("../Results/theGenerations_v" + to_string(simVersion) + "_11/gen_" + to_string(generation) + ".csv");

    // for (int i = 0; i < 100; i++) {
    //     cout << i << ": " << g.gpool[i].theGenes << ";    " << g.gpool[i].fitness << ";    " << g.gpool[i].visualTrait << endl;
    // }
    
    // 3 - Select the top 11 agents to play against each other
    // create file with genes of top 11 agents
    ofstream output("ScenarioIndicator/theGenotypes.txt");
    for (int i = 0; i < 11; i++) {
        output << g.gpool[i].theGenes << endl;
    }
    output.close();

    // 4a - Run a game with the top 11 agents
    ofstream output2("ScenarioIndicator/visualTraits.txt");
    for (int i = 0; i < 11; i++) {
        output2 << g.gpool[i].visualTrait << endl;
    }
    output2.close();

    double sum1 = 0.0, sum2 = 0.0, outcome, outcome2;
    for (int i = 0; i < numSamps; i++) {
        system("python3 main.py playGame 40");
        ifstream input("ScenarioIndicator/outcome0.txt");
        input >> outcome;
        input >> outcome2;
        input.close();
        // cout << outcome << endl;
        sum1 += outcome;
        sum2 += outcome2;
    }
    // cout << "  Same: " << (sum1 / numSamps) << "     " << (sum2 / numSamps) << endl;
    f << simVersion << "," << generation << ",Unchanged,Player 1," << sum1 / numSamps << endl;
    f << simVersion << "," << generation << ",Unchanged,Remaining Players," << sum2 / numSamps << endl;
    // char cmd[1024];
    // sprintf(cmd, "mv ../Results/theGameLogs/log_1000_1000.csv ../Results/theGameLogs_HomophilyTest/log_%i_%i_same.csv", simVersion, generation);
    // system(cmd);

    // 4b - Run a game with the top 11 agents (but with the top agents visual trait mutated)
    ofstream output3("ScenarioIndicator/visualTraits.txt");
    output3 << ((g.gpool[0].visualTrait + 50) % 101) << endl;
    for (int i = 1; i < 11; i++) {
        output3 << g.gpool[i].visualTrait << endl;
    }
    output2.close();

    // sprintf(cmd, "mv ../Results/theGameLogs/log_1000_1000.csv ../Results/theGameLogs_HomophilyTest/log_%i_%i_alt.csv", simVersion, generation);
    // system(cmd);
    sum1 = sum2 = 0.0;
    for (int i = 0; i < numSamps; i++) {
        system("python3 main.py playGame 40");
        ifstream input2("ScenarioIndicator/outcome0.txt");
        input2 >> outcome;
        input2 >> outcome2;
        input2.close();
        // cout << outcome << endl;
        sum1 += outcome;
        sum2 += outcome2;
    }
    // cout << "  Different: " << (sum1 / numSamps) << "     " << (sum2 / numSamps) << endl;
    f << simVersion << "," << generation << ",Mutated,Player 1," << sum1 / numSamps << endl;
    f << simVersion << "," << generation << ",Mutated,Remaining Players," << sum2 / numSamps << endl;

    sum1 = sum2 = 0.0;
    for (int i = 0; i < numSamps; i++) {
        system("python3 main.py playGame 40 true");
        ifstream input2("ScenarioIndicator/outcome0.txt");
        input2 >> outcome;
        input2 >> outcome2;
        input2.close();
        // cout << outcome << endl;
        sum1 += outcome;
        sum2 += outcome2;
    }
    // cout << "  Different: " << (sum1 / numSamps) << "     " << (sum2 / numSamps) << endl;
    f << simVersion << "," << generation << ",Mutated-None,Player 1," << sum1 / numSamps << endl;
    f << simVersion << "," << generation << ",Mutated-None,Remaining Players," << sum2 / numSamps << endl;

}

void testHomophily() {
    ofstream f("HomophilyTest.csv");

    f << "SimVersion,Generation,VisibleTrait,Who,Popularity" << endl;

    // doTestHomophily(1, 99, 10, f);

    for (int simVersion = 1; simVersion < 11; simVersion++) {
        cout << "onto simVersion = " << simVersion << endl;
        doTestHomophily(simVersion, 99, 10, f);
        doTestHomophily(simVersion, 149, 10, f);
        doTestHomophily(simVersion, 199, 10, f);
    }

    f.close();
}

int doTestPlayer11(int simVersion, int generation, string visibleConfig, int index, ofstream &output) {
    Generacion g("../Results/theGenerations_v" + to_string(simVersion) + "_11/gen_" + to_string(generation) + ".csv");

    // create file with genes of top 11 agents
    ofstream output3("ScenarioIndicator/theGenotypes.txt");
    for (int i = 0; i < 11; i++) {
        output3 << g.gpool[i].theGenes << endl;
    }
    output3.close();

    // set the visual traits based on visibleConfig
    ofstream output2("ScenarioIndicator/visualTraits.txt");
    if (visibleConfig == "Homogeneous") {
        for (int i = 0; i < 11; i++) {
            output2 << 100 << endl;
        }
    }
    else if (visibleConfig == "Minority") {
        output2 << "100\n100\n0\n100\n100\n50\n50\n100\n0\n50\n0" << endl;
    }
    else if (visibleConfig == "Majority") {
        output2 << "50\n0\n50\n100\n100\n0\n100\n0\n50\n100\n100" << endl;
    }
    else {
        cout << "visibleConfig " << visibleConfig << " not found" << endl;
        exit(1);
    }
    output2.close();


    // run the game
    double outcome, outcome2;
    system("python3 main.py playGame 39");
    ifstream input("ScenarioIndicator/outcome0.txt");
    input >> outcome;
    input >> outcome2;
    input.close();
    char cmd[1024];
    sprintf(cmd, "mv ../Results/theGameLogs/log_1000_1000.csv ../Results/theGameLogs_Player11Test/log_%i_%i_%s_B%i_%i.csv", simVersion, generation, visibleConfig.c_str(), (index/3)+1, index);
    system(cmd);

    // save it out to the file
    output << "B" << ((index / 3) + 1) << "," << generation << "," << visibleConfig << ",Bot,Player11," << outcome << endl;
    output << "B" << ((index / 3) + 1) << "," << generation << "," << visibleConfig << ",Bot,Remaining Players," << outcome2 << endl;

    return index+1;
}

void evaluatePlayer11() {
    ofstream output("tmp.csv");
    int index = 0;
    index = doTestPlayer11(3, 79, "Homogeneous", index, output);
    index = doTestPlayer11(3, 139, "Majority", index, output);
    index = doTestPlayer11(3, 199, "Minority", index, output);
    
    index = doTestPlayer11(3, 79, "Homogeneous", index, output);
    index = doTestPlayer11(3, 139, "Minority", index, output);
    index = doTestPlayer11(3, 199, "Majority", index, output);

    index = doTestPlayer11(3, 79, "Minority", index, output);
    index = doTestPlayer11(3, 139, "Majority", index, output);
    index = doTestPlayer11(3, 199, "Homogeneous", index, output);

    index = doTestPlayer11(3, 79, "Minority", index, output);
    index = doTestPlayer11(3, 139, "Homogeneous", index, output);
    index = doTestPlayer11(3, 199, "Majority", index, output);

    index = doTestPlayer11(3, 79, "Majority", index, output);
    index = doTestPlayer11(3, 139, "Minority", index, output);
    index = doTestPlayer11(3, 199, "Homogeneous", index, output);

    index = doTestPlayer11(3, 79, "Majority", index, output);
    index = doTestPlayer11(3, 139, "Homogeneous", index, output);
    index = doTestPlayer11(3, 199, "Minority", index, output);

    index = doTestPlayer11(3, 79, "Homogeneous", index, output);
    index = doTestPlayer11(3, 139, "Majority", index, output);
    index = doTestPlayer11(3, 199, "Minority", index, output);
    
    index = doTestPlayer11(3, 79, "Homogeneous", index, output);
    index = doTestPlayer11(3, 139, "Minority", index, output);
    index = doTestPlayer11(3, 199, "Majority", index, output);

    index = doTestPlayer11(3, 79, "Minority", index, output);
    index = doTestPlayer11(3, 139, "Majority", index, output);
    index = doTestPlayer11(3, 199, "Homogeneous", index, output);

    index = doTestPlayer11(3, 79, "Minority", index, output);
    index = doTestPlayer11(3, 139, "Homogeneous", index, output);
    index = doTestPlayer11(3, 199, "Majority", index, output);

    index = doTestPlayer11(3, 79, "Majority", index, output);
    index = doTestPlayer11(3, 139, "Minority", index, output);
    index = doTestPlayer11(3, 199, "Homogeneous", index, output);

    index = doTestPlayer11(3, 79, "Majority", index, output);
    index = doTestPlayer11(3, 139, "Homogeneous", index, output);
    index = doTestPlayer11(3, 199, "Minority", index, output);

    output.close();
}

vector<string> splitString(string line, string delimiter) {
    vector<string> palabras;
    string token;
    int posStart = 0;
    int posEnd = line.find(delimiter, posStart);
    while (posEnd != string::npos) {
        token = line.substr(posStart, posEnd - posStart);
        posStart = posEnd + 1;
        palabras.push_back(token);
        posEnd = line.find(delimiter, posStart);
    }

    palabras.push_back(line.substr(posStart));

    return palabras;
}

void getPayoffs(string nombre, int rnd) {
    ifstream input(nombre);

    if (!input) {
        cout << nombre << " not found" << endl;
        exit(1);
    }

    string line;
    for (int i = 0; i < (rnd+2); i++)
        getline(input, line);

    input.close();

    vector<string> words = splitString(line, ",");
    cout << words[6] << endl;
    double sum = 0.0;
    for (int i = 0; i < 10; i++) {
        sum += stod(words[7+i]);
    }
    cout << sum / 10.0 << endl;
}

int main(int argc, char *argv[]) {
    // testHomophily();
    // evaluatePlayer11();

    string este = argv[1];
    string fnombre = "../jhg-evolution-ui-main/ui/game/results/" + este;
    getPayoffs(fnombre, 39);

}