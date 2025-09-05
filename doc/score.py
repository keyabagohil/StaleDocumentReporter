import math

def sigmoid(x): return 1/(1+math.exp(-x))

def compute_score(age_gap_days, coverage_pct, broken_links, version_skew):
    age_gap_norm = sigmoid((age_gap_days - 7)/7)      # 7-day comfort window
    coverage_penalty = 1 - (coverage_pct/100.0)
    link_penalty = min(1.0, broken_links/3.0)
    skew_flag = 1.0 if any(v and v.get("docs")!=v.get("repo") for v in (version_skew or {}).values()) else 0.0
    score = 0.35*age_gap_norm + 0.35*coverage_penalty + 0.2*link_penalty + 0.1*skew_flag
    return max(0.0, min(1.0, score))
