#include <stdio.h>
#include "calculate.h"
#include <math.h>
int main()
{
    char operator;
    float first_nb, second_nb, answer;

    printf("Enter the Operator (+, -, *, /): ");
    scanf(" %c", &operator);

    printf("Enter First Number: ");
    scanf("%f", &first_nb);

    printf("Enter Second Number: ");
    scanf("%f", &second_nb);
    switch (operator)
    {
    case '+':
        answer = add(first_nb, second_nb);
        printf("%.2f + %.2f = %.2f\n", first_nb, second_nb, answer);
        break;
    case '-':
        answer = subtract(first_nb, second_nb);
        printf("%.2f - %.2f = %.2f\n", first_nb, second_nb, answer);
        break;
    case '*':
        answer = multiply(first_nb, second_nb);
        printf("%.2f * %.2f = %.2f\n", first_nb, second_nb, answer);
        break;
    case '/':
        answer = divide(first_nb, second_nb);
        if (isnan(answer))
            printf("Error! Division by zero");
        else
            printf("%.2f / %.2f = %.2f\n", first_nb, second_nb, answer);
        break;
    default:
        printf("Invalid Operator\n");
        break;
    }

    return 0;
}