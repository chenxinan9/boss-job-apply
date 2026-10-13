#!/usr/bin/env node
// One fixed launch configuration. No job matching, sending loop, cookies or retry engine.
import { spawnSync } from 'node:child_process';
import { mkdirSync, readFileSync, writeFileSync, realpathSync, existsSync, rmdirSync } from 'node:fs';
import { resolve } from 'node:path';
import { randomUUID } from 'node:crypto';
import { pathToFileURL } from 'node:url';

const HELP = `Usage (run from your private workspace):
  node /path/to/scripts/browser-session.mjs init /absolute/path/to/agent-browser[.exe|.js]
  node /path/to/scripts/browser-session.mjs start
  node /path/to/scripts/browser-session.mjs snapshot -i
  node /path/to/scripts/browser-session.mjs get url
  node /path/to/scripts/browser-session.mjs screenshot private/current.png
  node /path/to/scripts/browser-session.mjs click @e1
Existing native/Ego sessions do not use this CLI adapter. Read references/agent-browser.md first.`;

export function commandPrefix(executable) {
  if (/\.(cmd|bat|ps1)$/i.test(executable)) {
    throw new Error('Use the installed package bin/agent-browser.js or native executable, not a shell shim.');
  }
  return /\.m?js$/i.test(executable) ? [process.execPath, executable] : [executable];
}

// Command flags are deliberately allowlisted so a later call cannot change launch settings.
export function validateCommand(args) {
  const [action, ...rest] = args;
  const simple = { click: 1, hover: 1, fill: 2, press: 1, focus: 1,
    select: 2, scrollintoview: 1, back: 0, forward: 0, close: 0 };
  if (action in simple && rest.length === simple[action] && !rest.some(x => x.startsWith('-'))) return;
  if (action === 'snapshot' && rest.every(x => ['-i', '-c'].includes(x))) return;
  if (action === 'screenshot' && rest.length === 1 && !rest[0].startsWith('-')) return;
  if (action === 'get' && (rest.length === 1 && ['url', 'title'].includes(rest[0]) ||
      rest.length === 2 && ['text', 'value'].includes(rest[0]) && !rest[1].startsWith('-'))) return;
  if (action === 'tab' && (rest.length === 0 || rest.length === 1 && rest[0] === 'list')) return;
  if (action === 'scroll' && rest.length === 2 && ['up', 'down', 'left', 'right'].includes(rest[0]) && /^\d{1,4}$/.test(rest[1])) return;
  throw new Error('Unsupported command or launch override. Use the documented fixed-session commands; do not add startup flags.');
}

function run(executable, args) {
  const [bin, ...prefix] = commandPrefix(executable);
  const result = spawnSync(bin, [...prefix, ...args], {
    encoding: 'utf8', timeout: 45000, maxBuffer: 8 * 1024 * 1024, windowsHide: true,
    // Inherit network/system settings. Conflicting Agent Browser settings are rejected, never silently removed.
    env: process.env, shell: false,
  });
  if (result.error) throw new Error(`Browser command failed (${result.error.code}); no retry was made. Keep the browser open and inspect it.`);
  if (result.status !== 0) throw new Error((result.stderr || result.stdout || `Exit ${result.status}`).trim());
  return result.stdout.trim();
}

function readResult(raw) {
  let reply;
  try { reply = JSON.parse(raw); } catch { throw new Error('Browser did not return valid JSON; do not retry an action.'); }
  if (reply.success !== true) throw new Error(reply.error || 'Browser command failed; no retry was made.');
  return reply;
}

export function main(args = process.argv.slice(2), cwd = process.cwd()) {
  if (!args.length || args[0] === '--help') { console.log(HELP); return; }
  const overrides = Object.keys(process.env).filter(k => k.startsWith('AGENT_BROWSER_'));
  if (overrides.length) throw new Error(`Conflicting environment settings: ${overrides.join(', ')}. Inspect their purpose before changing them; this adapter will not override them.`);
  const root = resolve(cwd, 'private');
  mkdirSync(root, { recursive: true, mode: 0o700 });
  const configPath = resolve(root, 'browser-session.json');
  const lock = resolve(root, 'browser-command.lock');
  try { mkdirSync(lock); } catch { throw new Error('Another command is active, or a prior command was interrupted. Inspect it before removing private/browser-command.lock.'); }
  try {
    if (args[0] === 'init') {
      if (args.length !== 2) throw new Error(HELP);
      if (existsSync(configPath)) throw new Error('Session already configured. Keep it and use get url / snapshot; do not initialize again.');
      const executable = realpathSync(resolve(args[1]));
      commandPrefix(executable);
      const version = run(executable, ['--version']);
      if (!/^agent-browser \d+\.\d+\.\d+/.test(version)) throw new Error('Unexpected executable version.');
      const config = { headed: true, json: true, session: 'boss-' + randomUUID().slice(0, 12),
        profile: resolve(root, 'browser-profile'),
        _adapter: { executable, version, started: false } };
      writeFileSync(configPath, JSON.stringify(config, null, 2) + '\n', { flag: 'wx', mode: 0o600 });
      console.log(JSON.stringify({ status: 'CONFIGURED_ONLY', browser_ready: false, send_authorized: false }));
      return;
    }
    const config = JSON.parse(readFileSync(configPath, 'utf8'));
    if (JSON.stringify(Object.keys(config).sort()) !== JSON.stringify(['_adapter', 'headed', 'json', 'profile', 'session']) ||
        config.headed !== true || config.json !== true || !/^boss-[a-f0-9-]{12}$/.test(config.session) ||
        config.profile !== resolve(root, 'browser-profile') || typeof config._adapter?.started !== 'boolean') {
      throw new Error('Session configuration changed or moved. Stop and inspect; do not silently create a replacement.');
    }
    const { executable, version } = config._adapter;
    if (run(executable, ['--version']) !== version) throw new Error('Agent Browser version changed. Stop the task and review the upgrade before continuing.');
    const call = command => readResult(run(executable, ['--config', configPath, ...command]));
    if (args[0] === 'start') {
      if (args.length !== 1 || config._adapter.started) throw new Error('Start is allowed only once. Inspect the current window with get url / snapshot; do not restart after verification.');
      // Record before dispatch: even a timeout must not cause a second open.
      config._adapter.started = true;
      writeFileSync(configPath, JSON.stringify(config, null, 2) + '\n', { mode: 0o600 });
      console.log(JSON.stringify(call(['open', 'https://www.zhipin.com/'])));
      return;
    }
    validateCommand(args);
    if (!config._adapter.started) throw new Error('Run start once, then confirm the visible window.');
    const observations = ['get', 'snapshot', 'screenshot', 'tab', 'close'];
    if (!observations.includes(args[0])) {
      const url = call(['get', 'url']).data?.url;
      if (!url || !/^https:\/\/([a-z0-9-]+\.)*zhipin\.com(?:\/|$)/i.test(url)) {
        throw new Error('Current page is blank or outside BOSS. Action was NOT dispatched. Inspect the original window; do not restart or retry a prior click.');
      }
    }
    console.log(JSON.stringify(call(args)));
  } finally { rmdirSync(lock); }
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  try { main(); } catch (error) { console.error(error.message); process.exitCode = 1; }
}
