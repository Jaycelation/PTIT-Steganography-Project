from __future__ import annotations

import math


def estimated_vlc_size(coef: float) -> int:
    mag = abs(int(round(coef)))
    if mag == 0:
        return 1
    return 1 + int(math.floor(math.log2(mag + 1)))

