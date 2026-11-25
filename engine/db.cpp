#include "db.h"
#include <iostream>
#include <optional>

using namespace std;

static optional<string> getText(sqlite3_stmt *stmt, int col)
{
    if (sqlite3_column_type(stmt, col) == SQLITE_NULL)
    {
        return nullopt;
    }
    auto p = reinterpret_cast<const char *>(sqlite3_column_text(stmt, col));
    return std::string(p, sqlite3_column_bytes(stmt, col));
}

Database::Database(string path)
{
    if (sqlite3_open_v2(path.c_str(), &db, SQLITE_OPEN_READWRITE, nullptr) != SQLITE_OK)
    {
        cerr << "Error opening database: " << sqlite3_errmsg(db) << endl;
        sqlite3_close(db);
        db = nullptr;
        return;
    }
}

Database::~Database()
{
    sqlite3_close(db);
}

vector<Fields> Database::pullData()
{

    vector<Fields> rows;
    if (db == nullptr)
    {
        cerr << "Empty db object" << endl;
        return rows;
    }

    sqlite3_stmt *stmt;
    const char *sql =
        "SELECT cities.name, city_id, metric_type_id, category, normalized_value "
        "FROM city_metrics JOIN metric_types ON metric_type_id = metric_types.id JOIN cities ON city_id = cities.id";

    if (sqlite3_prepare_v2(db, sql, -1, &stmt, nullptr) != SQLITE_OK)
    {
        cerr << "Error preparing: " << sqlite3_errmsg(db) << endl;
        return rows;
    }

    int rc;
    while ((rc = sqlite3_step(stmt)) == SQLITE_ROW)
    {
        string city_name = getText(stmt, 0).value_or("null");
        int city_id = sqlite3_column_int(stmt, 1);
        int metric_type_id = sqlite3_column_int(stmt, 2);
        string category = getText(stmt, 3).value_or("null");
        double normalized_value;
        if (sqlite3_column_type(stmt, 4) != SQLITE_NULL)
        {
            normalized_value = sqlite3_column_double(stmt, 4);
        }
        else
        {
            cerr << "No normalized value found for city_id, metric_type_id: " << city_id << ", " << metric_type_id << endl;
            continue;
        }

        cout << city_name << ", " << city_id << ", " << metric_type_id << ", " << category << ", " << normalized_value << endl;
        Fields row{city_name, city_id, metric_type_id, category, normalized_value};
        rows.push_back(row);
    }

    if (rc != SQLITE_DONE)
    {
        cerr << "Error reading row: " << sqlite3_errmsg(db) << endl;
    }

    sqlite3_finalize(stmt);
    return rows;
}
