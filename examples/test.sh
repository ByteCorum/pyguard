#!/usr/bin/env bash
# Local equivalent of the "Llinux-tests.yml" GitHub Actions jobs.
#
# Usage:
#   ./test.sh                # run all 6 tests
#   ./test.sh complex        # run a single test group:
#                                        # complex | multifile | onefile |
#                                        # complex-legacy | multifile-legacy | onefile-legacy

set -uo pipefail

EXAMPLES_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$EXAMPLES_DIR/.." && pwd)"

if [ ! -f "$REPO_ROOT/src/main.py" ]; then
    echo "ERROR: could not locate src/main.py" >&2
    exit 1
fi

PYTHON="${PYTHON:-python3}"

run_test() {
    local name="$1"
    local example_dir="$2"
    shift 2

    echo
    echo "============================================================"
    echo "Running: $name"
    echo "============================================================"

    local target="$EXAMPLES_DIR/$example_dir"

    if [ ! -d "$target" ]; then
        echo "Failure: examples/$example_dir does not exist"
        return 1
    fi

    # Preparation For Test
    rm -rf "$target/obfuscated"

    # Obfuscation Test
    if ! (
        cd "$target" || exit 1
        "$PYTHON" ../../src/main.py "$@"
    ); then
        echo "Failure: obfuscation step failed for $name"
        return 1
    fi

    # Testing Results
    local output
    if ! output=$( cd "$target/obfuscated" && "$PYTHON" main.py ); then
        echo "Failure: running obfuscated main.py failed for $name"
        return 1
    fi

    echo "Output: $output"
    echo "Result: "
    if [ "$output" = "hello world" ]; then
        echo "Success: main.py output contains 'hello world'"
        return 0
    else
        echo "Failure: main.py output does not contain 'hello world'"
        return 1
    fi
}

# Test definitions
declare -A TESTS=(
    [complex]="
        obfuscate
        --aes --hashdata --fernet --chacha --base64
        --recursive 8 --follow-imports --no-input
        --files proxy.py --dirs dir main.py
    "
    [multifile]="
        obfuscate
        --aes --hashdata --fernet --chacha --base64
        --recursive 8 --follow-imports --no-input
        --files lib.py main.py
    "
    [onefile]="
        obfuscate
        --aes --hashdata --fernet --chacha --base64
        --recursive 8 --follow-imports --no-input
        main.py
    "
    [complex-legacy]="
        obfuscatelegacy
        --no-input --mode 4 --loops 6 --seplen 64
        --dirs dir --files main.py,proxy.py
    "
    [multifile-legacy]="
        obfuscatelegacy
        --no-input --mode 4 --loops 6 --seplen 64
        --files lib.py,main.py
    "
    [onefile-legacy]="
        obfuscatelegacy
        --no-input --mode 4 --loops 6 --seplen 64
        --files main.py
    "
)

# Test key
declare -A EXAMPLE_DIR=(
    [complex]="complex"
    [multifile]="multifile"
    [onefile]="onefile"
    [complex-legacy]="complex-legacy"
    [multifile-legacy]="multifile-legacy"
    [onefile-legacy]="onefile-legacy"
)

# Main
FAILED=()
PASSED=()

if [ $# -gt 0 ]; then
    KEYS=("$@")
else
    KEYS=(complex multifile onefile complex-legacy multifile-legacy onefile-legacy)
fi

for key in "${KEYS[@]}"; do
    if [ -z "${TESTS[$key]:-}" ]; then
        echo "Unknown test: $key" >&2
        echo "Valid tests: ${!TESTS[*]}" >&2
        exit 1
    fi
    # shellcheck disable=SC2086
    if run_test "$key" "${EXAMPLE_DIR[$key]}" ${TESTS[$key]}; then
        PASSED+=("$key")
    else
        FAILED+=("$key")
    fi
done

echo
echo "============================================================"
echo "Summary"
echo "============================================================"
echo "Passed: ${PASSED[*]:-none}"
echo "Failed: ${FAILED[*]:-none}"

if [ ${#FAILED[@]} -gt 0 ]; then
    exit 1
fi
exit 0
