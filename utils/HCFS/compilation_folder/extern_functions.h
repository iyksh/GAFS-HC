#ifndef extern_functions_h
#define extern_functions_h

#include <iostream>
#include <fstream>
#include <string>
#include <vector>

struct MeritResult {
    float merit;
    std::vector<std::vector<double>> correlation_ff;
    std::vector<double> correlation_fl;
};

char easytolower(char in);
static inline std::string &str_lower(std::string &data);
int evaluate_by_cfs(const char* path_chars, int population_size);


#endif