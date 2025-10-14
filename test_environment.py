"""
Test script to verify all required components for exercises are installed.
"""

import sys
from pathlib import Path


def test_python_version():
    """Check Python version is 3.13 or higher."""
    print("Checking Python version...", end=" ")
    if sys.version_info >= (3, 13):
        print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor}")
        return True
    else:
        print(f"✗ Python {sys.version_info.major}.{sys.version_info.minor} (requires 3.13+)")
        return False


def test_imports():
    """Test if all required packages can be imported with correct versions."""
    packages = {
        "dotenv": ("python-dotenv", None),
        "autogen_agentchat": ("autogen-agentchat", "0.7.5"),
        "autogen_ext": ("autogen-ext", "0.7.5"),
    }

    all_imports_ok = True

    for module_name, (package_name, required_version) in packages.items():
        print(f"Checking {package_name}...", end=" ")
        try:
            module = __import__(module_name)
            if required_version:
                # Check version
                version = getattr(module, "__version__", None)
                if version == required_version:
                    print(f"✓ (version {version})")
                elif version:
                    print(f"✗ version {version} (requires {required_version})")
                    all_imports_ok = False
                else:
                    print(f"⚠ installed but version unknown (requires {required_version})")
            else:
                print("✓")
        except ImportError:
            print(f"✗ (install with: pip install {package_name}=={required_version})" if required_version else f"✗ (install with: pip install {package_name})")
            all_imports_ok = False

    return all_imports_ok


def test_docker():
    """Check if Docker is available."""
    import subprocess

    print("Checking Docker...", end=" ")
    try:
        result = subprocess.run(
            ["docker", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✓ {version}")
            return True
        else:
            print("✗ Docker command failed")
            return False
    except FileNotFoundError:
        print("✗ Docker not found (install from https://www.docker.com/)")
        return False
    except Exception as e:
        print(f"✗ Error checking Docker: {e}")
        return False


def test_docker_running():
    """Check if Docker daemon is running."""
    import subprocess

    print("Checking Docker daemon...", end=" ")
    try:
        result = subprocess.run(
            ["docker", "ps"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            print("✓ Docker daemon is running")
            return True
        else:
            print("✗ Docker daemon not running (start Docker)")
            return False
    except Exception as e:
        print(f"✗ Error checking Docker daemon: {e}")
        return False


def test_work_directory():
    """Check if work directory exists or can be created."""
    work_dir = Path("coding")
    print(f"Checking work directory '{work_dir}'...", end=" ")

    if work_dir.exists():
        if work_dir.is_dir():
            print("✓ Directory exists")
            return True
        else:
            print("✗ Path exists but is not a directory")
            return False
    else:
        try:
            work_dir.mkdir(parents=True, exist_ok=True)
            print("✓ Directory created")
            return True
        except Exception as e:
            print(f"✗ Cannot create directory: {e}")
            return False


def main():
    """Run all tests."""
    print("=" * 60)
    print("Testing environment for Exercise 4: Code Generation with 2 Agents")
    print("=" * 60)
    print()

    results = []

    results.append(("Python Version", test_python_version()))
    print()

    results.append(("Package Imports", test_imports()))
    print()

    results.append(("Docker Installation", test_docker()))
    results.append(("Docker Daemon", test_docker_running()))
    print()

    results.append(("Work Directory", test_work_directory()))
    print()

    print("=" * 60)
    print("Summary:")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")

    print()
    print(f"Tests passed: {passed}/{total}")

    if passed == total:
        print("\n✓ All tests passed! You're ready to run the exercise.")
        return 0
    else:
        print("\n✗ Some tests failed. Please fix the issues above before running the exercise.")
        print("\nNote: API key is not tested here. Make sure to set API_KEY in .env file.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
