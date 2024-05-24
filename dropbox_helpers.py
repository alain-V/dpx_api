from dropbox import Dropbox
from dropbox.files import FileMetadata, ListFolderResult
from typing import List, Optional, Tuple
from tqdm import tqdm


def list_dirs(dpx: Dropbox, root_path: str) -> Optional[ListFolderResult]:
    try:
        return dpx.files_list_folder(
            root_path,
            recursive=True,
            include_media_info=True,
            include_mounted_folders=True,
        )
    except Exception as e:
        print(f"Error listing directory '{root_path}': {e}")
        return None


def get_total_entries(dbx, root_path: str):
    total_entries = 0
    try:
        result = dbx.files_list_folder(root_path, recursive=True)
        cursor = result.cursor
        total_entries += len(result.entries)
        print(f"Initial count: {total_entries - 1} entries found in root directory.")

        while result.has_more:
            result = dbx.files_list_folder_continue(cursor)
            cursor = result.cursor
            new_entries_count = len(result.entries)
            total_entries += new_entries_count
            print(f"Processed additional {new_entries_count} entries. Total so far: {total_entries} entries.")

    except Exception as e:
        print(f"Error counting files: {e}")
    return total_entries - 1


def list_all_files_recursive(dpx: Dropbox, root_path: str = '') -> Tuple[bool, List[str]]:
    files: List[str] = []

    try:
        result: Optional[ListFolderResult] = list_dirs(dpx, root_path)
        if result is None:
            return False, files

        cursor = result.cursor
        total_entries = get_total_entries(dpx, root_path)

        with tqdm(total=total_entries, desc="Processing files") as pbar:
            while True:
                for entry in result.entries:
                    if isinstance(entry, FileMetadata):
                        files.append(entry.path_display)

                if not result.has_more:
                    break

                result = dpx.files_list_folder_continue(cursor)
                cursor = result.cursor
                pbar.update(len(result.entries))

    except Exception as e:
        print(f"Error retrieving files from '{root_path}': {e}")
        exit(1)

    return True, files


def delete_files(dpx: Dropbox, file_paths: List[str]) -> None:
    for file_path in tqdm(file_paths, desc="Deleting files"):
        try:
            dpx.files_delete_v2(file_path)
            print(f"\nDeleted file: {file_path}")
        except Exception as e:
            print(f"\nError deleting file '{file_path}': {e}")
