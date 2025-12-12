import os
import uuid
import time
from abc import ABC, abstractmethod
from rich.console import Console
from rich.panel import Panel

console = Console()

class LLMClient(ABC):
    @abstractmethod
    def complete(self, prompt: str, system_message: str = "") -> str:
        pass

class InteractiveClient(LLMClient):
    """
    Writes prompts to the filesystem and waits for the Agent (User) to provide
    a response in a corresponding file.
    """
    def __init__(self, request_dir="agent_interaction/requests", response_dir="agent_interaction/responses"):
        self.request_dir = request_dir
        self.response_dir = response_dir
        os.makedirs(request_dir, exist_ok=True)
        os.makedirs(response_dir, exist_ok=True)

    def complete(self, prompt: str, system_message: str = "") -> str:
        req_id = str(uuid.uuid4())[:8]
        req_file = os.path.join(self.request_dir, f"req_{req_id}.md")
        resp_file = os.path.join(self.response_dir, f"resp_{req_id}.md")
        
        # 1. Write the Request
        content = f"# System Message\n{system_message}\n\n# User Prompt\n{prompt}"
        with open(req_file, "w") as f:
            f.write(content)
            
        console.print(Panel(
            f"ACTION REQUIRED: Please respond to the prompt.\n"
            f"1. Read: {req_file}\n"
            f"2. Write response to: {resp_file}\n"
            f"3. Press ENTER here when done.",
            title="Agent Handoff",
            style="bold yellow"
        ))
        
        # 2. Block until user signals readiness
        # In a real CLI usage, we use input(). 
        # The Agent controlling this CLI will see the message, write the file, then send newline to stdin.
        input() 
        
        # 3. Read the Response
        if not os.path.exists(resp_file):
            console.print(f"[red]Response file {resp_file} not found![/red]")
            return ""
            
        with open(resp_file, "r") as f:
            response_text = f.read()
            
        console.print(f"[green]Received response from Agent ({len(response_text)} chars).[/green]")
        return response_text

def get_llm_client() -> LLMClient:
    return InteractiveClient()
