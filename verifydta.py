import pandas as pd

main_arr = []

for i in range(10_000):
    df = pd.read_csv(str(i) + "_file.csv")
    for idx in range(len(df.values)):
        main_arr.append(df.values[idx])

pd.DataFrame(main_arr).to_csv("Thingiverse.csv")
