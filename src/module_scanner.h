#ifndef MODULE_SCANNER_H
#define MODULE_SCANNER_H

#include <Python.h>

typedef struct {
    const char *module_name;
    const char *function_name;
    double score;  // optional score for similarity/ranking
} FunctionMatch;

// Callback function type for processing each function
typedef int (*function_processor)(const char *module_name,
                                   const char *function_name,
                                   PyObject *result_list,
                                   void *user_data);

// Iterate through all loaded modules and their functions
// Calls the processor callback for each function found
void scan_all_modules(function_processor processor, void *user_data);

// Helper to create a result dictionary
PyObject* create_match_dict(const char *module_name,
                           const char *function_name,
                           double score);

#endif
