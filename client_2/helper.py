import hashlib
import random
import os
import string
import socket
import struct

from PIL import (
    Image, 
    ImageDraw,
    ImageFont
)

def draw_on_image(text: str) -> str:
    """Function for drawing text on an image""" 
    img = Image.open("white.png")

    # Create an object ImageDraw to draw on the image
    draw = ImageDraw.Draw(img)

    # Font for text
    font = ImageFont.truetype("arial.ttf", 30)

    # coords of the text
    x = (img.width // 2) - 100
    y = img.height // 2

    draw.text((x, y), text, fill="black", font=font)

    # Generate hash to call output image
    output_hash = generate_md5_hash(text) + random.choice(string.ascii_letters + string.ascii_uppercase)
    output_image_name = f"message_{output_hash}.png"
    img.save(output_image_name)
    
    return output_image_name

def generate_md5_hash(text: str) -> str:
    """Generate md5 hash"""
    return hashlib.md5(text.encode()).hexdigest()

def read_file(filename: str) -> bytes:
    """Read bytes from file"""
    with open(filename, "rb") as file:
        image_data = file.read()
    return image_data

def compose_image_from_bytes(path_dir: str, image_data: bytes) -> None:
    """Save image data to a file"""

    base_path = os.path.abspath(".")
    filename = f"received_message_{random.randint(1, 19999999999999999)}.png"
    full_path = os.path.join(base_path, filename)
    try:
        with open(full_path, "wb") as file:
            file.write(image_data)
        print("Image successfully saved as received_message.png")
    except Exception as e:
        print(f"Failed to save image: {e}")

def get_image_data(client_socket: socket.socket) -> bytes:
    """Getting bytes of image"""
    image_data = b""
    while True:
        chunk = client_socket.recv(4096)
        if not chunk:
            break
        image_data += chunk
    return image_data
