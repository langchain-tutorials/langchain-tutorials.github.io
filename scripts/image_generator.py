"""Multi-provider image generator (Pexels, Unsplash, Google Imagen 3, Pollinations Flux, Freepik) with automatic fallback and WebP compression"""
import os
import sys
import time
import random
import urllib.parse
import requests
from io import BytesIO
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import (
    GEMINI_API_KEY, FREEPIK_API_KEY, FREEPIK_ENDPOINT, POLLINATIONS_API_KEY,
    PEXELS_API_KEY, UNSPLASH_ACCESS_KEY,
    IMAGE_QUALITY, IMAGE_MAX_WIDTH, IMAGE_MAX_HEIGHT, OPTIMIZE_IMAGE
)
from google import genai

client = None
if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)


def get_genai_client():
    global client
    if client is None and GEMINI_API_KEY:
        client = genai.Client(api_key=GEMINI_API_KEY)
    return client


def generate_image_featured(prompt, output_path, keywords=None):
    """
    Generate or fetch high-quality featured image using the best available provider:
    1. Pexels API (Commercial Stock Photography - if PEXELS_API_KEY configured)
    2. Unsplash API (Commercial Stock Photography - if UNSPLASH_ACCESS_KEY configured)
    3. Google Imagen 3 (via GEMINI_API_KEY)
    4. Pollinations.ai (Flux with API Key authentication)
    5. Freepik AI (if FREEPIK_API_KEY is configured and valid)
    """
    print(f"\n🎨 Starting Image Retrieval/Generation for: {output_path}")

    # Method 1: Try Pexels Free Stock Photos
    if PEXELS_API_KEY and keywords:
        try:
            print("📸 Trying Provider 1: Pexels Commercial Stock API...")
            if fetch_image_pexels(keywords, output_path):
                return output_path
        except Exception as e:
            print(f"ℹ️ Pexels API skipped/failed: {e}")

    # Method 2: Try Unsplash Free Stock Photos
    if UNSPLASH_ACCESS_KEY and keywords:
        try:
            print("📸 Trying Provider 2: Unsplash Commercial Stock API...")
            if fetch_image_unsplash(keywords, output_path):
                return output_path
        except Exception as e:
            print(f"ℹ️ Unsplash API skipped/failed: {e}")

    print(f"📝 AI Prompt: {prompt[:120]}...")

    # Method 3: Try Google Imagen 3 via Gemini API
    if GEMINI_API_KEY:
        try:
            print("🚀 Trying Provider 3: Google Imagen 3...")
            ai_client = get_genai_client()
            if ai_client:
                result = ai_client.models.generate_images(
                    model='imagen-3.0-generate-002',
                    prompt=prompt,
                    config=dict(
                        number_of_images=1,
                        aspect_ratio='16:9',
                        output_mime_type='image/jpeg'
                    )
                )
                if result.generated_images:
                    image_bytes = result.generated_images[0].image.image_bytes
                    save_and_compress_image_bytes(image_bytes, output_path)
                    print("✅ Image successfully generated with Google Imagen 3!")
                    return output_path
        except Exception as e:
            print(f"ℹ️ Google Imagen 3 unavailable or failed: {e}")

    # Method 4: Try Pollinations AI (Flux with API Key authentication)
    try:
        masked_key = f"{POLLINATIONS_API_KEY[:7]}...{POLLINATIONS_API_KEY[-4:]}" if POLLINATIONS_API_KEY else "None"
        print(f"🚀 Trying Provider 4: Pollinations AI (Flux | Key: {masked_key})...")
        generate_image_pollinations(prompt, output_path)
        print("✅ Image successfully generated with Pollinations AI (Flux)!")
        return output_path
    except Exception as e:
        print(f"ℹ️ Pollinations AI failed ({e}), falling back to Freepik AI...")

    # Method 5: Try Freepik if key is provided
    if FREEPIK_API_KEY:
        try:
            print("🚀 Trying Provider 5: Freepik AI...")
            generate_image_freepik_direct(prompt, output_path)
            print("✅ Image successfully generated with Freepik AI!")
            return output_path
        except Exception as e:
            print(f"❌ Freepik API failed: {e}")

    # Method 6: Procedural modern tech banner fallback
    print("🚀 Trying Provider 6: Procedural Tech Banner fallback...")
    res = generate_fallback_tech_image(output_path)
    if res:
        return output_path

    raise RuntimeError(f"All image providers failed for: {output_path}")


def generate_fallback_tech_image(output_path):
    """Fallback generator that creates a modern dark-themed developer banner using Pillow"""
    try:
        from PIL import ImageDraw
        width, height = 1280, 720
        # Dark tech background (#0f172a slate-900)
        img = Image.new("RGB", (width, height), color=(15, 23, 42))
        draw = ImageDraw.Draw(img)

        # Draw subtle tech grid
        for x in range(0, width, 40):
            draw.line([(x, 0), (x, height)], fill=(30, 41, 59), width=1)
        for y in range(0, height, 40):
            draw.line([(0, y), (width, y)], fill=(30, 41, 59), width=1)

        # Draw central glowing circuit node / geometric accents
        cx, cy = width // 2, height // 2
        for r in range(180, 40, -30):
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(56, 189, 248), width=2)
        draw.ellipse([cx - 40, cy - 40, cx + 40, cy + 40], fill=(14, 165, 233))

        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
        img.save(output_path, "WEBP", quality=85)
        print(f"✅ Generated high-quality procedural tech banner: {output_path}")
        return output_path
    except Exception as e:
        print(f"⚠️ Procedural banner error: {e}")
        return None


def fetch_image_pexels(keywords, output_path):
    """Fetch commercial stock photo from Pexels API"""
    if not PEXELS_API_KEY:
        return False

    headers = {"Authorization": PEXELS_API_KEY}
    search_list = keywords if isinstance(keywords, list) else [keywords]

    for kw in search_list:
        if not kw or len(kw.strip()) < 2:
            continue
        try:
            clean_kw = kw.strip()
            print(f"🔎 Searching Pexels for: '{clean_kw}'...")
            url = f"https://api.pexels.com/v1/search?query={urllib.parse.quote(clean_kw)}&orientation=landscape&size=large&per_page=5"
            res = requests.get(url, headers=headers, timeout=15)
            if res.status_code == 200:
                data = res.json()
                photos = data.get("photos", [])
                if photos:
                    img_url = photos[0]["src"].get("large2x") or photos[0]["src"].get("landscape") or photos[0]["src"].get("large")
                    if img_url:
                        img_res = requests.get(img_url, timeout=30)
                        img_res.raise_for_status()
                        save_and_compress_image_bytes(img_res.content, output_path)
                        print(f"✅ Found and downloaded high-res Pexels photo for '{clean_kw}'!")
                        return True
        except Exception as e:
            print(f"⚠️ Pexels search for '{kw}' failed: {e}")
    return False


def fetch_image_unsplash(keywords, output_path):
    """Fetch commercial stock photo from Unsplash API"""
    if not UNSPLASH_ACCESS_KEY:
        return False

    headers = {"Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"}
    search_list = keywords if isinstance(keywords, list) else [keywords]

    for kw in search_list:
        if not kw or len(kw.strip()) < 2:
            continue
        try:
            clean_kw = kw.strip()
            print(f"🔎 Searching Unsplash for: '{clean_kw}'...")
            url = f"https://api.unsplash.com/search/photos?query={urllib.parse.quote(clean_kw)}&orientation=landscape&per_page=5"
            res = requests.get(url, headers=headers, timeout=15)
            if res.status_code == 200:
                data = res.json()
                results = data.get("results", [])
                if results:
                    img_url = results[0]["urls"].get("regular") or results[0]["urls"].get("full")
                    if img_url:
                        img_res = requests.get(img_url, timeout=30)
                        img_res.raise_for_status()
                        save_and_compress_image_bytes(img_res.content, output_path)
                        print(f"✅ Found and downloaded high-res Unsplash photo for '{clean_kw}'!")
                        return True
        except Exception as e:
            print(f"⚠️ Unsplash search for '{kw}' failed: {e}")
    return False


def generate_image_pollinations(prompt, output_path):
    """Generate image via Pollinations.ai (Flux model with API Key and random seed)"""
    clean_prompt = prompt.replace('\n', ' ').strip()
    encoded = urllib.parse.quote(clean_prompt)
    seed = random.randint(1, 999999999)

    url = f"https://image.pollinations.ai/prompt/{encoded}?width=1280&height=720&nologo=true&model=flux&seed={seed}"
    if POLLINATIONS_API_KEY:
        url += f"&key={POLLINATIONS_API_KEY}"

    print(f"📥 Requesting image from Pollinations.ai (Flux, Seed: {seed})...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    }
    if POLLINATIONS_API_KEY:
        headers['Authorization'] = f'Bearer {POLLINATIONS_API_KEY}'

    response = requests.get(url, headers=headers, timeout=90)
    response.raise_for_status()

    if len(response.content) < 1000:
        raise ValueError(f"Received invalid/empty image response from Pollinations ({len(response.content)} bytes)")

    save_and_compress_image_bytes(response.content, output_path)


def generate_image_freepik_direct(prompt, output_path):
    """Generate image using Freepik AI with polling"""
    headers = {
        "x-freepik-api-key": FREEPIK_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": prompt,
        "num_images": 1,
        "image": {"size": "1920x1080"},
        "aspect_ratio": "widescreen_16_9"
    }

    response = requests.post(FREEPIK_ENDPOINT, headers=headers, json=payload, timeout=60)
    if response.status_code == 401:
        raise Exception("Invalid Freepik API key")
    if response.status_code == 402:
        raise Exception("Freepik API credits exhausted")
    response.raise_for_status()

    data = response.json()
    task_id = data.get("data", {}).get("task_id")
    if not task_id:
        raise Exception(f"No task_id in response: {data}")

    image_url = poll_for_freepik_image(task_id, headers)
    img_response = requests.get(image_url, timeout=60)
    img_response.raise_for_status()

    save_and_compress_image_bytes(img_response.content, output_path)


def poll_for_freepik_image(task_id, headers, max_attempts=30):
    """Poll Freepik API until image is ready"""
    for attempt in range(1, max_attempts + 1):
        time.sleep(4)
        status_url = f"https://api.freepik.com/v1/ai/text-to-image/flux-dev/{task_id}"
        status_response = requests.get(status_url, headers=headers, timeout=30)
        status_response.raise_for_status()

        status_data = status_response.json()
        status = status_data.get("data", {}).get("status")

        if status == "COMPLETED":
            generated = status_data["data"].get("generated", [])
            if isinstance(generated, list) and len(generated) > 0:
                image_url = generated[0] if isinstance(generated[0], str) else generated[0].get("url")
                if image_url:
                    return image_url
            raise Exception("No URL in completed Freepik response")
        elif status == "FAILED":
            error_msg = status_data["data"].get("error", "Unknown error")
            raise Exception(f"Freepik generation failed: {error_msg}")

    raise Exception("Freepik generation timed out")


def save_and_compress_image_bytes(image_bytes, output_path):
    """Process and compress raw image bytes to optimized WebP"""
    os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
    img = Image.open(BytesIO(image_bytes)).convert("RGB")

    original_size = len(image_bytes)
    original_width, original_height = img.size
    print(f"📊 Original: {original_width}x{original_height}, {original_size / 1024:.1f} KB")

    # Resize if needed
    if original_width > IMAGE_MAX_WIDTH or original_height > IMAGE_MAX_HEIGHT:
        img.thumbnail((IMAGE_MAX_WIDTH, IMAGE_MAX_HEIGHT), Image.Resampling.LANCZOS)
        new_width, new_height = img.size
        print(f"🔧 Resized to: {new_width}x{new_height}")

    # Save as compressed WebP
    if OPTIMIZE_IMAGE:
        img.save(output_path, "WEBP", quality=IMAGE_QUALITY, method=6, optimize=True)
    else:
        img.save(output_path, "WEBP", quality=IMAGE_QUALITY)

    compressed_size = os.path.getsize(output_path)
    savings = (1 - compressed_size / original_size) * 100 if original_size > 0 else 0
    print(f"💾 Saved WebP: {output_path} ({compressed_size / 1024:.1f} KB, saved {savings:.1f}%)")


# Backward compatibility alias
def generate_image_freepik(prompt, output_path):
    return generate_image_featured(prompt, output_path)
