def calculate_risk(confidence, signal_strength, trend_alignment):

    # Very strong setup
    if (
        confidence >= 80
        and signal_strength == "STRONG"
        and trend_alignment == "ALIGNED"
    ):
        return "LOW 🟢"

    # Good confidence but some disagreement
    elif (
        confidence >= 70
        and signal_strength in ["STRONG", "MODERATE"]
        and trend_alignment in ["ALIGNED", "MIXED"]
    ):
        return "MEDIUM 🟡"

    # Moderate setup
    elif confidence >= 60:
        return "MEDIUM 🟡"

    # Weak setup
    else:
        return "HIGH 🔴"