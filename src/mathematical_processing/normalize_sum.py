def normalize_sum_to_one(a, b, c):
    """
    Normalizes three numbers so that their sum equals to 1 and their proportions remain the same.

    Parameters:
    a (float): First number.
    b (float): Second number.
    c (float): Third number.

    Returns:
    tuple: A tuple containing the normalized values of a, b, and c.
    """
    total = a + b + c
    if total == 0:
        return 0, 0, 0  # Avoid division by zero if the total is 0
    return a / total, b / total, c / total




