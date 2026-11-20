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
