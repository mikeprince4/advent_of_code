
from helpers import get_data

example = False

data = get_data(example)

matrix = {}
for row_idx, row in enumerate(data):
    matrix[row_idx] = {}
    row = list(str(row))
    for col_idx in range(len(row)):
        val = int(row[col_idx])
        matrix[row_idx][col_idx] = val

scores = {}

num_rows = len(data)

for i in range(num_rows):
    for j in range(num_rows):
        scores[(i, j)] = [0, 0, 0, 0]

        for row in range(i-1, -1, -1):
            scores[(i, j)][0] += 1

            if matrix[row][j] >= matrix[i][j]:
                break

        for row in range(i+1, num_rows):
            scores[(i, j)][1] += 1
            if matrix[row][j] >= matrix[i][j]:
                break

        for col in range(j-1, -1, -1):
            scores[(i, j)][2] += 1

            if matrix[i][col] >= matrix[i][j]:
                break

        for col in range(j+1, num_rows):
            scores[(i, j)][3] += 1

            if matrix[i][col] >= matrix[i][j]:
                break

# for key, lst in scores.items():
    #print(f"key = {key} lst = {lst}; {lst[0]*lst[1]*lst[2]*lst[3]}")
print(max([lst[0]*lst[1]*lst[2]*lst[3] for lst in scores.values()]))
