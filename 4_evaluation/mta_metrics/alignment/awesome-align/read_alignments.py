import sys

src_file = open(sys.argv[1], "r")
trg_file = open(sys.argv[2], "r")
align_file = open(sys.argv[3], "r")

src, trg = [], []
for l1, l2 in zip(src_file, trg_file):
    src.append(l1.strip().split())
    trg.append(l2.strip().split())

alignments = []
for line in align_file:
    line = line.strip().split()
    align = []
    for pair in line:
        align.append(tuple(map(int, pair.split('-'))))
    alignments.append(sorted(align))

src_file.close()
trg_file.close()
align_file.close()

# Generate word-word from the align file
f = open("token-token.align", "w")
for i in range(len(alignments)):
    for pair in alignments[i]:
        f.write("{} - {}\t".format(src[i][pair[0]], trg[i][pair[1]]))
    f.write("\n")

f.close()
