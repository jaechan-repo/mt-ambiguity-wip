import sys

def main():

    f1, f2, f3 = sys.argv[1], sys.argv[2], sys.argv[3]

    f = open(f1, "r")
    sources, targets = [], []

    for line in f:
        try:
            src, tgt = line.strip().split('|||')
        except:
            print("Weird: {}".format(line.strip()))
            src, tgt = "-----------------", "-----------------"

        sources.append(src)
        targets.append(tgt)

    f.close()
    g = open(f2, "w")
    h = open(f3, "w")

    for x, y in zip(sources, targets):
        g.write(x.strip() + "\n")
        h.write(y.strip() + "\n")

    g.close()
    h.close()

if __name__ == "__main__":
    main()
