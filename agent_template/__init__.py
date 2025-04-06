"""
Agent Template

Framework mẫu để xây dựng các agent tương tác với LLM.
"""

__version__ = "1.0.0"
__author__ = "Agent Template Team"

from agent_template.core.agent import agent, process_input
from agent_template.memory.persistence import (
    save_memory, 
    load_memory, 
    list_conversations, 
    create_new_thread,
    delete_conversation,
    Memory,
    Message
)
from agent_template.tools.logo import get_logo, display_logo, LogoResult
from agent_template.workflows.graph import process_with_graph, create_workflow

__version__ = "0.1.0" 