#include "db.h"


int main() {
    Database db("../data/smart_living.db");
    std::vector<Fields> rows = db.pullData();
    return 0;
}