import os
import subprocess
import chardet

# Funzione principale che esegue tutte le operazioni
def main():

    # Ottieni la cartella dove si trova lo script
    script_directory = os.path.dirname(os.path.abspath(__file__))
    
    # Chiede il nome della cartella
    project_name = input("Project's name?: ")

    authors = input("Author name(s): ")

    gen_html = ask_html_generation()

    gen_pdf = ask_pdf_generation()

    # Aggiunge il suffisso "-Docs"
    folder_name = f"{project_name}-Docs"
    
    # Crea il percorso completo della cartella di documentazione
    folder_path = os.path.join(script_directory, folder_name)

    # Crea la cartella e ci entra
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    os.chdir(folder_path)
    
  # Prepara le risposte per sphinx-quickstart (simulando l'interazione)
    responses = [
        "",    # Want to create divided folder dir? 
        project_name.lower(),  # Project name
        authors,  # Author names
        "",  # Project release
        "",  # Language of the project
    ]

    # Esegui sphinx-quickstart, passando le risposte simulate
    subprocess.run(
        ["sphinx-quickstart"], 
        input="\n".join(responses) + "\n", 
        text=True,  # To handle input as text
        check=True   # Ensure the process completes successfully
    )
    
    # Apre e modifica il file conf.py
    modify_conf_py()
    
    # Inizia il loop per aggiungere pacchetti alla documentazione
    while True:
        package_name = input("Inserisci il nome di un pacchetto da includere nella documentazione (o scrivi 'q' per terminare): ")

        
        if package_name.lower() == 'q':
            break

        # Controlla se l'input è vuoto
        if not package_name:
            print("Errore: Il nome del pacchetto non può essere vuoto. Riprova.")
            continue  # Ritorna all'inizio del ciclo e chiede nuovamente l'input

        # Definisci il percorso alla cartella che si trova due livelli sopra la cartella corrente
        parent_directory = os.path.abspath(os.path.join(".", os.pardir, os.pardir))  # Vai a ../..
        package_path = os.path.join(parent_directory, package_name)  # Aggiungi il nome del pacchetto
        
        # Controlla se la cartella esiste
        if os.path.isdir(package_path):
            print(f"La cartella '{package_name}' esiste nella cartella precedente.")
            
            # Esegui sphinx-apidoc per il pacchetto fornito
            subprocess.run(["sphinx-apidoc", "-o", ".", f"../../{package_name}"])

            ensure_modules_header()

            # Aggiungi il pacchetto alla fine del file modules.rst
            add_package_to_modules_rst(package_name)
        else:
            print(f"La cartella '{package_name}' non esiste nella cartella precedente.")
    
    # Aggiunge "modules" nel file index.rst
    add_modules_to_index_rst()
    
    # Esegue il comando make html
    #os.chdir(folder_path)
    if gen_html:
        subprocess.run([r".\make.bat", "html"])

    if gen_pdf:
        subprocess.run([r".\make.bat", "latex"])

        # Step 1: Add the custom code after \begin{document}
        tex_file_path = f".\\_build\\latex\\{project_name.lower()}.tex"  # Path to your .tex file
        # Step 1: Read the content of an external file
        code_file_path = "..\\front_page.tex"  # Path to the file containing the code you want to add
        with open(code_file_path, "r") as code_file:
            code_to_insert = code_file.read()  # Read the entire content of the file
            code_to_insert = code_to_insert.replace("Titolo della Documentazione", project_name)
            code_to_insert = code_to_insert.replace("Autore 1, Autore 2, Autore 3", authors)
        add_code_after_begin_document(tex_file_path, code_to_insert)


        # Step 2: Change to the _build/latex directory
        build_latex_dir = os.path.join(os.getcwd(), "_build", "latex")
        if os.path.exists(build_latex_dir):
            os.chdir(build_latex_dir)

            # Step 3: Run pdflatex on the project file
            nome_progetto_tex = f".\\{project_name.lower()}.tex"  # Replace with actual project file name
            nome_progetto_tex_no_ext = f"{project_name.lower()}"

            path = os.getcwd()
            subprocess.run(["pdflatex", nome_progetto_tex])

            # Step 4: Run makeindex to create the index
            subprocess.run(["makeindex", nome_progetto_tex_no_ext])

            # Step 5: Run pdflatex again (to ensure references and index are correct)
            subprocess.run(["pdflatex", nome_progetto_tex])
        else:
            print("Error: _build/latex directory not found!")
        
# Edit conf.py file
def modify_conf_py():
    conf_py_path = "conf.py"
    
    with open(conf_py_path, 'r') as file:
        conf_lines = file.readlines()
    
    # Add the import of the modules
    if not any("import os" in line for line in conf_lines):
        conf_lines.insert(0, "import os\nimport sys\nsys.path.insert(0, os.path.abspath('../../'))\n")
    
    # Add 'sphinx.ext.autodoc' to extensions list
    for i, line in enumerate(conf_lines):
        if line.strip().startswith('extensions = ['):
            conf_lines[i] = "extensions = ["
            conf_lines.insert(i+1, "'sphinx.ext.autodoc'] \n")
            break
    
    with open(conf_py_path, 'w') as file:
        file.writelines(conf_lines)

def ensure_modules_header():
    modules_rst_path = "modules.rst"
    """Controlla se la prima riga di modules.rst è 'Modules', altrimenti la sostituisce."""
    with open(modules_rst_path, 'r') as file:
        existing_lines = file.readlines()

    # Verifica se la prima riga è diversa da 'Modules' e la sostituisce
    if existing_lines and existing_lines[0].strip() != "Modules":
        existing_lines[0] = "Modules\n"  # Sostituisce la prima riga con 'Modules'

        # Riscrive il file con la prima riga corretta
        with open(modules_rst_path, 'w') as file:
            file.writelines(existing_lines)

        print(f"First line of {modules_rst_path} was not 'Modules'. It has been updated.")
    else:
        print(f"First line of {modules_rst_path} is already 'Modules'. No change needed.")


# Add the package name to modules.rst
def add_package_to_modules_rst(package_name):
    modules_rst_path = "modules.rst"
    
    # Read content in modules.rst
    with open(modules_rst_path, 'r') as file:
        existing_lines = file.readlines()

    # Verify if package name is already present
    if any(package_name in line for line in existing_lines):
        print(f"Package {package_name} added to {modules_rst_path}.")
    else:
        # Se non è presente, aggiungilo
        with open(modules_rst_path, 'a') as file:
            file.write(f"   {package_name}\n")
        print(f"Package {package_name} added to {modules_rst_path}.")
    
# Add "modules" to index.rst
def add_modules_to_index_rst():
    index_rst_path = "index.rst"
    
    # Read content from the file
    with open(index_rst_path, 'r') as file:
        index_lines = file.readlines()
    # Initialize variables for the section to remove
    start_line = None
    end_line = None

    # Find the start and end lines for removal
    for i, line in enumerate(index_lines):
        if "===" in line:
            start_line = i+1  # Mark start of the section to remove
        elif ".. toctree::" in line and start_line is not None:
            end_line = i-1  # Mark end of the section to remove
            break

    # If we found the section to remove, delete it
    if start_line is not None and end_line is not None:
        # Remove lines between start and end
        index_lines = index_lines[:start_line] + index_lines[end_line + 1:]

        # Write the modified content back to the file
        with open(index_rst_path, 'w') as file:
            file.writelines(index_lines)
        print("Removed content between '===' and '.. toctree::' in index.rst.")
    else:
        print("No content between '===' and '.. toctree::' found in index.rst.")
    
    # Read content from the file
    with open(index_rst_path, 'r') as file:
        index_lines = file.readlines()

    # Look where to add "modules"
    if "modules" not in [line.strip() for line in index_lines]:
        with open(index_rst_path, 'a') as file:
            file.write("\n   modules\n")
    
# Prompt to know if to generate html
def ask_html_generation():
    while True:
        html = input("Generate HTML? (Y/n): ").strip().lower() or 'y'
        if html in ['y', 'n']:
            return html == 'y'
        else:
            print("Invalid input. Respond with 'Y' for yes or 'N' for no.")

# Prompt to know if to generate pdf
def ask_pdf_generation():
    while True:
        pdf = input("Generate PDF? (Y/n): ").strip().lower() or 'y'
        if pdf in ['y', 'n']:
            return pdf == 'y'
        else:
            print("Invalid input. Respond with 'Y' for yes or 'N' for no.")

# Function to add code to the .tex file after \begin{document}
def add_code_after_begin_document(tex_file_path, code_to_add):
    # Automatically detect the encoding of the file
    with open(tex_file_path, "rb") as file:  # Open in binary mode to detect encoding
        raw_data = file.read()
        detected_encoding = chardet.detect(raw_data)['encoding']

    # Read the file using the detected encoding
    with open(tex_file_path, "r", encoding=detected_encoding) as file:
        lines = file.readlines()
    
    # Find where \begin{document} is and insert the code after it
    for i, line in enumerate(lines):
        if "\\begin{document}" in line:
            # Insert the new code right after \begin{document}
            lines.insert(i + 1, code_to_add + "\n")
            break

    # Remove the \printindex line (if it exists)
    lines = [line for line in lines if "\\printindex" not in line]

    # Write the modified content back to the file using the same encoding
    with open(tex_file_path, "w", encoding=detected_encoding) as file:
        file.writelines(lines)

# Function to remove the content between '===' and '.. toctree::' in index.rst
def remove_content_between_symbols():
    index_rst_path = "index.rst"

    with open(index_rst_path, 'r') as file:
        lines = file.readlines()

    # Initialize variables
    start_line = None
    end_line = None

    # Find the start and end lines for removal
    for i, line in enumerate(lines):
        if "===" in line:
            start_line = i  # Mark start of the section to remove
        elif ".. toctree::" in line and start_line is not None:
            end_line = i  # Mark end of the section to remove
            break

    # If we found the section to remove, delete it
    if start_line is not None and end_line is not None:
        # Remove lines between start and end
        lines = lines[:start_line] + lines[end_line + 1:]

        # Write the modified content back to the file
        with open(index_rst_path, 'w') as file:
            file.writelines(lines)
        print("Removed content between '===' and '.. toctree::' in index.rst.")
    else:
        print("No content between '===' and '.. toctree::' found in index.rst.")

if __name__ == "__main__":
    main()