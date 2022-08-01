import os
import subprocess
import sys
from pathlib import Path

if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    os.environ["CUSTOM_COMPILE_COMMAND"] = "requirements/compile.py"
    common_args = ["-m", "piptools", "compile", "-U", "--generate-hashes"] + sys.argv[1:]

    subprocess.run(
        [
            "python3.10",
            *common_args,
            "-P",
            "Django==3.2",
            "-o",
            "py310-django32.txt",
        ],
        check=True,
    )

    subprocess.run(
        [
            "python3.10",
            *common_args,
            "-P",
            "Django==4.0",
            "-o",
            "py310-django40.txt",
        ],
        check=True,
    )
