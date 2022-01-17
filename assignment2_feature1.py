import math
import numpy as np

def reo_eas (pref_ls):
    return sorted(pref_ls)


def sort_preference(preference_list):
    n = 20
    dist = lambda booth_id: traveling_time("Library", booth_id + 1, n)
    preference_list = sorted(preference_list, key=dist)
    return preference_list

def traveling_time(location1, location2, n):
    if str(location2) == "Library":
        return math.floor((location1+1)/2)
    elif str(location2) == "SC":
        return math.floor((n-location1+2)/2)
    if str(location1) == "Library":
        return math.floor((location2+1)/2)
    elif str(location1) == "SC":
        return math.floor((n-location2+2)/2)
    else:
        return abs(math.floor((location1+1)/2)-math.floor((location2+1)/2))


rng = np.random.default_rng()
a = rng.choice(20, size=10, replace=False)

print(a)

sum_d = 0
for i,e in enumerate(sort_preference(a)):
    if i == len(a)-1:
        break
    sum_d += traveling_time(a[i], a[i+1], 20)
print(sum_d)

sum_d = 0
for i,e in enumerate(reo_eas(a)):
    if i == len(a)-1:
        break
    sum_d += traveling_time(a[i], a[i+1], 20)
print(sum_d)

# print(traveling_time(11,15, 20))
# print(traveling_time(11,14, 20))


print(sort_preference(a))
print(reo_eas(a))

print()