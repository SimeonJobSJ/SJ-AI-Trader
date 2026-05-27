def calculate_risk(confidence):

    if confidence >= 80:
        return "LOW 🟢"

    elif confidence >= 60:
        return "MEDIUM 🟡"

    else:
        return "HIGH 🔴"