# tools/property_tools.py
# These are the AGENTIC TOOLS the AI uses to reason step by step.
# Claude decides which tool to call, Python executes it, result goes back to Claude.

TOOLS = [
    {
        "name": "analyse_customer_situation",
        "description": (
            "Use this tool FIRST for every customer message. "
            "Analyse what the customer's main concern is, what type of property owner they are, "
            "and what their primary need is."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "customer_type": {
                    "type": "string",
                    "enum": ["NRI", "local_owner", "investor", "unknown"],
                    "description": "Type of property owner"
                },
                "primary_concern": {
                    "type": "string",
                    "enum": ["security", "rental", "selling", "documentation", "management", "general"],
                    "description": "Main concern of the customer"
                },
                "property_status": {
                    "type": "string",
                    "enum": ["empty", "self_occupied", "rented", "unknown"],
                    "description": "Current status of the property"
                },
                "urgency": {
                    "type": "string",
                    "enum": ["high", "medium", "low"],
                    "description": "How urgent the situation is"
                },
                "summary": {
                    "type": "string",
                    "description": "One line summary of customer situation"
                }
            },
            "required": ["customer_type", "primary_concern", "property_status", "urgency", "summary"]
        }
    },
    {
        "name": "get_service_recommendations",
        "description": (
            "Fetch the most relevant Sruthi Agency services and generate "
            "a list of recommended options with pros and cons."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "concern_type": {
                    "type": "string",
                    "enum": ["security", "rental", "selling", "documentation", "management", "nri_advisory"],
                    "description": "Type of concern to get services for"
                },
                "options": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "option_name": {"type": "string"},
                            "description": {"type": "string"},
                            "pros": {"type": "array", "items": {"type": "string"}},
                            "cons": {"type": "array", "items": {"type": "string"}},
                            "best_for": {"type": "string"}
                        }
                    },
                    "description": "List of service options with pros and cons"
                }
            },
            "required": ["concern_type", "options"]
        }
    },
    {
        "name": "generate_advisor_response",
        "description": (
            "Craft the final warm, human-like advisor response "
            "that presents options clearly and ends with a call to action."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "opening": {
                    "type": "string",
                    "description": "Empathetic opening acknowledging the customer's situation"
                },
                "recommendations_summary": {
                    "type": "string",
                    "description": "Clear summary of recommended options"
                },
                "closing": {
                    "type": "string",
                    "description": "Closing line — question or CTA to connect with team"
                },
                "suggested_chips": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "2-4 quick reply chips for the customer",
                    "maxItems": 4
                }
            },
            "required": ["opening", "recommendations_summary", "closing", "suggested_chips"]
        }
    },
    {
        "name": "escalate_to_team",
        "description": "Use when customer wants to speak to the team or query is too complex.",
        "input_schema": {
            "type": "object",
            "properties": {
                "reason": {
                    "type": "string",
                    "description": "Why this is being escalated"
                },
                "customer_summary": {
                    "type": "string",
                    "description": "Brief summary of what the customer needs"
                }
            },
            "required": ["reason", "customer_summary"]
        }
    }
]


def execute_tool(tool_name: str, tool_input: dict) -> str:
    """Execute a tool call and return the result back to Claude."""

    if tool_name == "analyse_customer_situation":
        return (
            f"Situation Analysis Complete:\n"
            f"- Customer Type   : {tool_input['customer_type']}\n"
            f"- Primary Concern : {tool_input['primary_concern']}\n"
            f"- Property Status : {tool_input['property_status']}\n"
            f"- Urgency         : {tool_input['urgency']}\n"
            f"- Summary         : {tool_input['summary']}\n\n"
            f"Now call get_service_recommendations for: {tool_input['primary_concern']}"
        )

    elif tool_name == "get_service_recommendations":
        options_text = ""
        for i, opt in enumerate(tool_input.get("options", []), 1):
            pros = ", ".join(opt.get("pros", []))
            cons = ", ".join(opt.get("cons", []))
            options_text += (
                f"\nOption {i}: {opt['option_name']}\n"
                f"  Description : {opt['description']}\n"
                f"  Pros        : {pros}\n"
                f"  Cons        : {cons}\n"
                f"  Best For    : {opt.get('best_for', 'N/A')}\n"
            )
        return (
            f"Recommendations for '{tool_input['concern_type']}':\n"
            f"{options_text}\n"
            f"Now call generate_advisor_response to craft the final reply."
        )

    elif tool_name == "generate_advisor_response":
        return (
            f"Response Ready:\n"
            f"Opening         : {tool_input['opening']}\n"
            f"Recommendations : {tool_input['recommendations_summary']}\n"
            f"Closing         : {tool_input['closing']}\n"
            f"Chips           : {tool_input['suggested_chips']}\n\n"
            f"Now compose the final natural language response using these components."
        )

    elif tool_name == "escalate_to_team":
        return (
            f"Escalation Triggered:\n"
            f"Reason           : {tool_input['reason']}\n"
            f"Customer Summary : {tool_input['customer_summary']}\n\n"
            f"Inform the customer warmly that our team will reach out shortly."
        )

    return f"Tool '{tool_name}' executed."
