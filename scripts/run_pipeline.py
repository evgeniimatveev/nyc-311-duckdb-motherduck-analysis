import subprocess
import sys


def run_step(label: str, command: list[str]) -> None:
    print(f"\n=== {label} ===")
    result = subprocess.run(command)
    if result.returncode != 0:
        print(f"{label} failed with exit code {result.returncode}")
        sys.exit(result.returncode)


def main() -> None:
    run_step("Running ELT pipeline", ["python", "scripts/4_2_elt.py"])
    run_step("Running export pipeline", ["python", "scripts/4_3_export.py"])
    run_step("Running validation", ["python", "scripts/check_exports.py"])
    print("\nPipeline completed successfully.")


if __name__ == "__main__":
    main()
