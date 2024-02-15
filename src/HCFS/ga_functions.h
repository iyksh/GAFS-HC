#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <algorithm>
#include <cmath>
#include <cstdio>
#include <iomanip>
#include <limits.h>
#include <float.h>
#include <unistd.h>
#include <sstream>
#include "utils.h"
#include "cfs_functions.h"


using namespace std;

vector< vector<int> > inicialize_population(unsigned int bits, unsigned int population_size);

vector<double> evaluate(list <candidate> &open, priority_queue <candidate_queue> &open_queue, vector<long double> &fitness,
              const vector<vector<int>> &population, const vector< vector<double> > &correlation_ff_mat,
              const vector <double> &correlation_fl_vec);

//selecao eh pelo metodo roleta, que recebe o fitness como entrada

vector<int> mutation_point(const vector<int> parent);

vector < vector<int> > crossover_one_point(const vector<int> parent1, const vector<int> parent2);

candidate best_hf_att_subset(list <candidate> open, priority_queue <candidate_queue> open_queue);



