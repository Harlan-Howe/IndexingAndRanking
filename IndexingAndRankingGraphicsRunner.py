import random
import tkinter as tk
from math import sqrt
from typing import Optional

from numpy import sign
from tkinter import scrolledtext, Frame, X, Label, LEFT

from PageManager import PageManager
from WebpageNode import BOX_HALF_SIZE
from WebpageNode import rgb_to_color

ITERATION_REPORT_FREQUENCY = 50  # how often should we print that we are making progress on the PageRank iterations

ARROW_SIZE: int = 5  # size of the arrowheads
BREAK_BETWEEN_ITERATIONS: int = 20  # time (in ms) between successive calls to the iterate_ranking() method. Must be at
#                                     least 10 ms, so graphics can update.

NUM_ITERATIONS_TO_PERFORM: int = 1000  # how many times to call the iterate_ranking() method.


class IndexingAndRankingGraphicsRunner:
    def search(self, event) -> None:
        """
        event handler that gets called when the user hits return in the search bar.
        :param event: info about the event, which we aren't using.
        :return: None
        """
        print("Searching for: ", self.search_bar.get())
        page_num = self.manager.find_best_match(self.search_bar.get())

        self.set_selection(page_num)  # circle the page in the graphics canvas
        self.text_area.delete("1.0", tk.END)  # clear the text area

        if 0 <= page_num < self.manager.num_pages:  # update the text area.
            self.text_area.insert(tk.INSERT, f"{self.manager.page_nodes[page_num].title()}\n\n"
                                             f"{self.manager.page_nodes[page_num].body()}")
        else:
            self.text_area.insert(tk.INSERT, "Not Found.")

    def __init__(self):
        self.num_iterations_to_go: int = NUM_ITERATIONS_TO_PERFORM
        self.selection_circle: int = -1
        self.manager = PageManager()  # loads_the webpages
        self.window = tk.Tk()
        self.canvas: Optional[tk.Canvas] = None
        self.search_bar: Optional[tk.Entry] = None
        self.text_area: Optional[scrolledtext.ScrolledText] = None

        self.manager.build_index()  # builds the index, which you wrote for the textRunner.

        self.setup_GUI()  # constructs the window with canvas, search text field and output webpage area.
        self.draw_web()  # creates the boxes and arrows we use for the web of pages.

        self.window.after(BREAK_BETWEEN_ITERATIONS, self.iterate_ranking)

        self.window.mainloop()

    def setup_GUI(self):
        """
        builds the window and inserts the canvas, search field, and page content area
        :return:
        """
        self.window.geometry('800x800')
        self.canvas = tk.Canvas(self.window, width=800, height=600)  # Note: a bit shorter (vertically) than the window.
        self.canvas.pack()
        search_frame = Frame(self.window)
        search_frame.pack(fill=X)
        search_label = Label(search_frame, text="Search for:", width=11)
        search_label.pack(side=LEFT, padx=5, pady=5)
        self.search_bar = tk.Entry(search_frame, width=50)
        self.search_bar.bind("<Return>", self.search)
        self.search_bar.pack(side=LEFT)
        self.text_area = scrolledtext.ScrolledText(self.window, width=100,
                                                   height=8)  # height is in lines, so adjust as needed
        self.text_area.pack()

    def iterate_ranking(self) -> None:
        """
        A recursive method that tells the PageManager to iterate_page_rank NUM_ITERATIONS_TO_PERFORM times.
        :return: None
        """
        if self.num_iterations_to_go % ITERATION_REPORT_FREQUENCY == 0:
            print(f"{self.num_iterations_to_go=}")
        if self.num_iterations_to_go > 0:
            self.num_iterations_to_go -= 1
            self.manager.iterate_page_rank(self.canvas)
            # call this method recursively, after waiting BREAK_BETWEEN_ITERATIONS milliseconds.
            self.window.after(BREAK_BETWEEN_ITERATIONS, self.iterate_ranking)
        else:
            print("Done iterating PageRank.")

    def draw_web(self) -> None:
        """
        creates the boxes and lines that are in the canvas. These are treated as objects, so they won't need to be
        explicitly redrawn, but we can alter aspects of them, such as their fill color.
        :return: None
        """
        #  draw all the boxes for the pages.
        for page in self.manager.page_nodes:
            page.draw_self(self.canvas)

        #  loop through all the links in each page
        for page in self.manager.page_nodes:
            for link in page.links:
                #  identify the center coordinates of the box this link is pointing to.
                p2x = self.manager.page_nodes[link].xPos
                p2y = self.manager.page_nodes[link].yPos

                # find the sign (-1, 0, 1) of the difference in the xPos and yPos between the current "page" and the
                #   center of the box where each link is pointing. (But if there is an overlap between boxes in a
                #   dimension, we'll call that a zero, as well.)
                x_sign = sign(p2x-page.xPos) * (abs(p2x-page.xPos) > 2 * BOX_HALF_SIZE)
                y_sign = sign(p2y-page.yPos) * (abs(p2y-page.yPos) > 2 * BOX_HALF_SIZE)

                # identify the corner or center edge coordinate of the source page box
                p1x = page.xPos + x_sign * BOX_HALF_SIZE
                p1y = page.yPos + y_sign * BOX_HALF_SIZE

                # identify the corner or center edge coordinate of the target page box
                p2x -= x_sign * BOX_HALF_SIZE
                p2y -= y_sign * BOX_HALF_SIZE

                line_color = rgb_to_color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

                # calculate information needed to draw the arrowhead for this line.
                line_length = sqrt(pow(p1x-p2x, 2) + pow(p1y-p2y, 2))
                unit_vector_along_line = ((p2x-p1x)/line_length, (p2y-p1y)/line_length)
                unit_vector_normal = (-unit_vector_along_line[1], unit_vector_along_line[0])

                # draw the line with the arrowhead.
                self.canvas.create_line([(p1x, p1y),
                                        (p2x, p2y),
                                        (p2x-ARROW_SIZE*(unit_vector_along_line[0]+unit_vector_normal[0]),
                                         p2y-ARROW_SIZE*(unit_vector_along_line[1]+unit_vector_normal[1])),
                                        (p2x-ARROW_SIZE*(unit_vector_along_line[0]-unit_vector_normal[0]),
                                         p2y-ARROW_SIZE*(unit_vector_along_line[1]-unit_vector_normal[1])),
                                        (p2x, p2y)],
                                        fill=line_color, width=1)
        #  create a circle that can be used to indicate which page is selected.
        self.selection_circle = self.canvas.create_oval(-200-BOX_HALF_SIZE * 1.5, -200-BOX_HALF_SIZE * 1.5,
                                                        -200+BOX_HALF_SIZE * 1.5, -200+BOX_HALF_SIZE * 1.5,
                                                        outline="blue", width=2)

    def set_selection(self, which_page: int) -> None:
        """
        move the selection circle to circumscribe the selected page, or off-screen if which_page is out of range.
        :param which_page: the id of the page to circumscribe
        :return: None
        """

        p = (-200, -200)
        if 0 <= which_page < self.manager.num_pages:
            p = (self.manager.page_nodes[which_page].xPos, self.manager.page_nodes[which_page].yPos)
        self.canvas.coords(self.selection_circle, [p[0]-BOX_HALF_SIZE * 1.5, p[1]-BOX_HALF_SIZE * 1.5,
                                                   p[0]+BOX_HALF_SIZE*1.5, p[1]+BOX_HALF_SIZE*1.5])



if __name__ == "__main__":
    app = IndexingAndRankingGraphicsRunner()
