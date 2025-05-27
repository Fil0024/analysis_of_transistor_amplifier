from data_loader import load_data
from calc_beta import beta_results_visualisation
from calc_k import k_results_visualisation
from calc_freq_characteristic import freq_results_visualisation

if __name__ == "__main__":
    df_beta = load_data("data/pom-baza-emiter.csv", skiprows=[1, 2])
    beta_results_visualisation(df_beta, write_type='w')

    df_k = load_data("data/pom-425.csv" , skiprows=[1])
    k_results_visualisation(df_k, write_type='a')

    df_freq = load_data("data/pom-428.csv", skiprows=[1])
    freq_results_visualisation(df_freq, write_type='a')