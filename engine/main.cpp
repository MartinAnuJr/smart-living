#include "db.h"
#include "scoring.h"
#include <map>
#include <string>

int main() {
    Database db("../data/smart_living.db");
    std::vector<Fields> rows = db.pullData();
    Scoring scoring({"economy", "education", "housing"});
    Scoring::Weights testWeights = {
        {"economy", .7},
        {"education", .4},
        {"housing", .9}
    };
    return 0;
}