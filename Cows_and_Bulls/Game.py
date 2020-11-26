import random
bulls, cows, tries = 0, 0, 0
correct_number = str(random.randint(0, 9999))
correct_number = correct_number.zfill(4)

while True:
    num = str(input("Give me a number: "))
    if len(num) != 4:
        print("Try a 4 digit number")
        pass
    else:
        for i in range(len(correct_number)):
            if num[i] == correct_number[i]:
                cows += 1
            elif num[i] in correct_number:
                bulls += 1
        tries += 1
        if cows == 4:
            print("You won congratulations!!!")
            print("You had "+ str(tries)+" tries")
            break
        else:
            print("Cows: " + str(cows))
            print("Bulls: " + str(bulls))
            cows = 0
            bulls = 0