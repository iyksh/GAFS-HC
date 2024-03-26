#ifndef CHARGETRAININGSET_H
#define CHARGETRAININGSET_H
#include<fstream>
#include<string>
#include<vector>
#include<unordered_map>
#include<unordered_set>
#include<cmath>
#include<time.h>
#include"utils.h"

using namespace std;

class ChargeTrainingSet{
public:
  ifstream fin;
  string trainingFile;
  unsigned int numberOfAttributes;
  unsigned int numberOfTrainingExamples;
  unsigned int numberOfIndependentAttributeValues;
  unsigned int biggestLevel;//variável que sera utilizada para definir o tamanho da matriz que representara o grafo de dependencias em classifier.cpp
  bool mandatoryLeafNodePrediction;
  
  //Vetor que armazena, para cada valor de atributo, o seu indice correspondente no vector<> counter 
  vector< int > attributeIndex;
  vector< int >:: iterator it_attributeIndex;
  
  //Hash_map que armazena para cada classe (string) a frequencia com que ela ocorre com cada valor de atributo (vetor Counter) 
  unordered_map< string, vector< unsigned int > > classFreq;
  unordered_map< string, vector< unsigned int > >:: iterator it_classFreq;
  vector< unsigned int > counter;
  vector< unsigned int >:: iterator it2_classFreq;
  vector< unsigned int >:: iterator it_counter;
    
  //Hash-set utilizado para armazenar as classes da base de dados de treinamento para as quais serão calculadas as probabilidades P(C|X) e seus respectivos valores de usefulness
  unordered_map< string, double > classesForProbabilityEvaluation;
  unordered_map< string, double >:: iterator it_classesForProbabilityEvaluation;

  //Vetor para manipular os strings classId
  vector< string > classPerLevel;
  vector< string >:: iterator it_classPerLevel;
  
  void openTrainingFile();
  void closeTrainingFile();
  void getTrainingSet();
  
  void updateAttributeIndex(const unsigned int &index, const unsigned int &numberOfValues);
  void printAttributeIndex();
  int computeNumberOfIndependentAttributeValues();
  unsigned int getAttributeIndex(const unsigned int &attributeId);

  
  void initializeCounter();
  void updateCounter(const unsigned int &index);

  
  void updateClassFreq(const string &classId);
  unsigned int getAttributeValueClassFrequency(const unsigned int &attributeId, const unsigned int &attributeValue, const string &classId);
  unsigned int getClassFrequency(const string &classId);
  //void checkClassFreq();
  void printClassFreq();

  void setClassesForProbabilityEvaluation(const string &classId);
  bool notExistChild(const string &classId);
	void computeClassUsefulness();
	double getClassUsefulness(const string &classeId);
  void printClassesForProbabilityEvaluation();


  unsigned int initializeClassPerLevel(const string &classId);
  string getClassPerLevel(const int &index);
  string getSubsetClass(const int &level);
  void printClassPerLevel();
  
  //Constructor
  ChargeTrainingSet(const string &trainingFile, const unsigned int &numberOfAttributes, const unsigned int &numberOfTrainingExamples, const bool &mandatoryLeafNodePrediction){
    this->trainingFile = trainingFile;
	this->numberOfAttributes = numberOfAttributes;
	this->numberOfTrainingExamples = numberOfTrainingExamples;
	this->mandatoryLeafNodePrediction = mandatoryLeafNodePrediction;
	
	attributeIndex.resize(numberOfAttributes+1,0);
  }

  //Destructor
  ~ChargeTrainingSet(){
  }
};

#endif