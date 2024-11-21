import random
from typing import List, Tuple
import tkinter as tk

from WebpageNode import WebpageNode, BOX_HALF_SIZE


words_to_ignore: List[str] = ["the", "and", "that"]  # add more here....

class PageManager:

    def __init__(self):
        self.page_nodes: List[WebpageNode] = []
        self.num_pages: int = 0
        self.total_steps_taken: int = 0
        # self.page_index: <insert type here> = <insert initially empty structure here>
        self.load_pages()

    def load_pages(self) -> None:
        """
        reads from the webpages.txt file in this project and generates a list of WebpageNodes, based on this text.
        :return: None
        """
        MIN_DISTANCE_SQUARED = pow(BOX_HALF_SIZE*2*1.41+30,2)
        id_counter = 0

        used_locations:List[Tuple[int,int]] = []

        with open("webpages.txt", mode="r") as pagesFile:
            for line in pagesFile:
                num_links = random.randint(2, 8)
                links: List[int] = []
                for i in range(num_links):
                    link_to = random.randint(0, 49)
                    if link_to != id_counter:
                        links.append(link_to)

                too_close = True
                while(too_close):
                    too_close = False
                    x = random.randint(2+BOX_HALF_SIZE, 798-BOX_HALF_SIZE)
                    y = random.randint(2+BOX_HALF_SIZE, 598-BOX_HALF_SIZE)
                    for pt in used_locations:
                        if pow(x-pt[0], 2)+pow(y-pt[1], 2) < MIN_DISTANCE_SQUARED:
                            too_close = True
                            break
                used_locations.append((x,y))

                self.page_nodes.append(WebpageNode(id_num=id_counter,
                                                   page_content=line.strip(),
                                                   xPos=x,
                                                   yPos=y,
                                                   links=links))
                # print(self.page_nodes[-1])  # optional for status check that pages are loading.
                id_counter += 1
        self.purge_links()
        self.num_pages = len(self.page_nodes)

    def purge_links(self) -> None:
        """
        A little bit of behind-the-scenes magic to remove some of the excess links that are spatially far away, to make
        the graphics look a bit nicer,with fewer loooong lines.
        :return: None
        """
        for p in self.page_nodes:
            for i in range(len(p.links) - 1, -1, -1):
                # Probabilistically remove lines that are longer
                if random.random() < (abs(p.xPos - self.page_nodes[p.links[i]].xPos) + abs(
                        p.yPos - self.page_nodes[p.links[i]].yPos)) / 800:
                    del (p.links[i])
                # but don't remove any page's last link.
                if len(p.links) == 1:
                    break

    def build_index(self) -> None:
        """
        based on the self.page_nodes list, builds the self.page_index - a collection of word locations for this
        list of webpages, ignoring any words in the words_to_ignore list.
        :return: None
        """
        pass

    def search_for_word(self, target: str) -> List[Tuple[int, List[int]]]:
        """
        uses the self.page_index data structure to return a list of (page_id, [word locations]) tuples.
        :param target: word to find
        :return: a list of (page_id, [word locs]) where the word can be found.
        """
        pass

        return []

    def iterate_page_rank(self, canvas: tk.Canvas) -> None:

        which_to_iterate = 2 * random.randint(0, int(self.num_pages / 2))
        self.page_nodes[which_to_iterate].num_page_visits += 1
        self.total_steps_taken += 1

        self.recalculate_ranks_from_page_visits()
        self.update_colors(canvas)

    def recalculate_ranks_from_page_visits(self) -> None:
        for p in self.page_nodes:
            p.recalculate_rank(self.total_steps_taken)

    def update_colors(self, canvas: tk.Canvas) -> None:
        for p in self.page_nodes:
            p.update_color_for_rank(canvas)
