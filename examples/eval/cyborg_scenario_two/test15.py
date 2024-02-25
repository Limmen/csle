

if __name__ == '__main__':
    bline = """0.05859375 -6.87 -6.66 -7.07
0.1171875 -6.31 -6.19 -6.52
0.234375 -6.13 -5.55 -6.72
0.46875 -5.32 -5.08 -5.57
0.9375 -5.27 -4.62 -5.9
1.875 -5.45 -5.29 -5.62
3.75 -5.11 -4.79 -5.44
7.5 -5.16 -4.45 -5.86
15 -5.18 -4.52 -5.73
30 -4.50 -4.33 -4.67"""
    meander = """0.05859375 -9.50 -9.31 -9.69
0.1171875 -8.70 -8.63 -8.77
0.234375 -8.42 -8.29 -8.54
0.46875 -8.28 -8.15 -8.40
0.9375 -7.68 -7.58 -7.77
1.875 -7.64 -7.52 -7.76
3.75 -7.58 -7.53 -7.64
7.5 -7.32 -7.04 -7.59
15 -7.30 -6.92 -7.68
30 -6.92 -6.32 -7.49"""
    bline_lines = bline.split("\n")
    meander_lines = meander.split("\n")
    for i in range(len(bline_lines)):
        bline_components = bline_lines[i].split(" ")
        meander_components = meander_lines[i].split(" ")
        mean = float(bline_components[1])*0.5 + float(meander_components[1])*0.5
        std = max(abs(float(bline_components[1])-float(bline_components[2])), abs(float(meander_components[1])-float(meander_components[2])))
        print(f"{float(bline_components[0])} {mean} {mean-std} {mean+std}")
