#!/usr/bin/env python3
"""
LinkedIn Summary Generator
Generates copy-paste ready text for LinkedIn profile from website data.
Run: python _scripts/generate_linkedin_summary.py
"""

import yaml
from pathlib import Path
from datetime import datetime

def load_yaml(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def generate_linkedin_summary():
    base_path = Path(__file__).parent.parent

    # Load data
    scholar_stats = load_yaml(base_path / '_data/scholar_stats.yml')
    publications = load_yaml(base_path / '_data/publications.yml')
    config = load_yaml(base_path / '_config.yml')

    # Count publications by year
    recent_pubs = [p for p in publications if p.get('year', 0) >= 2023]
    total_pubs = len(publications)

    # Top cited papers
    top_papers = sorted(publications, key=lambda x: x.get('citations', 0), reverse=True)[:3]

    output = []
    output.append("=" * 60)
    output.append("LINKEDIN PROFILE UPDATE - Generated on " + datetime.now().strftime("%Y-%m-%d"))
    output.append("=" * 60)

    # About Section
    output.append("\n" + "─" * 60)
    output.append("📝 ABOUT SECTION (Copy to LinkedIn About)")
    output.append("─" * 60)
    output.append("""
Computer Science PhD with deep expertise in machine learning, spanning from foundational concepts to state-of-the-art architectures including CNNs, Transformers, GANs, and Diffusion models.

🔬 Research Focus:
• Medical Imaging: Interpretable AI for MRI-based diagnosis
• Bioinformatics: CRISPR-Cas systems & protein structure prediction
• Affective Computing: Multimodal stress detection & sentiment analysis
• Environmental Science: Deep learning for microplastics detection

📊 Academic Impact:
• Citations: {citations} | h-index: {hindex} | i10-index: {i10index}
• {total_pubs} peer-reviewed publications
• {recent_pubs} publications since 2023

🎓 Education:
• Ph.D. Computer Science - Ghent University, Belgium (2018-2025)
• M.S. Computer Engineering - Ajou University, South Korea
• B.S. Computer Science - Ajou University, South Korea

🏆 Awards:
• 2nd Place - MuSe-Personalisation Challenge 2023
• 3rd Place - MuSe-Stress Challenge 2022

👨‍🏫 Teaching:
Founder & Lead Instructor of AI Vacation School (AIVS) - 100+ hour ML bootcamp for undergraduates, covering regression to diffusion models.

🔗 Website: {website}
""".format(
        citations=scholar_stats.get('citations', 'N/A'),
        hindex=scholar_stats.get('hindex', 'N/A'),
        i10index=scholar_stats.get('i10index', 'N/A'),
        total_pubs=total_pubs,
        recent_pubs=len(recent_pubs),
        website=config.get('url', 'https://powersimmani.github.io')
    ))

    # Skills Section
    output.append("\n" + "─" * 60)
    output.append("🛠️ SKILLS (Add to LinkedIn Skills)")
    output.append("─" * 60)
    output.append("""
Machine Learning, Deep Learning, PyTorch, Python, Computer Vision,
Natural Language Processing, Transformers, CNNs, GANs, Diffusion Models,
Medical Image Analysis, Bioinformatics, SHAP, Explainable AI (XAI),
Transfer Learning, Feature Engineering, Data Science, Research
""")

    # Featured Publications
    output.append("\n" + "─" * 60)
    output.append("📚 FEATURED PUBLICATIONS (Add to LinkedIn Featured)")
    output.append("─" * 60)
    for i, paper in enumerate(top_papers, 1):
        output.append(f"\n{i}. {paper['title']}")
        output.append(f"   {paper['venue']} ({paper['year']})")
        output.append(f"   Citations: {paper.get('citations', 0)}")
        if paper.get('url'):
            output.append(f"   URL: {paper['url']}")

    # Recent Publications
    output.append("\n" + "─" * 60)
    output.append("📰 RECENT PUBLICATIONS (For LinkedIn Posts)")
    output.append("─" * 60)
    for paper in recent_pubs[:5]:
        output.append(f"\n🎉 New Publication Alert!")
        output.append(f"📄 \"{paper['title']}\"")
        output.append(f"📍 {paper['venue']} ({paper['year']})")
        output.append(f"👥 {paper['authors']}")
        if paper.get('url'):
            output.append(f"🔗 {paper['url']}")
        output.append(f"\n#MachineLearning #Research #PhD #AI #DeepLearning")
        output.append("-" * 40)

    # Headline suggestions
    output.append("\n" + "─" * 60)
    output.append("💡 HEADLINE OPTIONS (Choose one for LinkedIn Headline)")
    output.append("─" * 60)
    output.append("""
Option 1: PhD in Computer Science | Machine Learning Researcher | Medical AI & Bioinformatics

Option 2: ML Researcher @ Ghent University | Deep Learning for Healthcare & Bioinformatics | {citations}+ Citations

Option 3: Computer Science PhD | Transformers, GANs, Diffusion Models | AIVS Founder & ML Educator
""".format(citations=scholar_stats.get('citations', 'N/A')))

    # Get LinkedIn URL from config
    linkedin_url = "https://www.linkedin.com/in/park-ho-min-b46658a6"
    for link in config.get('author', {}).get('links', []):
        if 'linkedin' in link.get('url', '').lower():
            linkedin_url = link['url']
            break

    # Website link reminder
    output.append("\n" + "─" * 60)
    output.append("🔗 IMPORTANT: ADD WEBSITE LINK TO LINKEDIN")
    output.append("─" * 60)
    output.append(f"""
Add your website to LinkedIn:
  • Contact Info > Websites > {config.get('url', 'https://powersimmani.github.io')}
  • Featured Section > Add a link > {config.get('url', 'https://powersimmani.github.io')}

Your LinkedIn profile is linked on your website:
  • {linkedin_url}

This creates a two-way connection between your profiles!
""")

    output.append("\n" + "=" * 60)
    output.append("END OF LINKEDIN UPDATE SUMMARY")
    output.append("=" * 60)

    return "\n".join(output)

if __name__ == "__main__":
    summary = generate_linkedin_summary()
    print(summary)

    # Also save to file
    output_path = Path(__file__).parent.parent / '_scripts/linkedin_summary.txt'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(summary)
    print(f"\n✅ Summary also saved to: {output_path}")
