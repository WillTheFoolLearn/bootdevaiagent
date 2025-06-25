import os, subprocess
from google.genai import types

def run_python_file(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    target_dir = os.path.abspath(os.path.join(working_directory, file_path))
    if not target_dir.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(file_path):
        return f'Error: File "{file_path}" not found.'
    
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        completed_process = subprocess.run(["python3", target_dir], timeout=30, text=True, capture_output=True, cwd=working_directory)
    
        result = []
        if completed_process.stdout:
            result.append(f'STDOUT:\n{completed_process.stdout}')
        if completed_process.stderr:
            result.append(f'STDERR:\n{completed_process.stderr}')

        if completed_process.returncode != 0:
            result.append(f'Process existed with code {completed_process.returncode}')
        
        return '\n'.join(result) if result else "No output produced."
    
    except Exception as e:
        return f'Error: executing Python file: "{e}"'
    
schema_run_python = types.FunctionDeclaration(
    name="run_python_file",
    description="Determines whether a file is a Python file or not, attempts to read it and print the STDOUT, STDERR, return code if not 0, and prints the entirety of the file contents.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to read a file from, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file."
                ),
                description="Optional arguments to pass to the Python file."
            )
        },
        required=["file_path"],
    ),
)