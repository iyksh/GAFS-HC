#include<iostream>
#include "chargeTrainingSet.h"

using namespace std;

void ChargeTrainingSet::openTrainingFile(){
  fin.open(trainingFile);
  if(!fin.is_open()){
    cout << "Error opening training file!!!" << endl;
    exit(1);
  }
}

void ChargeTrainingSet::closeTrainingFile(){
  fin.close();
}
//####################### AttributeIndex Section #############################
void ChargeTrainingSet::updateAttributeIndex(const unsigned int &index, const unsigned int &numberOfValues){
  attributeIndex[index]= attributeIndex[index-1] + numberOfValues;
}

void ChargeTrainingSet::printAttributeIndex(){
  unsigned int i = 0;
  for(it_attributeIndex = attributeIndex.begin(); it_attributeIndex != attributeIndex.end(); it_attributeIndex++){
	cout << "Attribute " << i++ << "\t -> \t index " << *it_attributeIndex  << endl;
  }
}

int ChargeTrainingSet::computeNumberOfIndependentAttributeValues(){
  return(attributeIndex[numberOfAttributes-1]);
}

unsigned int ChargeTrainingSet::getAttributeIndex(const unsigned int &attributeId){
  return(attributeIndex[attributeId]);
}
//####################### Counter Section #############################
void ChargeTrainingSet::initializeCounter(){
  counter.clear();
  counter.resize(numberOfIndependentAttributeValues+1,0);//A ultima posicao do vetor armazenara a frequencia da classe na base de dados
  counter[numberOfIndependentAttributeValues] = 1;//Inicializando a ultima posicao com o valor 1
}

void ChargeTrainingSet::updateCounter(const unsigned int &index){
  counter[index]++;
}
//####################### ClassFreq Section #############################
void ChargeTrainingSet::updateClassFreq(const string &classId){
  if((it_classFreq = classFreq.find(classId)) == classFreq.end()) classFreq[classId] = counter;
  else{
	it_counter = counter.begin();
    for(it2_classFreq = it_classFreq->second.begin(); it2_classFreq != it_classFreq->second.end(); it2_classFreq++){
	  if((*it_counter) == 1) (*it2_classFreq)++;
	  it_counter++;
	}
  }
}

unsigned int ChargeTrainingSet::getAttributeValueClassFrequency(const unsigned int &attributeId, const unsigned int &attributeValue, const string &classId){
  if(classFreq.find(classId) != classFreq.end())
	return(classFreq[classId][getAttributeIndex(attributeId)+attributeValue]);
  else return(0);
}

unsigned int ChargeTrainingSet::getClassFrequency(const string &classId){
  if(classFreq.find(classId) != classFreq.end())
	return(classFreq[classId][numberOfIndependentAttributeValues]);//Retorna o valor da ultima posicao do vetor associado a classe classeId, o qual contem a sua frequencia
	else return(0);
}

void ChargeTrainingSet::printClassFreq(){
  int index;
  for(it_classFreq = classFreq.begin(); it_classFreq != classFreq.end(); it_classFreq++){
	cout << "Class " << it_classFreq->first << endl;
	index = 0;
	for(it2_classFreq = it_classFreq->second.begin(); it2_classFreq != it_classFreq->second.end(); it2_classFreq++){
	  cout << index << "\t" << *it2_classFreq << endl;
	  index++;
	}
  }
}

//####################### ClassesForProbabilityEvaluation Section #############################
void ChargeTrainingSet::setClassesForProbabilityEvaluation(const string &classId){//classeId eh uma string que ja esta sem a parte "R."
  int begin = -1, end = -1;
  string fatherNode, subsetClassId;

  //cout << "Tentando inserir - ClassId " << classId << endl;
  if(classesForProbabilityEvaluation.find(classId) == classesForProbabilityEvaluation.end()){//Se não existir a classeId em classesForProbabilityEvaluation...

	if(mandatoryLeafNodePrediction){
	  if(notExistChild(classId)){//Se não existir um filho de classId em classesForProbabilityEvaluation...
		classesForProbabilityEvaluation[classId] = 1;//O valor classid é inserido como sendo um no folha com treesize = 1
        //cout << "\tClasse Inserida: " << classId << "\tTamanho = " << (int)classesForProbabilityEvaluation.size() << endl;
		fatherNode.clear();
		while((end = classId.find(".",begin+1)) != string::npos){
		  fatherNode+= classId.substr(begin+1,end-begin-1);
		  classesForProbabilityEvaluation.erase(fatherNode);//Apaga todos os nos pais da classe inserida em classesForProbabilityEvaluation
		  //cout << "***Apagando o pai " << fatherNode << "\tTamanho = " << (int)classesForProbabilityEvaluation.size() << endl;
		  begin = end;
		  fatherNode+= ".";
		}

	  }
	}
	else{//Armazenando a classe e suas subclasses (p.ex., se classId = 1.2.1, as subclasses serão 1 e 1.2)
	  subsetClassId.clear();
	  while((end = classId.find(".",begin+1)) != string::npos){
		subsetClassId+= classId.substr(begin+1, end-begin-1);
		classesForProbabilityEvaluation[subsetClassId] = 1;
		begin = end;
		subsetClassId+= ".";
	  }
	  classesForProbabilityEvaluation[classId] = 1;
	}
  }
}

bool ChargeTrainingSet::notExistChild(const string &classId){
  for(it_classesForProbabilityEvaluation = classesForProbabilityEvaluation.begin(); it_classesForProbabilityEvaluation != classesForProbabilityEvaluation.end(); it_classesForProbabilityEvaluation++){
	if(it_classesForProbabilityEvaluation->first.size() > classId.size() && it_classesForProbabilityEvaluation->first.substr(0,(int)classId.size()) == classId) return(false);
  }
  return(true);
}

void ChargeTrainingSet::computeClassUsefulness(){
	int begin = -1, end = -1, maxTreeSize = 1;
	string fatherNode, classeId;

	//Inicializando todos os classes com valor 1
	for(it_classesForProbabilityEvaluation = classesForProbabilityEvaluation.begin(); it_classesForProbabilityEvaluation != classesForProbabilityEvaluation.end(); it_classesForProbabilityEvaluation++){
		it_classesForProbabilityEvaluation->second = 1;
	}
	//Computando o treesize de cada classe...
	for(it_classesForProbabilityEvaluation = classesForProbabilityEvaluation.begin(); it_classesForProbabilityEvaluation != classesForProbabilityEvaluation.end(); it_classesForProbabilityEvaluation++){
		fatherNode.clear();
		begin = -1;
		end = -1;
		classeId = it_classesForProbabilityEvaluation->first;
		while((end = classeId.find(".",begin+1)) != string::npos){
			fatherNode+= classeId.substr(begin+1,end-begin-1);
		  if(classesForProbabilityEvaluation.find(fatherNode) != classesForProbabilityEvaluation.end()){//Se existir a classeId em classesForProbabilityEvaluation...
				classesForProbabilityEvaluation[fatherNode]++;//Atualizando o número de classes descendentes...
			}
			begin = end;
			fatherNode+= ".";
		}
	}
	//Obtendo o maior treesize...
	for(it_classesForProbabilityEvaluation = classesForProbabilityEvaluation.begin(); it_classesForProbabilityEvaluation != classesForProbabilityEvaluation.end(); it_classesForProbabilityEvaluation++){
		if(it_classesForProbabilityEvaluation->second > maxTreeSize) maxTreeSize = it_classesForProbabilityEvaluation->second;
	}
	//Calculando o Usefulness de cada classe
	for(it_classesForProbabilityEvaluation = classesForProbabilityEvaluation.begin(); it_classesForProbabilityEvaluation != classesForProbabilityEvaluation.end(); it_classesForProbabilityEvaluation++){
		classesForProbabilityEvaluation[it_classesForProbabilityEvaluation->first] = 1 - log2(it_classesForProbabilityEvaluation->second)/log2(maxTreeSize+1);
	}
}

double ChargeTrainingSet::getClassUsefulness(const string &classeId){
	return(classesForProbabilityEvaluation[classeId]);
}


void ChargeTrainingSet::printClassesForProbabilityEvaluation(){
  cout << "*************Training Classes*************" << endl;
  for(it_classesForProbabilityEvaluation = classesForProbabilityEvaluation.begin(); it_classesForProbabilityEvaluation != classesForProbabilityEvaluation.end(); it_classesForProbabilityEvaluation++){
	cout << it_classesForProbabilityEvaluation->first << "\t" << it_classesForProbabilityEvaluation->second << endl;
  }
}
//####################### ClassPerLevel Section #############################
unsigned int ChargeTrainingSet::initializeClassPerLevel(const string &classId){//classeId eh uma string que ja esta sem a parte "R."
  int begin = -1, end = -1;

  classPerLevel.clear();
  while((end=classId.find(".",begin+1)) != string::npos){
	classPerLevel.push_back(classId.substr(begin+1,end-begin-1));
	begin = end;
  }
  classPerLevel.push_back(classId.substr(begin+1,classId.size()-begin-1));
  return(classPerLevel.size());
}

string ChargeTrainingSet::getClassPerLevel(const int &index){
  return(classPerLevel[index]);
}

string ChargeTrainingSet::getSubsetClass(const int &level){
  string subsetClassId;
  subsetClassId.clear();
  for(int i = 0; i < level; i++){
	//Montar a string com o nome da subclasse...
	subsetClassId+= getClassPerLevel(i);
	subsetClassId+= ".";
  }
  return(subsetClassId.substr(0,(int)subsetClassId.size()-1));//retornando a string sem o ultimo ponto
}

void ChargeTrainingSet::printClassPerLevel(){
  cout << "Class separated per level: ";
  for(it_classPerLevel = classPerLevel.begin(); it_classPerLevel != classPerLevel.end(); it_classPerLevel++){
	cout << *it_classPerLevel << "\t";
  }
  cout << endl;
}

//###################### Main Section #######################################
void ChargeTrainingSet::getTrainingSet(){
  int begin = -1, end = -1, i = -1, stop = 0;
  double t1 = 0, t2 = 0;
  unsigned int numberOfValues = 0, attributeId = 0;
  unsigned int numberOfLevels = 0;
  string line, lastLine, classId, attributeValue, subsetClassId;
  numberOfIndependentAttributeValues = 0;
  biggestLevel = 0;
  openTrainingFile();

  while(getline(fin,line) && lowercase(line.substr(0,5)) != "@data"){//Lendo cada linha do arquivo de entrada a partir do inicio (META-DADOS)...
    if(lowercase(line.substr(0,10)) != "@attribute") {//Lendo somente as linhas que contem informacoes sobre os atributos
      continue;
    }
	numberOfValues = 1;
    begin = line.find("{",9);
    while((end = line.find(",",begin+1)) != string::npos){
	  numberOfValues++;
	  begin = end;
    }
    updateAttributeIndex(attributeId+1,numberOfValues);
	attributeId++;
	lastLine = line;//Objetivo: armazenar a linha referente ao atributo classe.
  }
  //printAttributeIndex();
  numberOfIndependentAttributeValues = computeNumberOfIndependentAttributeValues();
  //cout << numberOfIndependentAttributeValues << endl;
  //cout << lastLine << endl;

  //**********Armazenando as classes que serao consideradas na classificacao****************
  //t1 = getCurrentCPUTime();
  begin = lastLine.find("{",9);
  while((end = lastLine.find(",",begin+1)) != string::npos){
    //cout << lastLine.substr(begin+1+2,end-begin-1-2) << endl;
	setClassesForProbabilityEvaluation(lastLine.substr(begin+1,end-begin-1));//Armazenando as classes (menos a última)
	begin = end;
  }
  end = lastLine.find("}", begin+1);
  //cout << lastLine.substr(begin+1+2,end-begin-1-2) << endl;
  setClassesForProbabilityEvaluation(lastLine.substr(begin+1,end-begin-1));//Armazenando a ultima classe
  //t2 = getCurrentCPUTime();
  //cout << "t1 = " << t1 << endl;
  //cout << "t2 = " << t2 << endl;
  //cout << "Tempo Gasto = " << t2 - t1 << endl;
  //printClassesForProbabilityEvaluation();
  //****************************************************************************************

  while(getline(fin,line)){//Lendo cada linha do arquivo de entrada (DADOS)...
    if (line.substr(0,1) == "%" || (int)line.size() == 0) {
      continue;
    }
    initializeCounter();//Definindo o tamanho do vetor Counter e zerando todas as suas posicoes
    //Ajustando as variaveis begin e end para coletar o valor do atributo classe
    begin = line.rfind(",");
		end = line.size();
		classId = line.substr(begin+1,end-begin-1);//O +2 e -2 sao para eliminacao do "R." ja tirei
		//cout << classId << endl;

		//Ajustando as variaveis begin e stop para coletar os valores dos atributos independentes
		stop = line.rfind(",");//Pto de parada eh a ultima virgula...
		begin = -1;
		attributeId = 0;
		while(begin < stop){
			end = line.find(",",begin+1);
			attributeValue = line.substr(begin+1,end-(begin+1));
			if(str2int(attributeValue) <= (getAttributeIndex(attributeId+1)-getAttributeIndex(attributeId)))//Verificando se os valores dos atributos estão de acordo com o que foi estabelecido nos META-DADOS.
			updateCounter(getAttributeIndex(attributeId)+str2int(attributeValue));//Atualizando a frequencia de cada valor de atributo
			else{
			cout << "Training File Error: Inconsistent Attribute Value for AttributeId = " << attributeId << endl;
			exit(1);
			}
			begin = end;
			attributeId++;
		}//fim da atualizacao do vetor Counter para 1 instancia da base de dados...

		numberOfLevels = initializeClassPerLevel(classId);//Cada posicao do vetor classPerLevel recebera a classe referente a um nivel da hierarquia representada na string classId
		if(numberOfLevels > biggestLevel) biggestLevel = numberOfLevels;
		//printClassPerLevel();

		//Atualizando a frequencia de todas as subclasses de "classId"
		for(int i = 1; i <= numberOfLevels; i++){
			updateClassFreq(getSubsetClass(i));//Atualizando a hash com o vetor Counter para a subclasse
		}
  }
  computeClassUsefulness();
	//printClassesForProbabilityEvaluation();
  //printClassFreq();
  closeTrainingFile();
}
