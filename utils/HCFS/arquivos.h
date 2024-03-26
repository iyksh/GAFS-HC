#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <algorithm>
#include <cmath>
#include <limits.h>
#include <float.h>
#include <unistd.h>
#include <sstream>
#include "utils.h"

using namespace std;


void create_files_for_grasp(vector <int> &s, string path);

vector <double> get_ranking(string path);

void write_final_result(vector <int> att,  vector <long double> hf, string path, int seed,
                        float current_time, int n_1l_max, vector <long double> improv_hf,
                        vector <float> improv_time, vector <float> improv_att);

void write_result_CFS(set <int> att,  long double hf, string path, vector<long double> best_evo,
                     vector<double> att_best_evo, vector<double> att_worse_evo, vector<double> att_avg_evo);


