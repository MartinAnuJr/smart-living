#include "db.h"

using namespace std;

int main() {
    Database db("../data/smart_living.db");
    vector<Fields> rows = db.pullData();
    return 0;
}