#!/bin/bash
for img in assets/images/image-{11..15}.jpg; do
  # Créer versions WebP
  cwebp -q 85 "$img" -o "${img%.jpg}.webp"

  # Créer versions responsive
  convert "$img" -resize 400x "${img%.jpg}-400.jpg"
  convert "$img" -resize 800x "${img%.jpg}-800.jpg"
  convert "$img" -resize 1200x "${img%.jpg}-1200.jpg"
done
