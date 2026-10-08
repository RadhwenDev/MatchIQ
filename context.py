import pandas as pd
from data_loader import load_all_matches


def get_team_history(matches, team, before_date, n=5):
    """
    Get the team's last n matches before the selected match.
    """

    history = matches[
        (
            (matches["HomeTeam"] == team) |
            (matches["AwayTeam"] == team)
        )
        &
        (matches["Date"] < before_date)
    ].copy()

    history = history.sort_values(
        ["Date", "Time"],
        ascending=False
    ).head(n)

    return history


def calculate_team_stats(history, team):
    """
    Calculate basic pre-match statistics
    using only previous matches.
    """

    if history.empty:
        return {
            "matches": 0,
            "wins": 0,
            "draws": 0,
            "losses": 0,
            "points": 0,
            "goals_for": 0,
            "goals_against": 0,
            "avg_goals_for": 0,
            "avg_goals_against": 0,
        }

    wins = draws = losses = 0
    points = 0
    goals_for = 0
    goals_against = 0

    for _, match in history.iterrows():

        if match["HomeTeam"] == team:
            gf = match["FTHG"]
            ga = match["FTAG"]

            if match["FTR"] == "H":
                wins += 1
                points += 3
            elif match["FTR"] == "D":
                draws += 1
                points += 1
            else:
                losses += 1

        else:
            gf = match["FTAG"]
            ga = match["FTHG"]

            if match["FTR"] == "A":
                wins += 1
                points += 3
            elif match["FTR"] == "D":
                draws += 1
                points += 1
            else:
                losses += 1

        goals_for += gf
        goals_against += ga

    total = len(history)

    return {
        "matches": total,
        "wins": wins,
        "draws": draws,
        "losses": losses,
        "points": points,
        "avg_goals_for": round(goals_for / total, 2),
        "avg_goals_against": round(goals_against / total, 2),
    }


def get_h2h(matches, home_team, away_team, before_date, n=5):
    """
    Get previous meetings between the two teams.
    """

    h2h = matches[
        (
            (
                (matches["HomeTeam"] == home_team) &
                (matches["AwayTeam"] == away_team)
            )
            |
            (
                (matches["HomeTeam"] == away_team) &
                (matches["AwayTeam"] == home_team)
            )
        )
        &
        (matches["Date"] < before_date)
    ].copy()

    return h2h.sort_values(
        ["Date", "Time"],
        ascending=False
    ).head(n)


def get_pre_match_context(matches, match_index):
    """
    Build the complete pre-match context
    for a selected historical match.
    """

    match = matches.iloc[match_index]

    date = match["Date"]
    home_team = match["HomeTeam"]
    away_team = match["AwayTeam"]

    home_history = get_team_history(
        matches,
        home_team,
        date,
        n=5
    )

    away_history = get_team_history(
        matches,
        away_team,
        date,
        n=5
    )

    h2h = get_h2h(
        matches,
        home_team,
        away_team,
        date,
        n=5
    )

    home_stats = calculate_team_stats(
        home_history,
        home_team
    )

    away_stats = calculate_team_stats(
        away_history,
        away_team
    )

    return {
        "match": match,
        "home": {
            "team": home_team,
            "history": home_history,
            "stats": home_stats,
        },
        "away": {
            "team": away_team,
            "history": away_history,
            "stats": away_stats,
        },
        "h2h": h2h,
    }


if __name__ == "__main__":

    matches = load_all_matches()

    # Example: Barcelona vs Vallecano
    # First Barcelona match of 2022/23
    index = matches[
        (matches["HomeTeam"] == "Mallorca") &
        (matches["AwayTeam"] == "Barcelona") &
        (matches["Date"] == pd.Timestamp("2025-08-16"))
    ].index[0]

    context = get_pre_match_context(
        matches,
        index
    )

    print("\n==============================")
    print("MATCH")
    print("==============================")

    match = context["match"]

    print(
        f"{match['HomeTeam']} vs "
        f"{match['AwayTeam']}"
    )

    print("Date:", match["Date"])

    print("\n==============================")
    print("HOME TEAM")
    print("==============================")

    print(context["home"]["stats"])

    print("\n==============================")
    print("AWAY TEAM")
    print("==============================")

    print(context["away"]["stats"])

    print("\n==============================")
    print("H2H")
    print("==============================")

    print(
        context["h2h"][
            ["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR"]
        ]
    )