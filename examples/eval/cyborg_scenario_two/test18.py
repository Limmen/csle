if __name__ == '__main__':
    data = """0.05859375 -25.05 -22.03 -28.08
0.1171875 -21.28 -20.556 -22.00
0.234375 -21.08 -20.7 -21.939
0.46875 -18.08 -16.76 -19.41
0.9375 -17.42 -16.34 -18.39
1.875 -14.73 -13.87 -15.8
3.75 -13.46 -12.65 -14.28
7.5 -13.08 -11.41 -14.75
15 -12.98 -11.43 -14.526
30 -13.32 -13.14 -13.50"""
    lines = data.split("\n")
    regret = 0
    for i in range(len(lines)):
        components = lines[i].split(" ")
        std = abs(float(components[1]) - float(components[2]))
        regret += max(-15.87 - float(components[1]), 0)
        mean = float(components[1])
        print(f"{(float(components[0]) * 100) / 60} {float(components[1])} {float(components[2])} {float(components[3])}")
