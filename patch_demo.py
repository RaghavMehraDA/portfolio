import re

p = '/home/user/portfolio/index.html'
s = open(p, encoding='utf-8').read()

def rep(old, new, expect=1, label=''):
    global s
    n = s.count(old)
    assert n == expect, f'{label}: found {n}, expected {expect}'
    s = s.replace(old, new)
    print(f'{n}x  {label}')

DASH = '\u2014'   # —
ELL  = '\u2026'   # …

# ========================= HERO PANEL =========================
rep(f'''          <!-- SAMPLE PANEL: the labels ("Sample metric", "Sample rate" {ELL}) mark every figure
               in this panel as sample data. Give them your own names and values, or delete the
               panel entirely if you prefer a simpler hero. -->''',
f'''          <!-- DASHBOARD PANEL
               The labels and figures here are illustrative placeholders.
               ADD YOUR NUMBERS: rename the labels ("Metric A" {ELL}) and change data-count="1284"
               to values of your own {DASH} or delete the whole panel for a simpler hero. -->''',
1, 'hero: panel comment')

rep('<div class="panel glass hero-dash" aria-label="Sample analytics interface (sample data)">',
    '<div class="panel glass hero-dash" aria-label="Analytics panel">',
1, 'hero: panel aria-label')

rep('''              <span class="panel__title">data-console</span>
              <span class="badge badge--demo">Demo Data</span>''',
    '              <span class="panel__title">data-console</span>',
1, 'hero: removed header badge')

rep('<p class="kpi__label">Sample metric</p>', '<p class="kpi__label">Metric A</p>', 1, 'hero: label 1')
rep('<p class="kpi__label">Sample rate</p>',   '<p class="kpi__label">Metric B</p>', 1, 'hero: label 2')
rep('<p class="kpi__label">Sample queue</p>',  '<p class="kpi__label">Metric C</p>', 1, 'hero: label 3')

rep('\n                <span class="chart__tag">sample visualization</span>', '', 1, 'hero: removed bar tag')
rep('\n                <span class="chart__tag">demo</span>', '', 1, 'hero: removed spark tag')
rep('aria-label="Sample bar chart with demo values"',  'aria-label="Bar chart"',  1, 'hero: bar aria-label')
rep('aria-label="Sample trend line with demo values"', 'aria-label="Trend line"', 1, 'hero: spark aria-label')
rep('<!-- Rotating terminal-ish status line (contents generated in script.js, all labels are demo) -->',
    '<!-- Rotating status line (text comes from PORTFOLIO_CONFIG.heroConsoleLines in script.js) -->',
1, 'hero: console comment')

# ========================= ANALYTICS =========================
rep(f'''            Work in this area usually means collecting data, cleaning and modelling it, then
            presenting it as dashboards and reports. The interface below is a layout sample {DASH}
            <strong>every figure is demo data</strong>.''',
f'''            Work in this area usually means collecting data, cleaning and modelling it, then
            presenting it as dashboards and reports. The interface below is built entirely with
            HTML, CSS, SVG and JavaScript {DASH} no charting library.''',
1, 'analytics: lead sentence')

rep(f'''        <!-- KPI ROW
             The counters animate when scrolled into view. The labels ("Demo metric A" {ELL})
             mark these as sample figures {DASH} they are NOT real measurements.
             ADD YOUR NUMBERS: change data-count="1280" to your own value and rename the label. -->''',
f'''        <!-- KPI ROW
             The counters animate when scrolled into view.
             ADD YOUR NUMBERS: change data-count="1280" to your own value and rename the label
             so each card describes a metric you actually track. -->''',
1, 'analytics: KPI comment')

for letter in 'ABCD':
    rep(f'<p class="kpi__label">Demo metric {letter}</p>',
        f'<p class="kpi__label">Metric {letter}</p>', 1, f'analytics: KPI label {letter}')

rep('<h3 class="chart-card__title">Sample bar chart</h3>',      '<h3 class="chart-card__title">Bar chart</h3>',      1, 'analytics: bar title')
rep('<h3 class="chart-card__title">Sample trend line</h3>',     '<h3 class="chart-card__title">Trend line</h3>',     1, 'analytics: line title')
rep('<h3 class="chart-card__title">Sample category split</h3>', '<h3 class="chart-card__title">Category split</h3>', 1, 'analytics: donut title')
rep('<h3 class="chart-card__title">Sample data grid</h3>',      '<h3 class="chart-card__title">Data grid</h3>',      1, 'analytics: grid title')

rep('\n              <span class="badge badge--demo">Sample Visualization</span>', '', 3, 'analytics: removed 3 chart badges')
rep('''              <span class="badge badge--demo">Demo Data</span>
            </header>
            <div class="data-table"''',
    '''            </header>
            <div class="data-table"''',
1, 'analytics: removed grid badge')

rep(f'aria-label="Sample bar chart {DASH} demo data only"',   'aria-label="Bar chart"',   1, 'analytics: bar aria-label')
rep(f'aria-label="Sample line chart {DASH} demo data only"',  'aria-label="Line chart"',  1, 'analytics: line aria-label')
rep(f'aria-label="Sample donut chart {DASH} demo data only"', 'aria-label="Donut chart"', 1, 'analytics: donut aria-label')
rep(f'aria-label="Sample data grid {DASH} demo data only"',   'aria-label="Data grid"',   1, 'analytics: grid aria-label')

rep('Sample series (demo)', 'Series A', 1, 'analytics: legend label')
rep('<text x="60" y="72" class="donut__center-label">demo</text>',
    '<text x="60" y="72" class="donut__center-label">total</text>', 1, 'analytics: donut centre label')
rep('\n            <p class="chart-card__foot">Percentages are arbitrary sample values.</p>',
    '\n            <!-- ADD YOUR SHARES: the data-share attributes on the circles above set each segment. -->',
1, 'analytics: removed percentages note')

rep('          <!-- Demo data table -->', '          <!-- Data grid of placeholder rows -->', 1, 'analytics: grid comment')

rep(f'<!-- Scrolling demo ticker (decorative {DASH} the values shown are demo data) -->',
    '<!-- Scrolling ticker (decorative, duplicated once so the loop is seamless) -->',
1, 'analytics: ticker comment')
rep('<span><span class="badge badge--demo">Demo Data</span> records: 0000</span>',
    '<span>records: 0000</span>', 2, 'analytics: ticker badge text')
rep('<span>sample row \u00b7 sample row \u00b7 sample row</span>',
    '<span>ingest \u00b7 transform \u00b7 load</span>', 2, 'analytics: ticker row text')

rep('''        <!-- REPLACE DEMO DATA: the figures in this section are samples. Swap them for your
             real numbers, or delete the dashboard and add your own screenshots. -->''',
'''        <!-- ADD YOUR NUMBERS: the figures in this section are placeholders. Replace them with
             your own values, or delete the whole dashboard block. -->''',
1, 'analytics: bottom comment')

# ========================= MISC =========================
rep('href="https://your-live-demo-url"', 'href="https://your-project-url"', 1, 'projects: example URL renamed')

open(p, 'w', encoding='utf-8').write(s)

visible = re.sub(r'<!--.*?-->', '', s, flags=re.S)
hits = re.findall(r'[^<>"]*([Dd]emo|[Ss]ample)[^<>"]*', visible)
print('\nvisible demo/sample text fragments:', hits or 'none')
