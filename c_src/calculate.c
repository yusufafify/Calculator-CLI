#include <stdio.h>
#include <math.h>
#include "calculate.h"

double add(double num1, double num2)
{
    return num1 + num2;
}
double subtract(double num1, double num2)
{
    return num1 - num2;
}
double multiply(double num1, double num2)
{
    return num1 * num2;
}
double divide(double num1, double num2)
{
    if (num2 != 0.0)
    {
        return num1 / num2;
    }
    else
    {
        return NAN;
    }
}
