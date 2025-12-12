import argparse
import sys
from rich.console import Console
from rich.panel import Panel

console = Console()

def main():
    parser = argparse.ArgumentParser(description="SleepMoney: Automated Sleep Video Generator")
    subparsers = parser.add_subparsers(dest="command", help="Available stages")

    # Stage 1: Discovery
    discovery_parser = subparsers.add_parser("discover", help="Find video topics")
    discovery_parser.add_argument("--topics", nargs="+", help="List of base topics to explore", default=["psychology", "history", "space"])

    # Stage 2: Content
    content_parser = subparsers.add_parser("content", help="Generate facts and script")
    content_parser.add_argument("--niche", required=True, help="Selected niche/subtopic")

    # Stage 3: Assets
    assets_parser = subparsers.add_parser("assets", help="Generate/fetch visuals and audio")
    assets_parser.add_argument("--script", help="Path to script file")

    # Stage 4: Assembly
    assembly_parser = subparsers.add_parser("assemble", help="Combine assets into final video")
    
    args = parser.parse_args()

    if args.command == "discover":
        console.print(Panel(f"Starting Discovery for: {args.topics}", title="Stage 1: Discovery"))
        from src.discovery.engine import DiscoveryEngine
        engine = DiscoveryEngine()
        
        # 1. Discover base niches
        niches = engine.discover_base_niches(args.topics)
        
        # 2. Identify winners
        winners = engine.identify_winners(niches)
        
        console.print("\n[bold green]Top Niches Found:[/bold green]")
        for i, niche in enumerate(winners[:3]):
            console.print(f"{i+1}. {niche.category} (Avg Views: {niche.avg_views:,}, Score: {niche.competition_score:.2f})")
            
        # 3. Drill down into the clear winner
        best = winners[0]
        console.print(f"\n[bold]Drilling into best candidate: {best.category}[/bold]")
        subniches = engine.generate_subniche_hypotheses(best)
        
        valid_gaps = []
        for sub in subniches:
            res = engine.validate_subniche_gap(sub)
            if res["is_gap"]:
                valid_gaps.append(res)
                console.print(f"  [green]FOUND GAP:[/green] {sub}")
            else:
                console.print(f"  [red]SATURATED:[/red] {sub}")

    elif args.command == "content":
        console.print(Panel(f"Generating Content for: {args.niche}", title="Stage 2: Content"))
        
        from src.content.harvester import ContentHarvester
        from src.content.narrative_engine import NarrativeEngine
        
        # 1. Harvest Facts
        harvester = ContentHarvester()
        facts = harvester.harvest_facts(args.niche, count=15)
        clean_facts = harvester.deduplicate_and_score(facts)
        console.print(f"[green]Harvested {len(clean_facts)} valid facts.[/green]")
        
        # 2. Narrative Engine (Architect -> Weaver)
        engine = NarrativeEngine()
        sections = engine.create_structured_outline(clean_facts)
        script_text = engine.write_narrative(sections, clean_facts)
        
        # Save script
        output_path = f"output/script_{args.niche.replace(' ', '_')}.txt"
        with open(output_path, "w") as f:
            f.write(script_text)
            
        console.print(f"[bold green]Hypnotic Script generated successfully at: {output_path}[/bold green]")

    elif args.command == "assets":
        console.print(Panel("Generating Assets...", title="Stage 3: Assets"))
        
        from src.assets.visuals import VisualGenerator
        from src.assets.audio import AudioEngine
        
        # 0. Check Input
        if not args.script:
             console.print("[red]Please provide --script path[/red]")
             return
             
        # 1. Visuals
        viz = VisualGenerator()
        # Read script to get context for prompts
        with open(args.script, 'r') as f:
            script_content = f.read()
            
        prompts = viz.generate_prompts(script_content)
        images = viz.create_images(prompts)
        
        # 2. Audio
        audio = AudioEngine()
        voiceover_path = audio.generate_tts(args.script)
        
        console.print("[bold green]Assets Ready![/bold green]")
        console.print(f"  Images: {len(images)}")
        console.print(f"  Voiceover: {voiceover_path}")

    elif args.command == "assemble":
        console.print(Panel("Assembling Video...", title="Stage 4: Assembly"))
        
        from src.assembly.editor import VideoEditor
        
        # For this harness, valid inputs would ideally come from a state file or args.
        # But let's assume standard paths for the demo based on previous steps default output.
        # We need to explicitly ask for inputs in a real app, but I'll scan the output dir for now.
        
        import glob
        
        images = sorted(glob.glob("output/images/*.png"))
        voiceovers = sorted(glob.glob("output/audio/*.mp3"))
        
        if not images or not voiceovers:
             console.print("[red]Missing assets! Please run 'assets' stage first.[/red]")
             return

        editor = VideoEditor()
        # Use first voiceover found
        editor.assemble_video(images, voiceovers[0])

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
