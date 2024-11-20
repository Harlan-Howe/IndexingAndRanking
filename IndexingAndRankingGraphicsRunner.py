import random
import tkinter as tk
from math import sqrt

from numpy import sign
from tkinter import scrolledtext, Frame, X, Label, LEFT

from PageManager import PageManager
from WebpageNode import BOX_HALF_SIZE

ARROW_SIZE = 5

def search(event):
    print("Searching for: ", search_bar.get())

def main():
    global search_bar, manager, canvas
    manager = PageManager()
    manager.build_index()

    window = tk.Tk()
    window.geometry('800x800')

    canvas = tk.Canvas(window, width=800, height=600)
    canvas.pack()

    search_frame = Frame(window)
    search_frame.pack(fill=X)
    search_label = Label(search_frame, text="Search for:", width=11)
    search_label.pack(side=LEFT, padx=5, pady=5)
    search_bar = tk.Entry(search_frame, width=50)
    search_bar.bind("<Return>", search)
    search_bar.pack(side=LEFT)

    text_area = scrolledtext.ScrolledText(window, width=100, height=6) # height is in lines, so adjust as needed
    text_area.pack()

    draw_web()

    window.mainloop()

def draw_web():
    for page in manager.page_nodes:
        page.draw_self(canvas)

    for page in manager.page_nodes:
        if page.xPos == 0:
            print(page)
        for link in page.links:
            p2x = manager.page_nodes[link].xPos
            p2y = manager.page_nodes[link].yPos

            x_sign = sign(p2x-page.xPos) * (abs(p2x-page.xPos) > 2 * BOX_HALF_SIZE)
            y_sign = sign(p2y-page.yPos) * (abs(p2y-page.yPos) > 2 * BOX_HALF_SIZE)

            p1x = page.xPos + x_sign * BOX_HALF_SIZE
            p1y = page.yPos + y_sign * BOX_HALF_SIZE

            p2x -= x_sign * BOX_HALF_SIZE
            p2y -= y_sign * BOX_HALF_SIZE

            line_color = rgb_to_color(random.randint(0,255),random.randint(0,255),random.randint(0,255))

            canvas.create_line(p1x, p1y, p2x, p2y, fill=line_color, width=1)

            line_length = sqrt(pow(p1x-p2x,2) + pow(p1y-p2y,2))

            unit_vector_along_line = ((p2x-p1x)/line_length, (p2y-p1y)/line_length)
            unit_vector_normal = (-unit_vector_along_line[1], unit_vector_along_line[0])

            canvas.create_line(p2x, p2y,
                               p2x-ARROW_SIZE*(unit_vector_along_line[0]+unit_vector_normal[0]),
                               p2y-ARROW_SIZE*(unit_vector_along_line[1]+unit_vector_normal[1]),
                               p2x-ARROW_SIZE*(unit_vector_along_line[0]-unit_vector_normal[0]),
                               p2y-ARROW_SIZE*(unit_vector_along_line[1]-unit_vector_normal[1]),
                               p2x, p2y,
                               fill=line_color, width=1)


def rgb_to_color(r:int, g:int, b:int) -> str:
    """
    converts rgb (0-255) values to a hex code, which is what tkinter uses for colors.
    :param r:  red (0-255)
    :param g:  green (0-255)
    :param b:  blue (0-255)
    :return: a hex code in format #rrggbb
    """
    return f"#{r:02x}{g:02x}{b:02x}"

if __name__ == "__main__":
    main()