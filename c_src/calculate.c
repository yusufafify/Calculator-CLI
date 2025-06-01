#include <stdio.h>
#include <math.h>
#include "calculate.h"

float add(float num1, float num2)
{
    return num1 + num2;
}
float subtract(float num1, float num2)
{
    return num1 - num2;
}
float multiply(float num1, float num2)
{
    return num1 * num2;
}
float divide(float num1, float num2)
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
