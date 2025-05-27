from data_loader import load_data, base_dir
from fitting import fit_linear
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def visualise_data(df: pd.DataFrame, beta, intercept) -> None:
    for col in ('I_B', 'I_C', 'u_I_C'):
        if col not in df.columns:
            raise ValueError(f"DataFrame musi zawierać kolumnę '{col}'.")

    x = df['I_B'].to_numpy()
    y = df['I_C'].to_numpy()
    yerr = df['u_I_C'].to_numpy()

    plt.figure(figsize=(8, 6))
    plt.errorbar(x, y, yerr=yerr, fmt='o', markersize=5, alpha=0.8,
                 ecolor='gray', elinewidth=1, capsize=3, label='dane pomiarowe')

    x_line = np.linspace(x.min(), x.max(), 200)
    y_line = beta * x_line + intercept
    plt.plot(x_line, y_line, '-', linewidth=2,
             label=fr'dopasownanie liniowe')

    plt.xlabel(r"$I_B$ [A]")
    plt.ylabel(r"$I_C$ [A]")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    plt.savefig(os.path.join(base_dir(), 'raport/figures', 'beta_plot.pdf'), dpi=300)
    plt.show()

def beta_results_visualisation(df, write_type = 'w'):
    df['I_C'] = df['I_C'] * 10**-3 # przeliczenie na ampery
    df['I_B'] = df['I_B'] * 10**-6 # przeliczenie na ampery
    df['U_B'] = df['U_B'] * 10**-3 # przeliczenie na wolt
    df['u_I_B'] = df['I_B'] * 0.03
    df['u_U_B'] = df['U_B'] * 0.03
    df['u_I_C'] = df['u_U_B'] / 20

    result = fit_linear(df, x_col='I_B', y_col='I_C', y_err_col='u_I_C', intercept0=True)

    visualise_data(df, result['slope'], result['intercept'])

    #znajdowanie napięcie optymalnego punktu pracy (U_CE = 5V)
    E = 10
    U_CE = 5
    R_L = 15000
    I_C_opt = (E - U_CE)/(R_L)

    beta = result['slope']
    I_B_opt = I_C_opt / beta

    R_B = (E - 0.65) / I_B_opt

    with open(os.path.join(base_dir(), 'results.txt'), write_type) as f:
        f.write(f"Beta: {result['slope']:.3f} +- {result['slope_err']:.3f}\n")
        f.write(f"Reduced Chi-squared: {result['reduced_chi2']:.3f}\n")
        f.write(f"U_CE: {U_CE:.2f} V\n")
        f.write(f"I_C w optymalnym punkcie pracy: {I_C_opt*10**3:.3f} mA\n") 
        f.write(f"I_B w optymalnym punkcie pracy: {I_B_opt*10**6:.3f}"+r"$\mu$A"+"\n")
        f.write(f"R_B w optymalnym punkcie pracy: {R_B:.2f} Ohm\n\n")

if __name__ == "__main__":
    df = load_data("data/pom-baza-emiter.csv", skiprows=[1, 2])
    beta_results_visualisation(df, write_type='a')
