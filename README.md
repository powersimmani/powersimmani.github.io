# Ho-min Park - Personal Academic Website

Personal academic website built with Jekyll and hosted on GitHub Pages.

## Features

- Responsive academic portfolio
- Automatic Google Scholar integration
- Publications list with citation counts
- CV page with downloadable PDF

## Setup

### Local Development

1. Install Ruby and Bundler
2. Clone this repository
3. Run:
   ```bash
   bundle install
   bundle exec jekyll serve
   ```
4. Visit `http://localhost:4000`

### Google Scholar Integration

1. Find your Google Scholar author ID from your profile URL
2. Add it as a GitHub secret: `GOOGLE_SCHOLAR_ID`
3. The GitHub Action will automatically update publication data weekly

### Manual Scholar Update

```bash
pip install scholarly pyyaml
python _scripts/update_scholar.py --author_id YOUR_SCHOLAR_ID
```

## Deployment

Push to the `main` branch. GitHub Actions will automatically build and deploy to GitHub Pages.

## Structure

```
.
├── _config.yml          # Jekyll configuration
├── _data/               # Data files (publications, navigation)
├── _includes/           # Reusable HTML components
├── _pages/              # Site pages (about, publications, cv)
├── _scripts/            # Python scripts for automation
├── assets/              # CSS, JS, images, files
└── .github/workflows/   # GitHub Actions
```

## Customization

- Edit `_config.yml` for site settings
- Update `_data/publications.yml` for manual publication updates
- Modify `_pages/*.md` for page content
- Add profile image to `assets/images/profile.jpg`

## License

MIT License
