from abc import ABC, abstractmethod
import os


class PackageSelector(ABC):

    def __init__(self, path: str):
        self.path = path

    def get_python_packages_from_folders(self):
        """
        Scans the folders inside the specified directory to find the Python packages (folders with __init__.py)
        """
        python_packages = []
        if os.path.exists(self.path):
            for folder in os.listdir(self.path):
                folder_path = os.path.join(self.path, folder)
                if os.path.isdir(folder_path) and "__init__.py" in os.listdir(folder_path):
                    python_packages.append(folder_path)
        return python_packages

    @abstractmethod
    def run() -> list[str]:
        pass