#include<iostream>
#include "chargeTestSet.h"

using namespace std;

void ChargeTestSet::openTestFile(){
  fin.open(testFile.c_str());
  //***********Verificando se o arquivo foi aberto*******************************
  while (!fin){
    cout << "\nErro na abertura do arquivo " << testFile << " em chargeTestSet.cpp!!!" << endl;
    exit(1);
  } 
}

void ChargeTestSet::closeTestFile(){
  fin.close();
}

//***************************TestSet Section******************************************
void ChargeTestSet::insertTestSet(const int &exampleId, const int &attributeId, const int &attributeValue){
  testSet[exampleId][attributeId] = attributeValue;
}

int ChargeTestSet::getAttributeValueTestSet(const int &exampleId, const int &attributeId){
  return(testSet[exampleId][attributeId]);
}

void ChargeTestSet::printTestSet(){
  int exampleId = 0;
  for(it_testSet = testSet.begin(); it_testSet != testSet.end(); it_testSet++){
	for(it2_testSet = (*it_testSet).begin(); it2_testSet != (*it_testSet).end(); it2_testSet++){
	  cout << *it2_testSet << " ";
	}
	cout << getClassTestSet(exampleId++) << endl;
  }
}
//***************************ClassTestSet Section******************************************
void ChargeTestSet::insertClassTestSet(const int &exampleId, const string &attributeValue){
  classTestSet[exampleId] = attributeValue;
}

string ChargeTestSet::getClassTestSet(const int &exampleId){
  return(classTestSet[exampleId]);
}

void ChargeTestSet::printClassTestSet(){
  for(it_classTestSet = classTestSet.begin(); it_classTestSet != classTestSet.end(); it_classTestSet++){
    cout << *it_classTestSet << endl;
  }
}
//**************************Main Section**************************************************
void ChargeTestSet::getTestSet(){
  string line;
  int i, begin, end, exampleId = 0, attributeId = 0;
  
  openTestFile(); 
  
  //Pulando linhas até o início das linhas de dados...
  while (lowercase(line.substr(0,5)) != "@data") getline(fin, line);
  
  while(getline(fin,line)){//Lendo cada linha do arquivo de entrada ...
    if (line.substr(0,1) == "%" || (int)line.size() == 0) {
      continue;
    }
    i = -1; 
    while (i < (int)line.size()){//Lendo o valor de cada atributo ...
      begin = i;
      if (begin == line.rfind(",")){//Verificando se chegou no último separador da linha ...
        end = line.size();
        insertClassTestSet(exampleId, line.substr(begin+1, end-(begin+1)));//Armazenando em memória o atributo classe ...
      }else{ 
        end = line.find (",", begin+1);
        insertTestSet(exampleId, attributeId, str2int(line.substr(begin+1, end-(begin+1))));//Armazenando em memória os atributos independentes ...
      }
      i = end;
      attributeId++;
    }
    exampleId++;
    attributeId = 0;
  }
  //printTestSet();
  closeTestFile();
}


