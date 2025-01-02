import os
import tkinter as tk
from tkinter import messagebox
from PackageSelector import PackageSelector

class PackageSelectorGUI(PackageSelector):
    def __init__(self, path):
        super().__init__(path=path)
        self.selected_folders = []  # List of selected packages

    def toggle_selection(self, folder):
        """
        Toggles a folder selection. If it is already selected, it removes it from the list, otherwise it adds it.
        """
        if folder in self.selected_folders:
            self.selected_folders.remove(folder)  # Deselect
        else:
            self.selected_folders.append(folder)  # Select

        self.update_package_list(self.python_packages)  # Render the new list to reflect the state

    def update_package_list(self, packages):
        """
        Updates the package list, maintaining the selection state.
        """
        # Removes existing widgets
        for widget in self.package_frame.winfo_children():
            widget.destroy()

        # Rebuild list with the newer state
        for package in packages:
            package_name = os.path.basename(package)

            # Create a line for every package
            row = tk.Frame(self.package_frame)
            row.pack(fill=tk.X, pady=2)

            # Label with the name of the package
            label = tk.Label(row, text=package_name, width=40, anchor="w")
            label.pack(side=tk.LEFT, padx=5)

            # Button to toggle selection
            button = tk.Button(row, text="+" if package not in self.selected_folders else "−", 
                               bg="lightgreen" if package not in self.selected_folders else "red")
            button.config(command=lambda p=package: self.toggle_selection(p))
            button.pack(side=tk.LEFT, padx=5)

    def filter_packages(self, event=None):
        """
        Filter packages based on the text entered in the search bar.
        """
        search_text = self.search_entry.get().lower()
        filtered = [pkg for pkg in self.python_packages if search_text in os.path.basename(pkg).lower()]
        self.update_package_list(filtered)

    def document(self):
        """
        When you press the "document" button, it collects the paths of the selected folders
        and closes the window.
        """
        if self.selected_folders:  # If there are selected packages
            self.root.quit()  # Close the window
        else:
            messagebox.showwarning("Uncomplete selection", "You must select at least one package")
            return

        return self.selected_folders  # Returns the list of packages selected

    def create_widgets(self):
        """
        Create the necessary widgets for the graphical interface.
        """
        # Titolo
        label = tk.Label(self.root, text="Select the Python packages for which you want to generate documentation:", font=("Arial", 12))
        label.pack(pady=10)

        # Etichetta per la barra di ricerca
        search_label = tk.Label(self.root, text="Seach packages:", font=("Arial", 10))
        search_label.pack(pady=5)

        # Barra di ricerca
        self.search_entry = tk.Entry(self.root, width=40)
        self.search_entry.pack(pady=5)
        self.search_entry.bind("<KeyRelease>", self.filter_packages)

        # Frame per la lista dei pacchetti
        self.package_frame = tk.Frame(self.root)
        self.package_frame.pack(pady=10)

        # Aggiorna la lista dei pacchetti
        self.update_package_list(self.python_packages)

        # Pulsante "document"
        document_button = tk.Button(self.root, text="Document", command=self.document)
        document_button.pack(pady=20)

    def run(self) -> list[str]:
        """
        Launch the Tkinter GUI and event loop.
        """
        self.root = tk.Tk()
        self.root.title("Select the Python packages for which you want to generate documentation")

        # Gets Python packages from the base directory
        self.python_packages = self.get_python_packages_from_folders()

        # Create GUI widgets
        self.create_widgets()

        # Start the Tkinter event loop
        self.root.mainloop()

        # After closing the window, it returns the selected paths
        return self.selected_folders