def decide_patient(
    triage_level,
    age,
    needs_surgery,
    needs_ventilator,
    internal_bleeding,
    available_doctors,
    available_or_rooms,
    available_icu_beds,
    available_ventilators,
):
    # Rule 1
    if triage_level == 1 and needs_ventilator:
        if available_icu_beds > 0 and available_ventilators > 0:
            return "IMMEDIATE_ICU"
        return "ESCALATE_TRANSFER"

    # Rule 2
    if triage_level == 1 and needs_surgery:
        if available_doctors > 0 and available_or_rooms > 0:
            return "IMMEDIATE_OR"
        if available_doctors == 0:
            return "ESCALATE_TRANSFER"
        return "WAITLIST"

    # Rule 3
    if triage_level == 1 and internal_bleeding:
        if available_doctors > 0 and available_or_rooms > 0:
            return "IMMEDIATE_OR"
        return "STABILIZE_AND_MONITOR"

    # Rule 4
    if internal_bleeding and needs_surgery:
        if available_doctors > 0 and available_or_rooms > 0:
            return "IMMEDIATE_OR"
        return "STABILIZE_AND_MONITOR"

    # Rule 5
    if needs_surgery and available_or_rooms == 0:
        if age < 5 or age > 65:
            return "ESCALATE_TRANSFER"
        return "WAITLIST"
    # Rule 6
    if needs_ventilator and available_icu_beds == 0:
        return "ESCALATE_TRANSFER"

    # Rule 7
    if internal_bleeding and available_or_rooms == 0:
        return "STABILIZE_AND_MONITOR"

    # Rule 8
    if triage_level == 2 and needs_surgery:
        return "STABILIZE_AND_MONITOR"

    # Rule 0
    if triage_level == 2 and needs_ventilator:
        if available_icu_beds > 0:
            return "IMMEDIATE_ICU"
        return "WAITLIST"

    # Rule 10
    if triage_level == 2 and internal_bleeding:
        return "IMMEDIATE_OR"

    # Rule 11
    if triage_level == 3 and needs_surgery:
        return "WAITLIST"

    # Rule 12
    if triage_level == 3 and needs_ventilator:
        if available_icu_beds > 0 and available_ventilators > 0:
            return "IMMEDIATE_ICU"
        return "WAITLIST"
    # Rule 13
    if triage_level >= 4:
        return "GENERAL_WARD"

    # Rule 14
    return "GENERAL_WARD"