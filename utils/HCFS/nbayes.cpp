#include"classifier.h"

using namespace std;
/*
void helpOptions(){
	cout << "nbayes -mlnp=[Mandatory leaf node prediction] -usf=[Usefulness] -trainingFile=[Name of training file] -testFile=[Name of test file] -resultFile=[Name of result file]" << endl;
	cout << "Options:" << endl;
	cout << "\t[Mandatory leaf node prediction] = y (for Yes) or n (for No) -- Default = n" << endl;
	cout << "\t[Usefulness] = y (for Yes) or n (for No) -- Default = n" << endl;
	cout << "\t[Name of training file] = string without space." << endl;
	cout << "\t[Name of test file] = string without space." << endl;
	cout << "\t[Name of result file] = string without space." << endl;
	cout << "\t[Name of dependency network file] = string without space." << endl;
}
*/

long double nbayes(string mlnp, string usf, string trainingFile, string testFile, string resultFile){

  //string depNetFile;
  unsigned int numberOfAttributes;
  unsigned int numberOfTrainingExamples;
  unsigned int numberOfTestExamples;
  bool mandatoryLeafNodePrediction = false, usefulness = false;
  long double result;

/*
  for (short i = 1; i < argc; i++){
		paramName = getParamName(argv[i]);
		if(paramName == "mlnp"){
			mlnp = getParamValue(argv[i]);
		}else if(paramName == "usf"){
			usf = getParamValue(argv[i]);
		}else if(paramName == "testFile"){
			testFile = getParamValue(argv[i]);
		}else if(paramName == "trainingFile"){
			trainingFile = getParamValue(argv[i]);
		}else if(paramName == "resultFile"){
			resultFile = getParamValue(argv[i]);
		}else if(paramName == "help"){
			helpOptions();
			return(1);
		}else{
			cout << "Parameter(s) not found!!!" << endl << endl;
			helpOptions();
			return(1);
		}
	}

	if (argc < 2){
		cout << "For help type: depnet -help" << endl;
		return(1);
	}
*/
	if (mlnp == "y") mandatoryLeafNodePrediction = true;
	if (usf == "y") usefulness = true;

	getDatasetsProfile(trainingFile, testFile, numberOfTrainingExamples, numberOfTestExamples,numberOfAttributes);

	//printParam(trainingFile, testFile, resultFile, numberOfTrainingExamples, numberOfTestExamples,numberOfAttributes, mlnp, usf);

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

  //return(0);
}

