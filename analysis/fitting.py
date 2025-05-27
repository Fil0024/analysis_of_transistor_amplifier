import numpy as np
from sklearn.linear_model import LinearRegression
import pandas as pd

def fit_linear(df: pd.DataFrame, x_col, y_col, y_err_col, intercept0 = False) -> dict:
    x = df[x_col].to_numpy()
    y = df[y_col].to_numpy()
    dy = df[y_err_col].to_numpy()

    w = 1.0 / dy**2

    if intercept0:
        X = x.reshape(-1, 1)
    else:
        X = np.column_stack((x, np.ones_like(x)))

    model = LinearRegression(fit_intercept=False)
    model.fit(X, y, sample_weight=w)

    if intercept0:
        a = model.coef_[0]
        b = 0.0
    else:
        a, b = model.coef_

    y_fit = model.predict(X)
    chi2 = np.sum( ( (y - y_fit)**2 ) * w )
    dof = len(x) - 2
    chi2_red = chi2 / dof

    XT_W = X.T * w 
    cov = np.linalg.inv(XT_W.dot(X)) * chi2_red

    sigma_a = np.sqrt(np.diag(cov)[0])
    sigma_b = 0.0 if intercept0 else np.sqrt(np.diag(cov)[1])

    return {
        'slope': a,
        'intercept': b,
        'slope_err': sigma_a,
        'intercept_err': sigma_b,
        'reduced_chi2': chi2_red
    }

