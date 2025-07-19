BASE_PROMPT: str = """
Convert the provided 3D avatar into a high-contrast, 100 percent black-and-white line art suitable for a rubber stamp.  
You have been supplied with some exemplars of expected outputs. These are 2D, monochromatic images.
• Style: Clean 2D vector line drawing with thick, uniform black outlines (no grayscale or shading).  
• Composition: FULL AVATAR VISIBLE—do not crop any limbs, head, or feet. Automatically scale or inset the avatar so the entire person fits comfortably within the frame, with a small margin of whitespace around.  
• Padding: Include at least 5 to 10 percent empty space on all sides so nothing touches or is cut off by the canvas edge.  
• Background: Fully transparent—no circles, shapes, text, or additional elements.  
• Fill: Remove all color fills; interior should be white or transparent.  
• Detail: Preserve key hair, clothing folds, facial features, and posture, but simplify to bold lines.  
• Output size: 1024 by 1024 px (or largest square that fits) with transparent background.  
• Output format: Single-layer PNG with transparency.
"""
