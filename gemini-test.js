const fs = require('fs'), path = require('path');
const { JSDOM, VirtualConsole } = require('jsdom');
const dir = '/home/user/portfolio';

let html = fs.readFileSync(path.join(dir, 'index.html'), 'utf8');
// Inject a fake key so the API code path runs (test only — never a real key)
let js = fs.readFileSync(path.join(dir, 'script.js'), 'utf8')
  .replace('const GEMINI_API_KEY = "YOUR_GEMINI_API_KEY";', 'const GEMINI_API_KEY = "TEST_KEY_1234567890";');

const errors = [];
const vc = new VirtualConsole();
vc.on('jsdomError', e => { if (!/Not implemented|getContext/.test(e.message)) errors.push(e.message); });
vc.on('error', (...a) => errors.push('console.error: ' + a.join(' ')));

let captured = null;      // last request
let nextBehaviour = null; // function returning a Response-like object

function beforeParse(window) {
  window.IntersectionObserver = class { constructor(cb){this.cb=cb;} observe(el){setTimeout(()=>this.cb([{target:el,isIntersecting:false,intersectionRatio:0}],this),0);} unobserve(){} disconnect(){} };
  window.fetch = (url, options) => {
    captured = { url, options };
    return Promise.resolve(nextBehaviour(url, options));
  };
}

const dom = new JSDOM(html, { url: 'file://' + dir + '/index.html', runScripts: 'dangerously', pretendToBeVisual: true, virtualConsole: vc, beforeParse });
const { window } = dom, { document } = window;
const s = document.createElement('script'); s.textContent = js; document.body.appendChild(s);

const results = [];
const t = (n, c, x = '') => results.push(`${c ? 'PASS' : 'FAIL'} — ${n}${c ? '' : ' :: ' + x}`);
const wait = ms => new Promise(r => setTimeout(r, ms));

function ok(body)      { return { ok: true,  status: 200, json: () => Promise.resolve(body) }; }
function httpError(st) { return { ok: false, status: st, json: () => Promise.resolve({ error: { code: st } }) }; }
function geminiText(text) {
  return { candidates: [{ content: { parts: [{ text }], role: 'model' }, finishReason: 'STOP' }] };
}

(async () => {
  await wait(1200);
  const toggle = document.getElementById('chatToggle');
  const input = document.getElementById('chatInput');
  const form = document.getElementById('chatForm');
  const msgs = () => Array.from(document.querySelectorAll('#chatMessages .chat-msg'));

  // ---------- 1. Successful call ----------
  nextBehaviour = () => ok(geminiText('Raghav works as a Data Analyst, Full Stack Web Developer and AI Automation Developer.'));
  toggle.click(); await wait(50);
  t('panel reported API-ready status', /Ready/.test(document.getElementById('chatStatusText').textContent), document.getElementById('chatStatusText').textContent);

  input.value = 'What does Raghav do?';
  form.dispatchEvent(new window.Event('submit', { bubbles: true, cancelable: true }));
  await wait(300);

  t('request went to the Gemini generateContent endpoint',
    captured && captured.url === 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent', captured && captured.url);
  t('method is POST', captured.options.method === 'POST', captured.options.method);
  t('key sent in x-goog-api-key header (not in the URL)',
    captured.options.headers['x-goog-api-key'] === 'TEST_KEY_1234567890' && !captured.url.includes('key='));
  const body = JSON.parse(captured.options.body);
  t('system instruction included', typeof body.system_instruction.parts[0].text === 'string' && body.system_instruction.parts[0].text.length > 100);
  t('system instruction forbids inventing facts', /never invent/i.test(body.system_instruction.parts[0].text));
  t('conversation sent as contents[0]', body.contents[0].role === 'user' && body.contents[0].parts[0].text === 'What does Raghav do?');
  t('free-tier friendly generation config', body.generationConfig.maxOutputTokens === 400 && body.generationConfig.temperature === 0.4);
  t('safety settings present', Array.isArray(body.safetySettings) && body.safetySettings.length === 4);
  t('AI reply rendered in the panel', msgs().some(m => m.classList.contains('chat-msg--ai') && /Raghav works as a Data Analyst/.test(m.textContent)), msgs().length + ' msgs');
  t('typing indicator cleaned up', !document.querySelector('[data-typing="true"]'));
  t('status reset after success', /Ready/.test(document.getElementById('chatStatusText').textContent));

  // ---------- 2. Conversation history is sent on the next turn ----------
  input.value = 'And what about projects?';
  form.dispatchEvent(new window.Event('submit', { bubbles: true, cancelable: true }));
  await wait(300);
  const body2 = JSON.parse(captured.options.body);
  t('history includes previous turns', body2.contents.length === 3 &&
      body2.contents[1].role === 'model' && body2.contents[2].parts[0].text === 'And what about projects?',
      JSON.stringify(body2.contents.map(c => c.role)));

  // ---------- 3. Rate limit (429) ----------
  nextBehaviour = () => httpError(429);
  input.value = 'rate limit test';
  form.dispatchEvent(new window.Event('submit', { bubbles: true, cancelable: true }));
  await wait(300);
  let last = msgs().slice(-1)[0];
  t('429 shows a rate-limit message', /Rate limit reached/.test(last.textContent), last.textContent.slice(0, 80));
  t('429 message styled as a notice', last.classList.contains('chat-msg--notice'));
  t('status shows error state', document.querySelector('.chat-panel__status').classList.contains('is-error'));

  // ---------- 4. Bad key (403) ----------
  nextBehaviour = () => httpError(403);
  input.value = 'bad key test';
  form.dispatchEvent(new window.Event('submit', { bubbles: true, cancelable: true }));
  await wait(300);
  last = msgs().slice(-1)[0];
  t('403 explains the key problem', /API key was refused/.test(last.textContent), last.textContent.slice(0, 80));

  // ---------- 5. Network failure (TypeError) ----------
  nextBehaviour = () => Promise.reject(new window.TypeError('Failed to fetch'));
  input.value = 'offline test';
  form.dispatchEvent(new window.Event('submit', { bubbles: true, cancelable: true }));
  await wait(300);
  last = msgs().slice(-1)[0];
  t('network failure explained clearly', /Network error/.test(last.textContent), last.textContent.slice(0, 80));

  // ---------- 6. Blocked prompt ----------
  nextBehaviour = () => ok({ promptFeedback: { blockReason: 'SAFETY' } });
  input.value = 'blocked test';
  form.dispatchEvent(new window.Event('submit', { bubbles: true, cancelable: true }));
  await wait(300);
  last = msgs().slice(-1)[0];
  t('blocked prompt handled', /blocked by the API \(SAFETY\)/.test(last.textContent), last.textContent.slice(0, 80));

  // ---------- 7. Send button is re-enabled after errors ----------
  t('send button re-enabled after errors', document.getElementById('chatSend').disabled === false);
  t('no unhandled runtime errors', errors.length === 0, errors.join(' | '));

  console.log(results.join('\n'));
  console.log('\nFAILURES: ' + results.filter(r => r.startsWith('FAIL')).length);
  process.exit(0);
})();
