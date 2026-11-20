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
