import os
from google.genai import types

def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    target_dir = os.path.abspath(os.path.join(working_directory, file_path))
    if not target_dir.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(target_dir):
        try:
            os.makedirs(os.path.dirname(target_dir), exist_ok=True)
        except Exception as e:
            return f'Error: Unable to create directory: {e}'

    if os.path.exists(target_dir) and os.path.isdir(target_dir):
        return f'Error: {file_path} is a directory, not a file'
    
    try:
        with open(target_dir, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: Unable to write contents: {e}'
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Creates a new file to write the specified contents to or overwrites an existing file if it already exists. Will also create the directory path if it doesn't exist.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path to read a file from, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The provided contents that are written to the file."
            )
        },
        required=["file_path", "content"]
    ),
)