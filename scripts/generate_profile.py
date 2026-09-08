#!/usr/bin/env python3
"""Generate GitHub-compatible profile artwork using only Python's standard library."""
import argparse
import json
import subprocess
import textwrap
from html import escape
from pathlib import Path
from urllib.parse import urlencode

ROOT = Path(__file__).resolve().parents[1]
THEMES = {
    'dark': dict(bg='#0d1117', panel='#161b22', line='#30363d', text='#f0f6fc', muted='#a3b1c2'),
    'light': dict(bg='#fffaf5', panel='#ffffff', line='#eaded3', text='#24292f', muted='#596778'),
}
PROJECTS = [
    ('leapview', '01', 'LEAPVIEW', 'Governed analytics. Defined in code.',
     'Semantic models, dashboards, and AI agents.', 'GO / DUCKDB / SQL / TYPESCRIPT', '#00b8d9', 'chart'),
    ('reposage', '02', 'REPOSAGE', 'Your codebase, in conversation.',
     'Local inference. Graph context. Source references.', 'PYTHON / LANGGRAPH / OLLAMA / CHROMADB', '#a78bfa', 'graph'),
    ('honeycloud', '03', 'HONEYCLOUD', 'Turn attack traffic into insight.',
     'Six protocols. Live telemetry. Attacker profiles.', 'RUST / AXUM / POSTGRESQL / DOCKER', '#f59e0b', 'hex'),
    ('plagiarism', '04', 'SEMANTIC PLAGIARISM DETECTOR', 'Find the meaning behind the match.',
     'Multilingual embeddings and paragraph comparisons.', 'PYTHON / SENTENCE TRANSFORMERS / FAISS', '#34d399', 'scan'),
]


def text(x, y, value, size=20, color='currentColor', weight=400, extra=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-weight="{weight}" {extra}>{escape(str(value))}</text>'


def svg(theme, height, title, body, defs=''):
    c = THEMES[theme]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="{height}" viewBox="0 0 960 {height}" role="img" aria-label="{escape(title, quote=True)}">
<title>{escape(title)}</title>
<defs>{defs}</defs>
<rect x="1" y="1" width="958" height="{height-2}" rx="22" fill="{c['bg']}" stroke="{c['line']}"/>
<g font-family="'Segoe UI',Arial,sans-serif" fill="{c['text']}">{body}</g>
</svg>
'''


def banner(theme):
    c = THEMES[theme]
    grid = ''.join(f'<path d="M{x} 16V264" stroke="{c["line"]}" opacity=".3"/>' for x in range(600, 950, 32))
    grid += ''.join(f'<path d="M600 {y}H944" stroke="{c["line"]}" opacity=".3"/>' for y in range(24, 270, 32))
    body = grid + '<path d="M610 230L680 164L733 191L811 87L901 48" fill="none" stroke="url(#warm)" stroke-width="4"/>'
    for x, y in [(610,230),(680,164),(733,191),(811,87),(901,48)]:
        body += f'<circle cx="{x}" cy="{y}" r="7" fill="#ff7a18" stroke="{c["bg"]}" stroke-width="3"/>'
    body += text(40, 48, 'AI ENGINEER / FLID AI', 15, '#f07424', 700, 'letter-spacing="3"')
    body += text(40, 115, 'Ganesh Kambli', 55, c['text'], 750)
    body += text(42, 158, 'Building useful systems for data, code, and AI.', 22, c['muted'])
    body += '<rect x="40" y="192" width="208" height="38" rx="19" fill="url(#warm)"/>'
    body += text(61, 217, 'BUILDING LEAPVIEW', 15, '#18120b', 700)
    body += text(269, 217, 'Go  /  DuckDB  /  Agent systems', 17, c['muted'])
    return svg(theme, 270, 'Ganesh Kambli — AI Engineer at Flid AI, building LeapView', body,
               '<linearGradient id="warm"><stop stop-color="#f74c00"/><stop offset="1" stop-color="#fbbf24"/></linearGradient>')


def terminal(theme):
    c = THEMES[theme]
    body = '<circle cx="29" cy="26" r="5" fill="#ff5f57"/><circle cx="48" cy="26" r="5" fill="#febc2e"/><circle cx="67" cy="26" r="5" fill="#28c840"/>'
    body += text(95, 31, 'ganesh@github  ~  /building', 14, c['muted'])
    body += f'<path d="M1 48H959" stroke="{c["line"]}"/>'
    scenes = [
        ('whoami', 'Ganesh Kambli', 'AI Engineer at Flid AI. Curious about the systems underneath.'),
        ('cat currently-building', 'LeapView / governed analytics as code', 'Go backends. DuckDB execution. Dashboards and AI agents.'),
        ('ls projects/', 'LeapView   RepoSage   HoneyCloud', 'Analytics, local code intelligence, and threat telemetry.'),
    ]
    for i, (cmd, answer, detail) in enumerate(scenes):
        body += f'<g class="scene scene{i}">'
        body += text(30, 78, '$ ' + cmd, 22, '#f07424', 600, 'font-family="monospace"')
        body += text(30, 115, answer, 27, c['text'], 650)
        body += '</g>'
    body += f'<rect class="cursor" x="30" y="128" width="10" height="18" fill="#f07424"/>'
    body += text(52, 210, 'explore the projects below', 15, c['muted'], extra='font-family="monospace"')
    styles = '''<style>
.scene{opacity:0;animation:cycle 15s infinite;animation-timing-function:steps(1,end)}
.scene0{opacity:1;animation-delay:0s}.scene1{animation-delay:5s}.scene2{animation-delay:10s}
@keyframes cycle{0%,32%{opacity:1}33%,100%{opacity:0}}
.cursor{animation:blink 1.2s steps(2,start) infinite}@keyframes blink{to{opacity:0}}
@media(prefers-reduced-motion:reduce){.scene,.cursor{animation:none}.scene0{opacity:1}.scene1,.scene2{opacity:0}}
</style>'''
    return svg(theme, 160, 'Animated terminal: whoami, currently building LeapView, and selected projects', body, styles)


def card(theme, project):
    slug, num, name, headline, detail, stack, accent, icon = project
    c = THEMES[theme]
    body = f'<rect x="1" y="16" width="5" height="88" rx="2" fill="{accent}"/>'
    body += text(24, 29, num + ' / ' + name, 16, accent, 750, 'letter-spacing="1.4"')
    body += text(24, 67, headline, 28, c['text'], 650)
    body += text(24, 98, stack, 14, c['muted'], 650, 'letter-spacing="1"')
    icons = {
        'chart': '<path d="M819 130V103M849 130V81M879 130V56"/><path d="M804 146H900"/>',
        'graph': '<path d="M814 68L881 86L842 137ZM814 68L842 137"/><circle cx="814" cy="68" r="10"/><circle cx="881" cy="86" r="10"/><circle cx="842" cy="137" r="10"/>',
        'hex': '<path d="M848 48L887 71V117L848 140L809 117V71ZM848 72L867 83V105L848 116L829 105V83Z"/>',
        'scan': '<path d="M822 56H801V77M877 56H898V77M801 118V139H822M898 118V139H877M824 83H875M824 99H865M824 115H875"/>',
    }
    body += f'<g transform="translate(300,-2) scale(.65)" stroke="{accent}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" fill="{c["bg"]}">{icons[icon]}</g>'
    return svg(theme, 120, name + ': ' + headline + ' ' + detail, body)


def validate_activity(data):
    if not isinstance(data, dict) or not isinstance(data.get('number'), int) or data['number'] <= 0:
        raise ValueError('Invalid public pull request number')
    if data.get('url') != f'https://github.com/flidai/leapview/pull/{data["number"]}':
        raise ValueError('Unexpected pull request URL')
    if data.get('state') not in ('open', 'closed') or not isinstance(data.get('title'), str):
        raise ValueError('Invalid public pull request data')
    return data


def refresh():
    # Fixed public repository and author; never use authenticated-user private events.
    meta = json.loads(subprocess.check_output(['gh', 'api', 'repos/flidai/leapview'], text=True))
    if meta.get('private') is not False:
        raise ValueError('Activity source must be public')
    query = urlencode({'q': 'repo:flidai/leapview author:Ganesh-403 is:pr', 'sort': 'updated', 'order': 'desc', 'per_page': 1})
    result = json.loads(subprocess.check_output(['gh', 'api', 'search/issues?' + query], text=True))
    if not result.get('items'):
        raise ValueError('No public LeapView pull requests found; retaining existing panel')
    pr = result['items'][0]
    data = validate_activity({'number': pr['number'], 'title': pr['title'], 'url': pr['html_url'],
                             'state': pr['state'], 'updated_at': pr['updated_at']})
    return data


def activity(theme, data):
    c = THEMES[theme]
    body = '<circle cx="36" cy="26" r="5" fill="#34d399"/>'
    body += text(52, 31, 'CURRENTLY BUILDING / LEAPVIEW', 15, '#f07424', 750, 'letter-spacing="2"')
    body += text(30, 64, f'Latest public PR · #{data["number"]} · {data["state"].upper()}', 22, c['text'], 650)
    lines = textwrap.wrap(' '.join(data['title'].split()), width=72, max_lines=2, placeholder='…')
    for i, line in enumerate(lines):
        body += text(30, 96 + i * 26, line, 21, c['text'])
    body += text(30, 153, 'PR updated ' + data['updated_at'][:10] + ' UTC · Refreshed every 12 hours', 15, c['muted'])
    return svg(theme, 174, 'Currently building LeapView. Latest public PR: ' + data['title'], body)


def mobile_art(theme, kind, data=None, project=None):
    c = THEMES[theme]
    height = 250
    if kind == 'banner':
        body = text(24, 38, 'AI ENGINEER / FLID AI', 16, '#f07424', 700)
        body += text(24, 96, 'Ganesh Kambli', 42, c['text'], 750)
        body += text(24, 139, 'Building useful systems', 24, c['muted'])
        body += text(24, 171, 'for data, code, and AI.', 24, c['muted'])
        body += text(24, 220, 'BUILDING LEAPVIEW  ↗', 21, '#f07424', 750)
        title = 'Ganesh Kambli — AI Engineer at Flid AI'
    elif kind == 'terminal':
        # Preserve the same animated scenes, with a compact two-line response.
        height = 164
        source = terminal(theme)
        import re
        style = re.search(r'<style>.*?</style>', source, re.S).group(0)
        body = text(24, 32, 'ganesh@github ~ /building', 16, c['muted'])
        scenes = [('whoami', 'Ganesh Kambli', 'AI Engineer at Flid AI.'),
                  ('cat currently-building', 'LeapView', 'Go. DuckDB. AI agents.'),
                  ('ls projects/', 'RepoSage / HoneyCloud', 'Code intelligence & telemetry.')]
        for i, (cmd, answer, detail) in enumerate(scenes):
            body += f'<g class="scene scene{i}">'
            body += text(24, 75, '$ ' + cmd, 22, '#f07424', 600, 'font-family="monospace"')
            body += text(24, 115, answer, 29, c['text'], 650)
            body += '</g>'
        body += '<rect class="cursor" x="24" y="133" width="11" height="19" fill="#f07424"/>'
        body = style + body
        title = 'Animated terminal — Ganesh, LeapView, RepoSage and HoneyCloud'
    elif kind == 'currently-building':
        height = 194
        body = text(24, 30, 'CURRENTLY BUILDING / LEAPVIEW', 17, '#f07424', 750)
        body += text(24, 65, f'Latest public PR · #{data["number"]} · {data["state"].upper()}', 23, c['text'], 650)
        for i, line in enumerate(textwrap.wrap(' '.join(data['title'].split()), 35, max_lines=2, placeholder='…')):
            body += text(24, 101+i*27, line, 22, c['text'])
        body += text(24, 171, 'PR updated ' + data['updated_at'][:10] + ' UTC', 18, c['muted'])
        title = 'Latest public LeapView PR: ' + data['title']
    else:
        slug, num, name, headline, detail, stack, accent, icon = project
        height = 146
        body = f'<rect x="1" y="14" width="5" height="118" rx="2" fill="{accent}"/>'
        label = name if slug != 'plagiarism' else 'SEMANTIC PLAGIARISM'
        body += text(20, 28, num + ' / ' + label, 18, accent, 750)
        for i, line in enumerate(textwrap.wrap(headline, 29)):
            body += text(20, 63+i*29, line, 27, c['text'], 650)
        short_stack = {'leapview':'GO / DUCKDB / SQL', 'reposage':'PYTHON / LANGGRAPH / OLLAMA',
                       'honeycloud':'RUST / AXUM / POSTGRESQL', 'plagiarism':'PYTHON / TRANSFORMERS / FAISS'}[slug]
        body += text(20, 126, short_stack, 16, c['muted'], 650)
        title = name + ': ' + headline
    result = svg(theme, height, title, body)
    return result.replace('width="960"', 'width="480"').replace(f'viewBox="0 0 960 {height}"', f'viewBox="0 0 480 {height}"').replace('width="958"', 'width="478"')


def outputs(data):
    out = {}
    for theme in THEMES:
        out[f'assets/banner-{theme}.svg'] = banner(theme)
        for kind in ['banner', 'terminal', 'currently-building']:
            out[f'assets/{kind}-{theme}-mobile.svg'] = mobile_art(theme, kind, data=data)
        out[f'assets/terminal-{theme}.svg'] = terminal(theme)
        out[f'assets/currently-building-{theme}.svg'] = activity(theme, data)
        for project in PROJECTS:
            out[f'assets/{project[0]}-{theme}.svg'] = card(theme, project)
            out[f'assets/{project[0]}-{theme}-mobile.svg'] = mobile_art(theme, 'card', project=project)
    out['data/public-activity.json'] = json.dumps(data, indent=2, ensure_ascii=False) + '\n'
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--refresh', action='store_true', help='Fetch latest public LeapView PR before generating')
    group.add_argument('--check', action='store_true', help='Verify committed artwork matches the generator')
    args = parser.parse_args()
    data = refresh() if args.refresh else validate_activity(json.loads((ROOT / 'data/public-activity.json').read_text()))
    for name, content in outputs(data).items():
        path = ROOT / name
        if args.check:
            if not path.exists() or path.read_text() != content:
                raise SystemExit(f'Out of date: {name}')
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
    print('Profile artwork checked.' if args.check else 'Profile artwork generated.')


if __name__ == '__main__':
    main()
