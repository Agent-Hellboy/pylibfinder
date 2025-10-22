#include <Python.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

// Calculate Levenshtein distance between two strings
static int levenshtein_distance(const char *s1, const char *s2) {
    int len1 = strlen(s1);
    int len2 = strlen(s2);

    int *d = (int *)malloc((len1 + 1) * (len2 + 1) * sizeof(int));

    for (int i = 0; i <= len1; i++) {
        d[i * (len2 + 1)] = i;
    }
    for (int j = 0; j <= len2; j++) {
        d[j] = j;
    }

    for (int i = 1; i <= len1; i++) {
        for (int j = 1; j <= len2; j++) {
            int cost = (s1[i - 1] == s2[j - 1]) ? 0 : 1;
            int del = d[(i - 1) * (len2 + 1) + j] + 1;
            int ins = d[i * (len2 + 1) + j - 1] + 1;
            int sub = d[(i - 1) * (len2 + 1) + j - 1] + cost;

            int min = del < ins ? del : ins;
            min = min < sub ? min : sub;
            d[i * (len2 + 1) + j] = min;
        }
    }

    int result = d[len1 * (len2 + 1) + len2];
    free(d);
    return result;
}

// Convert camelCase/PascalCase to lowercase with underscores
static char* normalize_name(const char *name) {
    int len = strlen(name);
    char *normalized = (char *)malloc(len * 2 + 1);
    int idx = 0;

    for (int i = 0; i < len; i++) {
        if (isupper(name[i]) && i > 0) {
            normalized[idx++] = '_';
            normalized[idx++] = tolower(name[i]);
        } else {
            normalized[idx++] = tolower(name[i]);
        }
    }
    normalized[idx] = '\0';
    return normalized;
}

// Calculate similarity score (0.0 to 1.0)
static double calculate_similarity(const char *query, const char *func_name) {
    char *normalized_query = normalize_name(query);
    char *normalized_func = normalize_name(func_name);

    int distance = levenshtein_distance(normalized_query, normalized_func);
    int max_len = strlen(normalized_query) > strlen(normalized_func) ?
                  strlen(normalized_query) : strlen(normalized_func);

    // Similarity: 1.0 - (distance / max_length)
    double similarity = 1.0 - ((double)distance / max_len);

    free(normalized_query);
    free(normalized_func);

    return similarity > 0.0 ? similarity : 0.0;
}

// Check if query is contained in func_name (bonus points for substring match)
static int has_substring_match(const char *query, const char *func_name) {
    char *normalized_query = normalize_name(query);
    char *normalized_func = normalize_name(func_name);

    int result = strstr(normalized_func, normalized_query) != NULL ? 1 : 0;

    free(normalized_query);
    free(normalized_func);

    return result;
}

static PyObject* find_similar(PyObject* self, PyObject* args) {
    const char *keyword;
    double threshold = 0.5;

    if (!PyArg_ParseTuple(args, "s|d", &keyword, &threshold)) {
        return NULL;
    }

    PyObject *modules_dict = PyImport_GetModuleDict();
    PyObject *result_list = PyList_New(0);

    Py_ssize_t pos = 0;
    PyObject *key, *value;

    while (PyDict_Next(modules_dict, &pos, &key, &value)) {
        PyObject *dir_result = PyObject_Dir(value);
        if (dir_result == NULL) {
            Py_DECREF(dir_result);
            continue;
        }

        Py_ssize_t len = PyList_Size(dir_result);
        for (Py_ssize_t i = 0; i < len; i++) {
            PyObject *item = PyList_GetItem(dir_result, i);
            const char *function_name = PyUnicode_AsUTF8(item);

            if (function_name == NULL) continue;

            // Calculate similarity
            double similarity = calculate_similarity(keyword, function_name);
            int substring_match = has_substring_match(keyword, function_name);

            // Boost score if substring matches
            if (substring_match) {
                similarity = (similarity + 1.0) / 2.0;
            }

            // Only include if above threshold
            if (similarity >= threshold) {
                PyObject *module_name = PyUnicode_FromString(PyModule_GetName(value));
                PyObject *func_name = PyUnicode_FromString(function_name);
                PyObject *similarity_score = PyFloat_FromDouble(similarity);

                PyObject *dict_item = PyDict_New();
                PyDict_SetItemString(dict_item, "Module", module_name);
                PyDict_SetItemString(dict_item, "Function", func_name);
                PyDict_SetItemString(dict_item, "Similarity", similarity_score);

                PyList_Append(result_list, dict_item);

                Py_DECREF(module_name);
                Py_DECREF(func_name);
                Py_DECREF(similarity_score);
                Py_DECREF(dict_item);
            }
        }
        Py_DECREF(dir_result);
    }

    return result_list;
}

static PyMethodDef module_methods[] = {
    {"find_similar", find_similar, METH_VARARGS, "Find similar functions in Python stdlib by semantic similarity."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef module_definition = {
    PyModuleDef_HEAD_INIT,
    "similarity_finder",
    "A lib to find similar functions in Python stdlib using semantic similarity",
    -1,
    module_methods
};

PyMODINIT_FUNC PyInit_similarity_finder(void) {
    return PyModule_Create(&module_definition);
}
