import random
import itertools

bulls, cows, tries, cow_count, j = 0, 0, 0, 0, 0
correct_number = str(random.randint(0, 9999))
correct_number = correct_number.zfill(4)
num = "0000"
num1, final_num = "", ""


while True:
    print("Give me a number: "+num)
    for i in range(len(correct_number)):
        if num[i] == correct_number[i]:
            cows += 1
        elif num[i] in correct_number:
            bulls += 1
    tries += 1
    if cow_count < 4:
        print(tries)
        num = str(1111 * tries)
        for i in range(cows):
            cow_count += 1
            num1 = num1 + str(tries-1)

    else:
        print(final_num)
        final_list = list(num1)
        final_array = list(itertools.permutations(final_list))
        final_num = final_array[j][0] + final_array[j][1] + final_array[j][2] + final_array[j][3]
        print(final_num)
        j += 1
        num = final_num

    if cows == 4:
        print("You won congratulations!!!")
        print("You had " + str(tries)+" tries")
        print("The number was: " + final_num)
        break
    else:
        print("Cows: " + str(cows))
        print("Bulls: " + str(bulls))
        cows = 0
        bulls = 0