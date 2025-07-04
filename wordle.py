#!/usr/bin/python3

from collections import Counter  # For counting frequency of letters in the candidate list

# =======================
# Load 5-letter words from the provided filename into a list
# =======================
def load_word_list(filename):
    with open(filename) as f:
        # Strip whitespace, convert to lowercase, keep only 5-letter words
        words = [line.strip().lower() for line in f if len(line.strip()) == 5]
    return words

# =======================
# Check if the word matches the known green pattern (correct letters in place)
# =======================
def matches_green(word, pattern):
    ## EXPLANATION:
    # For each letter and its pattern, accept if pattern is '.' (unknown) or if the letters match
    return all(w == p or p == '.' for w, p in zip(word, pattern))

# =======================
# Check if word satisfies all yellow patterns (correct letter, wrong position)
# =======================
def matches_yellow(word, yellow_patterns):
    ## EXPLANATION:
    # For each yellow pattern, ensure that the word contains the yellow letter, but NOT in the same position
    for yp in yellow_patterns:
        # Find the position (index) and the yellow letter in this pattern (e.g. '..k..' => idx=2, letter='k')
        idx = yp.find(next(filter(str.isalpha, yp)))
        letter = yp[idx]
        if letter not in word:
            # If the letter is not in the word at all, fail
            return False
        if word[idx] == letter:
            # If the letter is in the exact same spot as the yellow clue, fail
            return False
    return True  # All yellow patterns satisfied

# =======================
# Check if the word excludes all gray (eliminated) letters, except those "protected" (green/yellow in other slots)
# =======================
def matches_gray(word, gray_letters, green_pattern, yellow_patterns):
    ## EXPLANATION:
    # Gray letters (not in answer) should not appear in the word, unless they are 'protected'
    # (i.e., that letter is confirmed elsewhere by green/yellow clue)
    protected = set(green_pattern.replace('.', ''))  # Green letters
    for yp in yellow_patterns:
        protected.add(next(filter(str.isalpha, yp)))  # Add yellow letters too
    for letter in gray_letters:
        if letter in protected:
            # If letter is green/yellow somewhere else, skip the gray elimination for this letter
            continue
        if letter in word:
            # If gray letter is in word and not protected, fail
            return False
    return True

# =======================
# Main interactive function
# =======================
def main():
    # Load possible words (from word list file)
    words = load_word_list('list_wordles.txt')
    yellow_patterns = []  # Store all yellow clues as patterns (e.g. '..k..')
    gray_letters = set()  # Store all eliminated (gray) letters

    print("\nWordle Helper (Python Edition - Frequency Scoring)")
    print("Type known letters in correct positions (e.g. ..e.r), or . for unknowns.")

    while True:
        print()
        green_pattern = input("Pattern (blank to quit): ").strip().lower()
        if not green_pattern:
            break  # Exit the program if no input (blank line)
        if len(green_pattern) != 5:
            print("Pattern must be 5 characters (use . for unknowns).")
            continue

        # Get yellow (out-of-place) letters as a single pattern, e.g., .a.g.
        y = input("Out-of-place letters (format .a.g.), Enter to skip: ").strip().lower()
        yellow_patterns.clear()
        if y and len(y) == 5:
            for i, letter in enumerate(y):
                if letter != '.':
                    pattern = ['.'] * 5
                    pattern[i] = letter
                    yellow_patterns.append(''.join(pattern))

        # Get gray (eliminated) letters as a simple string, add each to set
        grays = input("Letters eliminated (gray), as a string: ").strip().lower()
        for l in grays:
            gray_letters.add(l)

        # Filtering logic: keep only words that match all clues
        matches = []
        for w in words:
            if not matches_green(w, green_pattern):
                continue  # Doesn't match green pattern
            if not matches_yellow(w, yellow_patterns):
                continue  # Doesn't match all yellow clues
            if not matches_gray(w, gray_letters, green_pattern, yellow_patterns):
                continue  # Doesn't match gray elimination
            matches.append(w)  # Keep candidate word

        print(f"\nResults ({len(matches)}):")
        if len(matches) == 0:
            print("No words found.")
        elif len(matches) <= 2:
            print(", ".join(matches))  # Just list the few matches found
        else:
            # =======================
            # Calculate frequency of each letter among remaining matches
            # =======================
            letter_counts = Counter("".join(matches))  # Count how often each letter appears in all matching words
            word_scores = []
            for w in matches:
                unique_letters = set(w)  # Only count each letter once per word
                # Score is the sum of how frequent each unique letter is among all matches
                score = sum(letter_counts[l] for l in unique_letters)
                word_scores.append((score, w))
            # Sort by highest score (most frequent letters), then alphabetically for tie-breaker
            word_scores.sort(key=lambda x: (-x[0], x[1]))
            print("Top suggestions (highest-frequency letters):")
            for score, w in word_scores[:10]:  # Show top 10 best guesses
                print(f"{w} (score: {score})")
            print("\nFull list:")
            print(", ".join(w for _, w in word_scores))

if __name__ == "__main__":
    main()  # Start the interactive loop
