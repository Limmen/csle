

if __name__ == '__main__':
    data = """0.05859375 -50.24 -47.56 -52.93
0.1171875 -46.40 -45.76 -47.03
0.234375 -46.22 -45.87 -46.57
0.46875 -47.29 -46.90 -47.68
0.9375 -47.02 -45.27 -46.34
1.875 -45.80 -45.27 -46.34
3.75 -45.15 -44.61 -45.69
7.5 -45.31 -44.90 -45.71
15 -45.19 -44.84 -45.54
30 -44.27 -43.14 -45.14"""
    lines = data.split("\n")
    regret = 0
    for i in range(len(lines)):
        components = lines[i].split(" ")
        std = abs(float(components[1])-float(components[2]))
        regret += max(-15.87 - float(components[1]), 0)
        print(f"{(float(components[0])*100)/60} {regret} {regret - std} {regret + std}")
