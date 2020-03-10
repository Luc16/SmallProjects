import random


def dist(p1, p2):
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2) ** .5


points = [[2, 5, 0], [5, 3, 0], [8, 5, 0], [10, 7, 0], [14, 8, 0], [16, 6, 0], [19, 12, 0], [3, 7, 0], [6, 9, 0],
          [9, 3, 0], [12, 11, 0], [15, 12, 0], [18, 11, 0], [20, 6, 0]]
k = int(input('input k '))

c = []
c_sum = []
final =[]
distances = []
for j in range(k):
    a = random.randint(0, 13)
    c.append([points[a][0], points[a][1]])
    c_sum.append([0, 0, 0])
while True:
    for i in range(len(points)):
        distances = [[dist(c[x], points[i]), x] for x in range(k)]
        distances.sort()
        points[i][2] = distances[0][1]
        c_sum[distances[0][1]][0] += points[i][0]
        c_sum[distances[0][1]][1] += points[i][1]
        c_sum[distances[0][1]][2] += 1

    for x in range(k):
        if c_sum[x][2]:
            if dist(c[x], [c_sum[x][0] / c_sum[x][2], c_sum[x][1] / c_sum[x][2]]) < 1.5:
                final.append(1)
            else:
                final.append(0)
        else:
            c[x] = [random.random() * 25, random.random() * 15]
    if sum(final) == k:
        break
    del final[:]
    for m in range(k):
        if c_sum[m][2]:
            c[m] = [c_sum[m][0]/c_sum[m][2], c_sum[m][1]/c_sum[m][2]]
        c_sum[m] = [0, 0, 0]

for i in range(k):
    print(c[i][0], c[i][1])
for i in points:
    print(i[0], i[1], i[2])




