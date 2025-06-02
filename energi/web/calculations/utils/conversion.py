def joule_to_kwh(value: float) -> float:
    # 1 kwh = 1000 wh = 1000 j/s*h = 1000 j/s * 3600 s = 3.6e6 j
    return value / 3.6e6
