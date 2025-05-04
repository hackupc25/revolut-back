import random
from io import BytesIO
import requests
from PIL import Image, ImageDraw, ImageFont
from django.core.files.base import ContentFile


def generate_placeholder_image(coin_name):
    """
    Generate a placeholder image when API image generation is not available.
    """
    try:
        # Create a basic colored circle with text
        width, height = 512, 512
        # Generate a random color for the coin
        color = (
            random.randint(150, 255),  # R
            random.randint(150, 255),  # G
            random.randint(0, 100),    # B
        )
        
        # Create an image with a plain background
        image = Image.new("RGB", (width, height), (30, 30, 30))
        draw = ImageDraw.Draw(image)
        
        # Draw a circle
        circle_radius = width // 3
        circle_center = (width // 2, height // 2)
        circle_bbox = (
            circle_center[0] - circle_radius,
            circle_center[1] - circle_radius,
            circle_center[0] + circle_radius,
            circle_center[1] + circle_radius,
        )
        draw.ellipse(circle_bbox, fill=color)
        
        # Add text
        try:
            # If PIL has access to fonts
            font = ImageFont.truetype("arial.ttf", 36)
        except IOError:
            # Fallback to default font
            font = ImageFont.load_default()
        
        # Add the coin name
        text = coin_name[:10].upper()  # Truncate long names
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        text_position = (
            (width - text_width) // 2,
            (height - text_height) // 2
        )
        draw.text(text_position, text, font=font, fill=(255, 255, 255))
        
        # Save to memory
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        
        # Return as ContentFile
        filename = f"{coin_name.lower().replace(' ', '_')}.png"
        return ContentFile(buffer.getvalue(), name=filename)
    
    except Exception as e:
        print(f"Error generating placeholder image: {e}")
        # Return an even more basic fallback if PIL fails
        return None


def generate_coin_image(coin_name, description=None):
    """
    Generate an image for a coin using Pollinations API.
    If that fails, generate a placeholder image.
    """
    try:
        # Default image parameters
        width = 512
        height = 512
        model = 'flux'
        seed = random.randint(1, 1000)  # Random seed for variety

        # Construct prompt based on coin name and description
        if description:
            prompt = (
                f"photorealistic image of a cryptocurrency coin "
                f"for {coin_name}. {description}. detailed, metallic, "
                f"3D rendering style, high quality."
            )
        else:
            prompt = (
                f"photorealistic image of a cryptocurrency coin "
                f"for {coin_name}. detailed, metallic, 3D rendering "
                f"style, high quality."
            )

        # Construct the Pollinations API URL
        image_url = f"https://pollinations.ai/p/{prompt}?width={width}&height={height}&seed={seed}&model={model}"
        
        # Fetch the image from the URL
        response = requests.get(image_url)
        
        if response.status_code == 200:
            # Image successfully fetched
            filename = f"{coin_name.lower().replace(' ', '_')}.png"
            return ContentFile(response.content, name=filename)
        else:
            print(f"Failed to fetch image from Pollinations API: {response.status_code}")
            return generate_placeholder_image(coin_name)

    except Exception as e:
        print(f"Error generating image: {e}")
        print("Falling back to placeholder image")
        return generate_placeholder_image(coin_name)
