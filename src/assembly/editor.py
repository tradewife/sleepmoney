import os
import math
import random
import ffmpeg
from typing import List
from rich.console import Console

console = Console()

class VideoEditor:
    def __init__(self, output_dir="output/video"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def assemble_video(self, image_paths: List[str], voiceover_path: str, output_filename="final_video.mp4"):
        """
        Combine voiceover, looped images, and background music.
        """
        console.print("[cyan]Starting video assembly...[/cyan]")
        
        if not image_paths:
             console.print("[red]No images provided![/red]")
             return
        
        # 1. Get Audio Duration
        try:
            probe = ffmpeg.probe(voiceover_path)
            audio_duration = float(probe['format']['duration'])
        except Exception as e:
            console.print(f"[red]Error probing audio (is ffmpeg installed?): {e}[/red]")
            # Fallback for mock if ffmpeg missing
            audio_duration = 10.0 

        console.print(f"  Audio Duration: {audio_duration:.2f}s")

        # 2. Plan Image Timeline
        # Simple Logic: Cycle images evenly
        num_images = len(image_paths)
        if num_images == 0:
            console.print("[red]No images to assemble.[/red]")
            return

        # Create a complex filter for slideshow
        # For simplicity in this harness version, we might just use a loop of the first image 
        # or concatenation. Let's try to do a crossfade loop if possible, or just a simple concatenation.
        
        # HARNESS SIMPLIFICATION:
        # Create a slide list text file for ffmpeg concat demuxer if we simply want cuts
        # BUT `ffmpeg-python` is better for programmatic.
        
        # Let's adjust input streams
        # Calculate how long each image should show to cover the audio
        # If we have 5 images and 100s audio -> 20s each.
        
        img_duration = audio_duration / num_images
        
        inputs = []
        for img_path in image_paths:
            # Loop each image for img_duration
            inputs.append(
                ffmpeg.input(img_path, loop=1, t=img_duration)
                .filter('scale', 1920, 1080)
                .filter('setsar', 1, 1)
            )
            
        # Concat video streams
        video_stream = ffmpeg.concat(*inputs)
        
        # Audio stream
        audio_stream = ffmpeg.input(voiceover_path)
        
        # Output path
        output_path = os.path.join(self.output_dir, output_filename)
        
        console.print(f"  Rendering to {output_path} (this may take time)...")
        
        try:
            (
                ffmpeg
                .output(video_stream, audio_stream, output_path, vcodec='libx264', acodec='aac', shortest=None)
                .overwrite_output()
                .run(quiet=True)
            )
            console.print(f"[bold green]Video rendered successfully: {output_path}[/bold green]")
            return output_path
        except ffmpeg.Error as e:
             console.print(f"[red]FFmpeg Error:[/red]")
             # console.print(e.stderr.decode('utf8'))
             return None
        except Exception as e:
             console.print(f"[red]Assembly Error: {e}[/red]")
             return None

