import os
from gtts import gTTS
from rich.console import Console

console = Console()

class AudioEngine:
    def __init__(self, output_dir="output/audio"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def generate_tts(self, script_path: str) -> str:
        """
        Convert script file to audio.
        """
        console.print(f"[cyan]Generating TTS from {script_path}...[/cyan]")
        
        with open(script_path, "r") as f:
            text = f.read()

        # Simple cleanup (remove markdown headers)
        clean_text = "\n".join([line for line in text.splitlines() if not line.startswith("##") and not line.startswith("TITLE:")])
        
        # Determine output path
        base_name = os.path.splitext(os.path.basename(script_path))[0]
        output_file = os.path.join(self.output_dir, f"{base_name}.mp3")
        
        if not text.strip():
            console.print("[red]Script is empty![/red]")
            return ""

        # Use gTTS
        tts = gTTS(text=clean_text[:5000], lang='en', slow=False) # Limit chars for demo speed
        tts.save(output_file)
        
        console.print(f"[green]Audio saved to: {output_file}[/green]")
        return output_file

    def get_music(self, mood: str = "ambient") -> str:
        """
        Get a music track.
        """
        console.print(f"[cyan]Fetching {mood} background music...[/cyan]")
        # Mock: Ensure a dummy wav exists
        music_path = os.path.join(self.output_dir, "background_loop.mp3")
        if not os.path.exists(music_path):
            console.print("[yellow]No music found, creating silent placeholder...[/yellow]")
            # Just create an empty file or rely on user providing it.
            # For a real harness, we'd download from Pixabay API 
            pass 
        return music_path
