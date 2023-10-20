from fastapi import FastAPI,responses
import rasterio
from PIL import Image
import numpy as np

app = FastAPI()

#-------------------------------------------------------------------
# Root endpoint
#-------------------------------------------------------------------

@app.get("/", tags=["root"])
async def read_root():
  
    message = "Welcome to the API"
    attributes_link = "http://localhost:8000/attributes/"
    thumbnail_link = "http://localhost:8000/thumbnail/" 

    # HTML content with links
    html_content = f"""
    <html>
    <body>
        <h1>{message}</h1>
        <p><a href="{attributes_link}">Attributes Endpoint</a></p>
        <p><a href="{thumbnail_link}">Thumbnail Endpoint</a></p>
        <p> Author: Miguel Chapela Rivas</p>
    </body>
    </html>
    """
    
    return responses.HTMLResponse(content=html_content)
#-------------------------------------------------------------------

#-------------------------------------------------------------------
# Attributes endpoint
#-------------------------------------------------------------------
@app.get("/attributes/", tags=["attributes"])
def get_image_attributes():
    try:
        with rasterio.open('files/S2L2A_2022-06-09.tiff') as src:
            # Extract attributes
            image_attributes = {
                "width": src.width,
                "height": src.height,
                "bands": src.count,
                "coordinate_reference_system": src.crs.to_string(),
                "bounding_box": {
                    "min_x": src.bounds.left,
                    "min_y": src.bounds.bottom,
                    "max_x": src.bounds.right,
                    "max_y": src.bounds.top,
                }
            }

            return image_attributes
    except Exception as e:
        return {"An error occurred": str(e)}


#-------------------------------------------------------------------


# Auxiliary functions to treat the sentinel 2 image 
# Source: https://www.satmapper.hu/en/rgb-images/
# Function to normalize a band to 8-bit range (0-255)
def normalize(band):
    # Calculate the minimum and maximum values in the band
    band_min, band_max = band.min(), band.max()
    # Normalize the band to the 8-bit range (0-255)
    return ((band - band_min) / (band_max - band_min) * 255).astype(np.uint8)

# Function to apply gamma correction to a band
def gammacorr(band):
    gamma = 2  # Adjust the gamma value as needed
    # Apply gamma correction to the band
    return np.power(band, 1/gamma)

#-------------------------------------------------------------------
#Thumbnail endpoint
#-------------------------------------------------------------------
@app.get("/thumbnail", tags=["thumbnail"])
async def create_thumbnail( resolution: int = 256):
    try:
           # Open the TIFF image using rasterio
        with rasterio.open('files/S2L2A_2022-06-09.tiff') as src:
            # Read the bands (modify the band indices as needed for RGB)
            red = src.read(4)
            green = src.read(3)
            blue = src.read(2)

            # Normalize pixel values for each band
            red_postprocess = normalize(gammacorr(red))
            green_postprocess = normalize(gammacorr(green))
            blue_postprocess = normalize(gammacorr(blue))

            # Stack the normalized bands to create an RGB image
            rgb_image = np.dstack((red_postprocess, green_postprocess, blue_postprocess))

        # Create a PIL image from the numpy array
        pil_image = Image.fromarray(rgb_image)

        # # Create an RGB thumbnail with PIL
        pil_thumbnail = pil_image.resize((resolution, resolution), Image.Resampling.LANCZOS)

        # Convert the PIL thumbnail to bytes
        thumbnail_path = "files/thumbnail.png"
        pil_thumbnail.save(thumbnail_path, format='PNG')

        return responses.FileResponse(thumbnail_path)
    except Exception as e:
        return {"An error occurred": str(e)}
#-------------------------------------------------------------------