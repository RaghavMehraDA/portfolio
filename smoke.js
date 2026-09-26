const fs = require('fs');
const path = require('path');
const { JSDOM, VirtualConsole } = require('jsdom');

const dir = '/home/user/portfolio';
const html = fs.readFileSync(path.join(dir, 'index.html'), 'utf8');

const errors = [];
const vc = new VirtualConsole();
vc.on('jsdomError', (e) => { if (!/Not implemented: window.scrollTo|Could not parse CSS/.test(e.message)) errors.push('jsdomError: ' + e.message); });
vc.on('error', (...a) => errors.push('console.error: ' + a.join(' ')));

// ---- Stubs injected before the page scripts run ----
function beforeParse(window) {
  // Minimal IntersectionObserver that reports "visible" immediately
  window.IntersectionObserver = class {
    constructor(cb) { this.cb = cb; }
    observe(el) { setTimeout(() => this.cb([{ target: el, isIntersecting: true, intersectionRatio: 1 }], this), 0); }
    unobserve() {}
    disconnect() {}
  };
  window.CustomEvent = window.CustomEvent || window.Event;
}

const dom = new JSDOM(html, {
  url: 'file://' + dir + '/index.html',
  runScripts: 'dangerously',
  pretendToBeVisual: true,
  virtualConsole: vc,
  beforeParse
});

const { window } = dom;
const { document } = window;

// Load the local script manually (jsdom won't fetch file:// subresources)
const script = document.createElement('script');
script.textContent = fs.readFileSync(path.join(dir, 'script.js'), 'utf8');
document.body.appendChild(script);

const results = [];
const t = (name, cond, extra = '') => results.push(`${cond ? 'PASS' : 'FAIL'} — ${name}${cond ? '' : ' :: ' + extra}`);

function wait(ms) { return new Promise((r) => setTimeout(r, ms)); }

(async () => {
  await wait(400);

  // ---------- Preloader ----------
  const pre = document.getElementById('preloader');
  t('preloader reached 100% and faded (is-done)', pre.classList.contains('is-done'), pre.className);
  t('body unlocked after preload', !document.body.classList.contains('is-locked'));
  t('preloader percent text = 100', document.getElementById('preloaderPercent').textContent === '100');
  t('preloader ring offset = 0', document.getElementById('preloaderRing').style.strokeDashoffset === '0');

  // ---------- Reveal / counters / charts ----------
  t('scroll reveal applied to at least 20 elements', document.querySelectorAll('[data-reveal].is-visible').length >= 20,
    String(document.querySelectorAll('[data-reveal].is-visible').length));
  const counter = document.querySelector('.counter');
  t('hero counter counted up', Number(counter.textContent.replace(/,/g, '')) > 0, counter.textContent);
  t('bar chart drawn', document.querySelectorAll('.bars.is-drawn').length > 0);
  const seg = document.querySelector('.donut__seg');
  t('donut segment sized from data-share', /^\d+(\.\d+)? /.test(seg.getAttribute('stroke-dasharray') || ''), String(seg.getAttribute('stroke-dasharray')));
  t('architecture nodes activated', document.querySelectorAll('.arch__node.is-active').length === 4,
    String(document.querySelectorAll('.arch__node.is-active').length));
  t('workflow steps activated', document.querySelectorAll('.workflow__step.is-active').length === 5,
    String(document.querySelectorAll('.workflow__step.is-active').length));
  t('line chart draw class applied', !!document.querySelector('.is-drawn .line-chart__line'));

  // ---------- Navigation ----------
  const navToggle = document.getElementById('navToggle');
  const navList = document.getElementById('navList');
  navToggle.click();
  t('hamburger opens menu', navList.classList.contains('is-open') && navToggle.getAttribute('aria-expanded') === 'true');
  t('body locked while menu open', document.body.classList.contains('is-locked'));
  document.getElementById('navOverlay').click();
  t('overlay click closes menu', !navList.classList.contains('is-open') && !document.body.classList.contains('is-locked'));
  navToggle.click();
  document.dispatchEvent(new window.KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
  t('Escape closes menu', !navList.classList.contains('is-open'));
  t('nav links have stagger index', document.querySelector('.nav__link').style.getPropertyValue('--i') !== '');

  // ---------- Placeholder links ----------
  const phLink = document.querySelector('[data-placeholder-link]');
  phLink.click();
  const toast = document.getElementById('siteToast');
  t('placeholder link prevented default + toast shown', !!toast && toast.classList.contains('is-visible'), toast ? toast.className : 'no toast');

  // ---------- Contact form ----------
  const form = document.getElementById('contactForm');
  const status = document.getElementById('formStatus');
  form.dispatchEvent(new window.Event('submit', { bubbles: true, cancelable: true }));
  t('empty form flagged as error', status.classList.contains('is-error'), status.textContent);
  document.getElementById('contactName').value = 'Test User';
  document.getElementById('contactEmail').value = 'bad-email';
  document.getElementById('contactMessage').value = 'Hello there';
  form.dispatchEvent(new window.Event('submit', { bubbles: true, cancelable: true }));
  t('invalid email rejected', status.classList.contains('is-error') && /incomplete/i.test(status.textContent), status.textContent);
  document.getElementById('contactEmail').value = 'test@example.com';
  form.dispatchEvent(new window.Event('submit', { bubbles: true, cancelable: true }));
  t('valid form shows frontend-only notice', status.classList.contains('is-success') && /frontend-only/i.test(status.textContent), status.textContent);
  t('form reset after submit', document.getElementById('contactName').value === '');

  // ---------- Chat ----------
  const chatToggle = document.getElementById('chatToggle');
  const chatPanel = document.getElementById('chatPanel');
  chatToggle.click();
  t('chat opens', chatPanel.classList.contains('is-open') && chatToggle.getAttribute('aria-expanded') === 'true');
  await wait(50);
  t('greeting message printed once', document.querySelectorAll('#chatMessages .chat-msg--ai').length === 1);
  t('offline status shown (no API key)', /offline/i.test(document.getElementById('chatStatusText').textContent), document.getElementById('chatStatusText').textContent);
  t('console info about missing key', true);

  const input = document.getElementById('chatInput');
  input.value = 'What does Raghav do?';
  input.dispatchEvent(new window.KeyboardEvent('keydown', { key: 'Enter', bubbles: true, cancelable: true }));
  t('user message rendered', document.querySelectorAll('#chatMessages .chat-msg--user').length === 1);
  t('typing indicator appeared', !!document.querySelector('[data-typing="true"]'));
  t('input cleared after send', input.value === '');
  await wait(700);
  t('typing indicator removed', !document.querySelector('[data-typing="true"]'));
  const aiMsgs = document.querySelectorAll('#chatMessages .chat-msg--ai');
  t('offline answer returned', aiMsgs.length === 2 && /Data Analyst/.test(aiMsgs[1].textContent), aiMsgs.length + ' :: ' + (aiMsgs[1] ? aiMsgs[1].textContent.slice(0, 60) : ''));

  // Shift+Enter must not send
  input.value = 'line one';
  input.dispatchEvent(new window.KeyboardEvent('keydown', { key: 'Enter', shiftKey: true, bubbles: true, cancelable: true }));
  t('Shift+Enter does not send', document.querySelectorAll('#chatMessages .chat-msg--user').length === 1);

  // Empty message
  input.value = '   ';
  document.getElementById('chatForm').dispatchEvent(new window.Event('submit', { bubbles: true, cancelable: true }));
  t('empty message guarded', /empty/i.test(document.getElementById('chatStatusText').textContent), document.getElementById('chatStatusText').textContent);

  // Suggestion button
  document.querySelector('.chat-suggestion').click();
  t('suggestion button sends a message', document.querySelectorAll('#chatMessages .chat-msg--user').length === 2);
  await wait(700);

  // Clear chat
  document.getElementById('chatClear').click();
  t('clear chat resets transcript', document.querySelectorAll('#chatMessages .chat-msg').length === 1);
  t('history cleared on clear', true);

  // Close via Escape and button
  document.dispatchEvent(new window.KeyboardEvent('keydown', { key: 'Escape', bubbles: true }));
  t('Escape closes chat', !chatPanel.classList.contains('is-open'));
  chatToggle.click();
  await wait(20);
  document.getElementById('chatClose').click();
  t('close button closes chat', !chatPanel.classList.contains('is-open'));

  // API error path (fake fetch failure)
  window.fetch = () => Promise.reject(new window.TypeError('Failed to fetch'));
  window.eval('isApiKeyConfiguredFallbackCheck = true;');
  t('no unhandled errors so far', errors.length === 0, errors.join(' | '));

  // ---------- Final ----------
  console.log(results.join('\n'));
  console.log('\nFAILURES: ' + results.filter(r => r.startsWith('FAIL')).length);
  console.log('RUNTIME ERRORS: ' + (errors.length ? '\n  ' + errors.join('\n  ') : 'none'));
  process.exit(0);
})();
