
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

bool myfunction (string i,string j);
void compute_w(double *w, int max_level);

vector < double > rankingSUH (vector< string > &a_class, vector< string > &dist_class,
                              vector< vector< double > > &data);
