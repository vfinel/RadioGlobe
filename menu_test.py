from display import Display
from ui_manager import UI_Manager
from menu import Menu, MenuItem


def get_input(ui_manager):
    """inspired by main.Process_UI_Events"""
    action = ""
    ui_events = []
    ui_manager.update(ui_events)

    for event in ui_events:
        print(f"{event=}")
        if event[0] == "Jog":
            if event[1] == -1:
                action = "up"
            elif event[1] == 1:
                action = "down"
        elif event[0] == "Random":
            action = "select"

    return action


def get_menu():
    # Create menu items
    menu_items = [
        MenuItem(
            name="Parameter 1", item_type="value", current=10, min_val=0, max_val=100
        ),
        MenuItem(name="Parameter 2", item_type="switch", current=True),
        MenuItem(
            name="Submenu",
            item_type="submenu",
            items=[
                MenuItem(
                    name="Sub-Parameter 1",
                    item_type="value",
                    current=5.5,
                    min_val=0.0,
                    max_val=10.0,
                ),
                MenuItem(name="Back", item_type="back"),
            ],
        ),
        MenuItem(name="Exit", item_type="exit"),
    ]

    # Create the root menu
    root_menu = Menu(menu_items)

    return root_menu


def test_menu():
    display_thread = Display(3, "Display")
    display_thread.start()
    ui_manager = UI_Manager()

    root_menu = get_menu()

    # Main loop
    while True:
        root_menu.display(display_thread)
        action = get_input(ui_manager)
        if action:
            display_thread.clear()

        result = root_menu.handle_input(action)

        if result == "exit":
            break


if __name__ == "__main__":
    test_menu()
