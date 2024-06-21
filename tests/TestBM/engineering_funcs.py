def calculate_beta_ACI_imperial(f_c_psi):
    """
    Calculate the beta (β₁) factor based on ACI 318-19 for imperial units.

    Args:
        f_c_psi (float): Concrete compressive strength in psi.

    Returns:
        float: The beta (β₁) factor.
    """
    if f_c_psi <= 4000:
        beta = 0.85
    else:
        beta = 0.85 - 0.05 * ((f_c_psi - 4000) / 1000)
        if beta < 0.65:
            beta = 0.65
    return beta

def calculate_beta_ACI_metric(f_c: float) -> float:
    
def calculate_beta_ACI_metric(f_c: float) -> float:
    """
    Calculate the beta (β₁) factor based on ACI 318-19.

    Args:
        f_c (float): Concrete compressive strength in MPa.

    Returns:
        float: The beta (β₁) factor.
    """
    if f_c <= 28:
        return 0.85
    else:
        beta = 0.85 - 0.05 * ((f_c - 28) / 7)
        return max(beta, 0.65)