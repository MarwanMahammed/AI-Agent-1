test_cases = [

    # Test Case 1
    {
        "name": "Test Case 1",
        "input": {
            "triage_level": 1,
            "age": 45,
            "needs_surgery": False,
            "needs_ventilator": True,
            "internal_bleeding": False,
            "available_doctors": 2,
            "available_or_rooms": 1,
            "available_icu_beds": 1,
            "available_ventilators": 1,
        },
        "expected": "IMMEDIATE_ICU"
    },


    # Test Case 2
    {
        "name": "Test Case 2",
        "input": {
            "triage_level": 1,
            "age": 30,
            "needs_surgery": True,
            "needs_ventilator": False,
            "internal_bleeding": False,
            "available_doctors": 1,
            "available_or_rooms": 1,
            "available_icu_beds": 1,
            "available_ventilators": 1,
        },
        "expected": "IMMEDIATE_OR"
    },


    # Test Case 3
    {
        "name": "Test Case 3",
        "input": {
            "triage_level": 3,
            "age": 40,
            "needs_surgery": True,
            "needs_ventilator": False,
            "internal_bleeding": False,
            "available_doctors": 1,
            "available_or_rooms": 0,
            "available_icu_beds": 1,
            "available_ventilators": 1,
        },
        "expected": "WAITLIST"
    },

    # Test Case 4
   {
    "name": "Test Case 4",
    "input": {
        "triage_level": 4,
        "age": 35,
        "needs_surgery": False,
        "needs_ventilator": False,
        "internal_bleeding": False,
        "available_doctors": 3,
        "available_or_rooms": 2,
        "available_icu_beds": 2,
        "available_ventilators": 2,
    },
    "expected": "GENERAL_WARD"
},


    # Test Case 5
    {
        "name": "Test Case 5",
        "input": {
            "triage_level": 1,
            "age": 55,
            "needs_surgery": False,
            "needs_ventilator": False,
            "internal_bleeding": True,
            "available_doctors": 0,
            "available_or_rooms": 0,
            "available_icu_beds": 1,
            "available_ventilators": 1,
        },
        "expected": "STABILIZE_AND_MONITOR"
    },


    # Test Case 6
    {
        "name": "Test Case 6",
        "input": {
            "triage_level": 1,
            "age": 60,
            "needs_surgery": True,
            "needs_ventilator": True,
            "internal_bleeding": False,
            "available_doctors": 1,
            "available_or_rooms": 1,
            "available_icu_beds": 1,
            "available_ventilators": 1,
        },
        "expected": "IMMEDIATE_OR"
    },


    # Test Case 7
    {
        "name": "Test Case 7",
        "input": {
            "triage_level": 1,
            "age": 70,
            "needs_surgery": True,
            "needs_ventilator": False,
            "internal_bleeding": True,
            "available_doctors": 1,
            "available_or_rooms": 1,
            "available_icu_beds": 1,
            "available_ventilators": 1,
        },
        "expected": "IMMEDIATE_OR"
    },


    # Test Case 8
    {
        "name": "Test Case 8",
        "input": {
            "triage_level": 1,
            "age": 3,
            "needs_surgery": True,
            "needs_ventilator": False,
            "internal_bleeding": False,
            "available_doctors": 1,
            "available_or_rooms": 0,
            "available_icu_beds": 1,
            "available_ventilators": 1,
        },
        "expected": "ESCALATE_TRANSFER"
    },


    # Test Case 9
    {
        "name": "Test Case 9",
        "input": {
            "triage_level": 1,
            "age": 45,
            "needs_surgery": False,
            "needs_ventilator": True,
            "internal_bleeding": False,
            "available_doctors": 2,
            "available_or_rooms": 1,
            "available_icu_beds": 1,
            "available_ventilators": 0,
        },
        "expected": "ESCALATE_TRANSFER"
    }
]