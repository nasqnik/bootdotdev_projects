import os
from google import genai
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description=(
        "Writes the provided text content to a file relative to the working directory. "
        "Creates parent directories if needed and overwrites any existing file."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description=(
                    "Path to the file to write, relative to the working directory "
                    '(for example: "notes/todo.txt" or "pkg/new_module.py").'
                ),
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The full text content to write into the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)

def write_file(working_directory, file_path, content):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(abs_working_dir, file_path))

        common = os.path.commonpath([abs_working_dir, abs_file_path])
        if common != abs_working_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # check the TARGET, not the working dir
        if os.path.isdir(abs_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        parent_dir = os.path.dirname(abs_file_path)
        os.makedirs(parent_dir, exist_ok=True)

        with open(abs_file_path, "w", encoding="utf-8") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"
