#ifndef UTILS_H
#define UTILS_H
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

using namespace std;



string lowercase(string str);

vector<string> explode(string str, char delimiter);

int in_array_string(string v_class, vector< string > &f_class);

int in_array(double value, vector< double > &v_value);

int in_array_int(int value, vector< int > &v_value);

bool is_descendant(string classA, string classB);

bool is_ascendant(string classA, string classB);

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
#endif


