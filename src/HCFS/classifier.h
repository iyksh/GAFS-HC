#ifndef CLASSIFIER_H
#define CLASSIFIER_H
#include<iostream>
#include<string>
#include<fstream>
#include<vector>
#include"chargeTrainingSet.h"
#include"chargeTestSet.h"
#include"utils.h"
#include<cmath>
#include<limits>

class Classifier{
public:
  static ChargeTrainingSet *auxCLCTR;
  static ChargeTestSet *auxCLCTE;
  ifstream fin;
  ofstream fout;

  unsigned int numberOfTrainingExamples;
  unsigned int numberOfTestExamples;
  unsigned int numberOfAttributes;
  string resultFile;
	bool usefulness;

  //Vetores que armazenam os resultados da classificacao (classes real e predita da instancia de teste)
  vector < string > t;
  vector < string > p;

  void openResultFile();
  void closeResultFile();


  long double computeProbabilityAttributeClass(const unsigned int &numberOfLevels, const unsigned int &attributeId, const string &classId);
  double computeProbabilityTrainingClass(const string &classId);

  void initializeT(const string &trueClass);
  void initializeP(const string &predictedClass);
  int getSizeT();
  int getSizeP();
	unsigned int minValue(const unsigned int &value1, const unsigned int &value2);
  int intersectionPT(const string &trueClass, const string &predictedClass);

  int numberOfLevels(const string &classId);


  long double applyClassifier();

  //Construtor
  Classifier(const unsigned int &numberOfTrainingExamples, const unsigned int &numberOfTestExamples, const unsigned int &numberOfAttributes, const string &resultFile, const bool &usefulness){
	this->numberOfTrainingExamples = numberOfTrainingExamples;
	this->numberOfTestExamples = numberOfTestExamples;
	this->numberOfAttributes = numberOfAttributes;
	this->resultFile = resultFile;
	this->usefulness = usefulness;
  }
  //Destrutor
  ~Classifier(){
  }
};


#endif
