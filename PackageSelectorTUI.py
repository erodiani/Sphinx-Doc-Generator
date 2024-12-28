import os
from prompt_toolkit import prompt
from prompt_toolkit.key_binding import KeyBindings
from PackageSelector import PackageSelector

class PackageSelectorTUI(PackageSelector):
    def __init__(self, path):
        super().__init__(path=path)
        self.folders = self.get_folders_with_init()
        self.selected_folders = []
        self.selected = [False] * len(self.folders)
        self.current_row = 0

    def get_folders_with_init(self):
        """Ottiene tutte le cartelle con un file __init__.py al loro interno."""
        folders = []
        for folder in os.listdir(self.path):
            folder_path = os.path.join(self.path, folder)
            if os.path.isdir(folder_path) and '__init__.py' in os.listdir(folder_path):
                folders.append(folder_path)
        return folders

    def render_folders(self):
        """Renderizza la lista delle cartelle e mostra la selezione."""
        print("\033c", end="")  # Comando per pulire la console (funziona su molti terminali)

        # Visualizza il messaggio continuo
        print("Seleziona le cartelle con Enter, usa le frecce per navigare, 'q' per uscire.\n")

        # Visualizza le cartelle con una freccia accanto a quella selezionata
        for idx, folder in enumerate(self.folders):
            prefix = "->" if idx == self.current_row else "  "
            selection = "[X]" if self.selected[idx] else "[ ]"
            if idx == self.current_row:
                print(f"{prefix} {os.path.basename(folder)} {selection}")  # Evidenzia la riga selezionata
            else:
                print(f"   {os.path.basename(folder)} {selection}")  # Righe non selezionate

    def run(self) -> list[str]:
        """Visualizza le cartelle e gestisce l'input dell'utente."""
        kb = KeyBindings()

        # Gestione della freccia su
        @kb.add('up')
        def up(event):
            if self.current_row > 0:
                self.current_row -= 1
                self.render_folders()  # Rende la nuova lista dopo la selezione

        # Gestione della freccia giù
        @kb.add('down')
        def down(event):
            if self.current_row < len(self.folders) - 1:
                self.current_row += 1
                self.render_folders()  # Rende la nuova lista dopo la selezione

        # Gestione della selezione/deselezione
        @kb.add('enter')
        def select(event):
            self.selected[self.current_row] = not self.selected[self.current_row]
            self.render_folders()  # Rende la nuova lista dopo la selezione

        # Gestione della chiusura con 'q'
        @kb.add('q')
        def quit(event):
            """Premendo 'q' esci e ritorna le cartelle selezionate."""
            self.selected_folders = [self.folders[i] for i, sel in enumerate(self.selected) if sel]
            raise KeyboardInterrupt  # Interrompe il loop per uscire

        # Rende la lista iniziale
        self.render_folders()

        # Ciclo principale
        try:
            while True:
                prompt("", key_bindings=kb)  # Mostra il prompt e ascolta le scorciatoie da tastiera
        except KeyboardInterrupt:
            # Ritorna la lista delle cartelle selezionate
            return self.selected_folders

# Funzione per eseguire l'interfaccia TUI
def run_folder_selector(path) -> list[str]:
    folder_selector = PackageSelectorTUI(path)
    selected_folders = folder_selector.run()
    print("\nCartelle selezionate:")
    for folder in selected_folders:
        print(folder)
    return selected_folders

# Esegui il programma con un percorso di esempio
if __name__ == "__main__":
    # Sostituisci con il percorso che desideri esplorare
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    prova = run_folder_selector(path)
    print(prova)
