#!/bin/bash
# Run task with optimal profile

if [ $# -eq 0 ]; then
    echo "Usage: ./run_with_profile.sh '<task description>'"
    exit 1
fi

TASK="$1"
PROFILE=$(python3 select_profile.py "$TASK")

echo "🎯 Task: $TASK"
echo "📊 Selected Profile: $PROFILE"
echo "🚀 Executing with evolved rule combination..."
echo ""

# Here you would integrate with actual Cursor execution
# For now, we'll show what would happen
echo "Would execute: cursor --profile $PROFILE --task '$TASK'"
