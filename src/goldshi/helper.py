def clamp(n: float, min: float, max: float) -> float:
    if n > max:
        return max
    if n < min:
        return min
    return n
