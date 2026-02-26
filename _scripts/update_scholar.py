#!/usr/bin/env python3
"""
Google Scholar Auto-Update Script
Fetches publication data from Google Scholar and updates the website.

Usage:
    python update_scholar.py --author_id YOUR_SCHOLAR_ID

Requirements:
    pip install scholarly pyyaml
"""

import argparse
import json
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

try:
    from scholarly import scholarly
except ImportError:
    print("Please install scholarly: pip install scholarly")
    exit(1)


def fetch_scholar_data(author_id: str) -> Dict[str, Any]:
    """Fetch author data from Google Scholar."""
    print(f"Fetching data for author ID: {author_id}")

    try:
        author = scholarly.search_author_id(author_id)
        author = scholarly.fill(author, sections=['basics', 'indices', 'publications'])

        return {
            'name': author.get('name', ''),
            'affiliation': author.get('affiliation', ''),
            'interests': author.get('interests', []),
            'citedby': author.get('citedby', 0),
            'hindex': author.get('hindex', 0),
            'i10index': author.get('i10index', 0),
            'publications': author.get('publications', [])
        }
    except Exception as e:
        print(f"Error fetching scholar data: {e}")
        return None


def process_publications(publications: List[Dict]) -> List[Dict[str, Any]]:
    """Process and sort publications by year."""
    processed = []

    for pub in publications:
        try:
            # Fill publication details
            pub_filled = scholarly.fill(pub)

            bib = pub_filled.get('bib', {})
            processed.append({
                'title': bib.get('title', 'Unknown Title'),
                'authors': bib.get('author', ''),
                'year': int(bib.get('pub_year', 0)) if bib.get('pub_year') else 0,
                'venue': bib.get('venue', bib.get('journal', bib.get('conference', ''))),
                'citations': pub_filled.get('num_citations', 0),
                'url': pub_filled.get('pub_url', ''),
                'abstract': bib.get('abstract', '')
            })
        except Exception as e:
            print(f"Error processing publication: {e}")
            continue

    # Sort by year (descending) then by citations (descending)
    processed.sort(key=lambda x: (-x['year'], -x['citations']))
    return processed


def save_scholar_data(data: Dict[str, Any], output_dir: Path):
    """Save scholar data to YAML files for Jekyll."""

    # Save stats
    stats = {
        'citations': data['citedby'],
        'hindex': data['hindex'],
        'i10index': data['i10index'],
        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    stats_file = output_dir / '_data' / 'scholar_stats.yml'
    stats_file.parent.mkdir(parents=True, exist_ok=True)

    with open(stats_file, 'w') as f:
        yaml.dump(stats, f, default_flow_style=False)
    print(f"Saved stats to {stats_file}")

    # Save publications
    publications = process_publications(data['publications'])

    pubs_file = output_dir / '_data' / 'publications.yml'
    with open(pubs_file, 'w') as f:
        yaml.dump(publications, f, default_flow_style=False, allow_unicode=True)
    print(f"Saved {len(publications)} publications to {pubs_file}")

    # Also save as JSON for potential JavaScript use
    json_file = output_dir / 'assets' / 'data' / 'publications.json'
    json_file.parent.mkdir(parents=True, exist_ok=True)

    with open(json_file, 'w') as f:
        json.dump({
            'stats': stats,
            'publications': publications
        }, f, indent=2, ensure_ascii=False)
    print(f"Saved JSON to {json_file}")


def main():
    parser = argparse.ArgumentParser(description='Update Google Scholar data')
    parser.add_argument('--author_id', required=True, help='Google Scholar author ID')
    parser.add_argument('--output_dir', default='.', help='Output directory for data files')
    args = parser.parse_args()

    output_dir = Path(args.output_dir)

    # Fetch data
    data = fetch_scholar_data(args.author_id)

    if data:
        print(f"\nAuthor: {data['name']}")
        print(f"Affiliation: {data['affiliation']}")
        print(f"Citations: {data['citedby']}")
        print(f"h-index: {data['hindex']}")
        print(f"i10-index: {data['i10index']}")
        print(f"Publications: {len(data['publications'])}")

        # Save data
        save_scholar_data(data, output_dir)
        print("\nUpdate complete!")
    else:
        print("Failed to fetch scholar data")
        exit(1)


if __name__ == '__main__':
    main()
