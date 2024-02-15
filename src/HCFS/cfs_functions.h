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


using namespace std;

double sum_vc(const vector<double> &a);

double mean(const vector<double> &b);

double sqsum(const vector<double> &a);

double stdev(const vector<double> &a);

vector<double> operator-(const vector<double> &a, const double &b);

vector<double> operator*(const vector<double> &a, const vector<double> &b);

double pearsoncoeff(const vector<double> &a, const vector<double> &b);

vector<double> binary_vec(double k, const vector<double> &a);

double pearsoncoeff_cat_num(const vector<double> &a, const vector<double> &b);

double prob_a_and_b(const vector<double> &a, const vector<double> &b);

double pearsoncoeff_cat_cat(const vector<double> &a, const vector<double> &b);

vector <string> possible_class_hierarchy(const vector<string> &a_class, const vector <string> &dist_class);

vector< vector<double> > a_class_to_vec(const vector<string> &a_class, const vector <string> &possible_class);

vector <double>  correlation_fl_multilabel(const vector< vector<double> > &class_vec, const vector< vector<double> > &data,
                                           vector <int> f_type);

vector <double> class_level(const vector <string> &possible_class);

vector <double> classes_per_level(int max_level, const vector <double> &possible_class_level);

vector <double>  correlation_fl_hierarchical(const vector< vector<double> > &class_vec, const vector< vector<double> > &data,
                                           const vector <int> &f_type, const vector <double> &class_level, double w_0,
                                           const vector <double> &classes_per_level);

vector< vector<double> > correlation_f_to_f_vec(const vector< vector<double> > &data, const vector <int> &f_type);

vector <long double> merit_cfs(const vector <int> &s, const vector< vector<double> > &correlation_ff_mat,
                               const vector <double> &correlation_fl_vec);
