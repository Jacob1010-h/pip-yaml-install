import platform
import subprocess
import sys
from typing import Dict

import yaml


def install_packages(packages: Dict[str, str]) -> None:
    """Install packages using pip."""
    for package, version in packages.items():
        try:
            print(f"Installing {package}=={version}...")
            # Use the same pip executable that's running this script
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", f"{package}=={version}"],
                stdout=subprocess.DEVNULL,
            )
            print(f"Successfully installed {package}=={version}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {package}=={version}: {e}")
        except Exception as e:
            print(f"Unexpected error installing {package}=={version}: {e}")


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <path_to_yaml_file>")
        sys.exit(1)

    yaml_file = sys.argv[1]

    try:
        with open(yaml_file, "r") as f:
            packages = yaml.safe_load(f)

        if not isinstance(packages, dict):
            print(
                "Error: YAML file must contain key-value pairs of package names and versions"
            )
            sys.exit(1)

        print(f"Found {len(packages)} packages to install")
        print(f"Python executable: {sys.executable}")
        print(f"Platform: {platform.system()} {platform.release()}")

        install_packages(packages)

    except FileNotFoundError:
        print(f"Error: File '{yaml_file}' not found")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
