import hashlib
import random
import string
import socket
import struct
import os

from PIL import Image, ImageDraw, ImageFont

def draw_on_image(text: str) -> str:
    """Function for drawing text on an image""" 
    img = Image.open("white.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", 30)
    x = (img.width // 2) - 100
    y = img.height // 2
    draw.text((x, y), text, fill="black", font=font)
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

def compose_image_from_bytes(image_data: bytes, path) -> None:
    """Создание изображения из данных"""
    # Читаем первые 4 байта для получения длины данных
    data_length = struct.unpack("!I", image_data[:4])[0]
    
    # Оставшиеся байты являются данными изображения
    image_bytes = image_data[4:data_length+4]
    
    # Создаем изображение из байтов
    try:
        with open(path, "wb") as file:
            file.write(image_bytes)
        print("Изображение успешно построено")
    except Exception as e:
        print(f"Ошибка при построении изображения: {e}")

def get_image_data(client_socket: socket.socket) -> bytes:
    """Получение данных изображения"""
    image_data = b""
    # Читаем первые 4 байта, чтобы получить размер данных
    data_length_bytes = client_socket.recv(4)
    if not data_length_bytes:
        return b""
    data_length = struct.unpack("!I", data_length_bytes)[0]
    image_data += data_length_bytes
    while len(image_data) < data_length:
        chunk = client_socket.recv(4096)
        if not chunk:
            break
        image_data += chunk
    
    return image_data
