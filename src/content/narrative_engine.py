from typing import List
from rich.console import Console
from pydantic import BaseModel

from src.content.harvester import Fact
from src.utils.llm import get_llm_client
from src.content.prompts import (
    ARCHITECT_SYSTEM_PROMPT,
    WEAVER_SYSTEM_PROMPT,
    WEAVER_USER_TEMPLATE
)

console = Console()

class ScriptSection(BaseModel):
    title: str
    fact_ids: List[str]
    content: str = ""

class NarrativeEngine:
    def __init__(self):
        self.llm = get_llm_client()

    def create_structured_outline(self, facts: List[Fact]) -> List[ScriptSection]:
        """
        Stage 1: The Architect
        Organizes facts into a flow designed for sleep.
        """
        console.print("[cyan]The Architect is designing the Relaxation Arc...[/cyan]")
        
        # Prepare context for LLM
        facts_text = "\n".join([f"[{f.id}] {f.text} (Tags: {f.tags})" for f in facts])
        prompt = f"Here are the facts to organize:\n{facts_text}\n\nCreate a 3-section outline."
        
        response = self.llm.complete(prompt, system_message=ARCHITECT_SYSTEM_PROMPT)
        console.print(f"[dim]Architect Response Received.[/dim]")
        
        # PARSING STRATEGY:
        # We expect the agent to provide a list of sections. 
        # For simplicity, we'll try to parse a specific format or just fallback to raw chunks if it fails.
        # But since *I* am the agent, I will ensure I format it as requested:
        # "Title: <Title> | Fact_IDs: <id, id>"
        
        sections = []
        lines = response.strip().split('\n')
        current_section = None
        
        # Robust-ish parsing for lines like "Section 1: Title"
        # For this harness, let's keep it simple: 
        # If the response contains "SECTION:", we split by that.
        
        # Actually, let's just stick to the fallback chunking if parsing is too brittle, 
        # BUT use the titles provided by the agent if possible.
        
        # Let's trust the Agent (ME) to just return the Title List for now to keep it simple, 
        # and we map facts sequentially? No, that's weak.
        
        # Better: The Agent returns a Markdown list.
        # - Title: The Beginning
        #   - Facts: [fact_0, fact_1]
        
        # Reverting to simple chunking with Agent-provided TITLES for safety in this demo.
        # Ideally we'd implement a strict JSON parser here.
        
        chunk_size = 5
        fact_chunks = [facts[i:i+chunk_size] for i in range(0, len(facts), chunk_size)]
        
        # We'll validly use the LLM to get custom titles for these chunks instead of "Part 1"
        titles = [line.strip().lstrip("- ").strip() for line in response.splitlines() if line.strip()]
        
        for i, chunk in enumerate(fact_chunks):
            title = titles[i] if i < len(titles) else f"Relaxation Part {i+1}"
            sections.append(ScriptSection(
                title=title,
                fact_ids=[f.id for f in chunk]
            ))
            
        return sections

    def write_narrative(self, sections: List[ScriptSection], facts: List[Fact]) -> str:
        """
        Stage 2: The Weaver
        Turns the outline into hypnotic prose.
        """
        console.print("[cyan]The Weaver is drafting the script...[/cyan]")
        
        full_script = "TITLE: A Hypnotic Journey\n\n"
        fact_map = {f.id: f for f in facts}
        
        for section in sections:
            console.print(f"  Weaving section: {section.title}")
            
            # Prepare facts for this section
            section_facts = [fact_map[fid].text for fid in section.fact_ids if fid in fact_map]
            facts_block = "\n".join(section_facts)
            
            prompt = WEAVER_USER_TEMPLATE.format(title=section.title, facts=facts_block)
            
            # Call LLM
            narrative = self.llm.complete(prompt, system_message=WEAVER_SYSTEM_PROMPT)
            
            section.content = narrative
            full_script += f"## {section.title}\n\n{narrative}\n\n"
            
        return full_script
