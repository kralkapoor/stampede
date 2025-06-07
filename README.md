# Stampede Image Processing Tools

#### Stampede Image Processing Tools is a Python project developed to automate various image processing tasks for the Stampede business. This toolkit includes capabilities for image resizing, recolouring, and creating transparent masks.

## Features:
- **Image resizing**: Resizes images and maintains aspect ratios, or resizes or specfific dimensions as specified in the cfg files
- **Image recolouring**: Changes the colour of the images to the desired preset colour themes by replacing each pixel to a new colour
- **Transparent masks**: Place transparent masks atop images to create a circular style image for use in Cricut software
- **Logging**: Some rudimentary logging is implemented for file tracking and debugging.

## Classes
- Currently available classes are the superclass ImageProcessor, and child classes Circles, Rectangles, and Stickers. More to follow later.
  - **Circles**: Processes all valid image files in the `/img` directory by resizing it to a standard size and recolouring it based on the file name suffix. A transparent mask is applied to convert the image into a circle shape.
  - **Rectangles**: `/img` files are processed into respective colours and folders for tidiness
  - **Stickers**: *WIP*. The stickers class will instead crop the images and maintain aspect ratio to facilitate the picture being processed into a circular sticker. N.B. unlike te circles class, this will cut content from the image as opposed to preserving it.

## Libraries
- Stampede uses a few key libraries to achieve the above features:
- **Pillow**: The Python imaging library is the heavy lifter for this project, which allows image manipulation for the given files.
- **OS**: The OS library is extensively used for accessing the computer's fs and iterating over the img directory
- **Mulitprocessing**: Not required but used to improve performance when processing multiple images concurrently. It is currently set to use the max available system cores.

## Environment variables
- Requires an OpenAI API key and, optionally, configuration for the project ID and organisation ID. Use the following as a template.
```
OPENAI_API_KEY={key}
OPENAI_PROJECT_ID={proj id}
OPENAI_ORG_ID={org id}
```