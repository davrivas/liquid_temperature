import framebuf

# finds image in pbm format
def find_image(ruta):
    image = open(ruta, "rb") # Open in bit read mode
    image.readline() # Method to go to the first line of the bits
    xy = image.readline() # Get the second line
    x = int(xy.split()[0]) # split returns a list of the elements of the variable only 2 elements
    y = int(xy.split()[1])
    icon = bytearray(image.read())  # save to byte array
    image.close() # close the file
    return framebuf.FrameBuffer(icon, x, y, framebuf.MONO_HLSB)