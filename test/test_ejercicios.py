import subprocess
import sys
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_program(filename, input_text):
    result = subprocess.run(
        [sys.executable, str(ROOT / filename)],
        input=input_text,
        text=True,
        capture_output=True,
        timeout=5
    )
    assert result.returncode == 0, result.stderr
    return result.stdout


def extract_numbers(output):
    return [float(x) for x in re.findall(r"-?\d+\.\d+|-?\d+", output)]


def assert_roots(output, expected):
    nums = extract_numbers(output)
    roots = nums[-2:]
    assert len(roots) == 2
    assert sorted(round(x, 2) for x in roots) == sorted(expected)


def test_ejercicio1_caso_base():
    output = run_program("ejercicio1.py", "1\n-11\n24\n")
    assert "x1:" in output
    assert "x2:" in output
    assert_roots(output, [3.00, 8.00])


def test_ejercicio1_otro_caso():
    output = run_program("ejercicio1.py", "1\n-5\n6\n")
    assert_roots(output, [2.00, 3.00])


def test_ejercicio1_dos_decimales():
    output = run_program("ejercicio1.py", "1\n-11\n24\n")
    assert re.search(r"x1:\s*-?\d+\.\d{2}", output)
    assert re.search(r"x2:\s*-?\d+\.\d{2}", output)


def test_ejercicio2_caso_base():
    output = run_program("ejercicio2.py", "4 -12 5\n")
    assert "x1:" in output
    assert "x2:" in output
    assert_roots(output, [0.50, 2.50])


def test_ejercicio2_otro_caso():
    output = run_program("ejercicio2.py", "1 -5 6\n")
    assert_roots(output, [2.00, 3.00])


def test_ejercicio2_no_usa_split():
    code = (ROOT / "ejercicio2.py").read_text(encoding="utf-8")
    assert ".split(" not in code
    assert "split(" not in code