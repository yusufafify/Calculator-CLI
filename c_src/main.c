/**
 * @file main.c
 * @brief Command-line calculator demonstrating basic arithmetic operations.
 */

#include <math.h>
#include <stdio.h>

#include "calculate.h"

int main(void) {
  char operator_char = '\0';
  float first_nb = 0.0f;
  float second_nb = 0.0f;
  float answer = NAN;

  printf("Enter the operator (+, -, *, /): ");
  if (scanf(" %c", &operator_char) != 1) {
    fprintf(stderr, "Invalid operator input\n");
    return 1;
  }

  printf("Enter first number: ");
  if (scanf("%f", &first_nb) != 1) {
    fprintf(stderr, "Invalid number input\n");
    return 1;
  }

  printf("Enter second number: ");
  if (scanf("%f", &second_nb) != 1) {
    fprintf(stderr, "Invalid number input\n");
    return 1;
  }

  switch (operator_char) {
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
      if (isnan(answer)) {
        printf("Error! Division by zero\n");
      } else {
        printf("%.2f / %.2f = %.2f\n", first_nb, second_nb, answer);
      }
      break;
    default:
      printf("Invalid operator\n");
      return 1;
  }

  return 0;
}
