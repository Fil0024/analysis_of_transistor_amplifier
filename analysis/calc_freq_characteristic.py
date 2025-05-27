from data_loader import load_data, base_dir
from fitting import fit_linear
import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

def scatter(df: pd.DataFrame, y_line = 0, x_line1 = 0, x_line2 = 0) -> None:
    x = df['Freq'].to_numpy()
    y = (df['Uwy']/df['Uwe']).to_numpy()

    plt.figure(figsize=(8, 6))
    plt.scatter(x, y, label='dane pomiarowe')
    if y_line != 0:
        plt.axhline(y=y_line, color='r', linestyle='--', label=r'$\text{max value}/\sqrt{2}$')
    if x_line1 != 0:
        plt.axvline(x=x_line1, color='g', linestyle='--', label=r'$\omega_{g1} \approx$ '+ str(x_line1))
    if x_line2 != 0:    
        plt.axvline(x=x_line2, color='b', linestyle='--', label=r'$\omega_{g2} \approx$ ' + str(x_line2))
    plt.xscale('log')
    plt.xlabel('Częstotliwość [rad/s]')
    plt.ylabel('Uwy/Uwe [V]') 
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    plt.savefig(os.path.join(base_dir(), 'raport/figures', 'amplifier_freq_characteristic.pdf'), dpi=300)
    plt.show()

def scatter_and_plot(df: pd.DataFrame, x_col: str, y_col: str, y_err_col: str, fit_func) -> None:
    x=0

def find_max_value(df, y_col: str) -> float:
    max_value = df[y_col].max()
    return max_value

def function_low(omega, omega1, A):
    return A*(omega/omega1)/np.sqrt(1 + (omega/omega1)**2)

def function_high(omega, omega2, A):
    return A*1/np.sqrt(1 + (omega/omega2)**2)

def visualize_freq_characteristic(df: pd.DataFrame, omega1: float, omega2: float) -> None:
    x = df['Freq'].to_numpy()
    y = (df['Uwy/Uwe']).to_numpy()
    max_value = find_max_value(df, 'Uwy/Uwe')
    max_idx = df['Uwy/Uwe'].idxmax()
    freq_at_max = df.loc[max_idx, 'Freq']


    omega_grid = np.logspace(np.log10(x.min()), np.log10(x.max()), 500)
    low_curve  = function_low(omega_grid, omega1, A=max_value)
    high_curve = function_high(omega_grid, omega2, A=max_value)

    mask_high = omega_grid >= freq_at_max
    mask_low = omega_grid <= freq_at_max
    plt.figure(figsize=(8, 6))
    plt.scatter(x, y, marker='o', label='dane pomiarowe')
    plt.plot(omega_grid[mask_low], low_curve[mask_low],  linestyle='--', label=f'filtr górno-przepustowy, ω₁={omega1:.1f}')
    plt.plot(omega_grid[mask_high], high_curve[mask_high], linestyle='-.', label=f'filtr dolno-przepustowy, ω₂={omega2:.1f}')

    plt.xscale('log')
    plt.yscale('linear')
    plt.xlabel('Częstotliwość ω [rad/s]')
    plt.ylabel('Wzmocnienie |Uwy/Uwe|')
    plt.grid(True, which='both', ls=':')
    plt.legend()
    plt.tight_layout()

    out_dir = os.path.join(base_dir(), 'raport/figures')
    os.makedirs(out_dir, exist_ok=True)
    plt.savefig(os.path.join(out_dir, 'amplifier_freq_characteristic_plots.pdf'), dpi=300)
    plt.show()

def freq_results_visualisation(df: pd.DataFrame, write_type='a') -> None:
    df['Uwe'] = df['Uwe'] * 10**-3  # przeliczenie na wolt
    df['Uwy/Uwe'] = df['Uwy'] / df['Uwe']
    df['u_Uwe'] = df['Uwe'] * 0.03
    df['u_Uwy'] = df['Uwy'] * 0.03
    df['u_Uwy/Uwe'] = df['Uwy/Uwe']*np.sqrt(df['u_Uwe']**2/df['Uwe']**2 + df['u_Uwy']**2/df['Uwy']**2)

    df['omega'] = 2 * np.pi * df['Freq']

    max_value = find_max_value(df, 'Uwy/Uwe')
    
    omega_g1 = 3 * 10**3 # Odczytane z wykresu
    omega_g2 = 9 * 10**5 #
    u_omega_g1 = 10**3 / np.sqrt(3)  # Odczytane z wykresu
    u_omega_g2 = 10**5 / np.sqrt(3)

    scatter(df, y_line = max_value/np.sqrt(2), 
            x_line1 = omega_g1,
            x_line2 = omega_g2)

    bandwidth = omega_g2 - omega_g1
    u_bandwidth = np.sqrt(u_omega_g1**2 + u_omega_g2**2)

    visualize_freq_characteristic(df, omega_g1, omega_g2)

    with open(os.path.join(base_dir(), 'results.txt'), 'a') as f:
        f.write(f"omega_g1: {omega_g1:.3f} +- {u_omega_g1:.3f} rad/s\n")
        f.write(f"omega_g2: {omega_g2:.3f} +- {u_omega_g2:.3f} rad/s\n")
        f.write(f"pasmo przenoszenia: {bandwidth:.3f} +- {u_bandwidth:.3f} rad/s\n\n")
    
    




if __name__ == "__main__":
    df = load_data("data/pom-428.csv", skiprows=[1])
    freq_results_visualisation(df, write_type='a')