from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from diffusers import StableDiffusionPipeline
import torch
import uuid
import os
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
import ffmpeg

# Create FastAPI app
app = FastAPI()

# Enable CORS (For frontend requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static directory for serving files
if not os.path.exists("static"):
    os.makedirs("static")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load Stable Diffusion Model (Optimized for CPU)
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float32
).to("cpu")

# Fix safety checker issue
pipe.safety_checker = lambda images, clip_input: (images, [False] * len(images))


# ✅ IMAGE GENERATION ENDPOINT
@app.get("/generate/")
def generate_image(prompt: str):
    """
    Generate AI-generated image from text prompt.
    """
    try:
        image = pipe(prompt).images[0]

        # Save the image with a unique filename
        image_id = str(uuid.uuid4())[:8]
        image_path = f"static/{image_id}.png"
        image.save(image_path)

        # Return the generated image URL
        return {"message": "Image generated!", "image_path": f"http://127.0.0.1:8000/{image_path}"}
    
    except Exception as e:
        return {"error": str(e)}


# ✅ VIDEO GENERATION ENDPOINT (Image-to-Video)
@app.get("/generate_video/")
def generate_video(prompt: str, num_frames: int = 10, fps: int = 8):
    """
    Generate AI animation by creating multiple frames and converting to video.
    """
    try:
        frame_folder = f"static/{uuid.uuid4()[:8]}"
        os.makedirs(frame_folder, exist_ok=True)

        # Generate multiple frames
        frame_paths = []
        for i in range(num_frames):
            image = pipe(prompt).images[0]
            frame_path = f"{frame_folder}/frame_{i}.png"
            image.save(frame_path)
            frame_paths.append(frame_path)

        # Convert frames to video
        video_path = f"{frame_folder}/output_video.mp4"
        clip = ImageSequenceClip(frame_paths, fps=fps)
        clip.write_videofile(video_path, codec="libx264", fps=fps)

        # Return video URL
        return {"message": "Video generated!", "video_path": f"http://127.0.0.1:8000/{video_path}"}
    
    except Exception as e:
        return {"error": str(e)}


# ✅ TEXT-TO-VIDEO USING RUNWAY ML (Requires API Key)
@app.get("/text_to_video/")
def text_to_video(prompt: str):
    """
    Generate AI-generated video from text prompt using Runway ML.
    """
    import requests

    API_KEY = "YOUR_RUNWAY_ML_API_KEY"  # Get from https://runwayml.com
    url = "https://api.runwayml.com/v1/models/stable-video-diffusion/run"

    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {"prompt": prompt, "motion_bucket_id": "0", "num_inference_steps": 50}

    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        video_url = response.json().get("video_url")
        return {"message": "Text-to-video generated!", "video_url": video_url}
    else:
        return {"error": response.text}
