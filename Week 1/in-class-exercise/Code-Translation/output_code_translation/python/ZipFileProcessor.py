import os
import sys
import zipfile
from dataclasses import dataclass
from typing import List


@dataclass
class ZipFileInfo:
    filename: str
    mode: str


class ZipFileProcessor:
    def __init__(self, zip_file_path: str):
        self.zip_file_path_ = zip_file_path

    def read_zip_file(self) -> ZipFileInfo:
        info = ZipFileInfo(filename=self.zip_file_path_, mode="r")
        try:
            with zipfile.ZipFile(self.zip_file_path_, "r"):
                pass
        except Exception:
            # If opening fails, info remains but caller can handle missing file
            pass
        return info

    def extract_all(self, output_directory: str) -> bool:
        if not output_directory:
            return False

        if not self._create_directory_if_not_exists(output_directory):
            return False

        try:
            with zipfile.ZipFile(self.zip_file_path_, "r") as archive:
                success = True
                for zip_info in archive.infolist():
                    output_path = os.path.join(output_directory, zip_info.filename)
                    if not self._extract_file_from_zip(archive, zip_info, output_path):
                        success = False
                return success
        except Exception as e:
            sys.stderr.write(f"Failed to open zip file: {self.zip_file_path_}\n")
            return False

    def extract_file(self, file_name: str, output_directory: str) -> bool:
        if not output_directory:
            return False

        if not self._create_directory_if_not_exists(output_directory):
            sys.stderr.write(f"Failed to create output directory: {output_directory}\n")
            return False

        try:
            with zipfile.ZipFile(self.zip_file_path_, "r") as archive:
                try:
                    zip_info = archive.getinfo(file_name)
                except KeyError:
                    sys.stderr.write(f"File not found in zip: {file_name}\n")
                    return False

                output_path = os.path.join(output_directory, file_name)
                return self._extract_file_from_zip(archive, zip_info, output_path)
        except Exception:
            sys.stderr.write(f"Failed to open zip file: {self.zip_file_path_}\n")
            return False

    def create_zip_file(self, files: List[str], output_zip_file: str) -> bool:
        try:
            with zipfile.ZipFile(output_zip_file, mode="w", compression=zipfile.ZIP_DEFLATED) as archive:
                for file_path in files:
                    if not os.path.isfile(file_path):
                        sys.stderr.write(f"Error adding file to zip (not a file): {file_path}\n")
                        return False
                    try:
                        archive.write(file_path, arcname=file_path)
                    except Exception:
                        sys.stderr.write(f"Error adding file to zip: {file_path}\n")
                        return False
            return True
        except Exception:
            sys.stderr.write(f"Error opening zip file: {output_zip_file}\n")
            return False

    # Private helpers
    def _extract_file_from_zip(self, archive: zipfile.ZipFile, zip_info: zipfile.ZipInfo, output_file_path: str) -> bool:
        try:
            # Ensure parent directories exist
            parent_dir = os.path.dirname(output_file_path)
            if parent_dir and not self._create_directory_if_not_exists(parent_dir):
                return False

            with archive.open(zip_info, "r") as src, open(output_file_path, "wb") as dst:
                while True:
                    chunk = src.read(4096)
                    if not chunk:
                        break
                    dst.write(chunk)
            return True
        except Exception as e:
            sys.stderr.write(f"Failed to extract file {zip_info.filename}: {e}\n")
            return False

    def _create_directory_if_not_exists(self, dir_path: str) -> bool:
        try:
            os.makedirs(dir_path, exist_ok=True)
            return True
        except Exception:
            return False
