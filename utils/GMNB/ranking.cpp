#include "ranking.h"

bool myfunction (string i, string j) { return (i.size() < j.size()); }

void compute_w(double *w, int max_level){
    for(int i = 0; i < max_level; ++i)
        w[i] = double((double(max_level) - (i+1) +1) * (2/(double(max_level)*(double(max_level)+1))));

}


//
vector < double > rankingSUH (vector< string > &a_class, vector< string > &dist_class,
                              vector< vector< double > > &data){

    vector < double > ranking, freq_class;
    vector < string > possible_class;

    stringstream concate;
    string possible_c;
    int maxlevel;
    //para cada classe distinta, calcular frequencia na base, max_level e possible_class
    maxlevel = getMaxLevel(dist_class);
    freq_class = frequence(dist_class, a_class);
    int tam_class = dist_class.size();
    for(int i = 0; i < tam_class; ++i){
        vector< string > aux_str = explode(dist_class[i],'.');
        int level = aux_str.size();

        //adicona as superclasses de classe em possible_class se for classe distinta
        for(int j = 0; j < level; ++j){
            if (j==0){
                concate << aux_str[j];
            }else{
                concate << "." << aux_str[j];
            }
            possible_c = concate.str();
            if(in_array_string(possible_c, possible_class) == -1){
				possible_class.push_back(possible_c); //se for classe nova, adicona no vector possible_class
				//cout << "Adicionei: " << possible_c << "\n";
			}
        }
        concate.str("");
    }
    //cout << "Terminei: " << max_level;

    //ordena o vetor de classes possiveis
    sort (possible_class.begin(), possible_class.end(), myfunction);

    double w[maxlevel];
    compute_w(w, maxlevel);
    double class_entropy = 0;
    vector< string > possible_class_cp;
    possible_class_cp = possible_class; //faz uma copia do vector possible_class

    vector < double > freq_node;
    //calcula entropia hierarquica do atributo classe
    for (int j = 0; j < maxlevel; ++j){  // para cada nivel

        double sum = 0;     // soma das instancias que participam do nivel avaliado
        double level_entropy = 0; // entropia calculada para o nivel avaliado
        string possible = possible_class_cp.front(); //pega primeiro elemento
        int mylevel = int (count (possible.begin(), possible.end(), '.'));
        //cout << "\n" << mylevel;
        //para cada possible que faz parte do nivel j
        while ((mylevel == j) && !(possible_class_cp.empty())){
            //cout << "\n" << possible;
            possible_class_cp.erase(possible_class_cp.begin()); //apaga primeiro elemento
            double freq = 0;
            for (int k = 0; k < tam_class; ++k) // para cada classe distinta
                if (is_ascendant(possible, dist_class[k])) // se a classe possivel esta contida na classe distinta
                    freq += freq_class[k];
            freq_node.push_back(freq);
            freq = 0;
            if (!(possible_class_cp.empty())){
                possible = possible_class_cp.front();
                mylevel = int(count (possible.begin(), possible.end(), '.'));
            }

        }

        int tam_level_nodes = freq_node.size();
        //soma o total de frequencia na base do nivel
        for (int i = 0; i < tam_level_nodes; ++i)  sum += freq_node[i];
        for (int i = 0; i < tam_level_nodes; ++i){
                double entropy = (freq_node[i]/sum)*log2((freq_node[i]/sum));
                level_entropy += entropy;
        }
        level_entropy = level_entropy * w[j];
        class_entropy += level_entropy;
        freq_node.erase(freq_node.begin(),freq_node.end());
    }

    //entropia hierarquica do atributo classe
    class_entropy = -(class_entropy);
    //cout << "\nEntropia da classe: " << class_entropy << "\n";
    //cout << "\nTamanho do vector possible: " << possible_class.size() << "\n";


   int tam_att = data[0].size(), tam_inst = data.size();

   // cacula o ranking SUH para cada atributo
    vector< double > att_value_dist;
    vector <int> freq_value_att;
    for (int i = 0; i < tam_att; ++i){

        //para cada instancia, calcula a frequencia de att distintos e guarda seus valores em att_value_dist
        for (int j = 0; j < tam_inst; ++j){
            //cout << "valor att de isnt: " << data[j][i] << "\n";
            int pos = in_array(data[j][i], att_value_dist);
            //cout << "valor de posicao: " << pos << "\n";
            if ( pos != -1){
                freq_value_att[pos]++;
                //cout << "freq atual: " << freq_value_att[pos] << "\n";
            }else{
                att_value_dist.push_back(data[j][i]);
                freq_value_att.push_back(1);
            }
        }
        //calcula entropia na base do att i
        double att_entropy = 0;
        for (unsigned int j = 0; j < att_value_dist.size(); ++j){
            double entropy = (double(freq_value_att[j])/double(tam_inst))*
                              log2(double(freq_value_att[j])/double(tam_inst));
            att_entropy += entropy;
        }
        att_entropy = -(att_entropy);
        //cout << "\nEntropia do att: " << att_entropy << "\n";

        //calcula a entropia hierarquica do atributo i em relacao ao att classe
        double att_entropy_related_class = 0;
        for (unsigned int v = 0; v < att_value_dist.size(); ++v){  // para cada valor distinto do att i
            possible_class_cp = possible_class; //faz uma copia do vector possible_class
            double att_value_entropy = 0;
            //calcula entropia hierarquica do valor atual do atributo i em relacao ao atributo classe
            for (int j = 0; j < maxlevel; ++j){  // para cada nivel
                double level_entropy = 0; // entropia calculada para o nivel avaliado
                string possible = possible_class_cp.front(); //pega primeiro elemento
                int mylevel = int (count (possible.begin(), possible.end(), '.'));

                //para cada possible que faz parte do nivel j
                while ((mylevel == j) && !(possible_class_cp.empty())){
                    //cout << "\n" << possible;
                    possible_class_cp.erase(possible_class_cp.begin()); //apaga primeiro elemento
                    double freq = 0;

                    for (int k = 0; k < tam_inst; ++k)
                        if ((data[k][i] == att_value_dist[v]) && (is_ascendant(possible, a_class[k])))
                            freq++;
                    //se nao foi computado frequencia para o valor do att, entao nao precisa calcular entropia
                    if (freq != 0)
                        freq_node.push_back(freq);
                    //cout << "\nFrequencia do no "<< possible << ": " << freq << "\n";
                    freq = 0;
                    if (!(possible_class_cp.empty())){
                        possible = possible_class_cp.front();
                        mylevel = int(count (possible.begin(), possible.end(), '.'));
                    }
                }
                int tam_level_nodes = freq_node.size();

                for (int k = 0; k < tam_level_nodes; ++k){
                    double entropy = (freq_node[k]/freq_value_att[v])*log2((freq_node[k]/freq_value_att[v]));
                   // cout << "\nEntropia no nivel " << j << " do no " << k << ": " << entropy << "\n";
                    level_entropy += entropy;
                }
                level_entropy = level_entropy * w[j];
                att_value_entropy += level_entropy;
                freq_node.erase(freq_node.begin(),freq_node.end());
            }
            att_entropy_related_class += att_value_entropy*(freq_value_att[v]/double(tam_inst));
        }
        att_entropy_related_class = -(att_entropy_related_class);
        //cout << "\nEntropia do att em relacao a classe: " << att_entropy_related_class << "\n";
        att_value_dist.erase(att_value_dist.begin(),att_value_dist.end());
        freq_value_att.erase(freq_value_att.begin(),freq_value_att.end());

        double gih = class_entropy - att_entropy_related_class;
        double suh = 2*(gih/(class_entropy+att_entropy));
        ranking.push_back(suh);

	}

    return ranking;
}
