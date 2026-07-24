# tools.py

# في ملف tools.py
def check_hospital_resources(resource_type: str = None):
    # رجع الموارد سواء اتبعت parameter أو لأ
    return {'ICU_beds': 2, 'ER_beds': 5, 'ventilators': 1}

def get_patient_history(patient_id: str = "P-101"):
    return {"patient_id": patient_id, "allergies": ["Penicillin"], "history": "Hypertension"}

def assess_surgery_risk(patient_id: str = "P-101"):
    return {"risk_score": "HIGH", "recommendation": "Require Senior Anesthesiologist"}

def check_transfer_options():
    return {"nearby_hospitals": ["City Central Hospital"], "transfer_available": True}

# في ملف tools.py
def allocate_resource(resource_type: str = "ICU_beds", **kwargs):
    """
    Allocates a specific hospital resource.
    Accepts flexible keyword arguments to prevent execution errors.
    """
    # لو الـ LLM بعت القيمة باسم مختلف زي resource أو bed_type
    target_resource = kwargs.get("resource") or kwargs.get("bed_type") or resource_type
    
    return f"Successfully allocated {target_resource}"