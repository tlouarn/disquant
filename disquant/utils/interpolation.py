from decimal import Decimal


def linear_interpolation(x1: Decimal, y1: Decimal, x2: Decimal, y2: Decimal, x: Decimal) -> Decimal:
    """
    Linear interpolation between two points implemented using Decimal.

    :param x1: x-axis coordinate of point 1
    :param y1: y-axis coordinate of point 1
    :param x2: x-axis coordinate of point 2
    :param y2: y-axis coordinate of point 2
    :param x: x-axis value to interpolate at
    :return: y-axis interpolated value
    """
    if not x1 <= x <= x2:
        raise ValueError(f"{x=} needs to be in [{x1}, {x2}]")

    w1 = (x2 - x) / (x2 - x1)
    w2 = (x - x1) / (x2 - x1)
    return w1 * y1 + w2 * y2
