/************************************************************************************
 * 
 *      This file is for the CFS .dll file. It is used to call the CFS merit function
 * 
 *      Clear the grasp.cpp file and put the following code:
 *      
 *      g++ -shared -fPIC -o src/merit.so -I./ ./src/HCFS/*.cpp src/HCFS/compilation_folder/extern_functions.cpp
 * 
 * **********************************************************************************/


#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <algorithm>
#include <cmath>
#include <set>
#include <list>
#include <queue>
#include <limits.h>
#include <float.h>
#include <cstdlib> //função rand
#include <time.h>
#include <unistd.h>
#include <sstream>
#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include "../utils.h"
#include "../arquivos.h"
#include "../cfs_functions.h"
#include "../ga_functions.h"
#include "extern_functions.h"

using namespace std;

extern "C" {
    #define EXPORT __attribute__((visibility("default")))

    EXPORT int return_cfs(const char* path, int population_size) {

        std::cout << "Path: " << path << std::endl;
        float fitness = evaluate_by_cfs(path , population_size);
        return fitness;
    }

}

char easytolower(char in){
  return tolower(in);
}

static inline std::string &str_lower(std::string &data) {
        transform(data.begin(), data.end(), data.begin(), easytolower);
        return data;
}


int evaluate_by_cfs(const char* path_chars, int population_size)
      
    
    {
    
    string filename = "generated-files/HCFS_POPULATION.txt"; // Change this to your file name
    vector<vector<int>> population = readPopulationFromFile(filename);
    
    string path = path_chars;
    ifstream file(path);
    string input_file, str, line;
 
    vector< vector< double > >  data; 
    vector< string > a_class, dist_class, header_attr;
    vector <int> f_type; //tipo do att, 1 para numerico e 2 para categorico
    vector < double > freq_class,   //guarda a frequencia da classe distinta
                        ranking;    //guarda o ranking suh dos atributos da base
    //vector< int > numeric_attr;
    string header = "", header_attr_class = "";

    getline(file, str);
    str_lower(str);
    while(str.find("@data") == string::npos){ //enquanto nao encontrar data

		//trata linhas em branco entre attribute classe e data
		if(str.find("@attribute class") != string::npos){ //se encontra atributo classe
			header_attr_class = str;
			while(str.find("@data") == string::npos){ //passa linhas em branco ate chegar em data
				getline(file, str);
				str_lower(str);
			}
			break;
		}

		//guarda o relation em header
		if(str.find("@relation") != string::npos)	header = str + "\n";

        //guarda no vector header_attr um atributo por linha quando acha attribute
		if(str.find("@attribute") != string::npos){
            header_attr.push_back(str + "\n");
            if (str.find("numeric") != string::npos) f_type.push_back(1);
            else  f_type.push_back(2);
		}

		getline(file, str);
		str_lower(str);
	}

    //pega as instancias
    while(getline(file, str)){

		if(!str.empty()){ //se str nao eh vazia
			vector< double > v_value;
			vector< string > v_str = explode(str,',');
			int tam = v_str.size();

			for(int i = 0; i < (tam-1); ++i)
                v_value.push_back(atof(v_str[i].c_str())); //converte a string para double

            //armazenando o atributo classe
			string classe = v_str[tam-1];
			if(in_array_string(classe, dist_class) == -1){
				dist_class.push_back(classe); //se for classe nova, adicona no vector de classes distintas dist_class
			}
			a_class.push_back(classe);
			data.push_back(v_value); //matriz de vetor
		}
    }
    file.close();


    vector <string> possible_classes = possible_class_hierarchy(a_class, dist_class); //vetor com todas as classes possiveis da hierarquia
    vector< vector<double> > a_class_vec = a_class_to_vec(a_class, possible_classes); //matriz com representacao binaria do atributo classe para cada classe possivel
    vector <double> classes_level = class_level(possible_classes); //vetor com o nivel de cada classe possivel
    int max_level = getMaxLevel(dist_class); // nivel maximo da hierarquia
    vector <double> number_classes_per_level = classes_per_level(max_level, classes_level); //numero de classes pertencentes a cada nivel da hierarquia
    //vector <double>  correlation_fl_multi = correlation_fl_multilabel(a_class_vec, data, f_type);//vetor com correlacao multilabel fxl de cada feature da base
    vector <double>  correlation_fl_hierar = correlation_fl_hierarchical(a_class_vec, data, f_type, classes_level, 0.75, number_classes_per_level);//vetor com correlacao hierarquica fxl de cada feature da base
    vector< vector<double> > correlation_f_to_f = correlation_f_to_f_vec(data, f_type);//matriz com a correlacao fxf

    list <candidate> open; // QQ eh isso
    list<candidate>::iterator it_open; // QQ eh isso
    priority_queue< candidate_queue, vector<candidate_queue>, less<candidate_queue> > open_queue; //fila de prioridade
    candidate best;
    candidate_queue current_top;
    vector<long double> best_evolution;
    vector<double> att_best_evo, att_worse_evo, att_avg_evo, current_att_results;
    
    vector <long double> fitness;
    fitness.reserve(population_size);
    for(int i = 0; i < population_size; ++i){
        fitness.push_back(0);
    }

    current_att_results = evaluate(open, open_queue, fitness, population, correlation_f_to_f, correlation_fl_hierar); // PROBLEMA AQUI


    att_best_evo.push_back(current_att_results[0]);
    att_worse_evo.push_back(current_att_results[1]);
    att_avg_evo.push_back(current_att_results[2]);
    current_att_results.erase(current_att_results.begin(),current_att_results.end());


    // Printa tudo:
    
    cout << "Best: " << att_best_evo[0] << endl;
    cout << "Worse: " << att_worse_evo[0] << endl;
    cout << "Avg: " << att_avg_evo[0] << endl;

    return 0;
}
