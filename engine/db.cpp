#include <stdlib.h>
#include <stdio.h>
#include <sqlite3.h>
#include <iostream>
#include <string>

using namespace std;

class Database {
    private:
    sqlite3 *db;

    public:
    Database() {
        if (sqlite3_open("smart_living.db", &db) != SQLITE_OK) {
            cerr << "Error opening database: " << sqlite3_errmsg(db) << endl;
            sqlite3_close(db);
        }
    }

    ~Database() {
        sqlite3_close(db);
    }

    void pullData() {
        struct fields {
            int city_id;
            int metric_type_id;
            string category;
            bool higher_is_better;
            float raw_value;
        };

        sqlite3_stmt* stmt;
        const char* sql = 
            "SELECT city_id, metric_type_id, category, higher_is_better, raw_value "
            "FROM city_metrics JOIN metric_types ON metric_type_id = id JOIN cities ON city_id = cities.id";

        sqlite3_prepare_v2(db, sql, -1, &stmt, nullptr);
    }
};