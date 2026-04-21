from pathlib import Path
from datetime import datetime

#variables
organization_folders_and_extensions = {
    'images': {'.png', '.jpg', '.jpeg', '.jfif', '.gif', '.svg', '.webp'},
    'documents': {'.txt', '.docx', '.pdf', '.csv', '.xlsx'},
    'audios': {'.mp3', '.wav', '.aiff', '.aac'},
    'videos': {'.mp4', '.avi', '.mkv', '.wmv', '.mov', '.webm'},
    'others': set()
}

#functions
def create_organization_folders(base_dir, categories):
    for folder in categories:
        new_dir = base_dir / folder
        new_dir.mkdir(parents=True, exist_ok=True)

def get_file_destination(base_dir, item, categories):
    suffix = item.suffix.lower()
    for key, value_list in organization_folders_and_extensions.items():
        if suffix in value_list and key in categories:
            destination = base_dir / key / item.name
            return key, destination
        elif suffix in value_list and key not in categories:
            return '', None
    if 'others' in categories:
        destination = base_dir / 'others' / item.name
        return 'others', destination
    else:
        return '', None

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
            

def organize_files(base_dir, categories, operationMode):
    logs = {}
    for item in base_dir.iterdir():
        if item.is_file():
            target_category, desired_destination = get_file_destination(base_dir, item, categories)
            if desired_destination != None:
                valid_destination = get_valid_destination(desired_destination)
                if operationMode=='move':
                    item.move(valid_destination)
                else:
                    item.copy(valid_destination)
                if 'details' in logs:
                    logs['details'].append(f"{item.name} -> {valid_destination}")
                else:
                    logs['details'] = []
                    logs['details'].append(f"{item.name} -> {valid_destination}")

                if target_category in logs:
                    logs[target_category] += 1
                else:
                    logs[target_category] = 1

                if "total" in logs:
                    logs["total"] += 1
                else:
                    logs["total"] = 1
    return logs

def organize_folder(main_dir, categories, operationMode):
    base_dir = Path(main_dir)
    create_organization_folders(base_dir, categories)
    logs = organize_files(base_dir, categories, operationMode)
    return logs

def exportLogs(folderPath, logs):
    fileName = f"{folderPath}/Logs-{datetime.now().strftime('%H_%M_%S')}.txt"
    with open(fileName, "w") as logFile:
        for log in logs:
            logFile.write(f"{log}\n")
    return fileName

def main(folderPath, categories, operationMode):
    error = ""
    logs = None
    if len(categories) == 0:
        error = "category"
    if folderPath == None:
        error = "folder"
    if error == "":
        main_dir = Path(folderPath)
        logs = organize_folder(main_dir, categories, operationMode)
    print(logs)
    return {"errors": error, "logs": logs}
   
