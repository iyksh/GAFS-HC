#ifndef UTILS_H
#define UTILS_H
#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <set>
#include <list>
#include <queue>
#include <algorithm>
#include <cmath>
#include <limits.h>
#include <float.h>
#include <unistd.h>
#include <sstream>
#include <random>
#include <cstdlib> //função rand

using namespace std;


struct solution{
    vector <int> att;
    vector <long double> hf;
};

struct candidate{
    set <int> att;
    long double merit;
    int size_set;
};

struct candidate_queue{
    int position;
    long double merit;
};


bool myfunction (string i,string j);

bool myfunction_int (int i, int j);

bool operator<(const candidate_queue& lhs, const candidate_queue& rhs );

void compute_w(double *w, int max_level);

string lowercase(string str);

vector<string> explode(string str, char delimiter);

int in_array_string(string v_class, const vector< string > &f_class);

int in_array(double value, const vector< double > &v_value);

int in_array_int(int value, vector< int > &v_value);

bool is_descendant(string classA, string classB);

bool is_ascendant(string classA, string classB);

vector <double> distinct(const vector<double> &categorical);

vector <double> frequence_double(const vector<double> &dist_class, const vector <double> &categorical);

vector <double> frequence(vector< string > dist_class, vector < string > a_class);

int getMaxLevel(vector< string > dist_class);

double mode(vector< double > v_values);

string getParamName(string parameter);

string getParamValue(string value);

void printParam(const string &trainingFile, const string &testFile, const string &resultFile,
                const unsigned int &numberOfTrainingExamples, const unsigned int &numberOfTestExamples,
                const unsigned int &numberOfAttributes, const string &mlnp, const string &usf);

int str2int(const string &value);

void getDatasetsProfile(const string &trainingFile, const string &testFile, unsigned int &numberOfTrainingExamples,
                        unsigned int &numberOfTestExamples, unsigned int &numberOfAttributes);

float randomico(float min, float max);

int roleta(const vector <long double> &ranking);

vector <double> escala(vector <double> &ranking);

vector <double> portion_of_ranking(vector <int> att, vector <double> ranking_all_att);

vector <int> portion_of_att(vector <int> att_s, vector <double> ranking_all_att);

vector <int> portion_of_att_int(vector <int> att_s, vector <int> possible_att);

vector <double> get_column(const vector< vector<double> > &matriz, int k);

long double in_list_candidate(int size_set, const set <int> cand, list< candidate > &list_c);

list< set<int> > create_successors(const set<int> &father, int number_att);

set<int> binary_to_subset(const vector<int> &vec_binary);

vector<vector<int>> readPopulationFromFile(const string& filename);

#endif