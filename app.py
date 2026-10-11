import html

import streamlit as st
import time
from match_selection import render_match_selection, play_zoom_transition

from data_loader import load_all_matches
from match_selection import render_match_selection
from match_context import render_match_context
from match_predict import render_match_prediction

# =========================================================
# CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="MatchIQ",
    page_icon="⚽",
    layout="wide",
)

STEPS = [
    "Select a match",
    "Study context",
    "Predict",
    "Reveal",
    "Learn",
]

if "page_transition" not in st.session_state:
    st.session_state["page_transition"] = False


# =========================================================
# SESSION STATE
# =========================================================

if "analysis_step" not in st.session_state:
    st.session_state["analysis_step"] = 1

if "match_selection_confirmed" not in st.session_state:
    st.session_state["match_selection_confirmed"] = False

if "selected_match_index" not in st.session_state:
    st.session_state["selected_match_index"] = None


# =========================================================
# WIZARD
# =========================================================

def render_stepper(current_step):
    items = []

    for number, label in enumerate(STEPS, start=1):
        if number < current_step:
            state = "done"
            icon = "✓"
        elif number == current_step:
            state = "active"
            icon = str(number)
        else:
            state = "todo"
            icon = str(number)

        items.append(
            f"""
            <div class="step {state}">
                <div class="circle">{icon}</div>
                <span class="step-label">{html.escape(label)}</span>
            </div>
            """
        )

        if number < len(STEPS):
            items.append('<div class="step-line"></div>')

    st.markdown(
        """
        <style>
        .stepper {
            display: flex;
            align-items: center;
            gap: 12px;
            background: #0d131c;
            padding: 16px;
            border-radius: 14px;
            margin: 10px 0 24px;
            width: 100%;
            box-sizing: border-box;
        }
        .step {
            display: flex;
            align-items: center;
            gap: 8px;
            white-space: nowrap;
        }
        .circle {
            width: 28px;
            height: 28px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            font-weight: 700;
            flex-shrink: 0;
        }
        .step-label {
            font-size: 12px;
            color: #7d8a9a;
        }
        .step-line {
            flex: 1;
            min-width: 8px;
            height: 1px;
            background: #2a3646;
        }
        .step.done .circle {
            background: #17382f;
            color: #6fd3a8;
        }
        .step.active .circle {
            background: #7fd9b0;
            color: #0d131c;
        }
        .step.active .step-label {
            color: #ffffff;
            font-weight: 700;
        }
        .step.todo .circle {
            background: #1b2635;
            color: #7d8a9a;
        }
        @media (max-width: 700px) {
            .stepper {
                gap: 5px;
                padding: 10px 6px;
            }
            .step {
                flex-direction: column;
                white-space: normal;
                text-align: center;
                gap: 4px;
            }
            .step-label {
                font-size: 9px;
            }
            .step-line {
                min-width: 4px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="stepper">'
        + "".join(items)
        + "</div>",
        unsafe_allow_html=True,
    )


# =========================================================
# LOAD DATA
# =========================================================

matches = load_all_matches()

if matches is None or matches.empty:
    st.error("No match data could be loaded.")
    st.stop()

if "League" not in matches.columns:
    matches["League"] = "La Liga"


# =========================================================
# VALIDATE SELECTED MATCH
# =========================================================

selected_index = st.session_state.get("selected_match_index")

if (
    st.session_state["match_selection_confirmed"]
    and (
        selected_index is None
        or selected_index not in matches.index
    )
):
    st.session_state["match_selection_confirmed"] = False
    st.session_state["selected_match_index"] = None
    st.session_state["analysis_step"] = 1


# =========================================================
# DISPLAY CURRENT STAGE
# =========================================================

step = int(st.session_state["analysis_step"])
step = max(1, min(step, len(STEPS)))

render_stepper(step)


# =========================================================
# STEP 1 — SELECT A MATCH
# =========================================================

if step == 1 or not st.session_state["match_selection_confirmed"]:
    st.session_state["analysis_step"] = 1
    render_match_selection(matches)

    # Zoom animation, then go to the context page
    if st.session_state.get("page_transition"):
        play_zoom_transition()
        time.sleep(0.7)   # same duration as the CSS animation
        st.session_state["page_transition"] = False
        st.session_state["match_selection_confirmed"] = True
        st.session_state["analysis_step"] = 2
        st.session_state["scroll_to_top"] = True 
        st.rerun()


# =========================================================
# STEP 2 — STUDY CONTEXT
# =========================================================

elif step == 2:
    render_match_context(
        matches,
        st.session_state["selected_match_index"],
    )

# =========================================================
# STEP 3 — PREDICT
# =========================================================

elif step == 3:
    render_match_prediction(
        matches,
        st.session_state["selected_match_index"],
    )

# =========================================================
# GET SELECTED MATCH FOR LATER STAGES
# =========================================================

else:
    selected_index = st.session_state["selected_match_index"]
    match = matches.loc[selected_index]

    home_team = match["HomeTeam"]
    away_team = match["AwayTeam"]

    st.caption(f"{home_team} vs {away_team}")

    # -----------------------------------------------------
    # STEP 4 — REVEAL
    # -----------------------------------------------------

    if step == 4:
        st.title("The Result")
        st.write(f"**{home_team} vs {away_team}**")

        if (
            "FTHG" not in match.index
            or "FTAG" not in match.index
            or not __import__("pandas").notna(match["FTHG"])
            or not __import__("pandas").notna(match["FTAG"])
        ):
            st.warning(
                "The actual score is unavailable for this fixture."
            )
        else:
            home_goals = int(match["FTHG"])
            away_goals = int(match["FTAG"])

            st.markdown(
                f"## {home_team} **{home_goals} – {away_goals}** "
                f"{away_team}"
            )

            actual_result = (
                "H" if home_goals > away_goals
                else "A" if away_goals > home_goals
                else "D"
            )

            prediction = st.session_state.get("prediction")

            if prediction is None:
                st.warning("No saved prediction was found.")
            elif prediction == actual_result:
                st.success("Correct prediction!")
            else:
                st.info("Your prediction was different from the actual outcome.")

            if st.button(
                "Continue to Learning →",
                type="primary",
                use_container_width=True,
            ):
                st.session_state["actual_result"] = actual_result
                st.session_state["analysis_step"] = 5
                st.rerun()

        if st.button("← Back to Prediction", use_container_width=True):
            st.session_state["analysis_step"] = 3
            st.rerun()

    # -----------------------------------------------------
    # STEP 5 — LEARN
    # -----------------------------------------------------

    elif step == 5:
        st.title("What Did You Learn?")
        st.write(
            "Reflect on your prediction. Which pre-match information "
            "influenced your decision, and what would you analyse "
            "differently next time?"
        )

        reflection = st.text_area(
            "Your analysis",
            placeholder=(
                "I predicted this outcome because...\n"
                "Next time, I would also consider..."
            ),
            key="learning_reflection",
        )

        if st.button(
            "Finish Analysis",
            type="primary",
            use_container_width=True,
        ):
            st.success("Analysis completed. Good work!")
            st.write("**Your reflection:**")
            st.write(reflection or "No reflection added.")

        if st.button("← Back to Result", use_container_width=True):
            st.session_state["analysis_step"] = 4
            st.rerun()