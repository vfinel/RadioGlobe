import os
import time
import subprocess
import ui_manager
from loggers.log_radio import make_listening_stats


class MenuItem:
    def __init__(
        self, name, item_type, current=None, min_val=None, max_val=None, items=None
    ):
        self.name = name
        self.type = item_type
        self.current = current
        self.min = min_val
        self.max = max_val
        self.items = items  # For submenus


class Menu:
    def __init__(self, items):
        assert len(items) <= 4, "The Menu cannot have more than 4 items for now"
        self.items = items
        self.current_index = 0
        self.parent = None  # For keeping track of the parent menu

    def display(self, display_thread):
        """Displays the current menu on the screen."""
        lines = ["", "", "", ""]

        for i, item in enumerate(self.items):
            if i == self.current_index:
                lines[i] = "> " + item.name
            else:
                lines[i] = "  " + item.name

            if i >= 4:  # cannot display more than 4 lines
                break

        display_thread.clear()
        display_thread.message(
            line_1=lines[0],
            line_2=lines[1],
            line_3=lines[2],
            line_4=lines[3],
        )

    def handle_input(self, action, display_thread=None, station_info={}):
        """Handles user input and updates the menu state."""
        item = self.items[self.current_index]

        if action == "up":
            self.current_index = (self.current_index - 1) % len(self.items)

        elif action == "down":
            self.current_index = (self.current_index + 1) % len(self.items)

        elif action == "select":
            if item.type == "value":
                self.adjust_value()
            elif item.type == "switch":
                self.toggle_switch()
            elif item.type == "submenu":
                self.enter_submenu()
            elif item.type == "back":
                self.go_back()
            elif item.type == "exit":
                return "exit"
            elif item.type == "shutdown":
                ui_manager.shutdown(display_thread)
                return "shutdown"
            elif item.type == "reboot":
                subprocess.call(["sh", "./reboot_globe.sh"])
            elif item.type == "restart":
                subprocess.call(["sh", "./restart_main.sh"])
                return "restart"
            elif item.type == "add_station":
                add_station_to_favorites(station_info, display_thread)
                return "exit"
            elif item.type == "show_stats":
                show_stats(display_thread)
                return "exit"
        else:
            return "continue"

    def adjust_value(self):
        """Adjusts the value of the selected item."""
        item = self.items[self.current_index]
        item.current += 1  # Or decrement, depending on input
        item.current = max(item.min, min(item.current, item.max))

    def toggle_switch(self):
        """Toggles the value of a switch item."""
        item = self.items[self.current_index]
        item.current = not item.current

    def enter_submenu(self):
        """Enters a submenu if available."""
        item = self.items[self.current_index]
        if item.items:
            # Save current menu state as a parent snapshot so we can restore it
            parent_snapshot = Menu(self.items)
            parent_snapshot.current_index = self.current_index
            parent_snapshot.parent = self.parent

            # Set the snapshot as this menu's parent, then replace items
            # with the submenu's items and reset the current index.
            self.parent = parent_snapshot
            self.items = item.items
            self.current_index = 0

    def go_back(self):
        """Goes back to the parent menu."""
        if self.parent:
            # Restore the parent menu's state
            self.items = self.parent.items
            self.current_index = self.parent.current_index
            self.parent = self.parent.parent  # Restore the grandparent
        else:
            # If at the root, do nothing
            pass

    def get_current_item(self):
        return self.items[self.current_index]

    def process_iteration(self, display_thread, ui_manager, station_info: dict):
        self.display(display_thread)
        action = self.get_input(ui_manager)
        if action:
            display_thread.clear()

        result = self.handle_input(action, display_thread, station_info)
        return result

    def get_input(self, ui_manager):
        """inspired by main.Process_UI_Events"""
        action = ""
        ui_events = []
        ui_manager.update(ui_events)

        for event in ui_events:
            if event[0] == "Jog":
                if event[1] == -1:
                    action = "up"
                elif event[1] == 1:
                    action = "down"
            elif event[0] == "enter_menu":
                action = "select"

            print(f"{event=} -> {action=}")
        return action


def get_menu():
    # Create menu items
    menu_items = [
        MenuItem(
            name="system",
            item_type="submenu",
            items=[
                MenuItem(  # shutdown confirmation (cancel first) to avoid errors
                    name="Shutdown globe",
                    item_type="submenu",
                    items=[
                        MenuItem(name="cancel shutdown", item_type="exit"),
                        MenuItem(name="confirm shutdown", item_type="shutdown"),
                    ],
                ),
                MenuItem(name="Reboot globe", item_type="reboot", current=True),
                MenuItem(name="Restart software", item_type="restart", current=True),
                MenuItem(name="Back", item_type="back"),
            ],
        ),
        MenuItem(
            name="radio stations",
            item_type="submenu",
            items=[
                MenuItem(
                    name="add station to fav",
                    item_type="add_station",
                    current=True,
                ),
                MenuItem(
                    name="show stats",
                    item_type="show_stats",
                ),
                MenuItem(name="Back", item_type="back"),
            ],
        ),
        MenuItem(name="Exit", item_type="exit"),
    ]

    # Create the root menu
    root_menu = Menu(menu_items)

    return root_menu


def add_station_to_favorites(station, display_thread):
    favourite_radio_file = "logs/favourite_globe_radios.csv"
    encoding = "utf-8"

    # create file if it does not exist yet
    if not os.path.isfile(favourite_radio_file):
        with open(favourite_radio_file, "w", encoding=encoding) as f:
            f.write("name,location,url,\n")

    # append radio to file
    with open(favourite_radio_file, "a", encoding=encoding) as f:
        f.write(f"{station['name']},{station['location']},{station['url']},\n")

    display_thread.clear()
    time.sleep(0.2)
    display_thread.message(
        line_2="Station added",
        line_3="to favorites",
    )
    time.sleep(1)


def show_stats(display_thread):
    n_total, n_listened, ratio = make_listening_stats()
    display_thread.clear()
    time.sleep(0.2)
    display_thread.message(
        line_1=f"listened: {n_listened}",
        line_2=f"total: {n_total}",
        line_3=f"> you listened {100 * ratio:.2f}%",
        line_4="of the world radios!",
    )
    time.sleep(10)
