#include <string>
#include "./GMNB/nbayes.h"

/************************************************************************************
 * 
 *      This file is the intermediary between the GMNB output and the C++ code
 * 
 *      Compile the GMNB output and this file into a shared object file:
 *      
 *      g++ -shared -fPIC -o ./src/nbayes.so ./src/GMNB/*.cpp ./src/call_nbayes.cpp
 * 
 * **********************************************************************************/

extern "C" {

    #define EXPORT __attribute__((visibility("default")))

    EXPORT float call_nbayes(char mlnp, char usf, const char* training_dataset, const char* test_dataset, const char* result_file) {
        
        std::string mlnpStr(1, mlnp);  
        std::string usfStr(1, usf);   

        long double result = nbayes(mlnpStr, usfStr, training_dataset, test_dataset, result_file);
        float floatValue_result = result; 

        return floatValue_result;
    }
}
