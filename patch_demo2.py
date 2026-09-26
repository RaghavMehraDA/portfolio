import re

DASH = '\u2014'

# ============================================================
#  1. index.html — rename the internal .responsive-demo classes
#     (they contain the word "demo" even though they are not
#      visible text; renaming keeps the source tidy)
# ============================================================
p = '/home/user/portfolio/index.html'
s = open(p, encoding='utf-8').read()
n = s.count('responsive-demo')
assert n == 4, n
s = s.replace('responsive-demo', 'responsive-check')
open(p, 'w', encoding='utf-8').write(s)
print(f'{n}x  html: .responsive-demo -> .responsive-check')

# ============================================================
#  2. style.css
# ============================================================
p = '/home/user/portfolio/style.css'
s = open(p, encoding='utf-8').read()

def rep(old, new, expect=1, label=''):
    global s
    c = s.count(old)
    assert c == expect, f'{label}: found {c}, expected {expect}'
    s = s.replace(old, new)
    print(f'{c}x  {label}')

rep('responsive-demo', 'responsive-check', 4, 'css: class rename')

# The "Demo Data" badge style is no longer used anywhere
rep('''.badge--demo {
  color: #ffd27d;
  border-color: rgba(255, 210, 125, 0.35);
  background: rgba(255, 210, 125, 0.1);
}

''', '', 1, 'css: removed unused .badge--demo rule')

rep('/* Demo data table */', '/* Data grid */', 1, 'css: grid comment')

# Mark the two now-optional helper styles
rep('.chart__tag {', '/* Optional small tag beside a chart title — unused by default. */\n.chart__tag {',
    1, 'css: chart__tag marked optional')
rep('.chart-card__foot {', '/* Optional footnote under a chart card — unused by default. */\n.chart-card__foot {',
    1, 'css: chart-card__foot marked optional')

open(p, 'w', encoding='utf-8').write(s)

# ============================================================
#  3. script.js
# ============================================================
p = '/home/user/portfolio/script.js'
s = open(p, encoding='utf-8').read()

rep('''  /* Text the hero console line cycles through (the panel is
     labelled "Demo Data", so these are sample system messages). */''',
'''  /* Text the hero console line cycles through (the hero panel is an
     illustrative dashboard, so these are generic system messages). */''',
1, 'js: config comment')

rep("'rows.staged = demo_dataset',", "'rows.staged = dataset_ready',", 1, 'js: hero console line')

rep('''   Numbers only animate for the figures in this file, which are
   all explicitly labelled "Demo Data" in the HTML.''',
'''   Numbers only animate for the placeholder figures in the HTML.
   They are examples — REPLACE THEM with your own values (see the
   ADD YOUR NUMBERS comments in index.html).''',
1, 'js: counters comment')

rep('/* ---- Rotating console line inside the sample panel ---- */',
    '/* ---- Rotating console line inside the hero panel ---- */',
1, 'js: hero console comment')

rep('''   All values here are DEMO values that are clearly labelled in
   the markup. Nothing in this section describes Raghav's real
   performance or data.''',
'''   All values here are placeholder figures. To use your own,
   change the data-count / data-share attributes and the bar
   heights (--h) in index.html.
   Nothing in this section describes real performance or data
   until you put your own numbers in.''',
1, 'js: charts comment')

rep('''- Clients, testimonials, real statistics or performance numbers. The Analytics section on the
  website is an illustrative sample dashboard only: its card labels say "Demo metric" and its
  chart titles start with "Sample". Never quote those numbers as real results.''',
'''- Clients, testimonials, real statistics or performance numbers. The Analytics section is an
  illustrative dashboard layout: its figures are placeholders, not measurements. Never quote
  those numbers as results.''',
1, 'js: PORTFOLIO_CONTEXT')

rep("""    return 'The Analytics section is a sample dashboard built with plain HTML, CSS, SVG and JavaScript. Its cards are labelled "Demo metric" and each chart title starts with "Sample", so none of those figures are real measurements.';""",
"""    return 'The Analytics section is a dashboard layout built with plain HTML, CSS, SVG and JavaScript. Its figures are placeholders rather than measurements, so I cannot quote them as results.';""",
1, 'js: offline analytics answer')

open(p, 'w', encoding='utf-8').write(s)

# ============================================================
#  4. README.md
# ============================================================
p = '/home/user/portfolio/README.md'
s = open(p, encoding='utf-8').read()

rep('''> **About the sample figures:** the captions that used to sit under the KPI numbers
> ("Demo Data", "demo value") have been removed on request — the numbers now read cleanly, and
> the wording that marks them as samples lives in `index.html` comments instead. What remains
> visible on purpose: the KPI labels ("Demo metric A" …), the chart titles ("Sample bar chart",
> "Sample trend line", "Sample category split", "Sample data grid"), the small badges in the
> chart headers, and the "Example image" badges on the project cards. Together they keep a
> visitor from mistaking the samples for real results.''',
'''> **About the sample figures:** the phrases "Demo Data" and "Sample Visualization" have been
> removed from the page entirely — including the KPI captions, the chart badges, the chart
> titles, the legends, the ticker and the `aria-label`s. The dashboard now reads as a clean
> interface, and the note that these figures are placeholders lives in `index.html` comments
> (search `ADD YOUR NUMBERS`).
>
> The KPI labels are neutral ("Metric A" … "Metric D") and the chart titles are plain
> ("Bar chart", "Trend line", "Category split", "Data grid"). **These numbers are still
> examples, so replace them with real figures before you publish the site** — otherwise a
> visitor has no way to tell them apart from your actual results. The "Example image" badges on
> the project cards are still shown, since those previews are obviously illustrations.''',
1, 'readme: sample-figures note')

rep('''| `REPLACE DEMO DATA` / `ADD YOUR DATA` | Analytics dashboard figures and table rows |''',
'''| `ADD YOUR NUMBERS` / `ADD YOUR DATA` | Analytics dashboard figures and table rows |''',
1, 'readme: search term table')

rep('''| Data Analytics | A dashboard-style section (KPI cards, bar chart, line chart, donut chart, data grid, ticker). Every number is labelled **Demo Data** / **Sample Visualization**. |''',
'''| Data Analytics | A dashboard-style section (KPI cards, bar chart, line chart, donut chart, data grid, ticker). The figures are placeholders — see `ADD YOUR NUMBERS` comments in `index.html`. |''',
1, 'readme: features table row')

open(p, 'w', encoding='utf-8').write(s)

print('\nall files patched')
