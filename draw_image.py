from PIL import (
    Image, 
    ImageDraw,
    ImageFont
)


def draw_on_image(text):
    img = Image.open("image_2.png")

    # Create an object ImageDraw to draw on the image
    draw = ImageDraw.Draw(img)

    # Font
    font = ImageFont.truetype("arial.ttf", 30)

    # coords
    x = img.width // 2
    y = img.height // 2

    draw.text((x, y), text, fill="black", font=font)
    img.save("output.png")

