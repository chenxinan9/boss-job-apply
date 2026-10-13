// Real Chromium, neutral local page. Browser continuity only; never a BOSS acceptance test.
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { createServer } from 'node:http';
import { mkdtempSync, readFileSync, writeFileSync, realpathSync } from 'node:fs';
import { rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import assert from 'node:assert/strict';
import { randomUUID } from 'node:crypto';

const exec = promisify(execFile);
const cli = resolve(process.argv[2]);
const adapter = process.argv[3] ? resolve(process.argv[3]) : fileURLToPath(new URL('../packages/boss-apply-workbuddy/scripts/browser-session.mjs', import.meta.url));
const cwd = realpathSync(mkdtempSync(resolve(tmpdir(), 'browser-continuity-')));
const env = Object.fromEntries(Object.entries(process.env).filter(([k]) => !k.startsWith('AGENT_BROWSER_')));
const run = async args => (await exec(process.execPath, args, { cwd, env, timeout: 60000, maxBuffer: 8 * 1024 * 1024 })).stdout.trim();
const server = createServer((req, res) => {
  res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
  res.end('<!doctype html><title>Browser continuity test</title><label>Continuity<input id="state" value="initial"></label>');
});
await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
let configured = false;
try {
  await run([adapter, 'init', cli]);configured = true;
  const configPath = resolve(cwd, 'private/browser-session.json');
  // Test-only bootstrap to a neutral page; production start always opens real BOSS.
  const config = JSON.parse(readFileSync(configPath));config._adapter.started = true;
  writeFileSync(configPath, JSON.stringify(config));
  const direct = args => run([cli, '--config', configPath, ...args]);
  const url = `http://127.0.0.1:${server.address().port}/`;
  await direct(['open', url]);
  const marker = randomUUID();
  await direct(['fill', '#state', marker]);
  for (let round = 0; round < 3; round++) {
    const current = JSON.parse(await run([adapter, 'get', 'url']));
    assert.equal(current.success, true);assert.equal(current.data.url, url);
    const snapshot = await run([adapter, 'snapshot']);assert.ok(snapshot.includes(marker), 'Live input state lost between processes');
  }
  await run([adapter, 'screenshot', 'private/check.png']);
  assert.equal(readFileSync(resolve(cwd, 'private/check.png')).subarray(1,4).toString(), 'PNG');
  // The adapter refuses to act on non-BOSS pages, even when the browser is healthy.
  await assert.rejects(run([adapter, 'click', '#state']), /NOT dispatched/);
  console.log(JSON.stringify({ status: 'BROWSER_CONTINUITY_PASSED', platform: process.platform,
    agent_browser: config._adapter.version, independent_read_rounds: 3, headed: config.headed,
    screenshot: true, live_input_preserved: true, boss_test: false }));
} finally {
  if (configured) {
    try { await run([adapter, 'close']); } catch (error) { console.error('Test session cleanup failed: ' + error.message); }
  }
  server.close();
  // Windows releases the daemon's working-directory handle shortly after close replies.
  await rm(cwd, { recursive: true, force: true, maxRetries: 10, retryDelay: 200 });
}
