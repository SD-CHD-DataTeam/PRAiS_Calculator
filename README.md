# PRAiS_Calculator
# PRAiS 2 Model (2009-2015 Calibration)

.

## Model Overview

The model calculates the probability based on 34 parameters. Each parameter has an associated regression coefficient and a condition that determines if it applies.

If a condition is satisfied, the parameter contributes to the prediction using its coefficient; otherwise, it does not.

## Parameters and Coefficients

| No. | Parameter | Coefficient | P-Value |
|:--|:--|:--|:--|
| 1 | Diagnosis grouping 1 | 0.000 | - |
| 2 | Diagnosis grouping 2 | -0.168 | - |
| 3 | Diagnosis grouping 3 | -0.330 | - |
| 4 | Diagnosis grouping 4 | -1.521 | - |
| 5 | Diagnosis grouping 5 | -0.512 | - |
| 6 | Diagnosis grouping 6 | -0.117 | - |
| 7 | Diagnosis grouping 7 | -0.054 | - |
| 8 | Diagnosis grouping 8 | -0.631 | - |
| 9 | Diagnosis grouping 9 | -0.468 | - |
| 10 | Diagnosis grouping 10 | -1.698 | - |
| 11 | Diagnosis grouping 11 | -1.241 | - |
| 12 | Specific procedure grouping 1 | 0.000 | - |
| 13 | Specific procedure grouping 2 | 0.216 | - |
| 14 | Specific procedure grouping 3 | 0.625 | - |
| 15 | Specific procedure grouping 4 | -0.090 | - |
| 16 | Specific procedure grouping 5 | 0.056 | - |
| 17 | Specific procedure grouping 6 | -0.747 | - |
| 18 | Specific procedure grouping 7 | 1.066 | - |
| 19 | Specific procedure grouping 8 | 0.788 | - |
| 20 | Specific procedure grouping 9 | 1.100 | - |
| 21 | Specific procedure grouping 10 | -0.787 | - |
| 22 | Specific procedure grouping 11 | -0.964 | - |
| 23 | Specific procedure grouping 12 | -0.202 | - |
| 24 | Specific procedure grouping 13 | -0.067 | - |
| 25 | Specific procedure grouping 14 | -0.937 | - |
| 26 | Specific procedure grouping 15 | -1.637 | - |
| 27 | Specific procedure grouping 20 (no specific procedure) | 0.428 | - |
| 28 | Bypass procedure | 0.398 | 0.01 |
| 29 | Definite indication of univentricular heart | 0.692 | <0.01 |
| 30 | Additional Cardiac Risk factor | 0.731 | <0.01 |
| 31 | Acquired Comorbidity | 0.538 | <0.01 |
| 32 | Congenital Comorbidity | 0.325 | 0.01 |
| 33 | Severity of Illness Indicator | 0.689 | <0.01 |
| 34 | Procedures from 2013 onwards | -0.280 | <0.01 |

## Special Notes

- For **prospective use**, the "Post 2013" coefficient can be absorbed into the model's constant term.

## Usage

Use the coefficients above, checking if each condition is satisfied for your case. If it is, add the coefficient to the linear predictor.

The probability of death is then calculated by applying the sigmoid (logistic) function to the linear predictor:

```math
p = \frac{1}{1 + e^{-z}}
```

where:
- \( p \) is the probability of death within 30 days
- \( z \) is the sum of the intercept and the relevant coefficients for a patient

## Example

Suppose the sum of the intercept and relevant coefficients (\( z \)) is 0.5, then:

```math
p = \frac{1}{1 + e^{-0.5}} \approx 0.622
```

Thus, the predicted probability of death would be approximately 62.2%.
