import os
import sys
import time
from pathlib import Path
from enum import Enum
from typing import Literal
from dotenv import load_dotenv

from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# 1) إعداد مسار المشروع وتحميل متغيرات البيئة (.env)
sys.path.insert(0, str(Path(__file__).parent))
load_dotenv()

# استيراد الأدوات من tools.py
from tools import (
    check_hospital_resources,
    get_patient_history,
    assess_surgery_risk,
    check_transfer_options,
    allocate_resource,
)

# 2) تعريف الأفعال المسموح بها فقط (Strict Enum)
class AllowedActions(str, Enum):
    CHECK_RESOURCES = "check_hospital_resources"
    GET_PATIENT_HISTORY = "get_patient_history"
    ASSESS_SURGERY_RISK = "assess_surgery_risk"
    CHECK_TRANSFERS = "check_transfer_options"
    ALLOCATE_RESOURCE = "allocate_resource"
    ESCALATE_TO_HUMAN = "escalate_to_human"
    FINAL_DECISION = "final_decision"

# 3) Pydantic Schema لتحديد مخرجات كل خطوة
class ConstrainedAgentStep(BaseModel):
    thought: str = Field(
        description="Detailed clinical reasoning and process strategy for the current step."
    )
    urgency_level: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"] = Field(
        description="Patient clinical urgency assessment."
    )
    action: AllowedActions = Field(
        description="The strictly allowed tool or status action to execute next."
    )
    action_input: dict = Field(
        default_factory=dict,
        description="Dynamic dictionary of parameters required for the selected action.",
    )

# 4) تهيئة الـ LLM
# 4) تهيئة الـ LLM مع كتابة المفتاح مباشرة
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.0,
    groq_api_key="groq_api_key"  # تم تغيير الاسم إلى groq_api_key أو تمريره مباشرة
)

structured_llm = llm.with_structured_output(ConstrainedAgentStep)

# 5) خريطة الربط الديناميكي بين الأفعال والدوال
tools_map = {
    AllowedActions.CHECK_RESOURCES: check_hospital_resources,
    AllowedActions.GET_PATIENT_HISTORY: get_patient_history,
    AllowedActions.ASSESS_SURGERY_RISK: assess_surgery_risk,
    AllowedActions.CHECK_TRANSFERS: check_transfer_options,
    AllowedActions.ALLOCATE_RESOURCE: allocate_resource,
}

# 6) Prompt النظام (تم إصلاح الأقواس المجعدة)
SYSTEM_PROMPT = """You are a Constrained Hospital Emergency Triage AI Agent.
Your primary directive is patient safety and strict adherence to protocol.

CRITICAL RULES:
1. You MUST ALWAYS perform reasoning and output ONLY data matching the target schema.
2. You CANNOT select any action outside the provided AllowedActions list.
3. Check hospital resources ONCE. Do NOT repeat 'check_hospital_resources' if observation data is already present in history.
4. When calling 'allocate_resource', set action_input resource_type to 'ICU_beds'.
5. Immediately after 'allocate_resource' succeeds, set action to 'final_decision'.
6. In your 'final_decision' step, write a comprehensive clinical summary in 'thought' detailing the resource check, bed availability, and final allocation result.
7. If risk is CRITICAL and resources are 0 or missing, set action to 'escalate_to_human'.
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("user", "Context & Trajectory History:\n{history}\n\nCurrent Task: {input}")
])

# 7) حلقة التنفيذ المخصصة (Deterministic Custom ReAct Loop)
def run_constrained_agent(user_query: str, max_steps: int = 5):
    history = []
    print(f"\n🚀 [Starting Constrained Agent Execution] Task: {user_query}\n")

    for step_num in range(1, max_steps + 1):
        history_text = "\n".join([f"- {h}" for h in history]) if history else "None"
        formatted_prompt = prompt.format_messages(history=history_text, input=user_query)

        step_output = None
        
        for attempt in range(1, 4):
            try:
                step_output = structured_llm.invoke(formatted_prompt)
                break
            except Exception as e:
                err_str = str(e)
                if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                    wait_time = attempt * 10
                    print(f"⚠️ Rate limit hit. Cooling down for {wait_time}s... (Attempt {attempt}/3)")
                    time.sleep(wait_time)
                else:
                    print(f"⚠️ API Error: {err_str}. Retrying in 2s...")
                    time.sleep(2)

        if not step_output:
            return "Execution failed due to API connection issues."

        print(f"--- Step {step_num} ---")
        print(f"🧠 Thought: {step_output.thought}")
        print(f"⚠️ Urgency: {step_output.urgency_level}")
        print(f"🛠️ Action Chosen: {step_output.action.value}")

        if step_output.action == AllowedActions.FINAL_DECISION:
            print("\n✅ [FINAL DECISION REACHED]")
            return step_output.thought

        if step_output.action == AllowedActions.ESCALATE_TO_HUMAN:
            print("\n🚨 [ESCALATED TO HUMAN DOCTOR]")
            return f"Escalated to medical staff: {step_output.thought}"

        tool_func = tools_map.get(step_output.action)
        if tool_func:
            try:
                observation = tool_func(**step_output.action_input)
                print(f"🔍 Observation: {observation}\n")
                history.append(f"Action '{step_output.action.value}' returned: {observation}")
            except Exception as e:
                error_msg = f"Tool execution error: {str(e)}"
                print(f"❌ Error: {error_msg}\n")
                history.append(error_msg)

        time.sleep(1)

    print("\n🛑 [MAX STEPS REACHED - AUTO ESCALATING]")
    return "Safety Escalation: Reached max interaction steps without resolution."


if __name__ == "__main__":
    query = "Patient P-102 needs urgent ICU bed allocation for severe trauma."
    result = run_constrained_agent(query)
    print(f"\n📋 Final Agent Outcome: {result}")