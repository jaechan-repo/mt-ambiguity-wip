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

    total_words_macro = sum([len(x) for x in source_words])
    unaligned_source_words_macro = sum([len(x) for x in unaligned_source_words])
    return (unaligned_source_words_macro / total_words_macro) * 100, non_monotonicity_score(aligned_positions)
