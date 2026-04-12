# Survival_analisys
Survival analysis of critically ill patients in 5 medical centres in USA.

## 🇬🇧 Data Preprocessing Steps
The preprocessing pipeline is specifically designed for Survival Analysis and addresses both statistical requirements and clinical domain knowledge.

1. **Dropping irrelevant and future-leaking columns (`aps`, `sps`, `surv2m`, `ca`, `sfdm2`, `avtisst`, etc.):**
   * *Reason:* Columns related to other predictions or containing future data (e.g., surrogate functional disability at month 2, average TISS days 3-25) were removed to prevent **Target Leakage**. In survival analysis, we can only use data available at Day 0.
2. **Cleaning Target Variables (`d.time`, `death`):**
   * *Reason:* Rows with missing survival time or death status were dropped. Additionally, patients with `d.time == 0` were removed because survival models often rely on logarithmic calculations that fail with zero values.
3. **Encoding Categorical Variables (`sex`, `race`):**
   * *Reason:* Machine learning algorithms require numerical input. `sex` was binary-mapped, and `race` was transformed using **One-Hot Encoding** to prevent the model from assuming false ordinal relationships between different races.
4. **Cohort Selection (Filtering for `Colon Cancer`):**
   * *Reason:* The dataset was restricted to patients with Colon Cancer to reduce disease heterogeneity and allow the model to find specific survival patterns for this particular cohort.
5. **Dropping sparse columns (`income`, `ph`, `glucose`):**
   * *Reason:* Columns with over 50% missing data were removed. Imputing such a massive amount of missing data would introduce significant bias and artificial patterns.
6. **Clinical Imputation for Physiological Variables (`alb`, `pafi`, `bun`, etc.):**
   * *Reason:* Missing physiological variables were imputed using standard "normal" clinical baseline values. This addresses the **Missing Not At Random (MNAR)** phenomenon in medicine, where the absence of a lab test usually implies the physician did not suspect any abnormalities.
7. **KNN Imputation for remaining variables (`edu`, `adls`, `adlp`):**
   * *Reason:* For general patient info with fewer missing values, a `KNNImputer` was used. It finds the 5 most similar patients ("medical twins") to accurately estimate the missing values, preserving data variance.
8. **Feature Scaling (`StandardScaler`):**
   * *Reason:* Continuous features were standardized (mean=0, std=1) to ensure all variables are on the same scale. This helps mathematical optimization algorithms converge faster and allows for an objective comparison of feature importances (hazard ratios). Target variables and binary columns were explicitly excluded from scaling.

---

## 🇵🇱 Kroki przetwarzania danych (Preprocessing)
Proces przygotowania danych został zaprojektowany specjalnie pod kątem Analizy Przeżycia, uwzględniając wymogi statystyczne oraz kliniczną wiedzę dziedzinową.

1. **Usunięcie kolumn nieistotnych i powodujących wyciek danych (`aps`, `sps`, `surv2m`, `ca`, `sfdm2`, `avtisst` itp.):**
   * *Uzasadnienie:* Kolumny zawierające prognozy innych modeli lub dane z przyszłości (np. stan niepełnosprawności w 2. miesiącu, średnia interwencji z dni 3-25) usunięto, aby zapobiec **Wyciekowi Danych (Target Leakage)**. W analizie przeżycia możemy bazować wyłącznie na informacjach dostępnych w Dniu 0.
2. **Czyszczenie zmiennych celu (`d.time`, `death`):**
   * *Uzasadnienie:* Usunięto wiersze z brakami w czasie przeżycia lub statusie zgonu. Dodatkowo odfiltrowano pacjentów z `d.time == 0`, ponieważ modele przeżycia często wykorzystują logarytmy, które nie obsługują wartości zerowych.
3. **Kodowanie zmiennych kategorycznych (`sex`, `race`):**
   * *Uzasadnienie:* Modele ML wymagają danych liczbowych. Płeć (`sex`) zmapowano binarnie, a rasę (`race`) zakodowano metodą **One-Hot Encoding**, aby uniknąć błędnego narzucenia modelowi hierarchii (relacji porządkowej) między rasami.
4. **Selekcja kohorty (Filtrowanie `Colon Cancer`):**
   * *Uzasadnienie:* Zbiór ograniczono wyłącznie do pacjentów z rakiem jelita grubego. Zmniejsza to heterogeniczność danych i pozwala modelowi znaleźć wzorce przeżycia specyficzne dla tej grupy.
5. **Usunięcie rzadkich kolumn (`income`, `ph`, `glucose`):**
   * *Uzasadnienie:* Kolumny mające powyżej 50% braków danych usunięto. Próba ich imputacji wygenerowałaby w większości sztuczne dane, co mocno zaburzyłoby wyniki modelu.
6. **Kliniczna imputacja zmiennych fizjologicznych (`alb`, `pafi`, `bun` itp.):**
   * *Uzasadnienie:* Brakujące wyniki badań laboratoryjnych uzupełniono standardowymi wartościami "w normie". Wynika to ze zjawiska **MNAR (Missing Not At Random)** w medycynie – jeśli lekarz nie zlecił danego badania, zazwyczaj oznacza to, że stan pacjenta nie wskazywał na odchylenia od normy.
7. **Imputacja KNN dla pozostałych zmiennych (`edu`, `adls`, `adlp`):**
   * *Uzasadnienie:* W przypadku danych ogólnych z mniejszą ilością braków zastosowano algorytm `KNNImputer`. Szuka on 5 najbardziej podobnych pacjentów ("medycznych sobowtórów"), aby precyzyjnie oszacować brakujące wartości, zachowując naturalną wariancję w danych.
8. **Skalowanie cech (`StandardScaler`):**
   * *Uzasadnienie:* Ciągłe zmienne numeryczne ustandaryzowano (średnia=0, odchylenie=1). Dzięki temu model optymalizuje się znacznie szybciej, a my możemy obiektywnie porównywać wpływ poszczególnych cech na ryzyko zgonu. Zmienne celu oraz zmienne binarne celowo wykluczono ze skalowania.
