score = 0
score += 3
score += 4
print(score)

cross = [[0, 1, 0],
         [1, 1, 1],
         [0, 1, 0]]

x = [[1, 0, 1],
     [0, 1, 0],
     [1, 0, 1]]

score = 0

for i in range(len(cross)):
    for j in range(len(cross[i])):
        score += cross[i][j]*x[i][j]
print(score)

a = 5
b = 1

if a > b:
    print("a가 크다")
elif a < b:
    print("b가 크다")
else:
    print("같다")

a = 5
b = 1   
if a > b:
    print("a가 짱")
elif a < b:
    print("b가 붕어 ")
else: 
    print("같다")

def mac(pattern, filter_):
    score = 0
    for i in range(len(pattern)):
        for j in range(len(pattern[i])):
            score += pattern[i][j] * filter_[i][j]
    return score
pattern = [[0, 1, 0],
           [1, 1, 1],
           [0, 1, 0]]

cross_filter = [[0, 1, 0],
                [1, 1, 1],
                [0, 1, 0]]

x_filter = [[1, 0, 1],
            [0, 1, 0],
            [1, 0, 1]]

score_cross = mac(pattern, cross_filter)
score_x = mac(pattern, x_filter)

print(score_cross)
print(score_x)

if score_cross > score_x:
    print("Cross")
elif score_cross < score_x:
    print("X")
else:
    print("UNDECIDED")

def add(a, b):
    return a + b

c = add(3, 4)
print(c)

line = ("안녕하세요. ")
print(line)

d = {"name": "예시", "size": 3, "expected": "+"}

print(d["name"])
print(d["size"])
print(d["expected"])


case = {"input": [[0, 1, 0],
                  [1, 1, 1],
                  [0, 1, 0]],
        "expected": "+"}

print(case["expected"])
print(case["input"])
print(case["input"][1])
print(case["input"][1][2])

import json

with open("sample.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(data["case1"]["expected"])

case1 = data["case1"]

s_cross = mac(case1["input"], cross_filter)
s_x = mac(case1["input"], x_filter)

print(s_cross)
print(s_x)

label_map = {"+": "Cross", "x": "X"}

expected = label_map[case1["expected"]]

print(case1["expected"])
print(expected)

if s_cross > s_x:
    result = "Cross"
elif s_cross < s_x:
    result = "X"
else:
    result = "UNDECIDED"

if result == expected:
    print("PASS")
else:
    print("FAIL")

for key in data:
    case = data[key]
    s_cross = mac(case["input"], cross_filter)
    s_x = mac(case["input"], x_filter)
    expected = label_map[case["expected"]]

    if s_cross > s_x:
        result = "Cross"
    elif s_cross < s_x:
        result = "X"
    else:
        result = "UNDECIDED"

    if result == expected:
        print(key, "PASS")
    else:
        print(key, "FAIL")