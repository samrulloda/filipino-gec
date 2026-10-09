import json
import random
import re
from pathlib import Path
from typing import List, Optional, Tuple

MARKER_MAP = {
    "ang": ["ng", "sa"], "ng": ["ang", "sa"], "sa": ["ang", "ng"],
    "Ang": ["Ng", "Sa"], "Ng": ["Ang", "Sa"], "Sa": ["Ang", "Ng"]
}

PRONOUN_MAP = {
    "ako": "ko", "ko": "ako", "ka": "mo", "mo": "ka", "ikaw": "mo",
    "siya": "niya", "niya": "siya", "kami": "namin", "namin": "kami",
    "tayo": "natin", "natin": "tayo", "sila": "nila", "nila": "sila",
    "Ako": "Ko", "Ko": "Ako", "Siya": "Niya", "Niya": "Siya"
}

LOANWORD_HYPHEN_REGEX = re.compile(r'\b(nag|mag|pag|i|ipag|ipinag|makapag)-([a-zA-Z]{3,})\b', re.IGNORECASE)
PAST_ADVERBS = {"kahapon", "kanina", "kagabi", "noong"}
FUTURE_ADVERBS = {"bukas", "mamaya", "samakalawa"}

ASPECT_CONVERSIONS = {
    "kumain": "kakain", "pumunta": "pupunta", "bumili": "bibili", "sumulat": "susulat",
    "nagluto": "magluluto", "nag-aral": "mag-aaral", "nagsalita": "magsasalita",
    "kakain": "kumain", "pupunta": "pumunta", "bibili": "bumili", "susulat": "sumulat",
    "magluluto": "nagluto", "mag-aaral": "nag-aral", "magsasalita": "nagsalita"
}

FOCUS_PAIRS = {
    "kumain": "kinain", "pumunta": "pinuntahan", "bumili": "binili", "sumulat": "isinulat",
    "nagluto": "iniluto", "nagbasa": "binasa", "gumawa": "ginawa",
    "kinain": "kumain", "pinuntahan": "pumunta", "binili": "bumili", "isinulat": "sumulat",
    "iniluto": "nagluto", "binasa": "nagbasa", "ginawa": "gumawa"
}

def perturb_case_marker(tokens: List[str]) -> Optional[Tuple[str, str]]:
    indices = [i for i, t in enumerate(tokens) if t in MARKER_MAP]
    if not indices: return None
    idx = random.choice(indices)
    original = tokens[idx]
    tokens = list(tokens)
    tokens[idx] = random.choice(MARKER_MAP[original])
    return " ".join(tokens), "Case Marker Substitution"

def perturb_pronoun_clitic(tokens: List[str]) -> Optional[Tuple[str, str]]:
    indices = [i for i, t in enumerate(tokens) if t in PRONOUN_MAP]
    if not indices: return None
    idx = random.choice(indices)
    original = tokens[idx]
    tokens = list(tokens)
    tokens[idx] = PRONOUN_MAP[original]
    return " ".join(tokens), "Pronoun Clitic Shift"

def perturb_taglish_hyphen(text: str) -> Optional[Tuple[str, str]]:
    matches = list(LOANWORD_HYPHEN_REGEX.finditer(text))
    if not matches: return None
    m = random.choice(matches)
    corrupted = text[:m.start()] + f"{m.group(1)}{m.group(2)}" + text[m.end():]
    return corrupted, "Taglish Hyphenation Error"

def perturb_aspect_inconsistency(tokens: List[str]) -> Optional[Tuple[str, str]]:
    lower_tokens = [t.lower().strip(".,!?\"'") for t in tokens]
    has_past = any(adv in lower_tokens for adv in PAST_ADVERBS)
    has_future = any(adv in lower_tokens for adv in FUTURE_ADVERBS)
    if not (has_past or has_future): return None

    indices = [i for i, t in enumerate(lower_tokens) if t in ASPECT_CONVERSIONS]
    if not indices: return None
    idx = random.choice(indices)
    rep = ASPECT_CONVERSIONS[lower_tokens[idx]]
    if tokens[idx][0].isupper(): rep = rep.capitalize()
    tokens = list(tokens)
    tokens[idx] = rep
    return " ".join(tokens), "Aspect Inconsistency"

def perturb_focus_confusion(tokens: List[str]) -> Optional[Tuple[str, str]]:
    lower_tokens = [t.lower().strip(".,!?\"'") for t in tokens]
    indices = [i for i, t in enumerate(lower_tokens) if t in FOCUS_PAIRS]
    if not indices: return None
    idx = random.choice(indices)
    rep = FOCUS_PAIRS[lower_tokens[idx]]
    if tokens[idx][0].isupper(): rep = rep.capitalize()
    tokens = list(tokens)
    tokens[idx] = rep
    return " ".join(tokens), "Focus Confusion"
