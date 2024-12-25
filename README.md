# Sphinx-Doc-Generator
# Documentation Generation Tool

This project is a Python-based tool designed to help you generate documentation for your Python projects using Sphinx. The tool automates the process of setting up a Sphinx documentation environment and generates HTML and PDF documentation for your project.

## Features

- **Quickstart for Sphinx Project**: The tool runs `sphinx-quickstart` to initialize a Sphinx project with essential configurations.
- **Automated Package Inclusion**: It allows the user to add Python packages to the documentation by scanning their project folder.
- **HTML & PDF Generation**: Based on user input, the tool can generate HTML and PDF documentation from the Sphinx project.
- **Customization**: Customize the LaTeX output with custom front pages and document metadata (project name and author).

## Requirements

- Python 3.x
- Sphinx
- LaTeX (for PDF generation)
- pdflatex (required for building the PDF version of the documentation)

To install the required dependencies, run:

```bash
pip install -r requirements.txt
