import os
import subprocess
import chardet
import sys
source = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(source)
from PackageSelectorTUI import PackageSelectorTUI
from PackageSelectorGUI import PackageSelectorGUI


class SphinxDocGenerator():
    def __init__(self, path: str, interfaceType: str = ["GUI", "TUI"]):
        self.path = path
        self.path = self.path.replace("\\", "\\\\")
        if interfaceType == "TUI":
            self.navigator = PackageSelectorTUI(path=self.path)
        if interfaceType == "GUI":
            self.navigator = PackageSelectorGUI(path=self.path)

    def run(self):
        script_directory = os.path.dirname(os.path.abspath(__file__))
        project_name = input("Project's name?: ")
        authors = input("Author name(s): ")
        gen_html = self.ask_html_generation()
        gen_pdf = self.ask_pdf_generation()
        folder_name = f"{project_name}-Docs"
        folder_path = os.path.join(script_directory, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        os.chdir(folder_path)
        responses = [
            "",    # Want to create divided folder dir? 
            project_name.lower(),  # Project name
            authors,  # Author names
            "",  # Project release
            "",  # Language of the project
        ]
        subprocess.run(
            ["sphinx-quickstart"], 
            input="\n".join(responses) + "\n", 
            text=True,  # To handle input as text
            check=True   # Ensure the process completes successfully
        )
        self.modify_conf_py()
        packages = self.navigator.run()
        for package in packages:
            if os.path.isdir(package):
                print(f"Package '{package}' was found.")
                
                # Generate .rst files with sphinx-apidoc
                subprocess.run(["sphinx-apidoc", "-o", ".", f"{package}"])

                # Add the .rst file to modules.rst
                self.add_package_to_modules_rst(os.path.basename(package))
            else:
                print(f"Folder '{package}' does not exist.")
        self.update_modules_header()
        self.add_modules_to_index_rst()
        if gen_html:
            subprocess.run([r".\make.bat", "html"])
        if gen_pdf:
            subprocess.run([r".\make.bat", "latex"])

            
            # Step 1: Add the custom code after \begin{document}
            tex_file_path = f".\\_build\\latex\\{project_name.lower()}.tex"  # Path to your .tex file
            # Step 2: Read the content of an external file
            """
            code_file_path = "..\\front_page.tex"  # Path to the file containing the code you want to add
            with open(code_file_path, "r") as code_file:
                code_to_insert = code_file.read()  # Read the entire content of the file
                code_to_insert = code_to_insert.replace("Documentation title", project_name)
                code_to_insert = code_to_insert.replace("Author 1, Author 2", authors)
            self.add_code_after_begin_document(tex_file_path, code_to_insert)
            """
            # Change to the _build/latex directory
            build_latex_dir = os.path.join(os.getcwd(), "_build", "latex")
            
            if os.path.exists(build_latex_dir):
                os.chdir(build_latex_dir)

                # Step 4: Run pdflatex on the project file
                nome_progetto_tex = os.path.join(".", f"{project_name.lower()}.tex")
                nome_progetto_tex_no_ext = f"{project_name.lower()}"

                path = os.getcwd()
                subprocess.run(["pdflatex", nome_progetto_tex])

                # Step 5: Run makeindex to create the index
                subprocess.run(["makeindex", nome_progetto_tex_no_ext])

                # Step 6: Run pdflatex again (to ensure references and index are correct)
                subprocess.run(["pdflatex", nome_progetto_tex])
            else:
                print("Error: _build/latex directory not found!")

    # Change the top name of modules.rst in "Modules"
    def update_modules_header(self):
        file_path = "modules.rst"
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            if lines and lines[0].strip() != "Modules":
                lines[0] = "Modules\n"
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.writelines(lines)
        except FileNotFoundError:
            print(f"File {file_path} does not exist.")
        except Exception as e:
            print(f"Error during editing of file: {e}")    

    """
    Add the path to packages in the conf.py 
    Add the extension to use sphinx-apidoc
    """
    def modify_conf_py(self):
        conf_py_path = "conf.py"
        
        with open(conf_py_path, 'r') as file:
            conf_lines = file.readlines()
        
        # Add the import of the modules
        if not any("import os" in line for line in conf_lines):
            conf_lines.insert(0, f"import os\nimport sys\nsys.path.append('{self.path}')\n")
        
        # Add 'sphinx.ext.autodoc' to extensions list
        for i, line in enumerate(conf_lines):
            if line.strip().startswith('extensions = ['):
                conf_lines[i] = "extensions = ["
                conf_lines.insert(i+1, "'sphinx.ext.autodoc'] \n")
                break
        
        with open(conf_py_path, 'w') as file:
            file.writelines(conf_lines)

    # Add the package name to modules.rst
    def add_package_to_modules_rst(self,package_name):
        modules_rst_path = "modules.rst"
        
        # Read content in modules.rst
        with open(modules_rst_path, 'r') as file:
            existing_lines = file.readlines()

        # Verify if package name is already present
        if any(package_name in line for line in existing_lines):
            print(f"Package {package_name} added to {modules_rst_path}.")
        else:
            # If package is not in the file, add it
            with open(modules_rst_path, 'a') as file:
                file.write(f"   {package_name}\n")
            print(f"Package {package_name} added to {modules_rst_path}.")
        
    # Add "modules" to index.rst
    def add_modules_to_index_rst(self):
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
    def ask_html_generation(self):
        while True:
            html = input("Generate HTML? (Y/n): ").strip().lower() or 'y'
            if html in ['y', 'n']:
                return html == 'y'
            else:
                print("Invalid input. Respond with 'Y' for yes or 'N' for no.")

    # Prompt to know if to generate pdf
    def ask_pdf_generation(self):
        while True:
            pdf = input("Generate PDF? (Y/n): ").strip().lower() or 'y'
            if pdf in ['y', 'n']:
                return pdf == 'y'
            else:
                print("Invalid input. Respond with 'Y' for yes or 'N' for no.")

    # Function to add code to the .tex file after \begin{document}
    def add_code_after_begin_document(self,tex_file_path, code_to_add):
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
    def remove_content_between_symbols(self):
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
