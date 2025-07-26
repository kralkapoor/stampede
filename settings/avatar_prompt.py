BASE_PROMPT: str = """
Convert the uploaded 3D avatar into a clean, high-contrast black-and-white line drawing suitable for a rubber stamp.
You have been supplied with some examples of expected outputs. These are 2D, simple avatars reminiscent of Bitmojis that can be successfully processed into ink stamps. You will ignore the text surrounding the avatar, as you will focus only on creating the bitmoji itself.
• Style: Clean 2D vector line drawing with thick, uniform black outlines (no grayscale or shading).  
• Composition: IMPERATIVE: DO NOT EXTRAPOLATE LIMBS OR OTHER BODY PARTS. ONLY INCLUDE IN THE OUTPUT IMAGE WHAT WAS INCLUDED IN THE INPUT. Automatically scale or inset the avatar so the avatar fits comfortably within the frame, with a small margin of whitespace around.  
• Padding: Include at least 5 to 10 percent empty space on all sides so nothing touches or is cut off by the canvas edge.  
• Background: Fully transparent: no circles, shapes, text, or additional elements.  
• Fill: Remove all color fills; interior should be transparent.  
• Detail: Preserve key hair shape and styling, clothing folds, facial features, and posture, but simplify to bold lines.  
• Output size: 1024 by 1024 px (or largest square that fits) with transparent background.  
• Output format: Single-layer PNG with transparency.
"""
