# 🛡️ Constrained ReAct Agent for Hospital Triage
This directory contains the implementation of the **Constrained ReAct Architecture** for Emergency Hospital Triage. It combines LLM-driven multi-step reasoning with strict engineering guardrails to prevent schema hallucinations, infinite loops, and unhandled runtime exceptions in critical care workflows.
##  Core Engineering Guardrails
The guardrails are explicitly defined in the code for maximum transparency and safety:
1. **Validation Schema (`ConstrainedAgentStep`)**: Built using `Pydantic` to enforce structured JSON output. Tool actions are restricted strictly to an explicit `Enum` to eliminate invalid tool calls[cite: 1].
2. **Tool Allow-List (`tools_map`)**: Limits dynamic execution strictly to authorized triage tools (`check_hospital_resources`, `allocate_resource`, `final_decision`)[cite: 1].
3. **Execution Budget (`MAX_STEPS = 6`)**: Enforces a strict upper bound on execution loops to guarantee fast termination or automatic escalation[cite: 1].
4. **Keyword Argument Resilience (`**kwargs`)**: Extended underlying tool signatures to support dynamic `**kwargs`, preventing `TypeError` during parameter parsing.
## File Structure
* `constrained_agent.py`: Main agent runtime, custom ReAct loop, and schema validation handling[cite: 1].
* `tools.py`: Emergency hospital tool implementations with dynamic parameter handling.
* `.env`: Template for environment variable setup.
* `README.md`: System documentation and execution guidelines.
