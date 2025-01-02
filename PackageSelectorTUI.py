import os
from prompt_toolkit import prompt
from prompt_toolkit.key_binding import KeyBindings
from PackageSelector import PackageSelector

class PackageSelectorTUI(PackageSelector):
    def __init__(self, path):
        super().__init__(path=path)
        self.folders = self.get_python_packages_from_folders()
        self.selected_folders = []
        self.selected = [False] * len(self.folders)
        self.current_row = 0

    def render_folders(self):
        """Render the list of folders and show selection"""
        print("\033c", end="")  # Clean the console

        # Show continous message
        print("Select packages with Enter, use up and down arrows to navigate, 'q' to confirm and exit.\n")

        # Show package with arrow on side of the one pointed
        for idx, folder in enumerate(self.folders):
            prefix = "->" if idx == self.current_row else "  "
            selection = "[X]" if self.selected[idx] else "[ ]"
            if idx == self.current_row:
                print(f"{prefix} {os.path.basename(folder)} {selection}")  # Selected row
            else:
                print(f"   {os.path.basename(folder)} {selection}")  # Not selected rows

    def run(self) -> list[str]:
        """Show packages and Handle user input"""
        kb = KeyBindings()

        # Up arrow handling
        @kb.add('up')
        def up(event):
            if self.current_row > 0:
                self.current_row -= 1
                self.render_folders()  # Renders new list after selection

        # Down arrow handling
        @kb.add('down')
        def down(event):
            if self.current_row < len(self.folders) - 1:
                self.current_row += 1
                self.render_folders()  # Renders new list after selection

        # Handling of selection/deselection
        @kb.add('enter')
        def select(event):
            self.selected[self.current_row] = not self.selected[self.current_row]
            self.render_folders()  # Renders new list after selection

        # Confirm and exit handling with 'q'
        @kb.add('q')
        def quit(event):
            """By pressing 'q' exit and return the selected packages"""
            self.selected_folders = [self.folders[i] for i, sel in enumerate(self.selected) if sel]
            raise KeyboardInterrupt  # Interrupts the loop to exit

        # Render initial list
        self.render_folders()

        # Main cycle
        try:
            while True:
                prompt("", key_bindings=kb)  # Listen for new inputs
        except KeyboardInterrupt:
            # Return the list of selected packages
            return self.selected_folders