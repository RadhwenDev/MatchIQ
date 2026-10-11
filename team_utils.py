import html

TEAM_LOGOS = {
    # Clubs present across multiple seasons
    "Barcelona": "https://crests.football-data.org/81.png",
    "Real Madrid": "https://crests.football-data.org/86.png",
    "Ath Madrid": "https://crests.football-data.org/78.png",
    "Atletico Madrid": "https://crests.football-data.org/78.png",
    "Ath Bilbao": "https://crests.football-data.org/77.png",
    "Athletic Bilbao": "https://crests.football-data.org/77.png",
    "Betis": "https://crests.football-data.org/90.png",
    "Real Betis": "https://crests.football-data.org/90.png",
    "Sociedad": "https://crests.football-data.org/92.png",
    "Real Sociedad": "https://crests.football-data.org/92.png",
    "Sevilla": "https://crests.football-data.org/559.png",
    "Valencia": "https://crests.football-data.org/95.png",
    "Villarreal": "https://crests.football-data.org/94.png",
    "Celta": "https://crests.football-data.org/558.png",
    "Getafe": "https://crests.football-data.org/82.png",
    "Osasuna": "https://crests.football-data.org/79.png",
    "Mallorca": "https://crests.football-data.org/89.png",
    "Vallecano": "https://crests.football-data.org/87.png",
    "Rayo Vallecano": "https://crests.football-data.org/87.png",

    # Clubs appearing in some of the four seasons
    "Alaves": "https://crests.football-data.org/263.png",
    "Almería": "https://crests.football-data.org/267.png",
    "Almeria": "https://crests.football-data.org/267.png",
    "Cadiz": "https://crests.football-data.org/264.png",
    "Cádiz": "https://crests.football-data.org/264.png",
    "Elche": "https://crests.football-data.org/285.png",
    "Espanol": "https://crests.football-data.org/80.png",
    "Espanyol": "https://crests.football-data.org/80.png",
    "Girona": "https://crests.football-data.org/298.png",
    "Granada": "https://crests.football-data.org/83.png",
    "Las Palmas": "https://crests.football-data.org/275.png",
    "Leganes": "https://crests.football-data.org/745.png",
    "Leganés": "https://crests.football-data.org/745.png",
    "Levante": "https://crests.football-data.org/88.png",
    "Valladolid": "https://crests.football-data.org/250.png",
    "Oviedo": "https://www.footylogos.com/logos/real-oviedo",
    }


def safe(value):
    return html.escape(str(value), quote=True)


def get_logo(team):
    return TEAM_LOGOS.get(str(team), "")


def get_initials(team):
    words = str(team).strip().split()
    if not words:
        return "FC"
    if len(words) == 1:
        return words[0][:2].upper()
    return (words[0][0] + words[-1][0]).upper()


def team_logo_html(team):
    """Return the crest <img> (with initials fallback) as an HTML string."""
    initials = safe(get_initials(team))
    logo = get_logo(team)

    if logo:
        return (
            f'<img class="club-logo" src="{safe(logo)}" alt="{safe(team)}" '
            f'onerror="this.style.display=\'none\';'
            f'this.nextElementSibling.style.display=\'flex\';">'
            f'<div class="club-fallback" style="display:none">{initials}</div>'
        )

    return f'<div class="club-fallback">{initials}</div>'