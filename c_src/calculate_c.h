#ifndef CALCULATE_H
#define CALCULATE_H
#ifdef _WIN32
#define DLL_EXPORT __declspec(dllexport)
#else
#define DLL_EXPORT
#endif

#ifdef __cplusplus
extern "C" {
#endif

DLL_EXPORT float add(float num1, float num2);
DLL_EXPORT float subtract(float num1, float num2);
DLL_EXPORT float multiply(float num1, float num2);
DLL_EXPORT float divide(float num1, float num2);

#ifdef __cplusplus
}
#endif

#endif  // CALCULATE_H
