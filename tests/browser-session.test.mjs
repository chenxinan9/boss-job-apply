import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, readFileSync, writeFileSync, rmSync, realpathSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';
import { commandPrefix, validateCommand } from '../packages/boss-apply-codex/scripts/browser-session.mjs';

const script = fileURLToPath(new URL('../packages/boss-apply-codex/scripts/browser-session.mjs', import.meta.url));
const env = Object.fromEntries(Object.entries(process.env).filter(([k]) => !k.startsWith('AGENT_BROWSER_')));
// Unit-test subprocess double only. This never counts as browser or BOSS acceptance.
const fake = `import fs from 'node:fs';
const a=process.argv.slice(2);
if(a[0]==='--version') console.log('agent-browser 0.27.0');
else { fs.appendFileSync('calls.jsonl',JSON.stringify(a)+'\\n');
if(fs.existsSync('fail')) { console.log(JSON.stringify({success:false,error:'intentional failure'}));process.exitCode=1; }
else console.log(JSON.stringify({success:true,data:{url:fs.existsSync('blank')?'about:blank':'https://www.zhipin.com/'}})); }
`;
function fixture(t) {
  const cwd = realpathSync(mkdtempSync(resolve(tmpdir(), 'browser 空格-')));
  t.after(() => rmSync(cwd, { recursive: true, force: true }));
  const cli = resolve(cwd, 'installed tool.mjs'); writeFileSync(cli, fake);
  const run = (...args) => spawnSync(process.execPath, [script, ...args], { cwd, env, encoding: 'utf8' });
  assert.equal(run('init', cli).status, 0);
  return { cwd, run, calls: () => readFileSync(resolve(cwd, 'calls.jsonl'), 'utf8').trim().split('\n').map(JSON.parse) };
}
test('subsequent independent processes always use the same explicit config', t => {
  const f=fixture(t);
  for(const args of [['start'],['get','url'],['snapshot','-i'],['click','@e1']]) assert.equal(f.run(...args).status,0);
  const calls=f.calls();assert.equal(calls.length,5);
  for(const call of calls) assert.deepEqual(call.slice(0,2),['--config',resolve(f.cwd,'private/browser-session.json')]);
  const c=JSON.parse(readFileSync(calls[0][1]));assert.equal(c.headed,true);assert.equal(c._adapter.started,true);
  assert.equal(f.run('start').status,1);assert.equal(f.calls().length,5);
});
test('override attempts and shell shims fail before spawning', () => {
  for(const args of [['click','@e1','--profile','other'],['snapshot','--headed=false'],['close','--all'],['cookies','get'],['eval','anything'],['connect','9222'],['open','https://example.com']]) assert.throws(()=>validateCommand(args));
  for(const ext of ['cmd','bat','ps1']) assert.throws(()=>commandPrefix(`C:/tools/agent-browser.${ext}`));
  assert.deepEqual(commandPrefix('/space path/agent-browser.js'),[process.execPath,'/space path/agent-browser.js']);
});
test('blank page prevents action; observations remain possible', t => {
  const f=fixture(t);assert.equal(f.run('start').status,0);writeFileSync(resolve(f.cwd,'blank'),'');
  const r=f.run('click','@e1');assert.equal(r.status,1);assert.match(r.stderr,/NOT dispatched/);
  assert.equal(f.calls().some(c=>c.includes('click')),false);assert.equal(f.run('snapshot').status,0);
});
test('failed start is never automatically repeated', t => {
  const f=fixture(t);writeFileSync(resolve(f.cwd,'fail'),'');
  assert.equal(f.run('start').status,1);assert.equal(f.run('start').status,1);assert.equal(f.calls().length,1);
});
test('foreign environment settings fail without exposing their values', t => {
  const f=fixture(t);
  const r=spawnSync(process.execPath,[script,'get','url'],{cwd:f.cwd,env:{...env,AGENT_BROWSER_PROFILE:'secret-value'},encoding:'utf8'});
  assert.equal(r.status,1);assert.match(r.stderr,/AGENT_BROWSER_PROFILE/);assert.doesNotMatch(r.stderr,/secret-value/);
});
test('changed configuration or tool version stops before browser action', t => {
  const f=fixture(t), p=resolve(f.cwd,'private/browser-session.json');
  const c=JSON.parse(readFileSync(p));c._adapter.version='agent-browser 0.1.0';writeFileSync(p,JSON.stringify(c));
  assert.equal(f.run('start').status,1);
  c._adapter.version='agent-browser 0.27.0';c.headed=false;writeFileSync(p,JSON.stringify(c));assert.equal(f.run('start').status,1);
});
