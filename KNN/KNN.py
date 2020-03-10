
def dist(p1, p2):
    return ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2) ** .5


def KNN(points, k, p):

    distances = []
    finalcount = 0
    finaldist = 0
    for i in points:
        distances.append([dist(p, i), i[2]])
    # print(distances)
    distances.sort()

    for l in range(k):
        tyarr[distances[l][1]][0] += 1
        tyarr[distances[l][1]][1] += distances[l][0]
    # print(tyarr)
    for n in range(types):
        if tyarr[n][0] > finalcount:
            final = n
            finalcount = tyarr[n][0]
            finaldist = tyarr[n][1]
        elif tyarr[n][0] == finalcount:
            if tyarr[n][1] < finaldist:
                final = n
                finalcount = tyarr[n][0]
                finaldist = tyarr[n][1]
    return final


if __name__ == '__main__':
    points = []
    yn = input('Do you want to provide the points?(y/n) ')

    if yn == 'y':
        types = int(input('How many types do you want? '))
        ipoints = input().split()
        for i in ipoints:
            if int(i[2]) <= types - 1:
                points.append(list(map(int, i)))
    else:
        types = 2
        points = [[1, 2, 0], [3, 4, 0], [9, 8, 0], [6, 7, 0], [3, 3, 0], [6, 6, 1], [2, 4, 1], [4, 9, 1], [0, 8, 1],
                  [7, 0, 1]]

    tyarr = [[0, 0] for i in range(types)]
    k = int(input('choose a k '))
    c = input('put the poits x and y ').split()
    p = [int(x) for x in c]

    print(KNN(points, k, p))
