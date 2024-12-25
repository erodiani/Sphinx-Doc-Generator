# Sphinx-Doc-Generator
# Documentation Generation Tool

This project is a Python-based tool designed to help you generate documentation for your Python projects using Sphinx. The tool automates the process of setting up a Sphinx documentation environment and generates HTML and PDF documentation for your project.

## Features

- **Quickstart for Sphinx Project**: The tool runs `sphinx-quickstart` to initialize a Sphinx project with essential configurations.
- **Automated Package Inclusion**: It allows the user to add Python packages to the documentation by scanning their project folder.
- **HTML & PDF Generation**: Based on user input, the tool can generate HTML and PDF documentation from the Sphinx project.
- **Customization**: Customize the LaTeX output with custom front pages and document metadata (project name and author).

## How to use

- Put this project's folder inside your project
- Then open it and run the Sphinx-Doc-Generator.py script
- Answer the prompts shown on terminal
- You have your own, already assembled, folder with the generated doc in the _build section as sphinx provides

## Requirements

- Python 3.x
- Sphinx
- Chardet (used to automatically detect the encoding of .tex files before reading and modifying them)
- LaTeX (for PDF generation)
- pdflatex (required for building the PDF version of the documentation)

To install the required dependencies, run:

```bash
pip install -r requirements.txt
