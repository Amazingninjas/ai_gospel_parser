#!/bin/bash
# Download all Vincent's Word Studies chapters from StudyLight.org
# URL pattern: https://www.studylight.org/commentaries/eng/vnt/{book}-{chapter}.html

# Output directory
OUTPUT_DIR="studylight_html"
mkdir -p "$OUTPUT_DIR"

# Base URL
BASE_URL="https://www.studylight.org/commentaries/eng/vnt"

# NT books with chapter counts
declare -A BOOKS
BOOKS["matthew"]=28
BOOKS["mark"]=16
BOOKS["luke"]=24
BOOKS["john"]=21
BOOKS["acts"]=28
BOOKS["romans"]=16
BOOKS["1-corinthians"]=16
BOOKS["2-corinthians"]=13
BOOKS["galatians"]=6
BOOKS["ephesians"]=6
BOOKS["philippians"]=4
BOOKS["colossians"]=4
BOOKS["1-thessalonians"]=5
BOOKS["2-thessalonians"]=3
BOOKS["1-timothy"]=6
BOOKS["2-timothy"]=4
BOOKS["titus"]=3
BOOKS["philemon"]=1
BOOKS["hebrews"]=13
BOOKS["james"]=5
BOOKS["1-peter"]=5
BOOKS["2-peter"]=3
BOOKS["1-john"]=5
BOOKS["2-john"]=1
BOOKS["3-john"]=1
BOOKS["jude"]=1
BOOKS["revelation"]=22

total_chapters=0
successful=0
failed=0

echo "Downloading Vincent's Word Studies from StudyLight.org..."
echo "=========================================================="

for book in "${!BOOKS[@]}"; do
    chapters=${BOOKS[$book]}
    echo "Downloading $book (${chapters} chapters)..."

    for ((ch=1; ch<=$chapters; ch++)); do
        url="${BASE_URL}/${book}-${ch}.html"
        outfile="${OUTPUT_DIR}/${book}-${ch}.html"

        # Skip if already exists
        if [ -f "$outfile" ]; then
            echo "  ✓ ${book}-${ch}.html (exists)"
            ((successful++))
            ((total_chapters++))
            continue
        fi

        # Download with wget (quiet mode, retry on failure)
        if wget -q -t 3 -T 30 "$url" -O "$outfile" 2>/dev/null; then
            # Check if file is not empty and contains actual content
            if grep -q "commentaries-entry-number" "$outfile" 2>/dev/null; then
                echo "  ✓ ${book}-${ch}.html"
                ((successful++))
            else
                echo "  ✗ ${book}-${ch}.html (no content)"
                rm "$outfile"
                ((failed++))
            fi
        else
            echo "  ✗ ${book}-${ch}.html (download failed)"
            rm -f "$outfile"
            ((failed++))
        fi

        ((total_chapters++))

        # Be nice to the server (small delay)
        sleep 0.5
    done
done

echo ""
echo "=========================================================="
echo "Download Summary:"
echo "  Total chapters: $total_chapters"
echo "  Successful: $successful"
echo "  Failed: $failed"
echo "  Output directory: $OUTPUT_DIR"
echo "=========================================================="
