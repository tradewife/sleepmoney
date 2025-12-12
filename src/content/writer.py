import time
from typing import List, Dict
from pydantic import BaseModel
from rich.console import Console
from src.content.harvester import Fact

console = Console()

class ScriptSection(BaseModel):
    title: str
    fact_ids: List[str]
    content: str = ""

class ScriptWriter:
    def __init__(self):
        pass

    def create_outline(self, facts: List[Fact]) -> List[ScriptSection]:
        """
        Organize facts into sections.
        """
        console.print("[cyan]Creating script outline...[/cyan]")
        # Simple grouping for mock
        sections = []
        chunk_size = 5
        for i in range(0, len(facts), chunk_size):
            chunk = facts[i:i+chunk_size]
            sections.append(ScriptSection(
                title=f"Chapter {len(sections)+1}: The relaxing nature of {chunk[0].tags[0]}",
                fact_ids=[f.id for f in chunk]
            ))
        return sections

    def write_script(self, sections: List[ScriptSection], facts: List[Fact]) -> str:
        """
        Generate the full script text.
        """
        console.print("[cyan]Writing full script...[/cyan]")
        full_script = "TITLE: A Journey into Sleep\n\n"
        
        fact_map = {f.id: f for f in facts}
        
        for section in sections:
            console.print(f"  Writing section: {section.title}")
            full_script += f"## {section.title}\n\n"
            # Simulate writing narrative
            section_text = "Welcome to this chapter. Let us explore... "
            for fid in section.fact_ids:
                fact = fact_map.get(fid)
                if fact:
                    section_text += f"{fact.text} "
            section_text += "And as we reflect on this, we feel calmer...\n\n"
            
            section.content = section_text
            full_script += section_text
            time.sleep(0.2)
            
        return full_script
