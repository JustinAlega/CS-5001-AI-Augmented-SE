def parabola_vertex(a, b, c):
    """Calculate the vertex of a parabola given coefficients a, b, and c.

    Args:
        a: Coefficient of x^2 term (must not be zero)
        b: Coefficient of x term
        c: Constant term

    Returns:
        tuple: (x, y) coordinates of the parabola's vertex
    """
    x = -b / (2 * a)
    y = (4 * a * c - b ** 2) / (4 * a)
    return (x, y)
