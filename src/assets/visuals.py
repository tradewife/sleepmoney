import os
import random
from typing import List
from PIL import Image, ImageDraw, ImageFont
from rich.console import Console

console = Console()

class VisualGenerator:
    def __init__(self, output_dir="output/images"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def generate_prompts(self, script_text: str, count: int = 5) -> List[str]:
        """
        Derive image prompts from the script.
        """
        console.print("[cyan]Deriving visual prompts from script...[/cyan]")
        # Mock logic
        prompts = [
            "A fast flowing river in a dark forest, cinematic lighting, photorealistic, 8k",
            "Ancient library with dust motes dancing in light beams, cozy, 8k",
            "Starry night sky over a desert canyon, time lapse style, 8k",
            "Soft clouds moving over a mountain peak during sunset, 8k",
            "Candle flickering on a wooden table, macro shot, bokeh, 8k"
        ]
        return prompts[:count]

    def create_images(self, prompts: List[str]) -> List[str]:
        """
        Generate images from prompts.
        """
        console.print(f"[cyan]Generating {len(prompts)} images...[/cyan]")
        image_paths = []
        
        for i, prompt in enumerate(prompts):
            # SIMULATION: Generate a placeholder image using Pillow
            # In production, call your AI Image Gen API here
            filename = f"image_{i}.png"
            path = os.path.join(self.output_dir, filename)
            
            self._generate_placeholder(path, prompt)
            image_paths.append(path)
            console.print(f"  Generated: {path}")
            
        return image_paths

    def _generate_placeholder(self, path: str, prompt: str):
        """
        Create a 'Greybox' placeholder with the prompt text.
        """
        width, height = 1920, 1080
        # Dark soothing background
        color = (20, 24, 40)
        img = Image.new('RGB', (width, height), color=color)
        d = ImageDraw.Draw(img)
        
        # Draw some soothing circles
        for _ in range(5):
            x = random.randint(0, width)
            y = random.randint(0, height)
            r = random.randint(200, 500)
            d.ellipse((x-r, y-r, x+r, y+r), fill=(30, 36, 60))

        # Attempt to draw text (simple word wrap)
        # Load default font if possible, else basic
        try:
             # Try to load a font, or use default
             font = ImageFont.load_default()
             # Scale isn't easily possible with load_default, but let's try
        except:
             font = None
             
        # Simple text drawing (center roughly)
        text_color = (200, 200, 220)
        # Wrap text manually
        words = prompt.split()
        lines = []
        current_line = []
        for word in words:
            current_line.append(word)
            if len(" ".join(current_line)) > 50: # arbitrary char limit
                lines.append(" ".join(current_line))
                current_line = []
        if current_line:
            lines.append(" ".join(current_line))
            
        y_text = height // 2 - (len(lines) * 15)
        for line in lines:
            # We can't easily center without font metrics, so just standard offset
            d.text((width//4, y_text), line, fill=text_color)
            y_text += 20
            
        d.rectangle([10, 10, width-10, height-10], outline=(100, 100, 150), width=5)
        
        img.save(path)

