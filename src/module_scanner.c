#include "module_scanner.h"
#include <string.h>

void scan_all_modules(function_processor processor, void *user_data) {
    PyObject *modules_dict = PyImport_GetModuleDict();

    Py_ssize_t pos = 0;
    PyObject *key, *value;

    while (PyDict_Next(modules_dict, &pos, &key, &value)) {
        PyObject *dir_result = PyObject_Dir(value);
        if (dir_result == NULL) {
            continue;
        }

        Py_ssize_t len = PyList_Size(dir_result);
        for (Py_ssize_t i = 0; i < len; i++) {
            PyObject *item = PyList_GetItem(dir_result, i);
            const char *function_name = PyUnicode_AsUTF8(item);

            if (function_name == NULL) continue;

            const char *module_name = PyModule_GetName(value);
            if (module_name == NULL) continue;

            // Call the processor callback with user_data as the result_list
            processor(module_name, function_name, (PyObject *)user_data, NULL);
        }
        Py_DECREF(dir_result);
    }
}

PyObject* create_match_dict(const char *module_name,
                           const char *function_name,
                           double score) {
    PyObject *dict_item = PyDict_New();
    if (!dict_item) return NULL;

    PyObject *mod_obj = PyUnicode_FromString(module_name);
    PyObject *func_obj = PyUnicode_FromString(function_name);
    PyObject *score_obj = PyFloat_FromDouble(score);

    if (!mod_obj || !func_obj || !score_obj) {
        Py_XDECREF(dict_item);
        Py_XDECREF(mod_obj);
        Py_XDECREF(func_obj);
        Py_XDECREF(score_obj);
        return NULL;
    }

    PyDict_SetItemString(dict_item, "Module", mod_obj);
    PyDict_SetItemString(dict_item, "Object Name", func_obj);
    if (score > 0) {
        PyDict_SetItemString(dict_item, "Score", score_obj);
    }

    Py_DECREF(mod_obj);
    Py_DECREF(func_obj);
    Py_DECREF(score_obj);

    return dict_item;
}

// Helper to determine object type string
const char* get_object_type(PyObject *item) {
    if (PyType_Check(item)) {
        return "Class";
    }
    if (PyCFunction_Check(item)) {
        return "Builtin";
    }
    if (PyFunction_Check(item)) {
        return "Function";
    }
    if (PyMethod_Check(item)) {
        return "Method";
    }
    if (PyCallable_Check(item)) {
        return "Callable";
    }
    return "Unknown";
}

// Helper to create a result dictionary with type information
PyObject* create_match_dict_with_type(const char *module_name,
                                      const char *function_name,
                                      double score,
                                      int is_type) {
    PyObject *dict_item = create_match_dict(module_name, function_name, score);
    if (!dict_item) return NULL;

    PyObject *type_obj = is_type ? Py_True : Py_False;
    PyDict_SetItemString(dict_item, "is_type", type_obj);

    return dict_item;
}

// New function to create result dict with object type
PyObject* create_match_dict_with_object_type(const char *module_name,
                                             const char *function_name,
                                             double score,
                                             const char *object_type) {
    PyObject *dict_item = create_match_dict(module_name, function_name, score);
    if (!dict_item) return NULL;

    PyObject *type_str = PyUnicode_FromString(object_type);
    if (type_str) {
        PyDict_SetItemString(dict_item, "Type", type_str);
        Py_DECREF(type_str);
    }

    return dict_item;
}
