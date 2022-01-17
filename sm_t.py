import ast
import numpy as np
import math

def traveling_time(location1, location2, n=20):
    tr_t = 0.0
    location1 = int(location1)
    location2 = int(float(location2))

    # Booth to booth

    tr_t = abs(math.floor((location2 + 1 + 1) / 2) - math.floor((location1 + 1 + 1) / 2))

    return tr_t

print(traveling_time(7,9))
