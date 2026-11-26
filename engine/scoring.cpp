#include "scoring.h"
#include <utility>

Scoring::Scoring(std::vector<std::string> categories) : categories_(std::move(categories)){

}

std::vector<std::string> Scoring::validateWeights(const Weights &weights) const { return {}; }
Scoring::Weights Scoring::applyDefaults(const Weights &user) const { return {}; }
std::vector<CityScore> Scoring::scoreCities(const std::vector<Fields> &rows, const Weights &weights) const { return {}; }
