# Responsive homepage images

The November 8, 2026 1:00 p.m. EST mobile PageSpeed report flags two oversized homepage images: the hero (231.3 KiB; estimated savings 137.7 KiB) and furnishing photo (187.2 KiB; estimated savings 140.5 KiB). Report: https://pagespeed.web.dev/analysis/https-www-mybnbdesign-com/ecpxxnryj4?form_factor=mobile.

Add 640, 960 and 1280 pixel-wide WebP variants for those two existing photographs. Variants are proportionally resized from the existing optimized files with Pillow LANCZOS, WebP quality 82/method 6. Filename hashes are the first 12 characters of SHA-256. The existing full-size images remain the fallback and highest-resolution candidates.

The hero fills the viewport width. Service images occupy one column up to 768 pixels (viewport minus 64 pixels container padding), then half the container minus the 48 pixel column gap; the container caps at 1100 pixels. Match these existing CSS rules with sizes hints. The media build adds srcset only where a page explicitly supplies sizes, so other image placements are unaffected. Existing eager hero loading, high fetch priority, alt text, dimensions and immutable filename caching are retained.

Guidance: https://web.dev/articles/serve-responsive-images. Verify actual image selection in browser at mobile and desktop widths as well as generated output and decoded image dimensions. A smaller transfer is measurable; do not promise a particular Lighthouse score or ranking change.
