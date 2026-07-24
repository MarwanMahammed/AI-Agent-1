from rules import decide_patient
from testCases import test_cases

passed = 0

for test in test_cases:
    result = decide_patient(**test["input"])

    print("-"*20)
    print(test["name"])
    print("Expected:", test["expected"])
    print("Actual  :", result)

    if result == test["expected"]:
        print("PASS")
        passed += 1
    else:
        print("FAIL")

print("-"*20)
print(f"Passed {passed}/{len(test_cases)} Test Cases")