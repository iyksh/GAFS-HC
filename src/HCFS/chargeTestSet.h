#ifndef CHARGETESTSET_H
#define CHARGETESTSET_H
#include<fstream>
#include<string>
#include<vector>
#include"utils.h"
using namespace std;

class ChargeTestSet{
public:
  ifstream fin;
  string testFile;
  unsigned int numberOfAttributes;
  unsigned int numberOfTestExamples;
  
  vector < vector < int > > testSet;//Número do exemplo (int) -> Valor dos atributos (int)
  vector < vector < int > >:: iterator it_testSet;
  vector < int >:: iterator it2_testSet;
  
  vector < string > classTestSet;//Valor da classe de cada instancia
  vector < string >:: iterator it_classTestSet;
  
  void openTestFile();
  void closeTestFile();
  
  void insertTestSet(const int &exampleId, const int &attributeId, const int &attributeValue);
  int getAttributeValueTestSet(const int &exampleId, const int &attributeId);
  void printTestSet();
  
  void insertClassTestSet(const int &exampleId, const string &attributeValue);
  string getClassTestSet(const int &exampleId);
  void printClassTestSet();


  void getTestSet();
  
  //constructor
  ChargeTestSet(const string &testFile, const int &numberOfTestExamples, const int &numberOfAttributes){
    this->testFile = testFile;
    this-> numberOfAttributes = numberOfAttributes;
	this->numberOfTestExamples = numberOfTestExamples;
    //Definindo a dimensão das estruturas
    testSet.resize(numberOfTestExamples);
    for(it_testSet = testSet.begin(); it_testSet != testSet.end(); it_testSet++){
      (*it_testSet).resize(numberOfAttributes-1);//Armazena somente o valor dos atributos independentes...
    }
    classTestSet.resize(numberOfTestExamples);
  }
  //destructor
  ~ChargeTestSet(){
  }
};

#endif
