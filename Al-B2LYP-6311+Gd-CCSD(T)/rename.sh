#!/bin/bash

for file in cc-Al*.log; do
    newname="${file#cc-}"
    mv "$file" "$newname"
done


# Loop through all matching files
for file in *; do
  # Skip if it's not a file
  [ -f "$file" ] || continue

  # New name with replacements
  newname="$file"
  newname="${newname//-a-/-anion-}"
  newname="${newname//-n-/-neutral-}"
  newname="${newname//-c-/-cation-}"
  newname="${newname//-s/-singlet}"
  newname="${newname//-t/-triplet}"
  newname="${newname//-d/-doublet}"
  newname="${newname//-q/-quartet}"

  # Rename if name changed
  if [[ "$file" != "$newname" ]]; then
    mv "$file" "$newname"
    echo "Renamed: $file → $newname"
  fi
done