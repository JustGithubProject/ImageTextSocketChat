import hashlib
import random
import string
import socket
import struct
import os

from PIL import Image, ImageDraw, ImageFont

def draw_on_image(text: str) -> str:
    """
    Draws text on an image and saves it.

    Args:
        text (str): Text to draw on the image.

    Returns:
        str: Name of the output image file.
    """
    # Open a blank image
    img = Image.open("white.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", 30)
    
    # Calculate position to center text
    x = (img.width // 2) - 100
    y = img.height // 2
    
    # Draw text on the image
    draw.text((x, y), text, fill="black", font=font)
    
    # Generate a unique output filename using MD5 hash and random character
    output_hash = generate_md5_hash(text) + random.choice(string.ascii_letters + string.ascii_uppercase)
    output_image_name = f"message_{output_hash}.png"
    
    # Save the image
    img.save(output_image_name)
    
    return output_image_name

def generate_md5_hash(text: str) -> str:
    """
    Generates an MD5 hash for a given text.

    Args:
        text (str): Input text to hash.

    Returns:
        str: MD5 hash string.
    """
    return hashlib.md5(text.encode()).hexdigest()

def read_file(filename: str) -> bytes:
    """
    Reads bytes from a file.

    Args:
        filename (str): Path to the file.

    Returns:
        bytes: Bytes read from the file.
    """
    with open(filename, "rb") as file:
        image_data = file.read()
    
    return image_data

def compose_image_from_bytes(image_data: bytes, path) -> None:
    """
    Creates an image from byte data.

    Args:
        image_data (bytes): Byte data of the image.
        path (str): Path to save the output image.
    """
    # Read the first 4 bytes to get the data length
    data_length = struct.unpack("!I", image_data[:4])[0]
    
    # The remaining bytes are image data
    image_bytes = image_data[4:data_length+4]
    
    # Create an image from the bytes
    try:
        with open(path, "wb") as file:
            file.write(image_bytes)
        print("Image successfully composed")
    except Exception as e:
        print(f"Error composing image: {e}")

def get_image_data(client_socket: socket.socket) -> bytes:
    """
    Retrieves image data from a socket.

    Args:
        client_socket (socket.socket): Socket connected to the client.

    Returns:
        bytes: Image data received from the socket.
    """
    image_data = b""
    
    # Read the first 4 bytes to get the data size
    data_length_bytes = client_socket.recv(4)
    if not data_length_bytes:
        return b""
    
    data_length = struct.unpack("!I", data_length_bytes)[0]
    image_data += data_length_bytes
    
    # Continue reading data until all bytes are received
    while len(image_data) < data_length:
        chunk = client_socket.recv(4096)
        if not chunk:
            break
        image_data += chunk
    
    return image_data
