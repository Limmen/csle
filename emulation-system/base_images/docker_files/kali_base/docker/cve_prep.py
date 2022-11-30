import pickle


def cves():
    cves = []
    with open('/allitems.csv', 'rb') as f:
        for line in f:
            cves.append(line.decode("ISO-8859-1").split(",")[0])
    with open('/allitems_prep.csv', 'w') as f:
        for item in cves:
            f.write("%s\n" % item)
    with open('/allitems_prep.pickle', 'wb') as f:
        pickle.dump(cves, f)


if __name__ == '__main__':
    cves()
