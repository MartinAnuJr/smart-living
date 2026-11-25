#pragma once
#include <string>
#include <vector>
#include <sqlite3.h>

struct Fields
{
    std::string city_name;
    int city_id;
    int metric_type_id;
    std::string category;
    double normalized_value;
};

class Database
{
private:
    sqlite3 *db;

public:
    Database(std::string path);
    ~Database();

    Database(const Database&) = delete;
    Database& operator=(const Database&) = delete;

    std::vector<Fields> pullData();

};
