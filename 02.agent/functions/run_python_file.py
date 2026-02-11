import os
import subprocess

from google import genai
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description=(
        "Executes a Python file within the working directory sandbox and returns "
        "its stdout and stderr, along with the exit code if non-zero."
    ),
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description=(
                    "Path to the Python file to run, relative to the working directory "
                    '(for example: "calculator/main.py" or "scripts/tool.py").'
                ),
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description=(
                    "Optional list of string arguments to pass to the Python file "
                    "after the file path, in order."
                ),
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Single command-line argument."
                ),
            ),
        },
        required=["file_path"],
    ),
)

def run_python_file(working_directory, file_path, args=None):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(abs_working_dir, file_path))

        common = os.path.commonpath([abs_working_dir, abs_file_path])
        if common != abs_working_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(abs_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", abs_file_path]

        if args:
            command.extend(args)
        
        process = subprocess.run(
            command,
            cwd=abs_working_dir,
            capture_output=True,
            text=True,
            timeout=30
            )

        output_parts = []

        if process.returncode != 0:
            output_parts.append(f"Process exited with code {process.returncode}")

        stdout = process.stdout.strip()
        stderr = process.stderr.strip()

        if not stdout and not stderr:
            output_parts.append("No output produced")
        else:
            if stdout:
                output_parts.append(f"STDOUT:\n{stdout}")
            if stderr:
                output_parts.append(f"STDERR:\n{stderr}")

        return "\n".join(output_parts)


    except Exception as e:
        return f"Error: {e}"