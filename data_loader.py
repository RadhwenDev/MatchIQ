import os

import pandas as pd
import streamlit as st


# =========================================================
# FILES: (season, file, division)
# =========================================================

WARMUP_SEASONS = {"2021/22"}   # history only, never selectable

FILES = [
    # La Liga
    ("2021/22", "SP1_2021.csv", 1),
    ("2022/23", "SP1_2022.csv", 1),
    ("2023/24", "SP1_2023.csv", 1),
    ("2024/25", "SP1_2024.csv", 1),
    ("2025/26", "SP1.csv",      1),

    # Segunda: history only (promoted teams)
    ("2021/22", "SP2_2021.csv", 2),
    ("2022/23", "SP2_2022.csv", 2),
    ("2023/24", "SP2_2023.csv", 2),
    ("2024/25", "SP2_2024.csv", 2),
]

LEAGUE_NAMES = {1: "La Liga", 2: "Segunda"}


# =========================================================
# COLUMNS (only those common to all seasons)
# =========================================================

COLUMNS = [
    "Div", "Date", "Time", "HomeTeam", "AwayTeam",
    "FTHG", "FTAG", "FTR", "HTHG", "HTAG", "HTR",
    "HS", "AS", "HST", "AST", "HF", "AF",
    "HC", "AC", "HY", "AY", "HR", "AR",

    # opening odds
    "B365H", "B365D", "B365A",
    "PSH", "PSD", "PSA",
    "AvgH", "AvgD", "AvgA",
    "B365>2.5", "B365<2.5", "Avg>2.5", "Avg<2.5",
    "AHh",

    # closing odds (keep for the Reveal stage only)
    "B365CH", "B365CD", "B365CA",
    "PSCH", "PSCD", "PSCA",
    "AvgCH", "AvgCD", "AvgCA",
    "AvgC>2.5", "AvgC<2.5",
    "AHCh",
]

NUMERIC_COLUMNS = [
    c for c in COLUMNS
    if c not in {"Div", "Date", "Time", "HomeTeam", "AwayTeam", "FTR", "HTR"}
]


# =========================================================
# TEAM NAMES: one name per club across all files
# =========================================================
# Fill it from check_team_names() below, e.g. {"Almeria": "Almería"}

NAME_MAP = {
}


@st.cache_data(show_spinner=False)
def load_all_matches():
    datasets = []
    missing_files = []

    for season, filename, division in FILES:
        if not os.path.exists(filename):
            missing_files.append(filename)
            continue

        df = pd.read_csv(filename, encoding="utf-8-sig")

        available = [c for c in COLUMNS if c in df.columns]
        df = df[available].copy()

        # rows without teams/date (empty trailing lines) are useless
        df = df.dropna(subset=["Date", "HomeTeam", "AwayTeam"])

        df["Season"] = season
        df["Division"] = division
        df["League"] = LEAGUE_NAMES[division]

        df["Date"] = pd.to_datetime(
            df["Date"], dayfirst=True, errors="coerce"
        )

        for col in NUMERIC_COLUMNS:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        datasets.append(df)

    if not datasets:
        return pd.DataFrame()

    matches = pd.concat(datasets, ignore_index=True)

    matches = matches.dropna(subset=["Date"])

    # unify team names
    matches["HomeTeam"] = matches["HomeTeam"].str.strip().replace(NAME_MAP)
    matches["AwayTeam"] = matches["AwayTeam"].str.strip().replace(NAME_MAP)

    # only La Liga matches from non-warm-up seasons can be chosen by the user
    matches["Playable"] = (
        (matches["Division"] == 1)
        & ~matches["Season"].isin(WARMUP_SEASONS)
    )

    matches = matches.sort_values(
        ["Date", "Time"],
        na_position="last",
        kind="mergesort",
    ).reset_index(drop=True)

    matches.attrs["missing_files"] = missing_files
    return matches


# =========================================================
# CHECKS (run: python data_loader.py)
# =========================================================

def check_team_names(matches):
    """Promoted teams per season + names that exist only in one division."""
    la_liga = matches[matches["Division"] == 1]
    teams = {
        s: set(g["HomeTeam"]) | set(g["AwayTeam"])
        for s, g in la_liga.groupby("Season")
    }

    seasons = sorted(teams)
    for prev, cur in zip(seasons, seasons[1:]):
        promoted = sorted(teams[cur] - teams[prev])
        print(f"{cur} promoted ({len(promoted)}):", promoted)

    # promoted teams must also appear in Segunda, otherwise the name differs
    segunda = matches[matches["Division"] == 2]
    segunda_teams = set(segunda["HomeTeam"]) | set(segunda["AwayTeam"])

    for prev, cur in zip(seasons, seasons[1:]):
        for team in sorted(teams[cur] - teams[prev]):
            if team not in segunda_teams:
                print(f"  ! {team} not found in Segunda files (name mismatch?)")


if __name__ == "__main__":
    matches = load_all_matches()

    print("Missing files:", matches.attrs.get("missing_files"))
    print("Total rows:", len(matches))
    print("Playable matches:", int(matches["Playable"].sum()))
    print()

    summary = (
        matches.groupby(["Season", "Division"])
        .agg(
            matches=("Date", "size"),
            first=("Date", "min"),
            last=("Date", "max"),
        )
    )
    print(summary)
    print()

    check_team_names(matches)