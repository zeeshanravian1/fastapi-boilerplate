#!/bin/bash

# Define threshold score for complexity, maintainability, exclude pattern and
# directory.
# Complexity score is minimum score for average cyclomatic complexity of code.
# Maintainability threshold ensures every file is greater than value set.
COMPLEXITY_SCORE="A"
MAINTAINABILITY_THRESHOLD="B"
EXCLUDE="venv/*"
DIRECTORY="./."

# Run radon cc to check complexity
radon_output=$(radon cc -a -e "$EXCLUDE" "$DIRECTORY")

# Check if radon found any Python files to analyze
if [[ -z "$radon_output" ]]; then
    average_complexity="$COMPLEXITY_SCORE"  # Default to threshold if no files
else
    # Extract average complexity from radon output
    average_complexity=$(echo "$radon_output" | grep -oP '(?<=Average complexity: )\S+' || echo "$COMPLEXITY_SCORE")

    # If average_complexity is empty (grep didn't find a match), set it to threshold
    if [[ -z "$average_complexity" ]]; then
        average_complexity="$COMPLEXITY_SCORE"
    fi
fi

# Calculate maintainability index using Radon's maintainability index tool and
# exclude any patterns specified.
maintainability_issues=$(radon mi -e "$EXCLUDE" "$DIRECTORY" --min "$MAINTAINABILITY_THRESHOLD")

# Check if average complexity is greater than threshold score and print out a
# warning message.
# Exit with a status of 1 if complexity is higher than threshold.
if [[ "$average_complexity" != "$COMPLEXITY_SCORE" ]]; then
    echo "Average complexity ($average_complexity) is higher than allowed threshold ($COMPLEXITY_SCORE)"
    radon cc -s -n "$COMPLEXITY_SCORE" -e "$EXCLUDE" "$DIRECTORY"
    exit 1
else
    echo "Average complexity ($average_complexity) is within allowed threshold ($COMPLEXITY_SCORE)"
fi

# Check if maintainability index is below threshold score and print out a
# warning message with affected files.
# Exit with a status of 1 if maintainability index is below threshold.
if [[ -n "$maintainability_issues" ]]; then
    echo "Maintainability index is below allowed threshold ($MAINTAINABILITY_THRESHOLD) for following files:"
    echo "$maintainability_issues"
    exit 1
else
    echo "Maintainability index is within allowed threshold ($MAINTAINABILITY_THRESHOLD)"
    exit 0
fi
