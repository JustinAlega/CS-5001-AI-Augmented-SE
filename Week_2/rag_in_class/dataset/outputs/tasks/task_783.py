def rgb_to_hsv(r, g, b):
    """Convert RGB values to HSV.

    Args:
        r: Red component (0-255)
        g: Green component (0-255)
        b: Blue component (0-255)

    Returns:
        tuple: (hue, saturation, value) where:
            - hue is in degrees [0, 360)
            - saturation is in percent [0, 100]
            - value is in percent [0, 100]
    """
    # Normalize RGB values to [0, 1] range
    r_norm = r / 255.0
    g_norm = g / 255.0
    b_norm = b / 255.0

    max_val = max(r_norm, g_norm, b_norm)
    min_val = min(r_norm, g_norm, b_norm)
    delta = max_val - min_val

    # Calculate Hue
    if delta == 0:
        hue = 0
    elif max_val == r_norm:
        hue = (60 * ((g_norm - b_norm) / delta) + 360) % 360
    elif max_val == g_norm:
        hue = (60 * ((b_norm - r_norm) / delta) + 120) % 360
    else:  # max_val == b_norm
        hue = (60 * ((r_norm - g_norm) / delta) + 240) % 360

    # Calculate Saturation
    saturation = 0 if max_val == 0 else (delta / max_val) * 100

    # Calculate Value
    value = max_val * 100

    return hue, saturation, value
