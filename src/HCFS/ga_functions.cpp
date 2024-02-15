#include "ga_functions.h"




vector< vector<int> > inicialize_population(unsigned int bits, unsigned int population_size){

    vector< vector<int> > population;

    for(int i = 0; i < population_size; ++i){
        vector<int> individual;
        for(int j = 0; j < bits; ++j){
            float aux = randomico(0.5,1.5);
            individual.push_back(int(aux));
        }
        population.push_back(individual);
    }

    return population;

}

vector<double> evaluate(list <candidate> &open, priority_queue <candidate_queue> &open_queue, vector<long double> &fitness,
              const vector<vector<int>> &population, const vector< vector<double> > &correlation_ff_mat,
              const vector <double> &correlation_fl_vec){

    
    if (population.size() != fitness.size())
    {
        std::cerr << "Population and fitness vector sizes are different." << std::endl;
    }
    

    vector<double> att_analises, att_vec_avg;
    double best_att, worse_att, avg_att; //guarda o numero de atributos do melhor, pior e numero de atributo medio dos subconjuntos
    long double best_merit=0, worse_merit=100;
    for(int i = 0; i < population.size(); ++i){
        set<int> aux = binary_to_subset(population[i]);
        cout << "stopper 2" << endl;
        
        int size_set = aux.size();
        long double merit_open = in_list_candidate(size_set, aux, open);
        //se subset ainda nao esta contido na lista open
        if (merit_open==-1){
            //inclui candidato na lista open
            candidate new_set;
            new_set.att = aux;
            vector<int> set_vec(aux.begin(),aux.end());

            //escolhe a forma de calcular merit
            if (set_vec.size() < 1)
                 fitness[i] = 0.0;
            else if(set_vec.size()==1)
                fitness[i] = correlation_fl_vec[set_vec[0]];
            else{

            vector <long double> fo_cfs_hierarq;
            fo_cfs_hierarq = merit_cfs(set_vec, correlation_ff_mat, correlation_fl_vec);
            new_set.merit = fo_cfs_hierarq[0];
            new_set.size_set = size_set;
            open.push_back(new_set);
            //cria um elemento para a fila de prioridade
            candidate_queue new_set_queue;
            new_set_queue.merit = new_set.merit;
            new_set_queue.position = open.size()-1;
            open_queue.push(new_set_queue);
            //atualiza o vetor fitness
            fitness[i] = new_set.merit;
            }
        }else //se esta contido na lista open, apenas atualiza fitness
            fitness[i] = merit_open;

        //faz a verificacao do melhor, pior e inclui numero de atributo para calculo da media
        if (fitness[i]>best_merit){
            best_merit = fitness[i];
            best_att = size_set;
        }else
            if (fitness[i]<worse_merit){
            worse_merit = fitness[i];
            worse_att = size_set;
            }
        //inclui size_set no att_vec_avg para calculo da media
        att_vec_avg.push_back(double(size_set));
    }

    cout << "stopper 3" << endl;

    for (unsigned int i = 0; i < fitness.size(); ++i)
        cout << " " << fitness[i];

    
    avg_att = mean(att_vec_avg);
    att_analises.push_back(best_att);
    att_analises.push_back(worse_att);
    att_analises.push_back(avg_att);

    // printing the best, worse and average number of attributes
    cout << "Best, worse and average number of attributes: ";
    for (int i = 0; i < att_analises.size(); ++i)
        cout << " " << att_analises[i];

    cout << "\n";
    return att_analises;

}

//selecao eh pelo metodo roleta, que recebe o fitness como entrada


//Point mutation operator
vector<int> mutation_point(const vector<int> parent){

    vector<int> offspring;
    //escolhe uma posicao aleatoriamente
    int att_size = parent.size();
    int point = int(randomico(0,att_size));
    //nao pode ser att_size
    if (point == att_size)
        point = point-1;

    for(int i = 0; i < att_size; ++i){
        if (i == point) {
        int bit = int(randomico(0.5,1.5));
        offspring.push_back(bit);
        }else
        offspring.push_back(parent[i]);

    }
    return offspring;

}

//one-point crossover que recebe dois pais e gere dois filhos
vector < vector<int> > crossover_one_point(const vector<int> parent1, const vector<int> parent2){

    vector<int> offspring1, offspring2, aux1, aux2, aux3;
    vector < vector<int> > offspring_list;
    aux1 = parent1;
    aux2 = parent2;
    //escolhe uma posicao aleatoriamente
    int att_size = parent1.size();
    int point = int(randomico(0,att_size));
    //nao pode ser att_size
    if (point == att_size)
        point = point-1;
    for(int i = 0; i < att_size; ++i){
        if (i == point) {
        aux3 = aux1;
        aux1 = aux2;
        aux2 = aux3;
        }

        offspring1.push_back(aux1[i]);
        offspring2.push_back(aux2[i]);
    }

    offspring_list.push_back(offspring1);
    offspring_list.push_back(offspring2);

    return offspring_list;
}

//acha o subset com melhor hF e menor numero de atributos possivel
candidate best_hf_att_subset(list <candidate> open, priority_queue <candidate_queue> open_queue){

    list<candidate>::iterator it_open1, it_open2;
    candidate best, aux;
    candidate_queue current_top = open_queue.top();
    open_queue.pop();
    it_open1 = open.begin();
    advance(it_open1,current_top.position);
    best = *it_open1;
    while (!open_queue.empty()){
        current_top = open_queue.top();
        open_queue.pop();
        it_open2 = open.begin();
        advance(it_open2,current_top.position);
        aux = *it_open2;
        if (best.merit == aux.merit){
            if (aux.size_set < best.size_set)
                best = aux;
        }else break;
    }

    return best;

}





