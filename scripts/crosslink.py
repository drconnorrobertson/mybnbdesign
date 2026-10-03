"""
Cross-linking engine for MyBnBDesign.
Adds 3-5 contextual internal links within body text of every HTML page.
Run via: python scripts/crosslink.py
"""
import re, os, glob

DOMAIN = "https://www.mybnbdesign.com"

LINK_MAP = {
    "beach house": "/blog/beach-house-airbnb-interior-design.html",
    "mountain cabin": "/blog/mountain-cabin-airbnb-interior-design.html",
    "urban apartment": "/blog/urban-apartment-airbnb-interior-design.html",
    "lake house": "/blog/lake-house-airbnb-interior-design.html",
    "desert property": "/blog/desert-airbnb-interior-design.html",
    "A-frame": "/blog/a-frame-airbnb-interior-design.html",
    "farmhouse property": "/blog/farmhouse-airbnb-interior-design.html",
    "ski chalet": "/blog/ski-chalet-airbnb-interior-design.html",
    "treehouse": "/blog/treehouse-airbnb-interior-design.html",
    "tiny home": "/blog/tiny-home-airbnb-interior-design.html",
    "cottage rental": "/blog/cottage-airbnb-interior-design.html",
    "tropical villa": "/blog/tropical-villa-airbnb-interior-design.html",
    "historic home": "/blog/historic-home-airbnb-interior-design.html",
    "ranch property": "/blog/ranch-airbnb-interior-design.html",
    "penthouse": "/blog/penthouse-airbnb-interior-design.html",
    "converted barn": "/blog/converted-barn-airbnb-interior-design.html",
    "container home": "/blog/container-home-airbnb-interior-design.html",
    "bedroom design": "/blog/airbnb-bedroom-design-guide.html",
    "primary bedroom": "/blog/airbnb-primary-bedroom-design.html",
    "guest bedroom": "/blog/airbnb-guest-bedroom-design.html",
    "bunk room": "/blog/airbnb-bunk-room-design.html",
    "bathroom design": "/blog/airbnb-bathroom-design-guide.html",
    "kitchen design": "/blog/airbnb-kitchen-design-guide.html",
    "kitchen essentials": "/blog/airbnb-kitchen-essentials-checklist.html",
    "living room design": "/blog/airbnb-living-room-design-guide.html",
    "dining room": "/blog/airbnb-dining-room-design.html",
    "outdoor space": "/blog/airbnb-outdoor-space-design.html",
    "patio and deck": "/blog/airbnb-patio-deck-design.html",
    "game room": "/blog/airbnb-game-room-design.html",
    "home theater": "/blog/airbnb-home-theater-design.html",
    "entryway": "/blog/airbnb-entryway-mudroom-design.html",
    "laundry room": "/blog/airbnb-laundry-room-design.html",
    "home office": "/blog/airbnb-home-office-design.html",
    "pool area": "/blog/airbnb-pool-area-design.html",
    "fire pit": "/blog/airbnb-fire-pit-area-design.html",
    "kids room": "/blog/airbnb-kids-room-design.html",
    "modern style": "/blog/modern-airbnb-interior-design.html",
    "farmhouse style": "/blog/farmhouse-style-airbnb-design.html",
    "coastal style": "/blog/coastal-style-airbnb-design.html",
    "bohemian style": "/blog/bohemian-airbnb-interior-design.html",
    "minimalist design": "/blog/minimalist-airbnb-interior-design.html",
    "mid-century modern": "/blog/mid-century-modern-airbnb-design.html",
    "industrial style": "/blog/industrial-airbnb-interior-design.html",
    "Scandinavian design": "/blog/scandinavian-airbnb-interior-design.html",
    "Art Deco": "/blog/art-deco-airbnb-interior-design.html",
    "Japandi": "/blog/japandi-airbnb-interior-design.html",
    "Mediterranean style": "/blog/mediterranean-airbnb-interior-design.html",
    "eclectic style": "/blog/eclectic-airbnb-interior-design.html",
    "luxury design": "/blog/luxury-airbnb-interior-design.html",
    "wabi-sabi": "/blog/wabi-sabi-airbnb-interior-design.html",
    "average daily rate": "/blog/how-interior-design-affects-airbnb-adr.html",
    "design ROI": "/blog/airbnb-design-roi-analysis.html",
    "five-star reviews": "/blog/airbnb-reviews-design-connection.html",
    "increase bookings": "/blog/design-elements-that-increase-bookings.html",
    "first impression": "/blog/airbnb-first-impression-design.html",
    "seasonal updates": "/blog/seasonal-design-updates-airbnb.html",
    "design mistakes": "/blog/airbnb-design-mistakes-costing-revenue.html",
    "color psychology": "/blog/color-psychology-airbnb-design.html",
    "Superhost status": "/blog/airbnb-design-for-superhost-status.html",
    "design trends": "/blog/airbnb-design-trends-2026.html",
    "repeat guests": "/blog/airbnb-design-for-repeat-guests.html",
    "listing photography": "/blog/airbnb-photography-guide.html",
    "photo staging": "/blog/airbnb-photo-staging-tips.html",
    "listing photo order": "/blog/airbnb-listing-photo-order.html",
    "hero shot": "/blog/airbnb-hero-shot-guide.html",
    "listing title": "/blog/airbnb-listing-title-optimization.html",
    "listing description": "/blog/airbnb-listing-description-design.html",
    "before and after": "/blog/airbnb-before-after-design.html",
    "video tours": "/blog/airbnb-video-tours-design.html",
    "virtual staging": "/blog/airbnb-virtual-staging.html",
    "furniture budget": "/blog/airbnb-furniture-budget-10k.html",
    "furniture sources": "/blog/best-airbnb-furniture-sources.html",
    "furniture durability": "/blog/airbnb-furniture-durability-guide.html",
    "bedding guide": "/blog/airbnb-bedding-guide.html",
    "art and decor": "/blog/airbnb-art-decor-sourcing.html",
    "lighting guide": "/blog/airbnb-lighting-guide.html",
    "rug selection": "/blog/airbnb-rug-guide.html",
    "outdoor furniture": "/blog/airbnb-outdoor-furniture-guide.html",
    "wholesale furniture": "/blog/wholesale-furniture-for-airbnb.html",
    "our services": "/services.html",
    "full-service design": "/services.html",
    "turnkey packages": "/services.html",
    "our portfolio": "/portfolio.html",
    "case studies": "/case-studies/index.html",
    "client reviews": "/reviews/index.html",
    "frequently asked questions": "/faq/index.html",
    "glossary of terms": "/glossary/index.html",
    "free consultation": "/contact.html",
    "best design companies": "/best-airbnb-design-companies/index.html",
    "top STR design services": "/top-str-design-services/index.html",
    "Scottsdale": "/markets/scottsdale-az.html",
    "Nashville": "/markets/nashville-tn.html",
    "Charleston": "/markets/charleston-sc.html",
    "Sedona": "/markets/sedona-az.html",
    "Park City": "/markets/park-city-ut.html",
    "Savannah": "/markets/savannah-ga.html",
    "Lake Tahoe": "/markets/lake-tahoe-ca.html",
    "Gatlinburg": "/markets/gatlinburg-tn.html",
    "Destin": "/markets/destin-fl.html",
    "Joshua Tree": "/markets/joshua-tree-ca.html",
    "Big Bear": "/markets/big-bear-ca.html",
    "Outer Banks": "/markets/outer-banks-nc.html",
    "Austin": "/markets/austin-tx.html",
    "Miami": "/markets/miami-fl.html",
    "Denver": "/markets/denver-co.html",
    "San Diego": "/markets/san-diego-ca.html",
    "New Orleans": "/markets/new-orleans-la.html",
    "Asheville": "/markets/asheville-nc.html",
    "Myrtle Beach": "/markets/myrtle-beach-sc.html",
    "Gulf Shores": "/markets/gulf-shores-al.html",
    "Pigeon Forge": "/markets/pigeon-forge-tn.html",
    "Orlando": "/markets/orlando-fl.html",
    "Phoenix": "/markets/phoenix-az.html",
    "Kissimmee": "/markets/kissimmee-fl.html",
    "Branson": "/markets/branson-mo.html",
    "Panama City Beach": "/markets/panama-city-beach-fl.html",
    "Hilton Head": "/markets/hilton-head-sc.html",
    "Breckenridge": "/markets/breckenridge-co.html",
    "Maui": "/markets/maui-hi.html",
    "Key West": "/markets/key-west-fl.html",
    "San Antonio": "/markets/san-antonio-tx.html",
    "Smoky Mountains": "/markets/smoky-mountains-tn.html",
}


def get_relative_path(file_path, repo_root):
    return "/" + os.path.relpath(file_path, repo_root)


def add_crosslinks(html, self_path, max_links=5):
    links_added = 0
    used_targets = set()
    sorted_keywords = sorted(LINK_MAP.keys(), key=len, reverse=True)
    
    for keyword in sorted_keywords:
        if links_added >= max_links:
            break
        target = LINK_MAP[keyword]
        if target in self_path or self_path.endswith(target):
            continue
        if used_targets.has(target) if hasattr(used_targets, 'has') else target in used_targets:
            continue
        
        escaped = re.escape(keyword)
        # Only match in text between > and <, not inside existing links
        pattern = r'(>[^<]*?)(\b' + escaped + r'\b)([^<]*?<)'
        match = re.search(pattern, html, re.IGNORECASE)
        if match:
            # Check we're not inside an <a> tag
            before = html[:match.start()]
            last_a_open = before.rfind('<a ')
            last_a_close = before.rfind('</a>')
            if last_a_open > last_a_close:
                continue  # Inside an <a> tag
            
            actual_text = match.group(2)
            full_url = DOMAIN + target
            replacement = match.group(1) + f'<a href="{full_url}">{actual_text}</a>' + match.group(3)
            html = html[:match.start()] + replacement + html[match.end():]
            links_added += 1
            used_targets.add(target)
    
    return html, links_added


def main():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # Find all HTML files
    patterns = [
        os.path.join(repo_root, "blog", "*.html"),
        os.path.join(repo_root, "markets", "*.html"),
        os.path.join(repo_root, "case-studies", "*.html"),
        os.path.join(repo_root, "faq", "**", "*.html"),
        os.path.join(repo_root, "glossary", "**", "*.html"),
        os.path.join(repo_root, "reviews", "**", "*.html"),
        os.path.join(repo_root, "alternatives", "**", "*.html"),
        os.path.join(repo_root, "best-airbnb-design-companies", "*.html"),
        os.path.join(repo_root, "top-str-design-services", "*.html"),
        os.path.join(repo_root, "best-vacation-rental-furnishing", "*.html"),
        os.path.join(repo_root, "*.html"),
    ]
    
    total_files = 0
    total_links = 0
    
    for pattern in patterns:
        for filepath in glob.glob(pattern, recursive=True):
            self_path = get_relative_path(filepath, repo_root)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                html = f.read()
            
            # Skip if file already has cross-links from a previous run
            # (check for our specific link pattern)
            existing_crosslinks = html.count(f'href="{DOMAIN}/')
            if existing_crosslinks >= 3:
                continue
            
            modified, count = add_crosslinks(html, self_path)
            
            if count > 0:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(modified)
                total_files += 1
                total_links += count
                print(f"  {count} links: {self_path}")
    
    print(f"\nTotal: {total_files} files modified, {total_links} links added")


if __name__ == "__main__":
    main()
