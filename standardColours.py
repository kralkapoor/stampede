# House all of the colours used by stampede here

colours = {
    'R' : (255,0,0,255),        # Red
    'G' : (60, 179, 113, 255),  # Medium Sea Green
    'B' : (100, 149, 237, 255), # Cornflour Blue
    'P' : (255, 105, 180, 255), # Hot Pink
    'PP' : (148, 0, 211, 255),  # Dark Violet
    'Black' : (0,0,0,255),      # Just Black
}


    
if __name__ == '__main__':
    for key, val in colours.items():
        if val == (148, 0, 211, 255):
            print(key)