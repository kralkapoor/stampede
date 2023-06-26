import os
from PIL import Image, ImageDraw

img_dir = os.listdir(f'C:/Users/k4rlk/Desktop/stampede-resizer/img') # FP

rects = [img for img in img_dir if img.endswith('png') or img.endswith('PNG')]

std_colours = (
    ((0, 0, 0, 255),'black'),
    ((255, 0, 0, 255),'red'),
    ((60, 179, 113, 255),'mediumseagreen'),
    ((100, 149, 237, 255),'cornflourblue'),
    ((255, 105, 180, 255),'hotpink'),
    ((148, 0, 211, 255),'darkviolet'))

for img in rects:
    
    rect = Image.open(f'img/{img}')
    canvas = Image.new('RGBA', rect.size, (255,255,255,255))
    ImageDraw.Draw(canvas)

    canvas.paste(rect)

    rect_data = canvas.getdata()
    
    path = ''

    for tup in std_colours:

        new_img = []

        match tup[1]:
            case 'black':
                path = '2 Black'
            case 'red':
                path = '3 Red'
            case 'mediumseagreen':
                path = '5 Seagreen'
            case 'cornflourblue':
                path = '6 Cornflour Blue'
            case 'hotpink':
                path = '4 Hot Pink'
            case 'darkviolet':
                path = '7 Dark Violet'

        for data in rect_data:
            if data[3] != 0 and data[0] < 200:
                new_img.append(tup[0]) 
            else:
                new_img.append((255,255,255,255))
        
        final_canvas = Image.new('RGBA', rect.size, (255,255,255,255))
        final_canvas.putdata(new_img)
        
        final_canvas.save(f'img/1 Final Rectangles/{path}/{tup[1]}_{img}',quality=100)

    os.replace(f'img/{img}',f'img/1 Final Rectangles/zArchive/{img}')

