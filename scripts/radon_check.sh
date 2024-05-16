#!/bin/bash

# Define the threshold score for complexity, maintainability, exclude pattern and directory
# Complexity score is the minimum score for the average cyclomatic complexity of the code
# The maintainability threshold ensures every file is greater than the value set.
COMPLEXITY_SCORE="A"
MAINTAINABILITY_THRESHOLD="B"
EXCLUDE="venv/*"
DIRECTORY="./."

# Calculate the average complexity using Radon's code complexity tool and
# exclude any patterns specified
average_complexity=$(radon cc -a -e "$EXCLUDE" "$DIRECTORY" | grep -oP '(?<=Average complexity: )\S+')

# Calculate the maintainability index using Radon's maintainability index tool and exclude any
# patterns specified
maintainability_index=$(radon mi -e "$EXCLUDE" "$DIRECTORY" --min "$MAINTAINABILITY_THRESHOLD")

# Check if the average complexity is greater than the threshold score and print
# out a warning message
# Exit with a status of 1 if the complexity is higher than the threshold
if [  "$average_complexity" != "$COMPLEXITY_SCORE" ]; then
    echo "Average complexity ($average_complexity) is higher than allowed threshold ($COMPLEXITY_SCORE)"
    radon cc -s -n "$COMPLEXITY_SCORE" -e "$EXCLUDE" "$DIRECTORY"
    exit 1
else
    echo "Average complexity ($average_complexity) is within the allowed threshold ($COMPLEXITY_SCORE)"
fi

# Check if the maintainability index is below the threshold score and print out a warning message
# with the affected files
# Exit with a status of 1 if the maintainability index is below the threshold
if [ -n "$maintainability_issues" ]; then
    echo "Maintainability index is below the allowed threshold ($MAINTAINABILITY_THRESHOLD) for the following files:"
    echo "$maintainability_issues"
    exit 1
else
    echo "Maintainability index is within the allowed threshold ($MAINTAINABILITY_THRESHOLD)"
    exit 0
fi
