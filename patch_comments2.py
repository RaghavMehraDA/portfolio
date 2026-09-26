import re

DASH = '\u2014'

# ============================================================
#  style.css
# ============================================================
p = '/home/user/portfolio/style.css'
s = open(p, encoding='utf-8').read()

def rep(old, new, expect=1, label=''):
    global s
    c = s.count(old)
    assert c == expect, f'{label}: found {c}, expected {expect}'
    s = s.replace(old, new)
    print(f'{c}x  {label}')

# ---- bring back the .badge--demo rule, commented out and ready to enable ----
rep('''.badge--placeholder {
  color: var(--violet);
  border-color: rgba(139, 123, 255, 0.35);
  background: rgba(139, 123, 255, 0.1);
}''',
'''.badge--placeholder {
  color: var(--violet);
  border-color: rgba(139, 123, 255, 0.35);
  background: rgba(139, 123, 255, 0.1);
}

/* ---------------------------------------------------------
   DEMO DATA BADGE (optional — currently OFF)
   The "Demo Data" / "Sample Visualization" labels were removed
   from the page on request. To bring them back:
     1. uncomment the rule below,
     2. add this inside any card in index.html:
        <span class="badge badge--demo">Demo Data</span>

.badge--demo {
  color: #ffd27d;
  border-color: rgba(255, 210, 125, 0.35);
  background: rgba(255, 210, 125, 0.1);
}
   --------------------------------------------------------- */''',
1, 'css: .badge--demo restored as a comment')

# ---- chart section header: name the demo data again ----
rep('/* =========================\n   11. DATA ANALYTICS DASHBOARD\n========================= */',
'''/* =========================
   11. DATA ANALYTICS DASHBOARD
   DEMO DATA: the figures rendered by these components are
   demo/sample values taken from the markup (see the DEMO DATA
   comments in index.html). The charts are SAMPLE VISUALIZATIONS
   drawn with CSS + SVG only.
========================= */''',
1, 'css: analytics section header')

# ---- restore the "demo data table" wording on the grid rules ----
rep('/* Data grid */',
    '/* Data grid (renders the DEMO DATA table rows) */',
1, 'css: data grid comment')

open(p, 'w', encoding='utf-8').write(s)

# ============================================================
#  script.js
# ============================================================
p = '/home/user/portfolio/script.js'
s = open(p, encoding='utf-8').read()

rep('''  /* Text the hero console line cycles through (the hero panel is an
     illustrative dashboard, so these are generic system messages). */''',
'''  /* Text the hero console line cycles through. The hero panel is
     labelled DEMO DATA in index.html, so these are sample system
     messages, not real output. */''',
1, 'js: config comment')

rep('''   Numbers only animate for the placeholder figures in the HTML.
   They are examples {DASH} REPLACE THEM with your own values (see the
   ADD YOUR NUMBERS comments in index.html).'''.replace('{DASH}', DASH),
'''   Numbers only animate for the figures in the HTML that are marked
   DEMO DATA there. REPLACE THEM with your own values (see the
   ADD YOUR NUMBERS comments in index.html).''',
1, 'js: counters comment')

rep('''   All values here are placeholder figures. To use your own,
   change the data-count / data-share attributes and the bar
   heights (--h) in index.html.
   Nothing in this section describes real performance or data
   until you put your own numbers in.''',
'''   All values here come from the markup and are DEMO DATA, shown as
   SAMPLE VISUALIZATIONS. To use your own, change the data-count /
   data-share attributes and the bar heights (--h) in index.html.
   Nothing in this section describes real performance or data until
   you put your own numbers in.''',
1, 'js: charts comment')

rep('''  /* ---- Rotating console line inside the hero panel ---- */''',
    '''  /* ---- Rotating console line inside the hero panel (DEMO DATA) ---- */''',
1, 'js: hero console comment')

# ---- The assistant should know the figures are demo data ----
rep('''- Clients, testimonials, real statistics or performance numbers. The Analytics section is an
  illustrative dashboard layout: its figures are placeholders, not measurements. Never quote
  those numbers as results.''',
'''- Clients, testimonials, real statistics or performance numbers. The Analytics section is a
  demo dashboard: every figure on it is DEMO DATA (a sample visualization), not a measurement.
  Never quote those numbers as results.''',
1, 'js: PORTFOLIO_CONTEXT')

rep("""    return 'The Analytics section is a dashboard layout built with plain HTML, CSS, SVG and JavaScript. Its figures are placeholders rather than measurements, so I cannot quote them as results.';""",
"""    return 'The Analytics section is a demo dashboard built with plain HTML, CSS, SVG and JavaScript. Every figure on it is demo data shown as a sample visualization, not a real measurement, so I cannot quote those numbers as results.';""",
1, 'js: offline analytics answer')

open(p, 'w', encoding='utf-8').write(s)

# ============================================================
#  README.md
# ============================================================
p = '/home/user/portfolio/README.md'
s = open(p, encoding='utf-8').read()

rep('''> **About the figures in the dashboard:** every label that flagged them as examples has been
> removed from the
> page {DASH} the KPI captions, the chart badges, the chart titles, the legends, the ticker and the
> `aria-label`s. The dashboard now reads as a clean interface, and the note that these figures
> are placeholders lives in `index.html` comments (search `ADD YOUR NUMBERS`).'''.replace('{DASH}', DASH),
'''> **About the figures in the dashboard:** the "Demo Data" / "Sample Visualization" labels were
> removed from the page itself, but the wording is kept **in the code comments** so you (or any
> developer) can still see exactly which numbers are samples. Search `DEMO DATA` in
> `index.html` (panel, KPI row, each chart card, the legend, the ticker) and in `style.css` /
> `script.js`.''',
1, 'readme: figures note')

rep('''| `ADD YOUR NUMBERS` / `ADD YOUR DATA` | Analytics dashboard figures and table rows |''',
'''| `DEMO DATA` | Every place that marks sample figures (used only in comments) |
| `ADD YOUR NUMBERS` / `ADD YOUR DATA` | Analytics dashboard figures and table rows |''',
1, 'readme: search table')

rep('''> The two small "Demo Data" / "Sample Visualization" badges and the "Example image" badges are
> intentionally kept: they tell visitors that those figures and graphics are samples, so nothing
> reads as a real statistic.''',
'''> **Admin note:** the figures on the dashboard read as real numbers now that the labels are
> gone, so replace them before publishing. The "Example image" badges on the project cards are
> still shown, since those previews are obviously illustrations.''',
1, 'readme: older badge note')

open(p, 'w', encoding='utf-8').write(s)
print('\nstyle.css, script.js and README.md updated')
