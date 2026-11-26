#pragma once
#include <string>
#include <map>

struct CityScore
{
    int city_id;
    std::string city_name;
    double total_score;
    std::map<std::string, double> category_scores;
};

struct Fields
{
    std::string city_name;
    int city_id;
    int metric_type_id;
    std::string category;
    double normalized_value;
};