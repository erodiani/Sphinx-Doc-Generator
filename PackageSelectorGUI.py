import os
import tkinter as tk
from tkinter import messagebox
from PackageSelector import PackageSelector

class PackageSelectorGUI(PackageSelector):
    def __init__(self, path):
        super().__init__(path=path)
        self.selected_folders = []  # Lista delle cartelle selezionate

    def get_python_packages_from_folders(self):
        """
        Scansiona le cartelle nella directory specificata per pacchetti Python (cartelle con __init__.py).
        """
        python_packages = []
        if os.path.exists(self.path):
            for folder in os.listdir(self.path):
                folder_path = os.path.join(self.path, folder)
                if os.path.isdir(folder_path) and "__init__.py" in os.listdir(folder_path):
                    python_packages.append(folder_path)
        return python_packages

    def toggle_selection(self, folder):
        """
        Alterna la selezione di una cartella. Se è già selezionata, la rimuove dalla lista, altrimenti la aggiunge.
        """
        if folder in self.selected_folders:
            self.selected_folders.remove(folder)  # Deseleziona
        else:
            self.selected_folders.append(folder)  # Seleziona

        self.update_package_list(self.python_packages)  # Rende la lista aggiornata per riflettere lo stato

    def update_package_list(self, packages):
        """
        Aggiorna la lista dei pacchetti, mantenendo lo stato di selezione.
        """
        # Rimuove i widget esistenti
        for widget in self.package_frame.winfo_children():
            widget.destroy()

        # Ricostruisce la lista con lo stato di selezione aggiornato
        for package in packages:
            package_name = os.path.basename(package)

            # Crea una riga per ogni pacchetto
            row = tk.Frame(self.package_frame)
            row.pack(fill=tk.X, pady=2)

            # Label per il nome del pacchetto
            label = tk.Label(row, text=package_name, width=40, anchor="w")
            label.pack(side=tk.LEFT, padx=5)

            # Bottone per alternare la selezione
            button = tk.Button(row, text="+" if package not in self.selected_folders else "−", 
                               bg="lightgreen" if package not in self.selected_folders else "red")
            button.config(command=lambda p=package: self.toggle_selection(p))
            button.pack(side=tk.LEFT, padx=5)

    def filter_packages(self, event=None):
        """
        Filtra i pacchetti in base al testo inserito nella barra di ricerca.
        """
        search_text = self.search_entry.get().lower()
        filtered = [pkg for pkg in self.python_packages if search_text in os.path.basename(pkg).lower()]
        self.update_package_list(filtered)

    def documenta(self):
        """
        Quando si preme il pulsante "Documenta", raccoglie i percorsi delle cartelle selezionate
        e chiude la finestra.
        """
        if self.selected_folders:  # Se ci sono cartelle selezionate
            self.root.quit()  # Chiude la finestra
        else:
            messagebox.showwarning("Selezione incompleta", "Devi selezionare almeno una cartella.")

        return self.selected_folders  # Restituisce la lista di percorsi

    def create_widgets(self):
        """
        Crea i widget necessari per l'interfaccia grafica.
        """
        # Titolo
        label = tk.Label(self.root, text="Seleziona i pacchetti Python da documentare:", font=("Arial", 12))
        label.pack(pady=10)

        # Etichetta per la barra di ricerca
        search_label = tk.Label(self.root, text="Cerca pacchetti:", font=("Arial", 10))
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

        # Pulsante "Documenta"
        document_button = tk.Button(self.root, text="Documenta", command=self.documenta)
        document_button.pack(pady=20)

    def run(self) -> list:
        """
        Avvia l'interfaccia grafica e il loop di eventi Tkinter.
        """
        self.root = tk.Tk()
        self.root.title("Seleziona i pacchetti Python da documentare")

        # Ottiene i pacchetti Python dalla directory di base
        self.python_packages = self.get_python_packages_from_folders()

        # Crea i widget dell'interfaccia grafica
        self.create_widgets()

        # Avvia il loop degli eventi Tkinter
        self.root.mainloop()

        # Dopo la chiusura della finestra, ritorna i percorsi selezionati
        return self.selected_folders


# Avvio dell'applicazione
if __name__ == "__main__":
    # Imposta la directory di base dove cercare i pacchetti (aggiusta il percorso se necessario)
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))  # Imposta il percorso
    navigator = PackageSelectorGUI(path)
    
    # Ottiene le cartelle selezionate quando l'utente preme "Documenta"
    selected_folders = navigator.run()
    print(selected_folders)  # Stampa la lista dei percorsi delle cartelle selezionate
