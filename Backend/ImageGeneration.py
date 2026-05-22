import asyncio
from random import randint
from PIL import Image
import requests
from dotenv import load_dotenv
import os
from time import sleep
import replicate

# -------------------- LOAD ENV --------------------
load_dotenv()
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")

if not REPLICATE_API_TOKEN:
    raise ValueError("REPLICATE_API_TOKEN not found in .env")

os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

# -------------------- OPEN IMAGES --------------------
def open_images(prompt):
    folder_path = "Data"
    prompt = prompt.replace(" ", "_")

    files = [f"{prompt}{i}.png" for i in range(1, 5)]

    for file in files:
        image_path = os.path.join(folder_path, file)

        try:
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            sleep(1)

        except Exception as e:
            print(f"Unable to open {image_path}: {e}")

# -------------------- GENERATE IMAGES (SEQUENTIAL - FIXED) --------------------
def generate_images(prompt: str):
    os.makedirs("Data", exist_ok=True)

    for i in range(1, 5):
        try:
            print(f"Generating image {i}/4...")

            # ✅ Correct working model version
            output = replicate.run(
                "stability-ai/sdxl:39ed52f2a78e934c5c3efefbb1d4f5c2d3a71a2fdfd3e8a2c8b3f4eb9bacf4c3",
                input={
                    "prompt": f"{prompt}, ultra realistic, 4k, cinematic lighting",
                    "seed": randint(0, 1000000)
                }
            )

            if output and len(output) > 0:
                image_url = output[0]

                img_data = requests.get(image_url).content
                file_path = f"Data/{prompt.replace(' ', '_')}{i}.png"

                with open(file_path, "wb") as f:
                    f.write(img_data)

                print(f"Saved: {file_path}")
            else:
                print(f"Failed to generate image {i}")

            # 🔥 IMPORTANT: avoid rate limit (free tier)
            sleep(10)

        except Exception as e:
            print(f"Error generating image {i}:", e)
            sleep(10)

# -------------------- MAIN WRAPPER --------------------
def GenerateImages(prompt: str):
    generate_images(prompt)
    open_images(prompt)

# -------------------- MAIN LOOP --------------------
while True:
    try:
        file_path = r"Frontend\Files\ImageGeneration.data"

        if not os.path.exists(file_path):
            sleep(1)
            continue

        with open(file_path, "r") as f:
            data = f.read().strip()

        if not data or "," not in data:
            sleep(1)
            continue

        prompt, status = data.rsplit(",", 1)

        if status.strip() == "True":
            print("Generating Images...")
            GenerateImages(prompt.strip())

            # Reset trigger
            with open(file_path, "w") as f:
                f.write("False,False")

        else:
            sleep(1)

    except Exception as e:
        print("Error:", e)
        sleep(2)