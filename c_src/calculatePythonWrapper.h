#define CALCULATE_H

#include <Python.h>

float add(float num1, float num2);
float subtract(float num1, float num2);
float multiply(float num1, float num2);
float divide(float num1, float num2);
float power(float num1, float power);

PyObject* py_add(PyObject* self, PyObject* args);
PyObject* py_subtract(PyObject* self, PyObject* args);
PyObject* py_multiply(PyObject* self, PyObject* args);
PyObject* py_divide(PyObject* self, PyObject* args);
PyObject* py_power(PyObject* self, PyObject* args);

PyMODINIT_FUNC PyInit_calculator_c(void);
