from typing import List, Optional
import tkinter as tk

BOX_HALF_SIZE = 15
PERCENTAGE_RANK_TO_COLOR_MULTIPLIER = 5000


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
        self.id_num = id_num
        self.content = page_content
        self.xPos = xPos
        self.yPos = yPos
        self.links = links
        self.color = "#8888ff"
        self.num_page_visits = 1
        self.rank = 0.02
        self.rect_id: Optional[int] = None
        self.text_id: Optional[int] = None

    def title(self) -> str:
        """
        returns just the portion of the web page between the <title> and </title> tags.
        :return: the title of this page.
        """
        end_title_loc = self.content.index("</title>")
        return self.content[7:end_title_loc]

    #  I'm not sure whether you'll need this, but I put it here for completeness, since we have a head() method.
    def body(self) -> str:
        """
        returns just the portion of the web page between the <body> and </body> tags.
        :return: the body of this page.
        """
        start_body_loc = self.content.index("<body>")
        return self.content[start_body_loc+6:-7]

    def __str__(self):
        return f"{self.id_num}\t({self.xPos}, {self.yPos})\t{self.title()}->{self.links}"

    def draw_self(self, canvas: tk.Canvas):
        if self.rect_id is None:
            self.rect_id = canvas.create_rectangle(self.xPos - BOX_HALF_SIZE, self.yPos - BOX_HALF_SIZE,
                                                   self.xPos + BOX_HALF_SIZE, self.yPos + BOX_HALF_SIZE,
                                                   outline="black", fill=self.color, width=2)
        if self.text_id is None:
            canvas.create_text(self.xPos-1, self.yPos-1, text=f"{self.id_num}", fill="lightgrey", font="Arial 12 bold")
            self.text_id = canvas.create_text(self.xPos, self.yPos, text=f"{self.id_num}", fill="black",
                                              font="Arial 12 bold")

    def recalculate_rank(self, total_steps_taken: int) -> None:
        self.rank = self.num_page_visits / total_steps_taken

    def update_color_for_rank(self, canvas: tk.Canvas) -> None:
        color_val = min(255, max(0, int(self.rank * PERCENTAGE_RANK_TO_COLOR_MULTIPLIER)))
        self.reset_rect_color(canvas, rgb_to_color(255-color_val, color_val, 0))

    def reset_rect_color(self, canvas: tk.Canvas, color: str) -> None:
        self.color = color
        canvas.itemconfig(self.rect_id, fill=color)
