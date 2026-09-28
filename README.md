# Survival_analysis: Project Summary

Comprehensive Survival Analysis of critically ill oncology patients from 5 medical centres in the USA based on the SUPPORT2 dataset.

---

## 🇬🇧 Executive Summary & Methodology

### 1. Data & Preprocessing Pipeline
The preprocessing pipeline is specifically designed for Survival Analysis and addresses both statistical requirements and clinical domain knowledge:
* **Cohort Selection**: Restricted from 9,105 patients to 512 oncology patients diagnosed with **Colon Cancer** to reduce heterogeneity.
* **Target Variables**: Survival time (`d.time` / `d_time`, days from enrollment to event/censoring) and binary event indicator (`death`, $1 = \text{death}$, $0 = \text{right-censored}$). Censoring rate: **16.60%** (85 censored, 427 deaths).
* **Target Leakage Prevention**: Dropped post-baseline and summary predictors (`aps`, `sps`, `surv2m`, `ca`, `sfdm2`, `avtisst`, cost variables, and physician estimates).
* **Missing Data Handling**: Dropped columns with $>50\%$ missingness (`income`, `ph`, `glucose`). Clinical baseline norm imputation was applied to physiological markers (`alb`, `bili`, `wblc`), and **KNN imputation** ($k=5$) was applied to functional and demographic features (`edu`, `adls`, `adlp`).
* **Feature Scaling**: Standardized continuous numerical variables using `StandardScaler` (mean = 0, std = 1), preserving raw binary and temporal columns.

---

### 2. Non-Parametric Survival Analysis
* **Actuarial Life-Table Method**:
  * Evaluated across 180-day (semi-annual) intervals to prevent masking early acute mortality.
  * Identified a major **hazard peak in the first 180 days** ($q_x = 0.4336$, 222 deaths), followed by flattening of the hazard curve after Day 360, reflecting medical stabilization for long-term survivors.
* **Kaplan-Meier Estimation**:
  * **Overall Median Survival Time**: **234 days** (95% CI: [200, 266] days). Mean survival: 460.34 days ($\pm 24.75$).
* **Stratification & Hypothesis Testing (Log-Rank & Wilcoxon)**:
  * **Stable Long-Term Predictors**:
    * **Years of Education (`edu`)**: Highly significant ($p < 0.0001$ for both Log-Rank and Wilcoxon). Higher education ($>12$ years) acts as a strong protective socio-economic factor.
    * **Number of Comorbidities (`num_co_c`)**: Statistically significant ($p = 0.0347$ Log-Rank, $p = 0.0172$ Wilcoxon). Patients with $\ge 2$ comorbidities show significantly worse survival.
  * **Early-Phase Predictors (Wilcoxon significant, Log-Rank non-significant)**:
    * **Age (`age_c`)**: Wilcoxon $p = 0.0108$, Log-Rank $p = 0.1792$. Patients aged $65+$ have significantly worse early survival (Bonferroni pairwise vs $<50$: $p = 0.0194$; vs 50–64: $p = 0.0205$).
    * **Functional Status (`ADL`)**: Wilcoxon $p = 0.0239$, Log-Rank $p = 0.2152$. High functional disability severely impacts early survival.
    * **Neurological State / Coma (`scoma`)**: Wilcoxon $p = 0.0133$, Log-Rank $p = 0.0685$.
    * **Race / Ethnicity**: Wilcoxon $p = 0.0275$, Log-Rank $p = 0.5541$.
    * **Cross-Stratification (`Sex * Age`)**: Wilcoxon $p = 0.0389$, Log-Rank $p = 0.3807$. Oldest male patients ($65+$) exhibit the steepest initial survival drops.
  * **Non-Significant Univariate Factors**:
    * **Sex (`sex`)**: Log-Rank $p = 0.5330$, Wilcoxon $p = 0.2927$.
    * **Diabetes (`diabetes`)**: Log-Rank $p = 0.2799$, Wilcoxon $p = 0.4433$.
    * **Dementia (`dementia`)**: Insufficient positive sample size ($N = 1$).

---

### 3. Semi-Parametric Survival Analysis (Cox Proportional Hazards)
* **Model Reduction & Selection**:
  * Full Ridge Model ($L_2 = 0.1$, 25 features): C-index = 0.6969, AIC = 4608.46.
  * **Final Reduced Model** (6 covariates, unpenalized): C-index = **0.6947**, AIC = **4564.05**, Log-Likelihood = -2276.03.
  * Retained variables: `adls`, `adlp`, `bili`, `edu`, plus clinical control covariates `hrt` and `num.co`. Serum albumin (`alb`) was eliminated due to non-proportionality and lack of predictive contribution in LR test.
* **Final Model Estimates**:
  * `adls` (ADL surrogate): $\text{HR} = 1.3215$ (95% CI: [1.2330, 1.4163], $p < 0.0001$) — Risk factor.
  * `adlp` (ADL patient): $\text{HR} = 1.1794$ (95% CI: [1.0898, 1.2763], $p < 0.0001$) — Risk factor.
  * `bili` (Serum Bilirubin): $\text{HR} = 1.0594$ (95% CI: [1.0304, 1.0892], $p < 0.0001$) — Risk factor / liver compromise.
  * `edu` (Years of Education): $\text{HR} = 0.9304$ (95% CI: [0.9034, 0.9581], $p < 0.0001$) — Protective factor.
  * `num.co` ($p = 0.0897$) and `hrt` ($p = 0.1375$) retained for clinical adjustment.
* **Diagnostics & Time-Varying Effects ($tt$)**:
  * Schoenfeld residual tests revealed non-proportionality for `adls` and `bili` over time.
  * An extended time-interaction model with $\log(t)$ interaction terms (`adls_x_logt`: $\text{HR} = 0.77$, $p < 0.005$; `bili_x_logt`: $\text{HR} = 0.92$, $p < 0.005$) demonstrated significant fit improvement (LR test $\chi^2(2) = 187.80$, $p < 0.0001$, C-index = 0.79).
  * Martingale and Deviance residual analysis confirmed proper functional linear form and validated extreme outliers ($|\text{deviance}| > 3$) as biologically genuine cases.

---

### 4. Parametric Survival Modeling & Bayesian Estimation
* **Baseline Distribution Selection (Null Models)**:
  * Tested Exponential, Weibull, Log-Logistic, Gamma, and Log-Normal.
  * **Log-Normal** ($\text{AIC} = 1788.84$, $\text{BIC} = 1797.32$) and **Gamma** ($\text{AIC} = 1790.27$, $\text{BIC} = 1802.99$) yielded optimal fits on probability plots and criterion values.
* **Multivariate Parametric Models (7 Core Predictors)**:
  * Reduced model features: `edu`, `alb`, `bili`, `adlp`, `adls`, `adlsc`, and `num_co`.
  * Gamma Reduced Model: $\text{AIC} = 1592.26$, $\text{BIC} = 1634.65$.
  * Log-Normal Reduced Model: $\text{AIC} = 1593.87$, $\text{BIC} = 1632.01$.
* **Bayesian Estimation (MCMC / Metropolis-Hastings via PROC LIFEREG)**:
  * Setup: 100,000 iterations, 20,000 burn-in, thinning interval of 10, non-informative Jeffreys priors.
  * Diagnostic convergence confirmed: Heidelberger-Welch passed, Gelman-Rubin $\hat{R} \le 1.0009$, autocorrelation dropped near zero, $\text{MCSE}/\text{SD} < 0.05$.
  * **95% HPD Credible Intervals**:
    * **Prolonging Survival**: Higher education (`edu`), higher albumin (`alb`), positive change in functional status (`adlsc`).
    * **Shortening Survival**: Higher bilirubin (`bili`), poorer baseline activity (`adlp`), poorer pre-admission status (`adls`).
    * **Uncertain Impact**: Comorbidity count (`num_co`) 95% HPD slightly crossed 0 (Log-Normal: $[-0.2823, 0.0706]$; Gamma: $[-0.2951, 0.0534]$).
  * **Model Comparison**: Gamma achieved a slightly better Deviance Information Criterion ($\text{DIC} = 1592.26$) than Log-Normal ($\text{DIC} = 1594.46$).

---

## 🇵🇱 Podsumowanie Wykonawcze i Metodologia

### 1. Przetwarzanie i Czyszczenie Danych (Preprocessing)
Proces przygotowania danych został zaprojektowany specjalnie pod kątem Analizy Przeżycia, uwzględniając wymogi statystyczne oraz kliniczną wiedzę dziedzinową:
* **Selekcja Kohorty**: Zawężenie zbioru z 9105 pacjentów do kohorty 512 osób ze zdiagnozowanym **rakiem jelita grubego (Colon Cancer)** w celu eliminacji heterogeniczności jednostek chorobowych.
* **Zmienne Celu**: Ciągły czas przeżycia (`d.time` / `d_time`, dni od hospitalizacji/kwalifikacji do zdarzenia lub końca obserwacji) oraz binarny status zdarzenia (`death`, $1 = \text{zgon}$, $0 = \text{cenzurowanie prawostronne}$). Odsetek cenzurowania: **16,60%** (85 osób ocenzurowanych, 427 zgonów).
* **Zapobieganie Wyciekowi Danych (Target Leakage)**: Usunięcie zmiennych tworzonych post-factum lub prognozujących zgon (`aps`, `sps`, `surv2m`, `ca`, `sfdm2`, `avtisst`, koszty leczenia, estymacje lekarzy).
* **Obsługa Braków Danych**: Odrzucenie kolumn o brakach $>50\%$ (`income`, `ph`, `glucose`). Imputacja normami klinicznymi dla wskaźników fizjologicznych (`alb`, `bili`, `wblc`) oraz algorytmem **KNN** ($k=5$) dla zmiennych demograficzno-funkcjonalnych (`edu`, `adls`, `adlp`).
* **Standaryzacja Cech**: Zmienne ciągłe przeskalowano za pomocą `StandardScaler` (średnia = 0, std = 1), wykluczając zmienne czasowe oraz kolumny binarne i kategoryczne.

---

### 2. Nieparametryczna Analiza Czasu Przeżycia
* **Metoda Aktuarialna (Tablice Wymieralności)**:
  * Zastosowano interwały półroczne (180 dni) zamiast rocznych, co zapobiegło zatarciu dynamiki zgonów w pierwszych miesiącach.
  * Zidentyfikowano wyraźny **szczyt hazardu w pierwszym półroczu** ($q_x = 0,4336$, 222 zgony), po którym następuje spłaszczenie funkcji hazardu (po 360. dniu), oznaczające stabilizację stanu chorych.
* **Estymacja Kaplana-Meiera**:
  * **Mediana czasu przeżycia w próbie**: **234 dni** (95% CI: [200; 266] dni). Średnia: 460,34 dni ($\pm 24,75$).
* **Stratyfikacja i Testy Jednorodności (Log-Rank i Wilcoxon)**:
  * **Czynniki o Wpływie Stabilnym i Długoterminowym**:
    * **Lata edukacji (`edu`)**: Wysoce istotne ($p < 0,0001$ w teście Log-Rank oraz Wilcoxona). Wykształcenie $>12$ lat silnie wydłuża czas przeżycia (efekt wyższego statusu socjoekonomicznego i świadomości zdrowotnej).
    * **Liczba chorób współistniejących (`num_co_c`)**: Istotne statystycznie ($p = 0,0347$ Log-Rank, $p = 0,0172$ Wilcoxon). Pacjenci z $\ge 2$ chorobami charakteryzują się najgorszym rokowaniem.
  * **Czynniki Różnicujące Głównie we Wczesnej Fazie (Istotny Wilcoxon, Nieistotny Log-Rank)**:
    * **Wiek (`age_c`)**: Wilcoxon $p = 0,0108$, Log-Rank $p = 0,1792$. Pacjenci w wieku $65+$ lat wykazują istotnie gorsze rokowanie tuż po rozpoczęciu leczenia (porównania Bonferroniego z grupą $<50$: $p = 0,0194$; z 50–64: $p = 0,0205$).
    * **Sprawność funkcjonalna (`ADL`)**: Wilcoxon $p = 0,0239$, Log-Rank $p = 0,2152$. Niska samodzielność zwiększa ryzyko wczesnego zgonu.
    * **Stan świadomości (`scoma`)**: Wilcoxon $p = 0,0133$, Log-Rank $p = 0,0685$.
    * **Przynależność etniczna / rasa**: Wilcoxon $p = 0,0275$, Log-Rank $p = 0,5541$.
    * **Stratyfikacja łączna (`Płeć * Wiek`)**: Wilcoxon $p = 0,0389$, Log-Rank $p = 0,3807$. Najkrótszym przeżyciem w początkowej fazie odznaczają się mężczyźni w wieku $65+$.
  * **Czynniki Nieistotne w Analizie Jednowymiarowej**:
    * **Płeć (`sex`)**: Log-Rank $p = 0,5330$, Wilcoxon $p = 0,2927$.
    * **Cukrzyca (`diabetes`)**: Log-Rank $p = 0,2799$, Wilcoxon $p = 0,4433$.
    * **Demencja (`dementia`)**: Zbyt mała liczebność do rzetelnej oceny ($N = 1$).

---

### 3. Semiparametryczny Model Regresji Coxa
* **Selekcja i Redukcja Modelu**:
  * Pełny model grzbietowy ($L_2 = 0,1$, 25 cech): C-index = 0,6969, AIC = 4608,46.
  * **Model Finalny** (6 predyktorów, brak regularyzacji): C-index = **0,6947**, AIC = **4564,05**, Log-Likelihood = -2276,03.
  * Zmienna albuminy (`alb`) została wykluczona ze względu na brak istotności i jednoczesne łamanie założenia proporcjonalności hazardu. Zmienne `hrt` i `num.co` zachowano jako kliniczne zmienne kontrolne.
* **Wyniki Estymacji Modelu Finalnego**:
  * `adls` (status sprawności przed przyjęciem): $\text{HR} = 1,3215$ (95% CI: [1,2330; 1,4163], $p < 0,0001$) — Czynnik ryzyka.
  * `adlp` (aktywność fizyczna pacjenta): $\text{HR} = 1,1794$ (95% CI: [1,0898; 1,2763], $p < 0,0001$) — Czynnik ryzyka.
  * `bili` (stężenie bilirubiny): $\text{HR} = 1,0594$ (95% CI: [1,0304; 1,0892], $p < 0,0001$) — Czynnik ryzyka (wydolność wątroby/przerzuty).
  * `edu` (lata edukacji): $\text{HR} = 0,9304$ (95% CI: [0,9034; 0,9581], $p < 0,0001$) — Czynnik protekcyjny.
  * `num.co` ($p = 0,0897$) oraz `hrt` ($p = 0,1375$) pełnią rolę zmiennych korygujących.
* **Diagnostyka i Interakcje Czasowe ($tt$)**:
  * Reszty Schoenfelda ujawniły naruszenie założenia PH dla zmiennych `adls` oraz `bili`.
  * Wdrożenie modelu z interakcjami czasowymi $\times \log(t)$ (`adls_x_logt`: $\text{HR} = 0,77$; `bili_x_logt`: $\text{HR} = 0,92$) przyniosło istotną poprawę dopasowania (test LR $\chi^2(2) = 187,80$, $p < 0,0001$, C-index = 0,79).
  * Analiza reszt martyngałowych potwierdziła liniową postać funkcyjną predyktorów, a reszty deviance wykazały brak sztucznych anomalii pomiarowych.

---

### 4. Modele Parametryczne i Wnioskowanie Bayesowskie
* **Wybór Rozkładu Bazowego (Modele Puste)**:
  * Porównano rozkłady: wykładniczy, Weibulla, log-logistyczny, gamma i log-normalny.
  * Najlepsze kryteria informacyjne uzyskał rozkład **log-normalny** ($\text{AIC} = 1788,84$, $\text{BIC} = 1797,32$) oraz **gamma** ($\text{AIC} = 1790,27$, $\text{BIC} = 1802,99$).
* **Zredukowane Modele Parametryczne (7 Predyktorów)**:
  * Wspólne zmienne zredukowane: `edu`, `alb`, `bili`, `adlp`, `adls`, `adlsc` oraz `num_co`.
  * Model zredukowany gamma: $\text{AIC} = 1592,26$, $\text{BIC} = 1634,65$.
  * Model zredukowany log-normalny: $\text{AIC} = 1593,87$, $\text{BIC} = 1632,01$.
* **Estymacja Bayesowska (MCMC / Metropolis-Hastings w SAS PROC LIFEREG)**:
  * Parametry: 100 000 iteracji, 20 000 odrzuconych (burn-in), thinning co 10 próbkę, rozkłady a priori Jeffreysa.
  * Testy zbieżności zakończone pomyślnie: Heidelberger-Welch zaliczony, Gelman-Rubin $\hat{R} \le 1,0009$, szybki zanik autokorelacji, błąd symulacji $\text{MCSE}/\text{SD} < 0,05$.
  * **Wnioski na Podstawie Przedziałów 95% HPD**:
    * **Wpływ dodatni (wydłużający życie)**: edukacja (`edu`), stężenie albumin (`alb`), poprawa stanu ADL (`adlsc`).
    * **Wpływ ujemny (skracający życie)**: podwyższona bilirubina (`bili`), gorsza sprawność wyjściowa (`adlp`, `adls`).
    * **Niepewność**: Liczba chorób towarzyszących (`num_co`) objęła zero w przedziale HPD (dla log-normalnego: $[-0,2823; 0,0706]$; dla gamma: $[-0,2951; 0,0534]$).
  * **Kryterium DIC**: Rozkład gamma osiągnął minimalnie lepszy wynik ($\text{DIC} = 1592,26$) niż log-normalny ($\text{DIC} = 1594,46$).

---

## Summary Comparison of Key Prognostic Factors / Zestawienie Czynników

| Feature / Zmienna | Impact on Survival / Wpływ na przeżycie | Classical Status / Nurt Klasyczny | Bayesian Status / Nurt Bayesowski | Clinical Interpretation / Znaczenie kliniczne |
| :--- | :--- | :--- | :--- | :--- |
| **Education (`edu`)** | **Positive** (Lengthens) | Fully significant ($p < 0.0001$) | Significant (95% HPD $> 0$) | Socioeconomic status, health literacy, prompt diagnosis |
| **Bilirubin (`bili`)** | **Negative** (Shortens) | Fully significant ($p < 0.0001$) | Significant (95% HPD $< 0$) | Liver dysfunction, potential liver metastases |
| **ADL Status (`adls`, `adlp`)** | **Negative** (Shortens) | Fully significant ($p < 0.0001$) | Significant (95% HPD $< 0$) | Functional impairment, frailty, advanced disease burden |
| **ADL Change (`adlsc`)** | **Positive** (Lengthens) | Excluded in Cox due to colinearity | Fully significant (95% HPD $> 0$) | Patient resilience and positive response to early care |
| **Albumin (`alb`)** | **Positive** (Lengthens) | Excluded in Cox (broke PH assumption) | Fully significant (95% HPD $> 0$) | Nutritional state, lack of severe systemic inflammation |
| **Comorbidities (`num_co`)** | **Negative** (Shortens) | Significant in KM / control in Cox | High uncertainty (HPD crosses 0) | Multimorbidity burden, competitive mortality causes |
| **Age (`age`)** | **Negative** (Shortens) | Significant in early phase (Wilcoxon) | Mediated by functional status | Correlates with ADL and physiological markers |