#include "calculate_c.h"
#ifndef EXCLUDE_PYTHON_CODE
#include "calculatePythonWrapper.h"
#endif  // EXCLUDE_PYTHON_CODE
#include <math.h>
#include <stdio.h>

float add(float num1, float num2) { return num1 + num2; }
float subtract(float num1, float num2) { return num1 - num2; }
float multiply(float num1, float num2) { return num1 * num2; }
float divide(float num1, float num2) {
  if (num2 != 0.0) {
    return num1 / num2;
  } else {
    fprintf(stderr, "Error: Division by zero\n");

    return NAN;
  }
}

#ifndef EXCLUDE_PYTHON_CODE
/* Python wrapper functions */

PyObject* py_add(PyObject* self, PyObject* args) {
  double a, b;
  if (!PyArg_ParseTuple(args, "dd", &a, &b)) {
    return NULL;
  }
  return PyFloat_FromDouble(add(a, b));
}

PyObject* py_subtract(PyObject* self, PyObject* args) {
  double a, b;
  if (!PyArg_ParseTuple(args, "dd", &a, &b)) {
    return NULL;
  }
  return PyFloat_FromDouble(subtract(a, b));
}

PyObject* py_multiply(PyObject* self, PyObject* args) {
  double a, b;
  if (!PyArg_ParseTuple(args, "dd", &a, &b)) {
    return NULL;
  }
  return PyFloat_FromDouble(multiply(a, b));
}

PyObject* py_divide(PyObject* self, PyObject* args) {
  double a, b;
  if (!PyArg_ParseTuple(args, "dd", &a, &b)) {
    return NULL;
  }
  if (b == 0.0) {
    PyErr_SetString(PyExc_ZeroDivisionError, "Division by zero");
    return NULL;
  }
  return PyFloat_FromDouble(divide(a, b));
}

// Method definitions
static PyMethodDef calculator_methods[] = {
    {"add", py_add, METH_VARARGS, "Add two numbers"},
    {"subtract", py_subtract, METH_VARARGS, "Subtract two numbers"},
    {"multiply", py_multiply, METH_VARARGS, "Multiply two numbers"},
    {"divide", py_divide, METH_VARARGS, "Divide two numbers"},
    {NULL, NULL, 0, NULL}};

// Module definition
static struct PyModuleDef calculator_module = {
    PyModuleDef_HEAD_INIT, "calculator_c",
    "A simple calculator implemented in C", -1, calculator_methods};

// Module initialization
PyMODINIT_FUNC PyInit_calculator_c(void) {
  return PyModule_Create(&calculator_module);
}

#endif  // EXCLUDE_PYTHON_CODE