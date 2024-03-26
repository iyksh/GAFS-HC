#include "utils.h"


string lowercase(string str){
	for(int i = 0; i < str.size(); i++){
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

// verifica se v_class esta no vector f_class
int in_array_string(string v_class, vector< string > &f_class){
	for(unsigned int j=0; j < f_class.size(); ++j){
		if(v_class.compare(f_class[j]) == 0){
			return j;
		}
	}

	return -1;
}

//verifica se value esta no vector v_value
int in_array(double value, vector< double > &v_value){
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
	int i = 0, checkNumberOfAttributes = 0, pos, begin, end, lastComma, classId;
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
		end = line.size();
		begin = line.rfind(",")+1;
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
		end = line.size();
		begin = line.rfind(",")+1;
		classId = str2int(line.substr(begin, end-begin));
		numberOfTestExamples++;
	}
	fin1.close();

}
