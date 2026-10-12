// Optional adapter for complete Chinese macOS AX snapshots, not a browser client.
// No network, persistent job ledger, score engine or automatic retry.
import { performance } from 'node:perf_hooks';
import { hasControlRisk } from './control-signals.mjs';

export function assertJobsAddress(text) {
  const rows = [...text.matchAll(/^.*Description: 地址和搜索栏, Value: ([^\n]+)/gm)];
  let url;
  try { if (rows.length === 1) url = new URL(rows[0][1].split(', Placeholder:')[0]); } catch {}
  if (!url || url.protocol !== 'https:' || !['www.zhipin.com', 'zhipin.com'].includes(url.hostname) ||
      url.pathname !== '/web/geek/jobs' || url.username || url.password || url.port) {
    throw Error('LIST_PAGE_REQUIRED_NO_ACTION');
  }
}

function targetAt(text, index) {
  if (!Number.isInteger(index)) throw Error('OBSERVED_INTEGER_INDEX_REQUIRED');
  const rows = text.split('\n').filter(row => row.match(/^\s*(\d+)\s/)?.[1] === String(index));
  if (rows.length !== 1) throw Error('CURRENT_CLICK_TARGET_NOT_UNIQUE');
  const match = rows[0].match(/^\s*\d+\s+(link|button|按钮)(?: Description:)?\s+(.+?)(?:, (?:Value|Help):.*|,\s*)?$/);
  if (!match) throw Error('CURRENT_CLICK_TARGET_ROLE_INVALID');
  return { role: match[1], label: match[2] };
}

export function createObservedUI({ getState, click, assertOwnership,
  clock = () => performance.now(), maxAgeMs = 10000 }) {
  if (![getState, click, assertOwnership, clock].every(x => typeof x === 'function')) throw Error('CALLBACKS_REQUIRED');
  if (!Number.isFinite(maxAgeMs) || maxAgeMs <= 0) throw Error('POSITIVE_MAX_AGE_REQUIRED');
  let observation = null, busy = false;
  const current = () => {
    const age = observation ? clock() - observation.at : Infinity;
    if (busy || !observation || age > maxAgeMs || age < 0) throw Error('FRESH_OBSERVATION_REQUIRED');
    return observation;
  };
  async function dispatch(index, expected, contact = false) {
    const observed = current(), target = targetAt(observed.text, index);
    if (target.label !== expected) throw Error('CURRENT_CLICK_LABEL_MISMATCH');
    assertJobsAddress(observed.text);
    const controls = observed.text.replace(/^\s*\d+ 标签 \(settable, boolean\)[^\n]*, Value: off\s*$/gm, '');
    if (hasControlRisk(controls)) throw Error('CURRENT_CONTROL_RISK_NO_CLICK');
    if (contact && /已向BOSS发送消息|Description: 继续沟通,/.test(observed.text)) throw Error('EXISTING_SESSION_NO_CLICK');
    // Consume before dispatch, even if ownership check or transport fails.
    observation = null; busy = true;
    try {
      if (await assertOwnership() !== true) throw Error('EXCLUSIVE_OWNERSHIP_REQUIRED');
      const age = clock() - observed.at;
      if (age > maxAgeMs || age < 0) throw Error('FRESH_OBSERVATION_REQUIRED');
      return await click(index);
    } finally { busy = false; }
  }
  return Object.freeze({
    async getState() {
      if (busy) throw Error('UI_OPERATION_IN_PROGRESS');
      busy = true; observation = null;
      try {
        const text = await getState();
        if (typeof text !== 'string') throw Error('FULL_AX_TEXT_REQUIRED');
        observation = { text, at: clock() };
        return text;
      } finally { busy = false; }
    },
    async contact(index) { return dispatch(index, '立即沟通', true); },
    async dismiss(index) { return dispatch(index, '留在此页'); },
    async selectCard(index, { job, company }) {
      const text = current().text, lines = text.split('\n');
      const pos = lines.findIndex(row => row.match(/^\s*(\d+)\s/)?.[1] === String(index));
      if (!job || !company || pos < 0) throw Error('CURRENT_CARD_REQUIRED');
      const depth = lines[pos].match(/^\s*/)[0].length;
      let start = pos - 1;
      while (start >= 0 && (!lines[start].trim() || lines[start].match(/^\s*/)[0].length >= depth)) start--;
      if (start < 0 || !/\d+ container\s*$/.test(lines[start])) throw Error('CURRENT_CARD_PARENT_REQUIRED');
      const parentDepth = lines[start].match(/^\s*/)[0].length;
      let end = pos + 1;
      while (end < lines.length && (!lines[end].trim() || lines[end].match(/^\s*/)[0].length > parentDepth)) end++;
      if (!lines.slice(start + 1, end).some(row => row.includes('link Description: ' + company + ', Value:'))) {
        throw Error('CURRENT_CARD_COMPANY_MISMATCH');
      }
      return dispatch(index, job);
    },
    invalidate() { observation = null; }
  });
}
