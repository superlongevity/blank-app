import random
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import streamlit as st

def create_random_mosaic(image, grid_size=(5, 5)):
    """
    Creates a random mosaic with different colored and overlapping variations of the input image.

    Parameters:
        image (PIL.Image): Input image object.
        grid_size (tuple): Number of rows and columns in the mosaic.
    """
    fig, ax = plt.subplots(figsize=(20, 20), dpi=100)
    ax.set_xlim(0, grid_size[1])
    ax.set_ylim(0, grid_size[0])
    ax.set_aspect('equal')
    ax.axis('off')

    for i in range(grid_size[0]):
        for j in range(grid_size[1]):
            x_offset = j + random.uniform(-0.3, 0.3)
            y_offset = i + random.uniform(-0.3, 0.3)
            scale = random.uniform(0.6, 1.2)
            rotation = random.uniform(-45, 45)

            color_tint = [random.uniform(0.5, 1.5) for _ in range(3)]
            image_array = np.array(image, dtype=np.float32)
            for channel in range(3):
                image_array[..., channel] *= color_tint[channel]
            image_array = np.clip(image_array, 0, 255).astype(np.uint8)

            tinted_image = Image.fromarray(image_array)
            transformed_image = tinted_image.resize(
                (int(image.width * scale), int(image.height * scale)), Image.ANTIALIAS
            ).rotate(rotation, expand=True)

            transformed_array = np.array(transformed_image)
            x_image, y_image = transformed_array.shape[1], transformed_array.shape[0]

            ax.imshow(
                transformed_array,
                extent=[x_offset, x_offset + x_image / 100, y_offset, y_offset + y_image / 100],
                interpolation='nearest'
            )

    st.pyplot(fig)

# Streamlit interface
st.title("Random Mosaic Generator")

uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
if uploaded_file:
    input_image = Image.open(uploaded_file).convert("RGBA")
    create_random_mosaic(input_image)
