import os
import shutil

def rename_ue_project(old_project_path, new_project_name):
    # Validate the old project path
    if not os.path.isdir(old_project_path):
        print(f"Error: The specified project path '{old_project_path}' does not exist.")
        return
    
    # Define new project paths and names
    old_project_name = os.path.basename(old_project_path)
    new_project_path = os.path.join(os.path.dirname(old_project_path), new_project_name)
    old_uproject_file = os.path.join(old_project_path, f"{old_project_name}.uproject")
    new_uproject_file = os.path.join(new_project_path, f"{new_project_name}.uproject")

    # Step 1: Rename the project folder
    print(f"Renaming project folder from '{old_project_path}' to '{new_project_path}'...")
    shutil.move(old_project_path, new_project_path)

    # Step 2: Rename the .uproject file
    print(f"Renaming .uproject file from '{old_uproject_file}' to '{new_uproject_file}'...")
    shutil.move(os.path.join(new_project_path, f"{old_project_name}.uproject"), new_uproject_file)

    # Step 3: Update references in .ini files
    config_path = os.path.join(new_project_path, "Config")
    if os.path.isdir(config_path):
        for root, _, files in os.walk(config_path):
            for file in files:
                if file.endswith(".ini"):
                    ini_file = os.path.join(root, file)
                    print(f"Updating references in {ini_file}...")
                    with open(ini_file, "r") as f:
                        content = f.read()
                    updated_content = content.replace(old_project_name, new_project_name)
                    with open(ini_file, "w") as f:
                        f.write(updated_content)

    # Step 4: Rename source code folders and update references
    source_path = os.path.join(new_project_path, "Source")
    if os.path.isdir(source_path):
        for root, dirs, files in os.walk(source_path):
            for dir_name in dirs:
                if old_project_name in dir_name:
                    old_dir = os.path.join(root, dir_name)
                    new_dir = os.path.join(root, dir_name.replace(old_project_name, new_project_name))
                    print(f"Renaming source folder from '{old_dir}' to '{new_dir}'...")
                    shutil.move(old_dir, new_dir)
            for file in files:
                if file.endswith((".h", ".cpp", ".cs")):
                    source_file = os.path.join(root, file)
                    print(f"Updating references in {source_file}...")
                    with open(source_file, "r") as f:
                        content = f.read()
                    updated_content = content.replace(old_project_name, new_project_name)
                    with open(source_file, "w") as f:
                        f.write(updated_content)

    # Step 5: Notify user
    print("Project renamed successfully! Make sure to regenerate project files if needed.")

# Example usage
old_project_path = "/path/to/old/project"  # Replace with your project's current path
new_project_name = "NewProjectName"       # Replace with your desired project name
rename_ue_project(old_project_path, new_project_name)
