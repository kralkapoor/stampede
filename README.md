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
3. **Run Application**: Execute `uv run python main.pyw` to launch the graphical interface
4. **Select Processing Type**: Choose from Rectangles, Circles, Stickers, New Avatar, or Edit Avatar
5. **Processed Results**: Find output images in `img/Processed/[ProcessingType]/`
6. **Original Archive**: Original images are automatically moved to `img/zArchive/` after processing

## Libraries
- **Pillow**: Image manipulation and processing
- **OpenAI**: AI-powered avatar generation and editing
- **PySide6**: Qt6-based GUI framework

## Environment Variables
Requires an OpenAI API key and, optionally, configuration for the project ID and organisation ID. Create a `.env` file in the root directory:
```
OPENAI_API_KEY={your_api_key}
OPENAI_PROJECT_ID={your_project_id}
OPENAI_ORG_ID={your_org_id}
```

## Installation
1. Clone the repository
2. Install [uv](https://docs.astral.sh/uv/getting-started/installation/)
3. Install dependencies:
   ```bash
   uv sync
   ```
   To include dev dependencies (pytest, linting, PyInstaller):
   ```bash
   uv sync --all-groups
   ```
4. Configure environment variables (see above)
5. Run the application:
   ```bash
   uv run python main.pyw
   ```

## Building an Executable
To distribute the application as a standalone executable that requires no Python or uv installation:
1. Install all dependencies including dev tools:
   ```bash
   uv sync --all-groups
   ```
2. Build the executable:
   - **Windows:**
     ```bash
     uv run pyinstaller --name stampede --onedir --windowed --add-data "assets;assets" main.pyw
     ```
   - **Linux:**
     ```bash
     uv run pyinstaller --name stampede --onedir --windowed --add-data "assets:assets" main.pyw
     ```
3. The self-contained `dist/stampede/` folder can be copied to a network share or another machine and run directly. The app will auto-create `img/` and processing subdirectories on first launch.

### Automated Builds (CI/CD)
A GitHub Actions workflow automatically builds the Windows exe on every push to `main`. The workflow runs tests first, then builds via PyInstaller on a Windows runner and uploads the result as a downloadable artifact.

To download: **Actions tab → click the workflow run → Artifacts → `stampede-windows`**

You can also trigger a build manually from the Actions tab using the "Run workflow" button.