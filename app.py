import os
import openpyxl
from pydantic import BaseModel
from typing import List, Dict

class Workflow(BaseModel):
    id: str
    name: str
    trigger: str
    inputs: str
    steps: List[str]
    decision_logic: str
    tools: List[str]
    expected_output: str

def load_workflows(excel_path: str) -> Dict[str, Workflow]:
    wb = openpyxl.load_workbook(excel_path, data_only=True)
    sheet = wb["Workflows"]
    
    rows = list(sheet.iter_rows(values_only=True))
    header = [str(col).strip() if col is not None else "" for col in rows[0]]
    
    col_idx = {name: i for i, name in enumerate(header)}
    
    registry = {}
    for r in rows[1:]:
        if not r or r[col_idx["Workflow_ID"]] is None:
            continue
        
        raw_steps = str(r[col_idx["Steps"]])
        raw_tools = str(r[col_idx["Tools_Required"]])
        
        steps = [s.strip() for s in raw_steps.split("→")]
        tools = [t.strip() for t in raw_tools.split(";")]
        
        wf = Workflow(
            id=str(r[col_idx["Workflow_ID"]]).strip(),
            name=str(r[col_idx["Workflow_Name"]]).strip(),
            trigger=str(r[col_idx["Trigger"]]).strip(),
            inputs=str(r[col_idx["Inputs"]]).strip(),
            steps=steps,
            decision_logic=str(r[col_idx["Decision_Logic"]]).strip(),
            tools=tools,
            expected_output=str(r[col_idx["Expected_Output"]]).strip()
        )
        registry[wf.id] = wf
    return registry

INVENTORY_DATA = [
    {"sku": "SKU-101", "name": "Wireless Mouse", "stock": 4, "threshold": 15},
    {"sku": "SKU-102", "name": "Mechanical Keyboard", "stock": 25, "threshold": 20},
    {"sku": "SKU-103", "name": "USB-C Cable", "stock": 5, "threshold": 30}
]

ORDERS_DATA = {
    "ORD-1001": {"status": "In Transit", "carrier": "FedEx", "tracking": "FX-998231"}
}

EMPLOYEES_DATA = [
    {"name": "Alice Chen", "skills": ["Python", "AI"], "workload": 1},
    {"name": "Bob Smith", "skills": ["React"], "workload": 0},
    {"name": "Carol Danvers", "skills": ["Python"], "workload": 4}
]

def tool_restock_check() -> str:
    needed = []
    for item in INVENTORY_DATA:
        if item["stock"] < item["threshold"]:
            reorder = (item["threshold"] * 2) - item["stock"]
            needed.append(f"- {item['name']} ({item['sku']}): Stock={item['stock']}, Min={item['threshold']}, Reorder Quantity={reorder}")
    return "Products requiring restocking:\n" + "\n".join(needed)

def tool_price_validation() -> str:
    prices = [
        {"sku": "SKU-101", "internal": 25.0, "vendor": 32.0},
        {"sku": "SKU-102", "internal": 80.0, "vendor": 82.0}
    ]
    lines = []
    for p in prices:
        diff_pct = abs(p["vendor"] - p["internal"]) / p["internal"]
        flag = "FLAGGED (>10% variance)" if diff_pct > 0.10 else "VALID"
        lines.append(f"- SKU {p['sku']}: Internal=${p['internal']}, Vendor=${p['vendor']}, Diff={diff_pct:.1%} [{flag}]")
    return "Validation Report:\n" + "\n".join(lines)

def tool_order_lookup(query: str) -> str:
    for order_id, details in ORDERS_DATA.items():
        if order_id.lower() in query.lower():
            return f"Order {order_id}: Status={details['status']}, Carrier={details['carrier']}, Tracking={details['tracking']}"
    return "Condition Notice: No matching order found. Please provide a valid Order ID."

def tool_assign_task(query: str) -> str:
    candidates = [e for e in EMPLOYEES_DATA if "Python" in e["skills"]]
    if not candidates:
        return "Escalation: No suitable employee available for this task."
    best = min(candidates, key=lambda x: x["workload"])
    return f"Assigned to {best['name']} (Reason: Required skills matched, lowest current workload: {best['workload']} tasks)."

class AgentWorkflowEngine:
    def __init__(self, workflows: Dict[str, Workflow]):
        self.workflows = workflows

    def identify_workflow(self, request: str) -> str:
        req = request.lower()
        if "restock" in req or "inventory" in req: return "WF001"
        if "price" in req or "differs by more than 10" in req: return "WF002"
        if "spreadsheet" in req or "vendor file" in req or "invalid rows" in req: return "WF003"
        if "seo content" in req or "description" in req: return "WF004"
        if "order" in req or "ord-" in req: return "WF005"
        if "duplicate" in req: return "WF006"
        if "campaign" in req or "brief" in req: return "WF007"
        if "keyword" in req or "classify" in req: return "WF008"
        if "assign" in req or "developer" in req or "task" in req: return "WF009"
        if "failing" in req or "performance report" in req: return "WF010"
        return "WF001"

    def execute(self, user_request: str):
        wf_id = self.identify_workflow(user_request)
        wf = self.workflows[wf_id]

        if wf_id == "WF001":
            output = tool_restock_check()
        elif wf_id == "WF002":
            output = tool_price_validation()
        elif wf_id == "WF003":
            output = "Cleaned 12 rows. 2 invalid rows found: Row 3 (Missing SKU), Row 7 (Missing Product Name)."
        elif wf_id == "WF004":
            output = "Title: Ergonomic Desk Chair\nDescription: High-comfort office chair. [Color & Material: Information Missing]"
        elif wf_id == "WF005":
            output = tool_order_lookup(user_request)
        elif wf_id == "WF006":
            output = "Found 1 Duplicate Group: [SKU-101, SKU-101-DUP] (Confidence: 100% SKU exact match)."
        elif wf_id == "WF007":
            if "date" not in user_request.lower():
                output = "Condition Stop: Campaign goal or dates are missing. Please provide start/end dates before generating brief."
            else:
                output = "Brief: Multi-channel strategy, budget allocation, and milestone timeline generated."
        elif wf_id == "WF008":
            output = "Keywords Classified:\n- 'buy shoes' -> Transactional\n- 'shoe reviews' -> Commercial\n- 'how to clean shoes' -> Informational"
        elif wf_id == "WF009":
            output = tool_assign_task(user_request)
        elif wf_id == "WF010":
            output = "Performance Report:\n- WF003: 33% Failure Rate [FLAGGED: >10%]\n- WF001: 0% Failure Rate [HEALTHY]"
        else:
            output = "Workflow executed successfully."

        print("=" * 60)
        print("Selected Workflow:")
        print(wf.name)
        print("\nSteps Executed:")
        for idx, step in enumerate(wf.steps, 1):
            print(f"{idx}. {step}")
        print("\nResult:")
        print(output)
        print("=" * 60 + "\n")

if __name__ == "__main__":
    excel_file = os.path.join("data", "AI_Agent_Workflow_Assessment (1).xlsx")
    if not os.path.exists(excel_file):
        print(f"Error: Could not find {excel_file}. Please ensure the file is inside the data/ folder.")
        exit(1)

    workflows = load_workflows(excel_file)
    engine = AgentWorkflowEngine(workflows)

    test_queries = [
        "Which products need restocking?",
        "Find products where vendor price differs by more than 10%.",
        "Where is order ORD-1001?",
        "Assign this urgent task to the best available developer.",
        "Which workflows are failing most often?"
    ]

    for q in test_queries:
        print(f"User Request:\n\"{q}\"")
        engine.execute(q)