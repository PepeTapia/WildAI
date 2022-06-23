import numpy as np
from PIL import ImageGrab
from PIL import ImageShow
from PIL import Image
from time import perf_counter

i = 0
total_time_elapsed = 0
while i < 10: 
    timer_start = perf_counter()
    screenshot = ImageGrab.grab()

    #ImageShow.show(screenshot) -- This works because screenshot is a direct image

    #Convert screenshot to np array
    screenshot_array = np.array(screenshot)
    #screenshot_array info
    print(type(screenshot_array))
    print(screenshot_array.shape)

    #Converting to an array requires converting back to an Image using Image.fromarray
    #!!!! Convert array as shown below. Use for debugging and eventually it would be used in tesseract somehow..

    #ss_array_to_image = Image.fromarray(screenshot_array)
    #ImageShow.show(ss_array_to_image)

    bluesb_region = screenshot_array[850:1070,720:915]
    bluesb_image = Image.fromarray(bluesb_region)
    print(type(bluesb_region))
    print(bluesb_region.shape)
    
    ImageShow.show(bluesb_image)
    i+=1

    timer_end = perf_counter()

    elapsed_time = timer_end - timer_start

    total_time_elapsed += elapsed_time
    print(f"Time elapsed in this loop is: {elapsed_time} ")
    print(f"Total time elapsed is: {total_time_elapsed}")