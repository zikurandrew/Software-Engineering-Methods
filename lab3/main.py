def solve_knapsack_dp(weights, values, capacity):
    n = len(weights)
    # Створення матриці (n+1) x (W+1)
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    # Заповнення таблиці
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            if weights[i-1] <= w:
                # Вибираємо максимум між "не брати" і "взяти" предмет
                dp[i][w] = max(dp[i-1][w], dp[i-1][w - weights[i-1]] + values[i-1])
            else:
                dp[i][w] = dp[i-1][w]

    # Відновлення набору предметів
    res_value = dp[n][capacity]
    w = capacity
    items_selected = []
    
    for i in range(n, 0, -1):
        if res_value <= 0:
            break
        if res_value != dp[i-1][w]:
            items_selected.append(i-1)
            res_value -= values[i-1]
            w -= weights[i-1]

    return dp[n][capacity], items_selected, dp

weights = [9, 9, 9, 7, 8, 9]
values = [9, 3, 15, 14, 8, 5]
W = 23

max_val, items, matrix = solve_knapsack_dp(weights, values, W)
print(f"Максимальна цінність: {max_val}")
print(f"Індекси предметів: {items}")