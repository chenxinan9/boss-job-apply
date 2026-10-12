import { readFileSync } from 'node:fs';
const config = JSON.parse(readFileSync(new URL('./control-signals.json', import.meta.url), 'utf8'));
const patterns = config.risk_patterns.map(value => new RegExp(value));
export function hasControlRisk(text) {
  return String(text).split('\n').some(raw => {
    const line = raw.replace(/^\s*\d+\s+(?:text|文本|标题|heading|button|按钮|link|文本栏)\s+(?:Description: )?/, '')
      .trim().split(/, (?:Value|Placeholder):/)[0];
    return patterns.some(pattern => pattern.test(line));
  });
}
