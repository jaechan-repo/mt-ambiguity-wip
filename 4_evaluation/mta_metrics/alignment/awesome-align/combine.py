import sys

def main():

    f1, f2, f3 = sys.argv[1], sys.argv[2], sys.argv[3]

    combined_files = []

    f = open(f1, "r")
    g = open(f2, "r")
    index = 0

    for line1, line2 in zip(f, g):

        if line2.strip() == '':
            tgt = "---------------------"
        else:
            tgt = line2.strip()

        if line1.strip() == '':
            src = "---------------------"
        else:
            src = line1.strip()

        combined_files.append(src + " ||| " + tgt)
        index += 1

    f.close()
    g.close()

    h = open(f3, "w")

    for x in combined_files:
        h.write(x + "\n")

    h.close()

if __name__ == "__main__":
    main()
