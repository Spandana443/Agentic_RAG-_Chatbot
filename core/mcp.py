# core/mcp.py

from dataclasses import dataclass
from typing import Dict, Any
import uuid

@dataclass
class MCPMessage:
    sender: str
    receiver: str
    type: str
    trace_id: str
    payload: Dict[str, Any]

def create_message(sender: str, receiver: str, type_: str, payload: Dict[str, Any]) -> MCPMessage:
    """
    Utility to create a new MCP message.
    """
    return MCPMessage(
        sender=sender,
        receiver=receiver,
        type=type_,
        trace_id=str(uuid.uuid4()),
        payload=payload
    )
