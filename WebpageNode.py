from typing import List, Optional
import tkinter as tk

BOX_HALF_SIZE = 15  # half the width and height of the page boxes when drawn on the screen.
PERCENTAGE_RANK_TO_COLOR_MULTIPLIER = 5000  # a factor to multiply the percentage factor (e.g., 0.02) by to get a color
#                                             value, 0-255 that looks good.


def rgb_to_color(r: int, g: int, b: int) -> str:
    """
    converts rgb (0-255) values to a hex code, which is what tkinter uses for colors.
    :param r:  red (0-255)
    :param g:  green (0-255)
    :param b:  blue (0-255)
    :return: a hex code in format #rrggbb
    """
    return f"#{r:02x}{g:02x}{b:02x}"


class WebpageNode:

    def __init__(self, id_num: int, page_content: str, xPos: int, yPos: int, links: List[int]):
        self.id_num: int = id_num
        self.content: str = page_content
        self.links: List[int] = links

        # needed for the graphics part of the program.
        self.xPos:int = xPos
        self.yPos:int = yPos
        self.color: str = "#ff0000"  # starting color of this box
        self.num_page_visits: int = 0
        self.rank: float = 0.02  # this will be calculated from the num_page_visits.
        self.rect_id: Optional[int] = None  # tag to identify which box on the screen belongs to this node.


    def title(self) -> str:
        """
        returns just the portion of the web page between the <title> and </title> tags.
        :return: the title of this page.
        """
        end_title_loc = self.content.index("</title>")
        return self.content[7:end_title_loc]

    def body(self) -> str:
        """
        returns just the portion of the web page between the <body> and </body> tags.
        :return: the body of this page.
        """
        start_body_loc = self.content.index("<body>")
        return self.content[start_body_loc+6:-7]

    def __str__(self) -> str:
        return f"{self.id_num}\t({self.xPos}, {self.yPos})\t{self.title()}->{self.links}"

    def draw_self(self, canvas: tk.Canvas) -> None:
        """
        creates the box and text objects that show up on the graphics canvas for this Node. You'll only call this
        once (per node), and then we can change the created object to alter its appearance elsewhere.
        :param canvas:  - the drawing area where these shapes wll appear.
        :return: None
        """
        self.rect_id = canvas.create_rectangle(self.xPos - BOX_HALF_SIZE, self.yPos - BOX_HALF_SIZE,
                                               self.xPos + BOX_HALF_SIZE, self.yPos + BOX_HALF_SIZE,
                                               outline="black", fill=self.color, width=2)
        canvas.create_text(self.xPos-1, self.yPos-1, text=f"{self.id_num}", fill="lightgrey", font="Arial 12 bold")
        canvas.create_text(self.xPos, self.yPos, text=f"{self.id_num}", fill="black", font="Arial 12 bold")

    def recalculate_rank(self, total_page_visits: int) -> None:
        """
        compute the rank for this Node, which will be a number 0.0 - 1.0, calculated from the num_page_visits and the
        total number of page visits. Ideally, the ranks for all the Nodes will add up to 1.0.
        :param total_page_visits: how many pages have been visited since the program started? (Ideally the sum of all
        the num_page_visits for all the nodes will sum up to this.
        :return: None
        """
        self.rank = self.num_page_visits / total_page_visits

    def update_color_for_rank(self, canvas: tk.Canvas) -> None:
        """
        calculates and updates the color of the box to reflect the rank of this node from 0.0 -> Red to 1.0 -> Green
        :param canvas: the drawing area on which this box is drawn.
        :return:  None
        """
        self.color = min(255, max(0, int(self.rank * PERCENTAGE_RANK_TO_COLOR_MULTIPLIER)))
        canvas.itemconfig(self.rect_id, fill=rgb_to_color(255-self.color, self.color, 0))


