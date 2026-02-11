import os
from google import genai
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    absolute_path = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(absolute_path, directory))
    valid_target_dir = os.path.commonpath([absolute_path, target_dir]) == absolute_path

    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    
    files = os.listdir(target_dir)
    lines = []

    for file in files:
        try:
            full_path = os.path.join(target_dir, file)

            file_size = os.path.getsize(full_path)
            is_dir = os.path.isdir(full_path)
            lines.append(f"  - {file}: file_size={file_size} bytes, is_dir={is_dir}")
        
        except Exception as e:
            return f"Error: {e}"
    
    return "\n".join(lines)