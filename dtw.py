import numpy as np

def dtw_distance(a, b):
    a = np.array(a)
    b = np.array(b)

    n, m = len(a), len(b)

    dp = np.full((n + 1, m + 1), np.inf)
    dp[0, 0] = 0

    for i in range(1, n + 1):
        for j in range(1, m + 1):

            cost = abs(a[i - 1] - b[j - 1])

            dp[i, j] = cost + min(
                dp[i - 1, j],
                dp[i, j - 1],
                dp[i - 1, j - 1]
            )

    return dp[n, m]