# Raghav Mehra — Portfolio Website

A personal portfolio for **Raghav Mehra — Data Analyst · Full Stack Web Developer · AI Automation**.

Built with **HTML5, CSS3 and vanilla JavaScript only**. No frameworks, no build step, no npm
install, no external images or fonts. It also includes an optional **Gemini AI chatbox**.

> **Content rule followed throughout this project:** the only information added about you is
> your **name** and your **three professional roles**. Every other detail (bio, projects,
> experience, contact details, statistics) is a clearly marked placeholder such as
> `[Add your email]`. Nothing has been invented for you.
>
> **No author notes are visible on the page.** Earlier drafts showed instructions such as
> `[Add a sentence about…]` or "Replace these figures…" to visitors. All of that guidance now
> lives inside `index.html` **HTML comments**, so the public page stays clean and professional.
>
> **One exception, added on request:** the Skills section and the AI Automation "Tools &
> platforms" card are pre-filled with a common **starter stack** (Python, SQL, Power BI… /
> HTML5, React, Node.js… / OpenAI API, n8n…). Treat those chips as a starting point — rename or
> delete anything you do not actually use. No skill levels or percentages are shown, because
> those are personal measurements that nobody else can guess.

---

## 1. Project overview

| Feature | What it does |
| --- | --- |
| Preloader | Animated "system boot" screen with the RM monogram, barcode-style bars, live percentage and status words. Fades out when the page has loaded. |
| Navigation | Sticky header, smooth scrolling, active-section indicator, animated underlines, hamburger menu on tablet/mobile. |
| Hero | Name, the three roles (with a typewriter effect), two CTAs and an analytics panel that shows off the dashboard aesthetic. |
| About | Your three disciplines as cards, a photo placeholder and an editable "at a glance" list. |
| Skills | Three category cards (Data Analytics, Full Stack Development, AI Automation) pre-filled with a common starter stack of technologies. Edit any chip; no skill percentages are shown. |
| Data Analytics | A dashboard-style section (KPI cards, bar chart, line chart, donut chart, data grid, ticker). The figures are placeholders — see `ADD YOUR NUMBERS` comments in `index.html`. |
| Full Stack Development | Animated browser mockup, code window, Frontend → API → Backend → Database flow with travelling data packets, plus a responsive-layout demonstration. |
| AI Automation | Animated User → AI → Automation → Process → Result workflow that lights up step by step. |
| Projects | Three empty, easy-to-replace project cards with example preview graphics and placeholder buttons. |
| Contact | Placeholder channels (email, LinkedIn, GitHub, location) and a **frontend-only** contact form. |
| Footer | Copyright line with the current year and a back-to-top button. |
| Gemini AI chatbox | Floating button (bottom-right) that opens a chat panel wired to the Gemini API, with offline fallback. |

All animations are CSS/JS driven: scroll reveal via `IntersectionObserver`, CSS transforms,
a decorative particle canvas, a custom cursor and magnetic buttons.

---

## 2. File structure

```text
portfolio/
│
├── index.html     ← all page content and structure (with comments explaining each section)
├── style.css      ← all styling, organised in 20 numbered sections
├── script.js      ← all behaviour, organised in 16 numbered sections
└── README.md      ← this file
```

That is the whole project — four files, no dependencies, no build tools.

---

## 3. How to run the portfolio

**Option A — double click (simplest)**

1. Open the `portfolio` folder.
2. Double-click `index.html`. It opens in your browser and everything works.

**Option B — small local server (recommended if you add the Gemini API key)**

```bash
# from inside the portfolio folder
python3 -m http.server 8000
# then open http://localhost:8000 in your browser
```

**Option C — VS Code Live Server**

Right-click `index.html` → *Open with Live Server*.

> The only feature that needs anything extra is the Gemini chat, which requires an API key
> (section 7). Everything else works by simply opening the file.

---

## 4. How to customise content

Open `index.html` in any text editor and search for the word **ADD** — every piece of guidance
sits in an HTML comment right where the content belongs, for example:

```html
<!-- ADD YOUR BIO HERE (2–3 sentences about you, your focus, how you work):
     <p class="about__bio">Your text goes here.</p> -->
```

Useful search terms (they are all comments, so nothing shows on the page):

| Search for | What it belongs to |
| --- | --- |
| `ADD YOUR BIO HERE` | About section biography |
| `ADD YOUR PHOTO` | About section photo (swap the SVG for an `<img>`) |
| `ADD MORE ROWS AS NEEDED` | The "at a glance" facts list (experience, location, availability) |
| `EDIT THE CHIPS` | Skills section technology chips |
| `DEMO DATA` | Every place that marks sample figures (used only in comments) |
| `ADD YOUR NUMBERS` / `ADD YOUR DATA` | Analytics dashboard figures and table rows |
| `ADD A DESCRIPTION OF THE AUTOMATIONS` | AI Automation card text |
| `ADD PROJECT DETAILS HERE` | Each project card (title, description, tags) |
| `LINK YOUR PROJECTS` | Live Demo / GitHub button URLs |
| `ADD YOUR EMAIL` / `ADD YOUR LINKEDIN` / `ADD YOUR GITHUB` | Contact channels |
| `ADD YOUR STACK` (arch diagram) | The Frontend → API → Backend → Database labels |
| `chip--tech` | Every technology chip in the markup |
| `data-count=` | The numbers the animated counters count up to |

> **About the figures in the dashboard:** the "Demo Data" / "Sample Visualization" labels were
> removed from the page itself, but the wording is kept **in the code comments** so you (or any
> developer) can still see exactly which numbers are samples. Search `DEMO DATA` in
> `index.html` (panel, KPI row, each chart card, the legend, the ticker) and in `style.css` /
> `script.js`.
>
> The figures therefore read as real numbers on the page now — replace them before publishing.
>
> The KPI labels are neutral ("Metric A" … "Metric D") and the chart titles are plain
> ("Bar chart", "Trend line", "Category split", "Data grid"). **These numbers are still
> examples, so replace them with real figures before you publish the site** — otherwise a
> visitor has no way to tell them apart from your actual results. The "Example image" badges on
> the project cards are still shown, since those previews are obviously illustrations.

**Replace your photo**

1. Create a folder called `assets` next to `index.html`.
2. Put your image there, e.g. `assets/photo.jpg`.
3. In the About section, replace the `<svg>…</svg>` inside `<figure class="about__photo">`
   with:

```html
<img src="assets/photo.jpg" alt="Raghav Mehra" />
```

**Change the colours**

All colours, radii and animation timings live in the `:root` block at the very top of
`style.css`. Changing `--cyan`, `--violet` and `--blue` re-themes the whole site.

**Edit the technology chips**

Each chip is one list item in the Skills section:

```html
<li class="chip chip--tech">Python</li>
```

* Rename the text to your own technology.
* Delete a `<li>` to remove it, or copy one to add more — the chips wrap automatically.
* The three card variants (`.skill-card--data`, `.skill-card--web`, `.skill-card--ai`) control
  the hover colour of their chips, so keep the class on the `<article>` if you move things around.
* Skill level bars are intentionally absent. If you ever want them, `index.html` contains a
  commented example and `initSkillBars()` in `script.js` animates any `.skill-bar[data-level]`
  element you add.

---

## 5. How to add projects

Find the comment `<!-- ADD YOUR PROJECT HERE -->` in the Projects section of `index.html`.
Copy the whole commented example (also shown below) and paste it as a new `<article>`:

```html
<article class="project-card card card--glass" data-reveal>
  <div class="project-card__preview">
    <img src="assets/project-01.png" alt="Screenshot of Project 01" loading="lazy" />
  </div>
  <div class="project-card__body">
    <p class="project-card__index">Project 04</p>
    <h3 class="project-card__title">Your project name</h3>
    <p class="project-card__text">One or two sentences about the problem and what you built.</p>
    <ul class="tag-list" role="list">
      <li class="tag">Technology</li>
      <li class="tag">Technology</li>
    </ul>
    <div class="project-card__actions">
      <a class="btn btn--small btn--primary" href="https://your-project-url" target="_blank" rel="noopener">Live Demo</a>
      <a class="btn btn--small btn--ghost" href="https://github.com/your-repo" target="_blank" rel="noopener">GitHub</a>
    </div>
  </div>
</article>
```

Notes:

* The `data-reveal-delay="100"` attribute (in ms) staggers the entrance animation — optional.
* Until you replace `href="#"`, the buttons show a small toast instead of navigating, so no
  fake links are ever published.
* The three example preview graphics are inline SVG drawn by the page itself (no copyrighted
  images). Swap them for your own screenshots whenever you like.
* Delete any card you do not need — the grid reflows automatically.

---

## 6. How to add social links

In the Contact section each channel is an `<a class="contact-link" …>` element:

```html
<a class="contact-link card card--glass" href="#" data-placeholder-link>
  <span class="contact-link__body">
    <small class="contact-link__label">LinkedIn</small>
    <span class="contact-link__value">[Add LinkedIn URL]</span>
  </span>
</a>
```

To activate one:

1. Replace `href="#"` with the real URL (`mailto:you@example.com` for email).
2. Remove the `data-placeholder-link` attribute (that attribute is what makes the click show a toast).
3. Replace the bracketed text with what you want visible.
4. For external links add `target="_blank" rel="noopener"`.

The same pattern is used by the footer and by any button you want to point at a real URL.

---

## 7. How to configure the Gemini API

1. Get a free API key from **Google AI Studio** (aistudio.google.com → *Get API key*).
2. Open `script.js` and find this block near the bottom (section 15 — *GEMINI AI CHAT*):

```javascript
/* =====================================================
   STEP 1 — ADD YOUR GEMINI API KEY HERE
   ===================================================== */
const GEMINI_API_KEY = "YOUR_GEMINI_API_KEY";
// Add your Gemini API key here.
// NEVER publish a real API key in a public GitHub repository.
```

3. Paste your key between the quotes and save the file.
4. Reload the page. The chat status text changes from *"Offline mode"* to *"Ready"*.

Choosing the model — just below the key:

```javascript
const GEMINI_MODEL = 'gemini-2.5-flash';
```

Change this string if you want a different (e.g. newer, free-tier friendly) model such as
`gemini-flash-latest`. The request URL is built from this name, so nothing else needs editing.

### What happens without a key

The chat still works, in **offline mode**: it answers from a small built-in knowledge base that
only repeats the confirmed facts (name + three roles) and clearly says that everything else has
not been added yet. It never invents information.

### What the assistant is told

`GEMINI_SYSTEM_INSTRUCTION` (in `script.js`) instructs the model to answer **only** from the
portfolio context, to never invent employers, projects, statistics, certifications or contact
details, and to say "this has not been added to the portfolio yet" instead of guessing.
When you fill in real content, add it to `PORTFOLIO_CONTEXT` so the assistant can talk about it.

### Errors you may see in the chat

| Message | Meaning |
| --- | --- |
| 400 — key or model wrong | Check `GEMINI_API_KEY` / `GEMINI_MODEL`. |
| 401/403 — key refused | Key invalid, API not enabled, or restricted to another website. |
| 404 — model not found | That model is not available to your key; try `gemini-flash-latest`. |
| 429 — rate limit | Free-tier limit reached; wait a moment and retry. |
| Network error | No internet, or you are viewing the page inside a sandboxed preview that blocks external requests. Open `index.html` directly in a browser. |

---

## 8. ⚠️ Gemini API security warning

> **A Gemini API key embedded in client-side JavaScript can be exposed to visitors.**
> Anyone can open your page, view the source or the network tab, and read the key — then use it
> for their own requests against your quota. For a production website, API requests should be
> routed through a secure backend/serverless function where the secret key is stored securely
> and never sent to the browser.

Practical guidance:

* Never commit a real key to a public GitHub repository. Use a separate key for local testing.
* Restrict the key in Google Cloud Console (HTTP referrer restrictions help but are not a full
  fix for client-side code).
* When you are ready for production, replace `requestGeminiReply()` in `script.js` with a
  `fetch()` to **your own** endpoint (for example a Cloud Function, Netlify/Vercel function or
  small Express route) that:
  1. receives the user's message,
  2. calls Gemini with the secret key kept server-side,
  3. returns only the answer text.

  Then delete the key from `script.js` entirely.
* For this HTML/CSS/JS-only version, the key stays a clearly marked placeholder.

---

## 9. How the animations work

Everything is CSS + vanilla JavaScript. The pattern used for almost all of them:

1. An element is marked in the HTML, e.g. `<div class="card" data-reveal>`.
2. `script.js` watches it with an **`IntersectionObserver`**.
3. When it scrolls into view, JavaScript adds a class (`.is-visible`, `.is-drawn`,
   `.is-active`).
4. `style.css` animates the change with a **transition or keyframes**.

Concrete pieces:

| Animation | Where |
| --- | --- |
| Scroll reveal (fade + slide up, staggered) | `.is-visible` + `[data-reveal]` / `[data-reveal-delay]` in `style.css`, `initScrollReveal()` in `script.js` |
| Bar / line / donut charts | `.bar__fill`, `.spark__line`, `.line-chart__line`, `.donut__seg` + `drawChart()` / `initDonutChart()` |
| Architecture packets & node glow | `.arch__packet`, `.arch__node.is-active` + `initArchitectureFlow()` |
| AI workflow steps | `.workflow__step.is-active`, `.workflow__pulse` + `initWorkflowFlow()` |
| Number counters | `.counter[data-count]` + `initCounters()` (placeholder numbers only) |
| Magnetic buttons | `[data-magnetic]` + `initMagneticElements()` (writes `--mx` / `--my`) |
| Custom cursor | `#cursorDot`, `#cursorRing` + `initCustomCursor()` (disabled on touch) |
| Background data network | `#bgCanvas` + `initBackgroundCanvas()` (paused when the tab is hidden) |
| Typing effect in the hero | `#roleTyped` + `initHero()` |

**Reduced motion:** if the visitor's system asks for less motion, the CSS media query
`@media (prefers-reduced-motion: reduce)` removes the animations and shows all content
immediately, and `script.js` checks the same setting before starting the canvas, cursor,
magnetic effects and typewriter.

**Performance:** animations only use `transform` and `opacity`, the canvas particle count scales
with the viewport and pauses when the page is hidden, all scroll handlers are throttled with
`requestAnimationFrame`, and observers unobserve elements after their one-time reveal.

---

## 10. How the preloader works

1. `#preloader` is a fixed overlay rendered immediately from the HTML (so it appears before CSS
   or JS finish loading).
2. `initPreloader()` in `script.js`:
   * blocks page scrolling (`body.is-locked`),
   * eases the percentage towards 92% while the page is still loading
     (the bar/dot animation and the `INITIALIZING → … → READY` status words are CSS + a small timer),
   * sets the target to 100% when the page reports it has loaded,
   * updates the SVG progress ring (`stroke-dashoffset`) and the number on every frame,
   * adds `.is-done` (fade out) and then `.is-hidden` (remove from the layout).
3. Safeguards so it can never trap a visitor:
   * it finishes after a **minimum display time** of 900 ms (no jarring flash),
   * it finishes immediately if the document is already parsed,
   * a **3.5 s safety timer** forces completion if the load event never arrives,
   * with `prefers-reduced-motion` it completes straight away.
4. With JavaScript disabled, the `<noscript>` block in `index.html` hides the preloader and
   shows all content.

To change the look: `.preloader` in the "06. PRELOADER" section of `style.css`.
To change the wording: `PORTFOLIO_CONFIG.preloaderStates` at the top of `script.js`.

---

## Deployment (optional)

Because there is no build step, you can drag the four files onto any static host:

* GitHub Pages — push the folder, then *Settings → Pages → Deploy from branch*.
* Netlify / Vercel / Cloudflare Pages — drag and drop the folder.
* Any web host — upload the files, then open `index.html`.

Remember: if you deployed with a real Gemini key inside `script.js`, move that key to a server
function first (section 8).

---

## Accessibility & browser support notes

* Semantic landmarks (`header`, `nav`, `main`, `section`, `footer`), one `<h1>`, sensible heading order.
* Keyboard accessible menus, chat panel, form and buttons; visible focus rings; `Escape` closes
  the menu and the chat; a "Skip to main content" link.
* The chat uses `role="dialog"`, `aria-expanded` on the toggle and `aria-live` for new messages.
* Decorative SVG/canvas layers are `aria-hidden`.
* Tested structure targets current Chrome, Edge, Firefox and Safari (desktop + mobile).
  `backdrop-filter` degrades gracefully where it is unsupported.
