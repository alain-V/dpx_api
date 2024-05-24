import time
from dotenv import load_dotenv
from typing import List

from dropbox import Dropbox
from dropbox.users import FullAccount

from regex_filter import filter_by_pattern
from dropbox_connector import initialize_dropbox
from dropbox_helpers import list_all_files_recursive, delete_files

load_dotenv()

start_time: float = time.perf_counter()
dpx: Dropbox = initialize_dropbox()

current_user: FullAccount = dpx.users_get_current_account()
username: str = current_user.name.display_name
print(f"Hi {username}")

root_path: str = '/Applications'
# root_path: str = ''
print(f"Getting all files from root directory: '{root_path}'")

exists, recur_root_files_path = list_all_files_recursive(dpx, root_path)
elapsed_time: float = time.perf_counter() - start_time

n_recur_root_files_path: int = len(recur_root_files_path)
if not exists:
    print(f"Root path not found: {root_path}")
    exit(1)

# for file_path in recur_root_files_path:
#     print(f"File: {file_path}")

print(f"\nTotal files retrieved: {n_recur_root_files_path}")
print(f"Elapsed time: {elapsed_time:.2f} ms")

pattern: str = r'.*/try\.txt$'
# pattern: str = r'.pdf'
filtered_files: List[str] = filter_by_pattern(recur_root_files_path, pattern, case_insensitive=True)

n_filtered_files: int = len(filtered_files)
if n_filtered_files == 0:
    print(f"No file with the corresponding pattern {pattern} was found in {root_path}")
    exit(1)

print(f"\nFiltered Files ({n_filtered_files}) - {n_filtered_files/n_recur_root_files_path:.2%}")
for file_path in filtered_files:
    print(f"File: {file_path}")

ask_permission = input("Do you want to delete these files? (yes/no): ").strip().lower() == 'yes'
if ask_permission:
    print("\nRemoving the concerned files from Dropbox:")
    delete_files(dpx, filtered_files)
    print(f"Deleted files: {filtered_files}")
else:
    print("No files were deleted.")
