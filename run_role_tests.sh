#!/bin/bash
# Run all role tests
# Usage: ./tests/roles/run_tests.sh

set -e

export ANSIBLE_COLLECTIONS_PATH="$(pwd)/collections"
export ANSIBLE_INVENTORY="localhost,"

echo "============================================"
echo "  ansible-stargate Role Tests"
echo "============================================"
echo ""

FAILED=0
PASSED=0

for testfile in tests/roles/test_*.yml; do
    role_name=$(basename "$testfile" | sed 's/test_\(.*\)\.yml/\1/')
    echo "Testing role: $role_name"
    echo "---"
    
    if ansible-playbook -i localhost, "$testfile" 2>&1; then
        echo "✅ $role_name PASSED"
        PASSED=$((PASSED + 1))
    else
        echo "❌ $role_name FAILED"
        FAILED=$((FAILED + 1))
    fi
    echo ""
done

echo "============================================"
echo "  Results: $PASSED passed, $FAILED failed"
echo "============================================"

exit $FAILED