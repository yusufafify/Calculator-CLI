#include <math.h>
#include <stdio.h>

#include "../c_src/calculate.h"
#include "Unity/unity.h"
void setUp(void) {}
void tearDown(void) {}

void test_add(void) {
  TEST_ASSERT_EQUAL_FLOAT(5.00, add(2.00, 3.00));
  TEST_ASSERT_EQUAL_FLOAT(-1.0, add(-2.0, 1.0));
  TEST_ASSERT_EQUAL_FLOAT(0.0, add(0.0, 0.0));
}
void test_subtract(void) {
  TEST_ASSERT_EQUAL_FLOAT(-1.0, subtract(2.0, 3.0));
  TEST_ASSERT_EQUAL_FLOAT(-3.0, subtract(-2.0, 1.0));
  TEST_ASSERT_EQUAL_FLOAT(0.0, subtract(0.0, 0.0));
}
void test_multiply(void) {
  TEST_ASSERT_EQUAL_FLOAT(6.0, multiply(2.0, 3.0));
  TEST_ASSERT_EQUAL_FLOAT(-2.0, multiply(-2.0, 1.0));
  TEST_ASSERT_EQUAL_FLOAT(0.0, multiply(0.0, 5.0));
}
void test_divide(void) {
  TEST_ASSERT_EQUAL_FLOAT(2.0, divide(6.0, 3.0));
  TEST_ASSERT_EQUAL_FLOAT(-2.0, divide(-4.0, 2.0));
  TEST_ASSERT_TRUE(isnan(divide(5.0, 0.0)));
}

int main(void) {
  UNITY_BEGIN();
  RUN_TEST(test_add);
  RUN_TEST(test_subtract);
  RUN_TEST(test_multiply);
  RUN_TEST(test_divide);
  return UNITY_END();
}