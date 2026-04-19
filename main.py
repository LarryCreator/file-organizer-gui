from pathlib import Path

#variables
organization_folders_and_extensions = {
    'images': {'.png', '.jpg', '.jpeg', '.jfif', '.gif', '.svg', '.webp'},
    'documents': {'.txt', '.docx', '.pdf', '.csv', '.xlsx'},
    'audios': {'.mp3', '.wav', '.aiff', '.aac'},
    'videos': {'.mp4', '.avi', '.mkv', '.wmv', '.mov', '.webm'},
    'others': set()
}

#functions
def create_organization_folders(base_dir):
    for folder in organization_folders_and_extensions:
        new_dir = base_dir / folder
        new_dir.mkdir(parents=True, exist_ok=True)

def get_file_destination(base_dir, item):
    suffix = item.suffix.lower()
    for key, value_list in organization_folders_and_extensions.items():
        if suffix in value_list:
            destination = base_dir / key / item.name
            return destination
    destination = base_dir / 'others' / item.name
    return destination

def get_valid_destination(destination):
    item_name = destination.stem
    suffix = destination.suffix.lower()
    destination = destination.parent
    new_destination = destination / f"{item_name}{suffix}"
    index = 1
    while new_destination.is_file():
        new_item_name = item_name + f"-{index}{suffix}"
        new_destination = destination / new_item_name
        index += 1
    return new_destination
            

def move_files(base_dir):
    moved_files = 0
    for item in base_dir.iterdir():
        if item.is_file():
            desired_destination = get_file_destination(base_dir, item)
            valid_destination = get_valid_destination(desired_destination)
            item.rename(valid_destination)
            print(f"{item.name} -> {valid_destination}")
            moved_files += 1
    return moved_files

def organize_folder(main_dir):
    base_dir = Path(main_dir)
    create_organization_folders(base_dir)
    moved_files = move_files(base_dir)
    return moved_files

def main():
    #example C:\Users\USER\Desktop\target_test
    main_dir = Path(input("Absolute path to folder:\n"))
    if main_dir.is_dir():
        moved_files = organize_folder(main_dir)
        print(f"Done!\n\nTotal files moved: {moved_files}")
    else:
        print("This directory does not exist!")

#main call
main()
        
