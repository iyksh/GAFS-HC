#include"classifier.h"
#include <stdio.h>

using namespace std;

long double nbayes(string mlnp, string usf, string trainingFile, string testFile, string resultFile){
  try
  {
	
	unsigned int numberOfAttributes;
	unsigned int numberOfTrainingExamples;
	unsigned int numberOfTestExamples;
	bool mandatoryLeafNodePrediction = false, usefulness = false;
	long double result;

	if (mlnp == "y") mandatoryLeafNodePrediction = true;
	if (usf == "y") usefulness = true;

	getDatasetsProfile(trainingFile, testFile, numberOfTrainingExamples, numberOfTestExamples,numberOfAttributes);

	ChargeTrainingSet *CTR;
	CTR = new ChargeTrainingSet(trainingFile,numberOfAttributes,numberOfTrainingExamples, mandatoryLeafNodePrediction);
	CTR->getTrainingSet();

	ChargeTestSet *CTE;
	CTE = new ChargeTestSet(testFile,numberOfTestExamples,numberOfAttributes);
	CTE->getTestSet();

	Classifier *CL;
	CL = new Classifier(numberOfTrainingExamples, numberOfTestExamples, numberOfAttributes, resultFile, usefulness);
	Classifier::auxCLCTR = CTR;
	Classifier::auxCLCTE = CTE;
	result = CL->applyClassifier();


	delete CL;
	delete CTE;
	delete CTR;
	return result;
	
  }
  catch(const std::exception& e)
  {
	std::cout << "Error: " << e.what() << ", returning -1" << std::endl;
	return -1;
  }
  


}

