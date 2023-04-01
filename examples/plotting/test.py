import math

if __name__ == '__main__':
    v1 = math.factorial(4)/(math.factorial(2)*(math.factorial(4-2)))
    v2 = math.factorial(1000)/(math.factorial(998)*(math.factorial(1000-998)))
    print(v2*v2/(1000000000))