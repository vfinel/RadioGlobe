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

    def handle_input(self, action):
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
