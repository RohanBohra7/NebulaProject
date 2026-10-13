"""
Quantitative evaluation metrics for NEBULA's adaptive presentation architecture.
Computes Flesch-Kincaid readability, lexical diversity, technical term density,
and empirical grounding fidelity.
"""
import re
import math
from typing import Dict, Any, List

# Core astrophysical domain vocabulary
ASTRONOMY_LEXICON = {
    "astrophysics", "astronomical", "astronomy", "eccentricity", "semi-major", "perihelion", "aphelion",
    "periastron", "apoastron", "keplerian", "barycenter", "inclination", "ascending",
    "precession", "resonance", "laplace", "hydrostatic", "thermonuclear", "equilibrium",
    "spectroscopy", "bolometric", "luminosity", "metallicity", "photosphere", "chromosphere",
    "corona", "supernova", "progenitor", "schwarzschild", "singularity", "virial",
    "gravitational", "hill", "roche", "magnetosphere", "troposphere", "albedo", "parsec",
    "insolation", "photoevaporation", "convection", "anorthositic", "regolith", "sub-neptune",
    "super-earth", "exoplanet", "habitable", "transiting", "pulsation", "ephemeris",
    "terrestrial", "radial", "velocity", "magnitude", "photometry", "spectral", "spectroscopic",
    "equilibrium", "photospheric", "thermodynamic", "gravitation", "orbits", "orbital",
    "trappist", "proxima", "kepler", "periapsis", "apoapsis", "convective", "radiative"
}

def clean_sentences_for_metrics(text: str) -> List[str]:
    # Replace common abbreviations that have periods
    cleaned = re.sub(r'\b(e\.g\.|i\.e\.|et al\.|fig\.|dr\.)', 'eg', text, flags=re.IGNORECASE)
    # Treat double newlines or punctuation as sentence boundaries
    raw_sentences = re.split(r'[.!?\n]+', cleaned)
    return [s.strip() for s in raw_sentences if len(s.strip()) > 10]


def count_syllables_word(word: str) -> int:
    """Estimates syllables in a single word using heuristic vowel groupings."""
    word = word.lower().strip()
    if len(word) <= 3:
        return 1
    # Remove trailing 'e'
    if word.endswith('e') and not word.endswith('le'):
        word = word[:-1]
    vowel_groups = re.findall(r'[aeiouy]+', word)
    return max(1, len(vowel_groups))

def compute_text_readability(text: str) -> Dict[str, Any]:
    """
    Computes Flesch Reading Ease (FRE) and Flesch-Kincaid Grade Level (FKGL).
    """
    # Clean text: remove markdown symbols for word counting
    clean = re.sub(r'[#*`$\-\n]', ' ', text)
    words = [w for w in re.findall(r'\b[A-Za-z]+\b', clean) if len(w) > 0]
    sentences = clean_sentences_for_metrics(text)

    num_words = max(1, len(words))
    num_sentences = max(1, len(sentences))
    num_syllables = sum(count_syllables_word(w) for w in words)

    avg_sentence_len = num_words / num_sentences
    avg_syllables_per_word = num_syllables / num_words

    # Flesch Reading Ease: 206.835 - 1.015*(words/sentences) - 84.6*(syllables/words)
    fre = 206.835 - (1.015 * avg_sentence_len) - (84.6 * avg_syllables_per_word)
    fre = max(0.0, min(100.0, fre))

    # Flesch-Kincaid Grade Level: 0.39*(words/sentences) + 11.8*(syllables/words) - 15.59
    fkgl = (0.39 * avg_sentence_len) + (11.8 * avg_syllables_per_word) - 15.59
    fkgl = max(1.0, min(22.0, fkgl))

    # Technical term density
    tech_count = sum(1 for w in words if w.lower() in ASTRONOMY_LEXICON)
    tech_density_pct = (tech_count / num_words) * 100.0

    # Math expressions count
    latex_matches = re.findall(r'\$.*?\$', text)
    math_expressions_count = len(latex_matches)

    return {
        "word_count": num_words,
        "sentence_count": num_sentences,
        "flesch_reading_ease": round(fre, 1),
        "flesch_kincaid_grade": round(fkgl, 1),
        "technical_term_count": tech_count,
        "technical_term_density_percent": round(tech_density_pct, 2),
        "math_expressions_count": math_expressions_count,
        "avg_words_per_sentence": round(avg_sentence_len, 1)
    }

def compute_grounding_score(text: str, expected_grounded_points: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Checks what fraction of expected empirical figures appear in the response text.
    """
    if not expected_grounded_points:
        return {"grounding_score_percent": 100.0, "matched_points": 0, "total_points": 0}

    matched = 0
    text_lower = text.lower()
    for pt in expected_grounded_points:
        val = str(pt["value"]).lower()
        prop = pt["property"].lower()
        if val in text_lower or prop in text_lower:
            matched += 1

    score = (matched / len(expected_grounded_points)) * 100.0
    return {
        "grounding_score_percent": round(score, 1),
        "matched_points": matched,
        "total_points": len(expected_grounded_points)
    }
