from data_loader import load_data, base_dir
from fitting import fit_linear
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

def scatter_Uwe_Uwy(df: pd.DataFrame) -> None:
    for col in ('U_wej', 'U_wyj'):
        if col not in df.columns:
            raise ValueError(f"DataFrame musi zawierać kolumnę '{col}'.")

    x = df['U_wej'].to_numpy()
    y = df['U_wyj'].to_numpy()

    plt.figure(figsize=(8, 6))
    plt.scatter(x, y, label='dane pomiarowe')
    plt.xlabel(r"$U_{we}$ [V]")
    plt.ylabel(r"$U_{wy}$ [V]")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    plt.savefig(os.path.join(base_dir(), 'raport/figures', 'amplifier_scatter.pdf'), dpi=300)
    plt.show()

def visualise_425(df: pd.DataFrame, k, intercept) -> None:
    for col in ('U_wej', 'U_wyj', 'u_U_wyj'):
        if col not in df.columns:
            raise ValueError(f"DataFrame musi zawierać kolumnę '{col}'.")

    x = df['U_wej'].to_numpy()
    y = df['U_wyj'].to_numpy()
    yerr = df['u_U_wyj'].to_numpy()

    plt.figure(figsize=(8, 6))
    plt.errorbar(x, y, yerr=yerr, fmt='o', markersize=5, alpha=0.8,
                 ecolor='gray', elinewidth=1, capsize=3, label='dane pomiarowe')

    x_line = np.linspace(x.min(), x.max(), 200)
    y_line = k * x_line + intercept
    plt.plot(x_line, y_line, '-', linewidth=2,
             label=fr'dopasownanie liniowe')

    plt.xlabel(r"$U_we$ [V]")
    plt.ylabel(r"$U_wy$ [V]")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    plt.savefig(os.path.join(base_dir(), 'raport/figures', 'k_plot.pdf'), dpi=300)
    plt.show()

def k_results_visualisation(df: pd.DataFrame, write_type = 'a'):
    df['U_wej'] = df['U_wej'] * 10**-3
    df['u_U_wyj'] = df['U_wyj'] * 0.03
    scatter_Uwe_Uwy(df)

    df = df[df['U_wej'] < 0.15]

    results = fit_linear(df, x_col='U_wej', y_col='U_wyj', y_err_col='u_U_wyj', intercept0 = True)

    with open(os.path.join(base_dir(), 'results.txt'), 'a') as f:
        f.write(f"k: {results['slope']:.3f} +- {results['slope_err']:.3f}\n")
        f.write(f"Reduced Chi-squared: {results['reduced_chi2']:.3f}\n\n")

    visualise_425(df, results['slope'], results['intercept'])



if __name__ == "__main__":
    df = load_data("data/pom-425.csv" , skiprows=[1])
    k_results_visualisation(df, write_type='w')