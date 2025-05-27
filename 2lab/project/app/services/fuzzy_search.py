import time
from typing import List, Dict

def levenshtein_distance(word1: str, word2: str) -> int:
    n, m = len(word1), len(word2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = 0 if word1[i - 1] == word2[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,
                dp[i][j - 1] + 1,
                dp[i - 1][j - 1] + cost
            )
    return dp[n][m]

def search_with_levenshtein(text: str, word: str, threshold: int = 3) -> List[Dict]:
    words = text.split()
    results = []
    for w in set(words):
        dist = levenshtein_distance(word.lower(), w.lower())
        if dist <= threshold:
            results.append({"word": w, "distance": dist})
    return sorted(results, key=lambda x: x["distance"])