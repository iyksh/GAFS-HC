#include "cfs_functions.h"


double sum_vc(const vector<double> &a){

    double s = 0;
	for (int i = 0; i < a.size(); i++)
		s += a[i];
	return s;
}

double mean(const vector<double> &b){
	return sum_vc(b) / b.size();
}

double sqsum(const vector<double> &a){

	double s = 0;
	for (int i = 0; i < a.size(); i++)
		s += pow(a[i], 2);
	return s;
}

double stdev(const vector<double> &a){

	double n = a.size();
	return pow(sqsum(a), 0.5);
}

vector<double> operator-(const vector<double> &a, const double &b){

	vector<double> retvect(a);
	for (int i = 0; i < a.size(); i++)
		retvect[i] = a[i] - b;
	return retvect;
}

vector<double> operator*(const vector<double> &a, const vector<double> &b){

	vector<double> retvect(a);
	for (int i = 0; i < a.size() ; i++)
		retvect[i] = a[i] * b[i];

	return retvect;
}

double pearsoncoeff(const vector<double> &a, const vector<double> &b){

    vector<double> dif_a(a), dif_b(a), mul(a);
    double mean_a, mean_b, test;
    long double pearson;
    mean_a = mean(a);
    mean_b = mean(b);
    dif_a = operator-(a,mean_a);
    dif_b = operator-(b,mean_b);
    mul = operator*(dif_a, dif_b);
    test = stdev(dif_a)*stdev(dif_b);
    pearson = abs((sum_vc(mul))/(stdev(dif_a)*stdev(dif_b)));
    if (isnan(pearson)){
        //cout << "Erro de divisao por zero" << endl;
        pearson = 0.00000001;
    }

	return  pearson;
}

//percorre o vector da valores de um atributo da base e retorna um vetor binario de 0 ou 1 para o valor especifico k referenciado
vector<double> binary_vec(double k, const vector<double> &a){

    int tam = a.size();
    vector<double> b(tam,0);
    for(unsigned int i = 0; i < a.size(); ++i)
        if (a[i] == k) b[i] = 1;
    return b;

}

//calcula a correlacao entre dois atributos, sendo a o categorico e b o numerico
double pearsoncoeff_cat_num(const vector<double> &a, const vector<double> &b){

    vector<double> binary;
    double pearson, sum = 0;
    int tam = a.size();
    //cout << tam  << " tamanho inst\n";
    vector <double> dist = distinct(a);
    vector <double> freq = frequence_double(dist, a);


    for(unsigned int k = 0; k < dist.size(); ++k){
        binary = binary_vec(dist[k],a);
        pearson = pearsoncoeff(binary, b);
        sum += ((freq[k]/tam)*abs(pearson));
	}

    //cout << sum  << " pearson_cat_num\n";
	return sum;
}

double prob_a_and_b(const vector<double> &a, const vector<double> &b){

    double tam = a.size();
    double sum = 0;

    for(unsigned int k = 0; k < tam; ++k)
        if (a[k] == 1 && b[k] == 1)
            ++sum;
    return (sum/tam);

}



//calcula a correlacao entre dois atributos categoricos
double pearsoncoeff_cat_cat(const vector<double> &a, const vector<double> &b){

    vector<double> binary_a, binary_b;
    double prop, pearson, sum = 0;
    vector <double> dist_a = distinct(a);
    vector <double> freq_a = frequence_double(dist_a, a);
    vector <double> dist_b = distinct(b);
    vector <double> freq_b = frequence_double(dist_b, b);


    for(unsigned int k = 0; k < dist_a.size(); ++k){
        binary_a = binary_vec(dist_a[k],a);
        for(unsigned int i = 0; i < dist_b.size(); ++i){
            binary_b = binary_vec(dist_b[i],b);
            prop = prob_a_and_b(binary_a, binary_b);
            pearson = pearsoncoeff(binary_a, binary_b);
            sum += (prop*abs(pearson));
        }
	}

	return sum;
}

//cria vetor de classes possiveis da hierarquia
vector <string> possible_class_hierarchy(const vector<string> &a_class, const vector <string> &dist_class){

    vector <string> possible_class;
    string possible_c;
    stringstream concate;

    //percorre o vetor de classes distintas e cria o vetor de classes possiveis
    int tam_class = dist_class.size();
    for(int i = 0; i < tam_class; ++i){
        vector<string> aux_str = explode(dist_class[i],'.');
        int level = aux_str.size();
        //adicona as superclasses de classe em possible_class se ainda nao estiver no vetor
        for(int j = 0; j < level; ++j){
            if (j==0)
                concate << aux_str[j];
            else
                concate << "." << aux_str[j];
            possible_c = concate.str();
            if(in_array_string(possible_c, possible_class) == -1)
				possible_class.push_back(possible_c); //se for classe nova, adicona no vector possible_class
				//cout << "Adicionei: " << possible_c << "\n";
        }
        concate.str("");
    }
    //ordena o vetor de classes possiveis
    sort (possible_class.begin(), possible_class.end(), myfunction);
    return possible_class;

}

//cria a matriz de classes possiveis (colunas) da base e sua ocorrencia (1) ou nao (0) nas instancias da base (linhas)
vector< vector<double> > a_class_to_vec(const vector<string> &a_class, const vector <string> &possible_class){

    //cria matriz de ocorrencia e inicializa com zero
    vector< vector<double> > occurrence;

    string current_c;
    stringstream concate;
    int position;

    //percorre o vetor de classes distintas e cria o vetor de classes possiveis
    int tam_instances = a_class.size();
    int tam_possible_c = possible_class.size();
    for(int i = 0; i < tam_instances; ++i){
        vector <double> instance_vec(tam_possible_c,0);
        vector<string> aux_str = explode(a_class[i],'.');
        int level = aux_str.size();
        //adicona as superclasses de classe em possible_class se ainda nao estiver no vetor
        for(int j = 0; j < level; ++j){
            if (j==0)
                concate << aux_str[j];
            else
                concate << "." << aux_str[j];
            current_c = concate.str();
            position = in_array_string(current_c, possible_class);
            instance_vec[position] = 1;
        }
        concate.str("");
        occurrence.push_back(instance_vec);
    }

    return occurrence;

}

//cria o vetor de correlacao entre todas as features da base e o atributo classe, considerando cada classe da heirarquia como classe binaria
vector <double>  correlation_fl_multilabel(const vector< vector<double> > &class_vec, const vector< vector<double> > &data,
                                           vector <int> f_type){

    vector <double> correlation;
    double pearson_normal, pearson, sum_correlation;
    int tam_class_vec = class_vec[0].size();
    int tam_features = data[0].size();


    for(unsigned int k = 0; k < tam_features; ++k){
        vector <double> feature = get_column(data, k);
        //cout << k << " to nessa feature aqui!!!\n";

        sum_correlation = 0;
        //se f_typo for 1, att eh numerico, se for 2, eh categorico
        if (f_type[k]==1){
            for(unsigned int i = 0; i < tam_class_vec; ++i){
                vector <double> label = get_column(class_vec, i);
                pearson = pearsoncoeff(feature, label);
                sum_correlation += abs(pearson);
                //cout << sum_correlation  << " correlacao soma\n";
            }
        }else{
            for(unsigned int i = 0; i < tam_class_vec; ++i){
                vector <double> label = get_column(class_vec, i);
                pearson = pearsoncoeff_cat_num(feature, label);
                sum_correlation += abs(pearson);
                //cout << sum_correlation  << " correlacao soma\n";
            }
        }
        //cout << sum_correlation  << " correlacao soma final\n";
        //cout << tam_class_vec  << " tamanho vetor classes\n";
        pearson_normal = sum_correlation/tam_class_vec;
        //cout << pearson_normal << " pearson retornada\n";
        correlation.push_back(pearson_normal);
	}

	return correlation;

}

//percorre o vetor de classes possiveis e retorna um vetor de mesmo tamanho com o nivel da classe
vector <double> class_level(const vector <string> &possible_class){

    vector <double> level_vec;
    for(unsigned int i = 0; i < possible_class.size(); ++i){
                vector<string> aux_str = explode(possible_class[i],'.');
                int level = aux_str.size();
                level_vec.push_back(level);
    }
    return level_vec;
}

//percorre o vetor de classes possiveis e retorna um vetor com o total de classes por nivel da hierarquia
vector <double> classes_per_level(int max_level, const vector <double> &possible_class_level){

    vector <double> total_classes_per_level(max_level,0);
    for(unsigned int i = 0; i < possible_class_level.size(); ++i){
        ++total_classes_per_level[possible_class_level[i]-1];
    }
    return total_classes_per_level;
}


//cria o vetor de correlacao entre todas as features da base e o atributo classe, considerando cada classe da heirarquia como classe binaria
//com um peso do nivel atribuido a cada classe
vector <double>  correlation_fl_hierarchical(const vector< vector<double> > &class_vec, const vector< vector<double> > &data,
                                           const vector <int> &f_type, const vector <double> &class_level, double w_0,
                                           const vector <double> &classes_per_level){

    vector <double> correlation;
    double pearson_normal, pearson, sum_correlation, sum_weight=0;
    int tam_class_vec = class_vec[0].size();
    int tam_features = data[0].size();

    //calcula o total de pesos multiplicados pelo total de classes por nivel da hierarquia (denominador do calculo rFL)
    for(unsigned int k = 0; k < classes_per_level.size(); ++k){
        sum_weight += (pow(w_0, k+1)*classes_per_level[k]);

    }

    for(unsigned int k = 0; k < tam_features; ++k){
        vector <double> feature = get_column(data, k);
        sum_correlation = 0;
        //se f_typo for 1, att eh numerico, se for 2, eh categorico
        if (f_type[k]==1){
            for(unsigned int i = 0; i < tam_class_vec; ++i){
                vector <double> label = get_column(class_vec, i);
                pearson = pearsoncoeff(feature, label);
                sum_correlation += abs(pearson)*(pow(w_0, class_level[i])); //multiplica a correlacao pela peso do nivel
            }
        }else{
            for(unsigned int i = 0; i < tam_class_vec; ++i){
                vector <double> label = get_column(class_vec, i);
                pearson = pearsoncoeff_cat_num(feature, label);
                sum_correlation += abs(pearson)*(pow(w_0, class_level[i])); //multiplica a correlacao pela peso do nivel
            }
        }

        pearson_normal = sum_correlation/sum_weight;
        correlation.push_back(pearson_normal);
	}

	return correlation;
}

vector< vector<double> > correlation_f_to_f_vec(const vector< vector<double> > &data, const vector <int> &f_type){

    vector< vector<double> > correlation_matrix;
    vector <double> correlation;

    double pearson_normal, pearson, sum_correlation;
    int tam_features = data[0].size();
    /*
    cria uma matriz de correlacao fxf do tipo:
    0[1 2 3]
    1[2 3]
    2[3]
    */
    for(unsigned int k = 0; k < tam_features-1; ++k){
        for(unsigned int j = k+1; j < tam_features; ++j){
            //se f_typo for 1, att eh numerico, se for 2, eh categorico
            if (f_type[k]==1 && f_type[j]==1){ //numerico e numerico
                vector <double> f1 = get_column(data, k);
                vector <double> f2 = get_column(data, j);
                pearson = pearsoncoeff(f1, f2);
                correlation.push_back(pearson);

            }else if (f_type[k]==1 && f_type[j]==2){ //numerico e categorico
                vector <double> f1 = get_column(data, k);
                vector <double> f2 = get_column(data, j);
                pearson = pearsoncoeff_cat_num(f2, f1);
                correlation.push_back(pearson);

            }else if (f_type[k]==2 && f_type[j]==1){ //categorico e numerico
                vector <double> f1 = get_column(data, k);
                vector <double> f2 = get_column(data, j);
                pearson = pearsoncoeff_cat_num(f1, f2);
                correlation.push_back(pearson);
            }else{//categorico e categorico
                vector <double> f1 = get_column(data, k);
                vector <double> f2 = get_column(data, j);
                pearson = pearsoncoeff_cat_cat(f1, f2);
                correlation.push_back(pearson);
            }
        }
        correlation_matrix.push_back(correlation);
        correlation.erase(correlation.begin(),correlation.end());
    }

    return correlation_matrix;
}

//recebe o conjunto de att candidatos, a matriz de correlacao fxf e o vetor de correlacao fxl e retorna o valor da funcao merit
vector <long double> merit_cfs(const vector <int> &s, const vector< vector<double> > &correlation_ff_mat,
                               const vector <double> &correlation_fl_vec){
    vector <long double> merit;
    long double merit_value, merit_denominator, sum_correlation_ff=0, sum_correlation_fl=0;
    vector <int> att_vec = s;
    int tam_features = att_vec.size();
    //double aux;


    sort(att_vec.begin(), att_vec.end(), myfunction_int); //atributos ordenados de maneira crescente

    for(unsigned int k = 0; k < tam_features-1; ++k){
        for(unsigned int j = k+1; j < tam_features; ++j){
            //aux = correlation_ff_mat[att_vec[k]][att_vec[j]-att_vec[k]-1];
            //cout << aux << " ff_max\n";
            sum_correlation_ff += correlation_ff_mat[att_vec[k]][att_vec[j]-att_vec[k]-1];
        }
    }
    for(unsigned int k = 0; k < tam_features; ++k){
        //aux = correlation_fl_vec[att_vec[k]];
        //cout << aux << " fl_vec\n";
        sum_correlation_fl += correlation_fl_vec[att_vec[k]];
    }

    merit_denominator = pow((tam_features+(tam_features*(tam_features-1)*sum_correlation_ff)), 0.5);
    if (isnan(merit_denominator)){
        //cout << "Erro de divisao por zero" << endl;
        merit_denominator = 0.00000001;
    }
    //cout << merit_denominator << " denominador";
   // aux = (tam_features*sum_correlation_fl);
   // cout << aux << " numerador";
    merit_value = (tam_features*sum_correlation_fl)/(merit_denominator);
    merit.push_back(merit_value);

    return merit;

}


