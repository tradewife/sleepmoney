import random
import time
from typing import List, Dict
from pydantic import BaseModel
from rich.console import Console

console = Console()

class Fact(BaseModel):
    id: str
    text: str
    source: str
    tags: List[str]

class ContentHarvester:
    def __init__(self):
        pass

    def harvest_facts(self, subniche: str, count: int = 20) -> List[Fact]:
        """
        Generate facts about the subniche.
        """
        console.print(f"[cyan]Harvesting {count} facts for subniche: {subniche}[/cyan]")
        facts = []
        for i in range(count):
            # SIMULATION: In real app, call Perplexity/LLM
            # Enriched Mock Data
            context_list = ["Ancient History", "Scientific Marvel", "Sensory Detail", "Mythology"]
            tag = random.choice(context_list)
            
            facts.append(Fact(
                id=f"fact_{i}",
                text=f"Did you know that in {subniche}, element {i} emits a gentle frequency similar to white noise? This was discovered by researchers who noted its calming effect on the human mind.",
                source="https://wikipedia.org",
                tags=[tag, "calm"]
            ))
            time.sleep(0.05) # Simulate API latency
        
        return facts

    def deduplicate_and_score(self, facts: List[Fact]) -> List[Fact]:
        """
        Remove duplicates and sort by 'sleepy' score.
        """
        console.print("[yellow]Deduplicating and scoring facts...[/yellow]")
        # Mock logic: just return them all for now
        return facts
