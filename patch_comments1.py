import re

DASH = '\u2014'
ELL  = '\u2026'

p = '/home/user/portfolio/index.html'
s = open(p, encoding='utf-8').read()

def rep(old, new, expect=1, label=''):
    """Plain (literal) replacement, with a count guard."""
    global s
    c = s.count(old)
    assert c == expect, f'{label}: found {c}, expected {expect}'
    s = s.replace(old, new)
    print(f'{c}x  {label} (literal)')

def rex(pattern, new, expect=1, label=''):
    """Regex replacement, tolerant of indentation and line breaks."""
    global s
    s, c = re.subn(pattern, new, s, flags=re.S)
    assert c == expect, f'{label}: found {c}, expected {expect}'
    print(f'{c}x  {label} (regex)')

# ---------- 1. Hero dashboard panel ----------
rex(r'<!-- DASHBOARD PANEL.*?-->',
f'''<!-- DASHBOARD PANEL {DASH} DEMO DATA
               Every figure in this panel is demo data (sample values chosen to shape the
               layout), not a real measurement: data-count="1284", "92", "47".
               ADD YOUR NUMBERS: rename the labels ("Metric A" {ELL}) and change those data-count
               values to your own {DASH} or delete the whole panel for a simpler hero. -->''',
1, 'hero: panel comment')

# ---------- 2. Hero bar chart + sparkline ----------
rep('<!-- Animated bar chart (pure CSS + a tiny JS reveal trigger) -->',
f'''<!-- SAMPLE VISUALIZATION {DASH} animated bar chart
                 Demo data: the bar heights (--h: 46%, 68%, 32% {ELL}) are sample values.
                 Animated with CSS plus a small JS reveal trigger. -->''',
1, 'hero: bar chart comment')

rep('<!-- Sparkline drawn in SVG with a draw-on animation -->',
f'''<!-- SAMPLE VISUALIZATION {DASH} sparkline drawn in SVG
                 Demo data: the path coordinates below are sample values. -->''',
1, 'hero: sparkline comment')

# ---------- 3. Analytics section header ----------
rex(r'<!--\s*=+\s*\n\s*6\. DATA ANALYTICS SECTION.*?=+ -->',
f'''<!-- =====================================================
             6. DATA ANALYTICS SECTION
             Dashboard-style UI.
             DEMO DATA: every figure in this section is demo data, and each
             chart is a SAMPLE VISUALIZATION built with HTML, CSS, SVG and
             JavaScript only {DASH} no charting library. Nothing here is a real
             measurement until you replace it with your own numbers.
             ===================================================== -->''',
1, 'analytics: section comment')

# ---------- 4. KPI row ----------
rex(r'<!-- KPI ROW.*?-->',
f'''<!-- KPI ROW {DASH} DEMO DATA
             These four counters (1280, 94, 36, 12) are demo values, not real metrics.
             The counters animate when scrolled into view.
             ADD YOUR NUMBERS: change data-count="1280" to your own value and rename the label
             so each card describes a metric you actually track.
             To show a "Demo Data" badge again, uncomment the .badge--demo rule in style.css
             and add this inside any card:
             <span class="badge badge--demo">Demo Data</span> -->''',
1, 'analytics: KPI row comment')

# ---------- 5. One comment per chart card ----------
rep('<!-- Bar chart -->',
f'''<!-- Bar chart {DASH} SAMPLE VISUALIZATION (DEMO DATA)
               The bar heights (--h values below) are sample numbers. -->''',
1, 'analytics: bar card comment')

rep('<!-- Line chart -->',
f'''<!-- Line chart {DASH} SAMPLE VISUALIZATION (DEMO DATA)
               The SVG path points and the four marker circles are sample numbers. -->''',
1, 'analytics: line card comment')

rep('<!-- Donut chart -->',
f'''<!-- Donut chart {DASH} SAMPLE VISUALIZATION (DEMO DATA)
               The data-share values 45 / 30 / 25 are sample percentages. -->''',
1, 'analytics: donut card comment')

rep('<!-- Data grid of placeholder rows -->',
f'''<!-- Data grid {DASH} DEMO DATA
               The four rows below are empty placeholder records (Item 01-04, values "{DASH} {DASH}"). -->''',
1, 'analytics: data grid comment')

# ---------- 6. Legends + ticker + bottom note ----------
rep('''            <ul class="legend" role="list">''',
f'''            <!-- Legend for the line chart (DEMO DATA {DASH} rename "Series A" to your own series) -->
            <ul class="legend" role="list">''',
1, 'analytics: line legend comment')

rep('''              <ul class="legend legend--stack" role="list">''',
f'''              <!-- Legend for the donut (DEMO DATA: 45% / 30% / 25% are sample shares) -->
              <ul class="legend legend--stack" role="list">''',
1, 'analytics: donut legend comment')

rep('<!-- Scrolling ticker (decorative, duplicated once so the loop is seamless) -->',
f'''<!-- Scrolling ticker {DASH} decorative, and the values inside it are DEMO DATA.
             The track is duplicated once so the loop is seamless. -->''',
1, 'analytics: ticker comment')

rep('''<!-- ADD YOUR NUMBERS: the figures in this section are placeholders. Replace them with
             your own values, or delete the whole dashboard block. -->''',
f'''<!-- ADD YOUR NUMBERS: everything above is DEMO DATA / SAMPLE VISUALIZATION.
             Replace the figures with your own values, or delete the whole dashboard block. -->''',
1, 'analytics: bottom comment')

open(p, 'w', encoding='utf-8').write(s)
print('\nindex.html updated')
