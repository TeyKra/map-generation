import noise
import numpy as np
from PIL import Image
import random  # Import for generating random seed

# Global parameters
shape = (128, 128)  # Dimensions of the noise map
scale = 25.0  # Scale factor for the noise
octaves = 2  # Number of noise layers
lacunarity = 2.0  # Frequency multiplier between successive octaves
persistence = 1.2  # Amplitude multiplier between successive octaves

# Colors for different biomes
colors = {
    "water": (66, 110, 225),  # RGB color for water
    "beach": (240, 210, 172),  # RGB color for beach
    "grass": (36, 135, 32),  # RGB color for grass
    "mountain": (140, 140, 140),  # RGB color for mountain
    "snow": (250, 250, 250),  # RGB color for snow
}

# File path to save the generated image
image_filepath = "noise.png"

def generate_noise_map(shape, scale, octaves, persistence, lacunarity, seed):
    """
    Generates a 2D noise map using Perlin noise with a random seed.
    
    Args:
        shape (tuple): Dimensions of the noise map.
        scale (float): Scale factor for the noise.
        octaves (int): Number of noise layers.
        persistence (float): Amplitude multiplier for octaves.
        lacunarity (float): Frequency multiplier for octaves.
        seed (int): Random seed for generating unique noise maps.
        
    Returns:
        numpy.ndarray: 2D array representing the noise map.
    """
    noise_map = np.zeros(shape)  # Initialize a blank noise map
    for x in range(shape[0]):  # Iterate through each row
        for y in range(shape[1]):  # Iterate through each column
            value = noise.pnoise2(  # Generate Perlin noise value
                x / scale,  # Scale the x-coordinate
                y / scale,  # Scale the y-coordinate
                octaves=octaves,  # Use the specified number of octaves
                persistence=persistence,  # Apply persistence
                lacunarity=lacunarity,  # Apply lacunarity
                repeatx=shape[0],  # Repeat noise for seamless tiling along x
                repeaty=shape[1],  # Repeat noise for seamless tiling along y
                base=seed  # Use the random seed
            )
            noise_map[x, y] = value  # Assign the noise value to the map
    return noise_map

def map_value_to_color(value):
    """
    Maps a noise value to a color based on predefined thresholds.
    
    Args:
        value (float): The noise value to map.
        
    Returns:
        tuple: RGB color corresponding to the noise value.
    """
    if value < -0.07:
        return colors["water"]  # Map values below -0.07 to water
    elif value < 0:
        return colors["beach"]  # Map values below 0 to beach
    elif value < 0.25:
        return colors["grass"]  # Map values below 0.25 to grass
    elif value < 0.50:
        return colors["mountain"]  # Map values below 0.50 to mountain
    else:
        return colors["snow"]  # Map values above 0.50 to snow

def generate_image_from_noise(noise_map):
    """
    Generates an image from a noise map by mapping values to colors.
    
    Args:
        noise_map (numpy.ndarray): 2D array representing the noise map.
        
    Returns:
        PIL.Image.Image: Image generated from the noise map.
    """
    img = Image.new("RGB", noise_map.shape)  # Create a new RGB image
    for x in range(noise_map.shape[0]):  # Iterate through each row
        for y in range(noise_map.shape[1]):  # Iterate through each column
            color = map_value_to_color(noise_map[x, y])  # Map value to color
            img.putpixel((x, y), color)  # Set the pixel to the corresponding color
    return img

# Generate a random seed for the noise map
random_seed = random.randint(0, 1000000)

# Generate the noise map using the random seed
noise_map = generate_noise_map(shape, scale, octaves, persistence, lacunarity, random_seed)

# Generate an image from the noise map
image = generate_image_from_noise(noise_map)

# Save the generated image
image.save(image_filepath)
print(f"Image saved at: {image_filepath} with seed: {random_seed}")
