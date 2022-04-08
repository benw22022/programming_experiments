import pandas as pd

df = pd.read_csv("../TauClassifier2/config/stats_df.csv", index_col=0)

print(df)
print(df.loc["TauTracks_nInnermostPixelHits"])

print("\n\n\n\n")
stats_df = pd.read_csv("../TauClassifier2/config/stats_df.csv", index_col=0)
print(stats_df)
print(stats_df['TauTracks_nInnermostPixelHits'])