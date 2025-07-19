# Stampede Image Processing Tools

#### Stampede Image Processing Tools is a Python project developed to automate various image processing tasks for the Stampede business. This toolkit includes capabilities for image resizing, recolouring, creating transparent masks, and AI-powered avatar generation.

## Features:
- **Image resizing**: Resizes images and maintains aspect ratios, or resizes to specific dimensions as specified in the cfg files
- **Image recolouring**: Changes the colour of the images to the desired preset colour themes by replacing each pixel to a new colour
- **Transparent masks**: Place transparent masks atop images to create a circular style image for use in Cricut software
- **AI Avatar Generation**: Create new avatars from scratch using OpenAI's image generation models
- **AI Avatar Editing**: Edit existing avatars with custom prompts using OpenAI's image editing capabilities
- **Logging**: Comprehensive logging is implemented for file tracking and debugging

## Processing Types
The application provides several processing modes through an intuitive GUI interface:

### Image Handlers
- **Circles**: Processes all valid image files in the `/img` directory by resizing to a standard size and recolouring based on the file name suffix. A transparent mask is applied to convert the image into a circle shape.
- **Rectangles**: `/img` files are processed into respective colours and organized into folders for tidiness
- **Stickers**: Crops images and maintains aspect ratio to facilitate processing into circular stickers. Unlike the circles class, this will cut content from the image as opposed to preserving it.

### Avatar Processing (NEW)
- **New Avatar**: Generate brand new avatars using OpenAI's AI models with customizable prompts for creating rubber stamp-style line art
- **Edit Avatar**: Modify existing avatars by placing a single image in the `/img` directory and providing custom editing instructions

## Usage
1. **Setup Environment**: Configure your `.env` file with OpenAI credentials (see Environment Variables section)
2. **Place Images**: Add images to the `/img` directory
3. **Run Application**: Execute `python GUI.pyw` to launch the graphical interface
4. **Select Processing Type**: Choose from Rectangles, Circles, Stickers, New Avatar, or Edit Avatar
5. **Processed Results**: Find output images in `img/Processed/[ProcessingType]/`
6. **Original Archive**: Original images are automatically moved to `img/zArchive/` after processing

## Libraries
Stampede uses several key libraries to achieve the above features:
- **Pillow**: The Python imaging library is the heavy lifter for this project, which allows image manipulation for the given files
- **OpenAI**: Official OpenAI Python client for AI-powered avatar generation and editing
- **Tkinter**: Built-in Python GUI framework for the user interface
- **Threading**: Used for non-blocking UI during AI processing operations
- **Multiprocessing**: Used to improve performance when processing multiple images concurrently. Currently set to use 4 processes for optimal performance
- **Requests**: HTTP library for downloading AI-generated images from URLs

## Environment Variables
Requires an OpenAI API key and, optionally, configuration for the project ID and organisation ID. Create a `.env` file in the root directory:
```
OPENAI_API_KEY={your_api_key}
OPENAI_PROJECT_ID={your_project_id}
OPENAI_ORG_ID={your_org_id}
```

## Installation
1. Clone the repository
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure environment variables (see above)
5. Run the application:
   ```bash
   python GUI.pyw
   ```