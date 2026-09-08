# Profile artwork

The profile uses repository-owned SVGs: light/dark desktop and mobile banners, an animated terminal, four project cards, and a public LeapView activity panel. Mobile images are selected below 600px. The terminal honors reduced-motion preferences.

Edit `generate_profile.py` to change copy, colors, or layouts. Then run:

```sh
python3 scripts/generate_profile.py
python3 -m unittest discover -s scripts -p 'test_*.py'
python3 scripts/generate_profile.py --check
```

To fetch the latest public LeapView pull request, authenticate GitHub CLI and run `python3 scripts/generate_profile.py --refresh`. The generator checks that the fixed source repository is public, escapes titles into SVG text, and retains existing assets if fetching fails. It never queries private user events. `data/public-activity.json` is the reproducible source snapshot, including the linked PR URL and update timestamp.

`profile-artwork.yml` refreshes the panel every 12 hours after merge. `snake.yml` updates the orange/gold contribution snake daily. Both commit assets to the branch they run on; scheduled runs use the default branch. They share a concurrency group with the existing README activity updater to serialize writes. Generated assets are committed, so the README has a complete preview before schedules run.
