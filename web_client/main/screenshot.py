from PIL import ImageGrab
from pynput.mouse import Listener, Controller


def result_screenshot():
    def on_press(x, y, button, pressed):
        global first_x, first_y, second_x, second_y
        if pressed:
            print(F"Pressed at {x, y}")
            first_x, first_y = x, y
        else:
            second_x, second_y = x, y
            print(f"Released at {x, y}")

        if not pressed:
            # Stop listener
            return False

    with Listener(on_click=on_press) as listener:
        listener.join()

    minim_x = min(first_x, second_x)
    maxim_x = max(first_x, second_x)

    minim_y = min(first_y, second_y)
    maxim_y = max(first_y, second_y)

    im = (ImageGrab.grab(bbox=(minim_x, minim_y, maxim_x, maxim_y)))
    im.show()  # при таком виде, если запускать отдельно этот код, то все работает

    return im.save("main/temp_files/img.jpg")


# result_screenshot()
