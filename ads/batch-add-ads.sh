#!/bin/bash
# Batch script to add Adsterra ads to all calculator tools
# Usage: ./batch-add-ads.sh "AD_CODE_728x90" "AD_CODE_300x250"

AD_728x90="$1"
AD_300x250="$2"

if [ -z "$AD_728x90" ] || [ -z "$AD_300x250" ]; then
    echo "Usage: ./batch-add-ads.sh 'AD_CODE_728x90' 'AD_CODE_300x250'"
    exit 1
fi

# Directory containing HTML files
DIR="/Users/austin/Personal/economic-activity/projects/static-tools"

# Count of updated files
COUNT=0

for file in "$DIR"/*-calculator.html "$DIR"/*-converter.html; do
    if [ -f "$file" ]; then
        # Skip if already has ads
        if grep -q "adsterra" "$file" 2>/dev/null; then
            echo "Skipping (already has ads): $file"
            continue
        fi

        echo "Processing: $file"
        COUNT=$((COUNT + 1))
    fi
done

echo "Found $COUNT files to update"
echo "Run with actual ad codes to update files"
