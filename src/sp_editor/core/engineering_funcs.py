def calculate_beta1(f_c):
    """
    Calculate beta1 according to ACI 318-19 specifications.

    Parameters:
    f_c (float): Compressive strength of concrete in psi.

    Returns:
    float: The value of beta1.
    """
    f_c = f_c * 1000

    if f_c <= 4000:
        beta1 = 0.85
    else:
        beta1 = 0.85 - 0.05 * ((f_c - 4000) / 1000)
        if beta1 < 0.65:
            beta1 = 0.65

    return beta1


def calculate_beta1_metric(f_c):
    """
    Calculate beta1 according to ACI 318-19 specifications (metric units).

    Parameters:
    f_c (float): Compressive strength of concrete in MPa.

    Returns:
    float: The value of beta1.
    """
    if f_c <= 27.6:
        beta1 = 0.85
    else:
        beta1 = 0.85 - 0.05 * ((f_c - 27.6) / 6.9)
        if beta1 < 0.65:
            beta1 = 0.65
    return beta1
