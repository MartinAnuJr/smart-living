#pragma once
#include "types.h"
#include <string>
#include <vector>
#include <sqlite3.h>

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
