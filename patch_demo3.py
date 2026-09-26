DASH = '\u2014'
ELL = '\u2026'

# ---------------- index.html ----------------
p = '/home/user/portfolio/index.html'
s = open(p, encoding='utf-8').read()

def rep(old, new, expect=1, label='', store=None):
    global s
    c = s.count(old)
    assert c == expect, f'{label}: found {c}, expected {expect}'
    s = s.replace(old, new)
    print(f'{c}x  {label}')

rep(f'''         Left: text and calls to action. Right: a live-looking
         analytics panel labelled as a sample visualization.''',
f'''         Left: text and calls to action. Right: an analytics
         panel that demonstrates the dashboard aesthetic.''',
1, 'html: hero section comment')

rep('        <!-- ---------- Hero visual: sample analytics panel ---------- -->',
    '        <!-- ---------- Hero visual: hero analytics panel ---------- -->',
1, 'html: hero visual comment')

rep(f'''         Dashboard-style UI. EVERY number in this section is
         explicitly labelled "Demo Data" / "Sample Visualization".
         Replace them inside the HTML once you have real figures.''',
f'''         Dashboard-style UI.
         The figures in this section are placeholders {DASH} replace them
         with your own numbers inside this section.''',
1, 'html: analytics section comment')

open(p, 'w', encoding='utf-8').write(s)

# ---------------- style.css ----------------
p = '/home/user/portfolio/style.css'
s = open(p, encoding='utf-8').read()
rep('/* ---- Hero visual: sample analytics panel ---- */',
    '/* ---- Hero visual: hero analytics panel ---- */',
1, 'css: hero visual comment')
open(p, 'w', encoding='utf-8').write(s)

# ---------------- README.md ----------------
p = '/home/user/portfolio/README.md'
s = open(p, encoding='utf-8').read()

rep('''> **No author notes are visible on the page.** Earlier drafts showed instructions such as
> `[Add a sentence about…]` or "Replace the demo figures…" to visitors. All of that guidance now
> lives inside `index.html` **HTML comments**, so the public page stays clean and professional.''',
'''> **No author notes are visible on the page.** Earlier drafts showed instructions such as
> `[Add a sentence about…]` or "Replace these figures…" to visitors. All of that guidance now
> lives inside `index.html` **HTML comments**, so the public page stays clean and professional.''',
1, 'readme: author-notes paragraph')

rep('| Hero | Name, the three roles (with a typewriter effect), two CTAs and a sample analytics panel clearly labelled as demo data. |',
    '| Hero | Name, the three roles (with a typewriter effect), two CTAs and an analytics panel that shows off the dashboard aesthetic. |',
1, 'readme: hero row')

rep('plus a responsive-layout demo. |', 'plus a responsive-layout demonstration. |', 1, 'readme: dev row')

rep('''> **About the sample figures:** the phrases "Demo Data" and "Sample Visualization" have been
> removed from the page entirely — including the KPI captions, the chart badges, the chart
> titles, the legends, the ticker and the `aria-label`s. The dashboard now reads as a clean
> interface, and the note that these figures are placeholders lives in `index.html` comments
> (search `ADD YOUR NUMBERS`).''',
'''> **About the figures in the dashboard:** every "demo/sample" label has been removed from the
> page — the KPI captions, the chart badges, the chart titles, the legends, the ticker and the
> `aria-label`s. The dashboard now reads as a clean interface, and the note that these figures
> are placeholders lives in `index.html` comments (search `ADD YOUR NUMBERS`).''',
1, 'readme: figures note')

rep('href="https://your-live-demo-url"', 'href="https://your-project-url"', 1, 'readme: example URL')

rep('| Number counters | `.counter[data-count]` + `initCounters()` (demo numbers only) |',
    '| Number counters | `.counter[data-count]` + `initCounters()` (placeholder numbers only) |',
1, 'readme: counters row')

open(p, 'w', encoding='utf-8').write(s)
print('\ndone')
