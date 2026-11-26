#pragma once
#include "types.h"
#include <map>
#include <string>
#include <vector>

class Scoring
{
private:
    std::vector<std::string> categories_;

public:
    using Weights = std::map<std::string, double>;

    explicit Scoring(std::vector<std::string> categories);

    std::vector<std::string> validateWeights(const Weights &) const;
    Weights applyDefaults(const Weights &user) const;
    std::vector<CityScore> scoreCities(const std::vector<Fields> &rows, const Weights &weights) const;
};
