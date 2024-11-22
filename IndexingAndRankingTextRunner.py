from typing import List, Tuple

from PageManager import PageManager

if __name__ == "__main__":
    manager = PageManager()
    manager.build_index()
    # print(manager.page_index)  # uncomment to print out your page index to see whether it looks right.
    while True:
        search_term = input("Enter a word to search for: ")
        response: List[Tuple[int,List[int]]] = manager.search_for_word(search_term)
        if len(response) == 0:
            print("Word not found.")
        else:
            print(f"I found \"{search_term}\" on the following pages:")
            for page in response:
                page_id = page[0]
                locations = page[1]
                print(f"\t\"{manager.page_nodes[page_id].title()}\":{locations}")
