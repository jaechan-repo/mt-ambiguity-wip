import statistics


# Compute Non-Monotonicty as Alignment Deviation from the Diagonal
def non_monotonicity_score(positions):
    scores = []
    for p in positions:
        if len(p) == 0:
            continue
        n_pos = len(p)
        abs_diff = sum([abs(num[0] - num[1]) for num in p])
        scores.append((abs_diff / n_pos) * 100)

    return statistics.mean(scores)


# Read the Alignments and Collect Scoring Information
def read_alignments(source_words, target_words, alignment_lines):
    i, aligned_positions, unaligned_source_words = 0, [], []

    for line in alignment_lines:
        temp_aligned_positions, unaligned_source_positions = [], []
        aligned_source_positions = [int(y.split("-")[0]) for y in line.strip().split()]
        source_length = len(source_words[i])

        # Save the position of Word Alignments
        target_length = len(target_words[i])
        if source_length == 0 or target_length == 0:
            pass
        else:
            temp_aligned_positions = [
                (
                    (int(y.split("-")[0]) + 1) / source_length,
                    (int(y.split("-")[1]) + 1) / target_length,
                )
                for y in line.strip().split()
            ]
        aligned_positions.append(temp_aligned_positions)

        # Check if all source word positions are aligned
        for x in range(source_length):
            if x not in aligned_source_positions:
                unaligned_source_positions.append(x)

        unaligned_source_words.append(unaligned_source_positions)
        i = i + 1

    return aligned_positions, unaligned_source_words


def process_lists(source_list, align_list, target_list):
    # Process the Source List
    source_words = [line.strip().split() for line in source_list]

    # Process the Target List
    target_words = [line.strip().split() for line in target_list]

    # Process the Alignments
    aligned_positions, unaligned_source_words = read_alignments(
        source_words, target_words, align_list
    )

    usw_scores = [
        (len(x) / len(y)) * 100 for x, y in zip(unaligned_source_words, source_words)
    ]
    total_words = sum([len(x) for x in source_words])
    usw_mean = sum([u * len(s) for u, s in zip(usw_scores, source_words)]) / total_words
    
    nm_scores = []
    for positions in aligned_positions:
        nm_scores.append(non_monotonicity_score([positions]))
    nm_mean = statistics.mean(nm_scores)

    return usw_scores, nm_scores, usw_mean, nm_mean
