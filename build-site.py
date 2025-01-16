import subprocess
import sys
import os
import webbrowser
import shutil
from pathlib import Path


def run_pip_command(command_args):
    """
    Run a pip command using subprocess in a platform-independent way
    """
    try:
        subprocess.check_call([sys.executable, "-m", "pip"] + command_args)
    except subprocess.CalledProcessError as e:
        print(f"Error running pip command: {e}")
        sys.exit(1)


def run_jupyter_command(notebook_path, output_dir):
    """
    Run jupyter nbconvert in a platform-independent way
    """
    try:
        subprocess.check_call(
            [
                sys.executable,
                "-m",
                "jupyter",
                "nbconvert",
                "--to",
                "html",
                "--execute",
                str(notebook_path),
                "--output-dir",
                str(output_dir),
            ]
        )
    except subprocess.CalledProcessError as e:
        print(f"Error converting notebook {notebook_path}: {e}")
        sys.exit(1)


def copy_directory_contents(src_dir, dest_dir):
    """
    Copy directory contents 
    """
    try:
        for item in src_dir.glob("*"):
            if item.is_file():
                shutil.copy2(item, dest_dir)
            elif item.is_dir():
                shutil.copytree(item, dest_dir / item.name, dirs_exist_ok=True)
    except Exception as e:
        print(f"Error copying directory contents: {e}")
        sys.exit(1)


def setup_environment():
    """
    Set up the Python environment and install requirements
    """
    print("Setting up environment...")

    run_pip_command(["install", "--upgrade", "pip"])

    run_pip_command(["install", "jupyter", "nbconvert"])

    requirements_path = Path("requirements.txt")
    if requirements_path.exists():
        run_pip_command(["install", "-r", str(requirements_path)])
    else:
        print("Warning: requirements.txt not found")


def extend_datasets():
    """
    Run the dataset generation script
    """
    print("Extending datasets...")
    extend_script = Path("extend-datasets.py")
    if extend_script.exists():
        try:
            subprocess.check_call([sys.executable, str(extend_script)])
        except subprocess.CalledProcessError as e:
            print(f"Error extending datasets: {e}")
            sys.exit(1)
    else:
        print("Warning: extend-datasets.py not found")


def convert_notebooks():
    """
    Convert Jupyter notebooks to HTML
    """
    print("Converting notebooks...")

    site_dir = Path("_site")
    images_dir = site_dir / "assets" / "images"
    site_dir.mkdir(exist_ok=True)
    images_dir.mkdir(parents=True, exist_ok=True)

    assets_images = Path("assets") / "images"
    if assets_images.exists():
        copy_directory_contents(assets_images, images_dir)

    template_path = Path("assets") / "templates" / "index.html"
    if template_path.exists():
        shutil.copy2(template_path, site_dir / "index.html")

    for notebook in Path(".").rglob("*.ipynb"):
        if ".ipynb_checkpoints" not in str(notebook):
            run_jupyter_command(notebook, site_dir)


def open_site():
    """
    Open the generated site in the default browser
    """
    index_path = Path("_site") / "index.html"
    if index_path.exists():
        print("Opening site in browser...")
        try:
            webbrowser.open(index_path.absolute().as_uri())
        except Exception as e:
            print(f"Warning: Could not open browser automatically: {e}")
            print(f"Please open {index_path.absolute()} manually")
    else:
        print("Warning: Generated index.html not found")


def main():
    try:
        print("Starting build process...")

        # Run all setup and build steps
        setup_environment()
        extend_datasets()
        convert_notebooks()
        open_site()

        print("Build process completed successfully!")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
