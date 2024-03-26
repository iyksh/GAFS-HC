#include "utils.h"


bool myfunction (string i, string j) { return (i.size() < j.size()); }

bool myfunction_int (int i, int j) { return (i < j); }


bool operator<(const candidate_queue& lhs, const candidate_queue& rhs ) {  return lhs.merit < rhs.merit; }

void compute_w(double *w, int max_level){
    for(int i = 0; i < max_level; ++i)
        w[i] = double((double(max_level) - (i+1) +1) * (2/(double(max_level)*(double(max_level)+1))));

}

string lowercase(string str){
	for(unsigned int i = 0; i < str.size(); i++){
		str.replace(i,1,1,tolower(str[i]));
	}
	return(str);
}


//pega a linha de atributos da base e coloca cada atributo num vector de string
vector<string> explode(string str, char delimiter){
	vector<string> out;
	size_t found = str.find(delimiter);
	while(found != string::npos){
		string sub_str = str.substr(0,found);
		out.push_back(sub_str);
		str = str.substr(found+1);
		found = str.find(delimiter);
	}
	// add the last one
	out.push_back(str);
	return out;
}

// verifica se v_class esta no vector f_class e retorna posicao
int in_array_string(string v_class, const vector< string > &f_class){
	for(unsigned int j=0; j < f_class.size(); ++j){
		if(v_class.compare(f_class[j]) == 0){
			return j;
		}
	}

	return -1;
}

//verifica se value esta no vector v_value
int in_array(double value, const vector< double > &v_value){
	for(unsigned int j=0; j < v_value.size(); ++j){
		if(value == v_value[j]){
			return j;
		}
	}

	return -1;
}

//verifica se value esta no vector v_value
int in_array_int(int value, vector< int > &v_value){
	for(unsigned int j=0; j < v_value.size(); ++j){
		if(value == v_value[j]){
			return j;
		}
	}

	return -1;
}

//verifica se classB esta contida em classA
bool is_descendant(string classA, string classB){
	if(classA.find(classB) == 0) return true;
	return false;
}

//verifica se a classA esta contida em classB
bool is_ascendant(string classA, string classB){
	if(classB.find(classA) == 0) return true;
	return false;
}

//recebe um vector de valores categoricos de um atributo e retorna um vetor de valores distintos
vector <double> distinct(const vector<double> &categorical){

	vector<double> distinct;
	distinct.push_back(categorical[0]);
	for(unsigned int i = 1; i < categorical.size(); ++i)
        if (in_array(categorical[i], distinct) == -1)
            distinct.push_back(categorical[i]);

    return distinct;
}

//recebe um vetor de valores distintos e conta na base a frequencia de cada valor, retornando o vetor de frequencia
vector <double> frequence_double(const vector<double> &dist_class, const vector <double> &categorical){
    int position;
    int tam = dist_class.size();
    vector <double> frequence(tam,0);
    for(unsigned int k = 0; k < categorical.size(); ++k){
		position = in_array(categorical[k], dist_class);
		frequence[position]+= 1;
	}


    return frequence;
}

//recebe um vector de classes distintas e um vector de classes na base e calcula a frequencia de cada classe na base
vector <double> frequence(vector< string > dist_class, vector < string > a_class){
	vector< double > freq_class;

	for(unsigned int i = 0; i < dist_class.size(); ++i){
        int mycount = count (a_class.begin(), a_class.end(), dist_class[i]);
        freq_class.push_back(double(mycount));
	}
    return freq_class;
}

//recebe um vector de classes distintas e calcula o maior nivel da hierarquia de classes
//se o valor retornado for zero, entao o nivel maximo eh 1
int getMaxLevel(vector< string > dist_class){
    int maxlevel = 0;
    for(unsigned int i = 0; i < dist_class.size(); ++i){
        vector< string > aux_str = explode(dist_class[i],'.');
        int level = aux_str.size();
        //se for maior, guarda o nivel atual
        if (level > maxlevel) maxlevel = level;
    }
    return maxlevel;
}

//recebe um vector de valores e calcula frequencia dentro desse vector e retorna o valor mais frequente
//tem um vector de valores v_distinct e um vector de contador de ocorrencias de elementos de v_distinct, f_distinct

double mode(vector< double > v_values){
	vector< double > v_distinct, f_distinct;
	int position;

	for(unsigned int k = 0; k < v_values.size(); ++k){
		position = in_array(v_values[k], v_distinct);
		if(position == -1){
			v_distinct.push_back(v_values[k]);
			f_distinct.push_back(1);
		} else {
			f_distinct[position]++;
		}
	}
//pega o id de maior frequencia em f_distinct
	double max = LONG_MIN;
	int id;
	for(unsigned int k = 0; k < f_distinct.size(); ++k){
		if(f_distinct[k] > max){
			max = f_distinct[k];
			id = k;
		}
	}
//retorna o valor de maior frequencia
	return v_distinct[id];
}

string getParamName(string parameter){
  return(parameter.substr(parameter.find("-")+1,parameter.find("=")-(parameter.find("-")+1)));
}

string getParamValue(string value){
	return(value.substr(value.find("=")+1,value.find(" ")-(value.find("=")+1)));
}

void printParam(const string &trainingFile, const string &testFile, const string &resultFile, const unsigned int &numberOfTrainingExamples, const unsigned int &numberOfTestExamples, const unsigned int &numberOfAttributes, const string &mlnp, const string &usf){
	cout << "\tTraining File = " << trainingFile << endl;
	cout << "\tTest File = " << testFile << endl;
	cout << "\tResult File = " << resultFile << endl;
	cout << "\tNumber of Training Examples = " << numberOfTrainingExamples << endl;
	cout << "\tNumber of Test Examples = " << numberOfTestExamples << endl;
	cout << "\tNumber of Attributes = " << numberOfAttributes << endl;
	cout << "\tMandatory Leaf Node Prediction = " << mlnp << endl;
	cout << "\tUsefulness = " << usf << endl;


}

int str2int(const string &value){
	int result = 0;
	for(int i = 0; i < (int)value.size(); i++){
			if (isdigit(value[i]))
        result = (result * 10) + (value[i] - '0');
	}
	return(result);
}

void getDatasetsProfile(const string &trainingFile, const string &testFile, unsigned int &numberOfTrainingExamples, unsigned int &numberOfTestExamples, unsigned int &numberOfAttributes){
	string line, lastLine;
	unsigned int i = 0, checkNumberOfAttributes = 0, pos, lastComma; //classId, begin, end,
	numberOfAttributes = 1;
	numberOfTrainingExamples = 0;
	numberOfTestExamples = 0;

	//Obtendo os parâmetros da base de dados de treinamento...
	ifstream fin, fin1;
	fin.open(trainingFile.c_str());

	if(!fin.is_open()){
	  cout << "Error opening training file!!!" << endl;
	  exit(1);
	}

	//Pulando linhas até o início das linhas de dados...
	while (getline(fin, line) && lowercase(line.substr(0,5)) != "@data"){
	  if(lowercase(line.substr(0,10)) != "@attribute"){
		continue;
      }
      checkNumberOfAttributes++;
	}

	while(getline(fin,line)){//Lendo cada linha do arquivo de entrada ...
		if (line.substr(0,1) == "%" || (int)line.size() == 0) {//Se for linha comentada ou vazia...
			continue;
		}
		//end = line.size();
		//begin = line.rfind(",")+1;
		//classId = str2int(line.substr(begin, end-begin));
		numberOfTrainingExamples++;
		lastLine = line;//Armazenando a última do arquivo para posteriormente contar o número de atributos
	}
	lastComma = (int)lastLine.rfind(",");
	while (i < lastComma){
		pos = lastLine.find(",",i);
		i = pos + 1;
		numberOfAttributes++;//númerno de atributos = número de vírgulas + 1
	}
	fin.close();

	if(numberOfAttributes != checkNumberOfAttributes){
	  cout << numberOfAttributes << "\t" << checkNumberOfAttributes << endl;
	  cout << "Training File Error: Inconsistent Number of Attributes!" << endl;
	  exit(1);
	}

	//Obtendo os parâmetros da base de dados de teste...
	fin1.open(testFile.c_str());

	//Pulando linhas até o início das linhas de dados...
	while (lowercase(line.substr(0,5)) != "@data") getline(fin1, line);

	while(getline(fin1,line)){//Lendo cada linha do arquivo de entrada ...
		if (line.substr(0,1) == "%" || (int)line.size() == 0) {
			continue;
		}
		//end = line.size();
		//begin = line.rfind(",")+1;
		//classId = str2int(line.substr(begin, end-begin));
		numberOfTestExamples++;
	}
	fin1.close();

}




/* Gera numero aleatorio entre min e max */
float randomico(float min, float max){
  if (min == max) return min;
  return ((float) (rand()%10000/10000.0)*(max-min) + min);
}



//roleta recebe uma metrica para cada att e devolve o indice do att escolhido, dando maior chance
//para aqueles com maior valor no ranking passado como parametro

int roleta(const vector <long double> &ranking){

    int index = 0;
    long double sum = 0;
    float aux;
    vector <long double> fraction, cumulative_prob;

    for (unsigned int j = 0; j < ranking.size(); ++j)
        sum += ranking[j];

    for (unsigned int j = 0; j < ranking.size(); ++j)
        fraction.push_back((ranking[j]/sum));

    //for (unsigned int j = 0; j < ranking.size(); ++j)
    //    cout << "prob: " << fraction[j] << "\n";

    cumulative_prob.push_back(fraction[0]);
    for (unsigned int j = 1; j < ranking.size(); ++j)
        cumulative_prob.push_back(cumulative_prob[j-1]+fraction[j]);

   // for (unsigned int j = 0; j < ranking.size(); ++j)
    //    cout << "prob_cumulativa: " << cumulative_prob[j] << "\n";

    aux = randomico(0,1);
    while (cumulative_prob[index] < aux) index++;
    //cout << "randomico: " << aux << "\n";
    return index;
}

//funcao que calcula novo ranking dos att, atribuindo maior valor para aquele att
//que tem menor valor no ranking original
vector <double> escala(vector <double> &ranking){

    double tg_alfa;

    vector< double > ranking_cp, ranking_escala;
    ranking_cp = ranking; //faz uma copia do vector ranking

    //ordena crescentemente
    sort (ranking_cp.begin(), ranking_cp.end());

    tg_alfa = 100 / (ranking_cp.back() - ranking_cp.front());

    for (unsigned int j = 0; j < ranking.size(); ++j){
        double escala = tg_alfa * (ranking_cp.back() - ranking[j]);
        ranking_escala.push_back(escala);
    }
    return ranking_escala;
}


vector <double> portion_of_ranking(vector <int> att, vector <double> ranking_all_att){

    vector <double> new_ranking;

    for (unsigned int j = 0; j < att.size(); ++j)
        new_ranking.push_back(ranking_all_att[att[j]]);
    return new_ranking;
}

//adicona no vector de int somente os att que nao estao em s
vector <int> portion_of_att(vector <int> att_s, vector <double> ranking_all_att){

    vector <int> new_att;

    for (unsigned int j = 0; j < ranking_all_att.size(); ++j)
        if (in_array_int(j, att_s)== -1)
            new_att.push_back(j);
    return new_att;
}

//adicona no vector de int somente os att que nao estao em s e estao em possible_att
vector <int> portion_of_att_int(vector <int> att_s, vector <int> possible_att){

    vector <int> new_att;

    for (unsigned int j = 0; j < possible_att.size(); ++j)
        if (in_array_int(possible_att[j], att_s)== -1)
            new_att.push_back(possible_att[j]);
    return new_att;
}


//recebe uma matriz e retorna os valores da coluna na posicao k
vector <double> get_column(const vector< vector<double> > &matriz, int k){

    vector <double> vec;
    int tam_lines = matriz.size();
    for (unsigned int j = 0; j < tam_lines; ++j)
        vec.push_back(matriz[j][k]);
    return vec;
}

//verifica se o subconjunto esta na lista passada e retorna merit ou -1 se nao estiver
long double in_list_candidate(int size_set, const set <int> cand, list< candidate > &list_c){

	list<candidate>::iterator it;
	for (it=list_c.begin(); it!=list_c.end(); ++it)
        if (it->size_set == size_set){
            //long double teste = it->merit;
            //cout << "comparei size! merit: " << teste << "\n";
            if (it->att == cand) return it->merit;
        }


	return -1;
}


list< set<int> > create_successors(const set<int> &father, int number_att){

    list <set<int>> successors;
    pair<set<int>::iterator,bool> it;

    for (unsigned int j = 0; j < number_att; ++j){
        set<int> aux = father;
        it = aux.insert(j);
        if (it.second==true)
            successors.push_back(aux);
    }

    return successors;
}


set<int> binary_to_subset(const vector<int> &vec_binary){

    set<int> aux;
    for (unsigned int j = 0; j < vec_binary.size(); ++j){
        if (vec_binary[j]==1)
            aux.insert(j);
    }
    return aux;
}


vector<vector<int>> readPopulationFromFile(const string& filename) {
    vector<vector<int>> population;
    ifstream file(filename);
    if (!file.is_open()) {
        cerr << "Error opening file: " << filename << endl;
        return population;
    }

    string line;
    while (getline(file, line)) {
        vector<int> individual;
        stringstream ss(line);
        int num;
        while (ss >> num) {
            individual.push_back(num);
        }
        population.push_back(individual);
    }

    file.close();
    return population;
}