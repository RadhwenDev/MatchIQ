import pandas as pd


FILES = {
    "2022/23": "SP1_2022.csv",
    "2023/24": "SP1_2023.csv",
    "2024/25": "SP1_2024.csv",
    "2025/26": "SP1.csv",
}


COLUMNS = [
    "Date",
    "Time",
    "HomeTeam",
    "AwayTeam",
    "FTHG",
    "FTAG",
    "FTR",
    "HTHG",
    "HTAG",
    "HTR",
    "HS",
    "AS",
    "HST",
    "AST",
    "HF",
    "AF",
    "HC",
    "AC",
    "HY",
    "AY",
    "HR",
    "AR",
    "B365H",
    "B365D",
    "B365A",
]


def load_all_matches():
    datasets = []

    for season, filename in FILES.items():
        df = pd.read_csv(filename)

        # Keep only columns available in this season
        available = [col for col in COLUMNS if col in df.columns]
        df = df[available].copy()

        df["Season"] = season

        # Convert date
        df["Date"] = pd.to_datetime(
            df["Date"],
            dayfirst=True,
            errors="coerce"
        )

        datasets.append(df)

    matches = pd.concat(
        datasets,
        ignore_index=True
    )

    matches = matches.sort_values(
        ["Date", "Time"],
        na_position="last"
    ).reset_index(drop=True)

    return matches


if __name__ == "__main__":
    matches = load_all_matches()

    print("Total matches:", len(matches))
    print("Seasons:", matches["Season"].unique())
    print()
    print(matches[
        ["Season", "Date", "HomeTeam", "AwayTeam", "FTR"]
    ].head(10))