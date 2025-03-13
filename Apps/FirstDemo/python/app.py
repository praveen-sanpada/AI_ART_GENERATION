from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from diffusers import StableDiffusionPipeline
import torch
import uuid
import os

# Create FastAPI app
app = FastAPI()

# Enable CORS (Allow frontend requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (Change in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static directory for image serving
if not os.path.exists("static"):
    os.makedirs("static")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load Stable Diffusion Model (Optimized for CPU)
pipe = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float32
).to("cpu")

# ✅ Fix safety_checker error
pipe.safety_checker = lambda images, clip_input: (images, [False] * len(images))

@app.get("/generate/")
def generate_image(prompt: str):
    """
    API Endpoint to generate AI images.
    """
    try:
        # Generate image from the prompt
        image = pipe(prompt).images[0]

        # Save the image with a unique filename
        image_id = str(uuid.uuid4())[:8]
        image_path = f"static/{image_id}.png"
        image.save(image_path)

        # Return the full image URL
        return {"message": "Image generated!", "image_path": f"http://127.0.0.1:8000/{image_path}"}
    
    except Exception as e:
        return {"error": str(e)}


# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles
# from diffusers import StableDiffusionPipeline
# import torch
# import uuid
# import os

# # Create FastAPI app
# app = FastAPI()

# # Enable CORS to allow frontend requests
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allows all origins (change to specific frontend URL in production)
#     allow_credentials=True,
#     allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
#     allow_headers=["*"],  # Allows all headers
# )

# # Mount directory for serving images
# if not os.path.exists("static"):
#     os.makedirs("static")
# app.mount("/static", StaticFiles(directory="static"), name="static")

# # Load Stable Diffusion on CPU
# pipe = StableDiffusionPipeline.from_pretrained(
#     "runwayml/stable-diffusion-v1-5",
#     torch_dtype=torch.float32
# ).to("cpu")

# # Disable safety checker (Optional, speeds up generation)
# pipe.safety_checker = lambda images, **kwargs: (images, False)

# @app.get("/generate/")
# def generate_image(prompt: str):
#     """
#     API Endpoint to generate an AI image from a text prompt.
#     """
#     try:
#         # Generate the image from the prompt
#         image = pipe(prompt).images[0]

#         # Save image with a unique filename
#         image_id = str(uuid.uuid4())[:8]  # Generate unique ID
#         image_path = f"static/{image_id}.png"
#         image.save(image_path)

#         # Return the image URL
#         return {"message": "Image generated!", "image_path": f"http://127.0.0.1:8000/{image_path}"}
    
#     except Exception as e:
#         return {"error": str(e)}


# from fastapi import FastAPI
# from fastapi.staticfiles import StaticFiles
# from diffusers import StableDiffusionPipeline
# import torch
# import uuid
# import os

# # Create the FastAPI app
# app = FastAPI()

# # Mount a directory to serve generated images
# if not os.path.exists("static"):
#     os.makedirs("static")
# app.mount("/static", StaticFiles(directory="static"), name="static")

# # Load Stable Diffusion pipeline (Running on CPU)
# pipe = StableDiffusionPipeline.from_pretrained(
#     "runwayml/stable-diffusion-v1-5",
#     torch_dtype=torch.float32  # Optimized for CPU
# ).to("cpu")

# # Disable safety checker (optional - speeds up generation)
# pipe.safety_checker = lambda images, **kwargs: (images, False)

# @app.get("/generate/")
# def generate_image(prompt: str):
#     """
#     API Endpoint to generate an AI image from a text prompt.
#     """
#     try:
#         # Generate image from the prompt
#         image = pipe(prompt).images[0]

#         # Save image with a unique filename
#         image_id = str(uuid.uuid4())[:8]  # Generate unique ID
#         image_path = f"static/{image_id}.png"
#         image.save(image_path)

#         # Return image URL
#         return {"message": "Image generated!", "image_path": f"http://127.0.0.1:8000/{image_path}"}
    
#     except Exception as e:
#         return {"error": str(e)}


# from fastapi import FastAPI
# from diffusers import StableDiffusionPipeline
# import torch

# app = FastAPI()
# # pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5").to("cuda")
# pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5").to("cpu")


# @app.get("/generate/")
# def generate_image(prompt: str):
#     image = pipe(prompt).images[0]
#     image.save("output.png")
#     return {"message": "Image generated!", "image_path": "output.png"}
