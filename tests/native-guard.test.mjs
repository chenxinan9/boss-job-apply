import test from 'node:test';
import assert from 'node:assert/strict';
import { createObservedUI, assertJobsAddress } from '../packages/boss-apply-codex/optional/native-guard/fresh-ui.mjs';
const address = '1 text Description: 地址和搜索栏, Value: https://www.zhipin.com/web/geek/jobs';
const page = address + '\n2 button Description: 立即沟通,\n3 button Description: 留在此页,';
function setup({ text = page, failure = false, owned = true } = {}) {
  let time=0, clicks=0;
  const ui = createObservedUI({getState: async () => text, click: async () => {clicks++; if(failure) throw Error('TRANSPORT');},
    assertOwnership: async () => owned, clock: () => time});
  return {ui, count: () => clicks, setTime: value => {time=value;}};
}
test('dispatch consumes snapshot',async()=>{
 const {ui,count}=setup(); await ui.getState(); await ui.contact(2);
 await assert.rejects(ui.contact(2),/FRESH/); assert.equal(count(),1);
});
test('failed transport cannot reuse observation',async()=>{
 const {ui,count}=setup({failure:true}); await ui.getState(); await assert.rejects(ui.contact(2),/TRANSPORT/);
 await assert.rejects(ui.contact(2),/FRESH/); assert.equal(count(),1);
});
test('expired or invalidated observations never dispatch',async()=>{
 const {ui,count,setTime}=setup(); await ui.getState(); setTime(10001); await assert.rejects(ui.contact(2),/FRESH/);
 await ui.getState(); ui.invalidate(); await assert.rejects(ui.contact(2),/FRESH/); assert.equal(count(),0);
});
test('ownership rejection blocks sending',async()=>{
 const {ui,count}=setup({owned:false}); await ui.getState(); await assert.rejects(ui.contact(2),/OWNERSHIP/); assert.equal(count(),0);
});
test('risk and current existing conversation block sending',async()=>{
 for(const extra of ['请完成验证','今日沟通人数已达上限','Description: 继续沟通,']) {
  const {ui,count}=setup({text:page+'\n4 text '+extra}); await ui.getState(); await assert.rejects(ui.contact(2)); assert.equal(count(),0);
 }
});
test('ambiguous target and wrong labels cannot dispatch',async()=>{
 for(const text of [page+'\n2 button Description: 立即沟通,',page.replace('立即沟通','继续沟通')]) {
  const {ui,count}=setup({text}); await ui.getState(); await assert.rejects(ui.contact(2)); assert.equal(count(),0);
 }
});
test('only exact list origin and path accepted',()=>{
 assert.doesNotThrow(()=>assertJobsAddress(address));
 for(const url of ['https://www.zhipin.com.evil.invalid/web/geek/jobs','https://www.zhipin.com/job_detail/example.html','http://www.zhipin.com/web/geek/jobs']) {
  assert.throws(()=>assertJobsAddress('1 text Description: 地址和搜索栏, Value: '+url));
 }
 assert.throws(()=>assertJobsAddress(address+'\n'+address));
});
test('card selection binds title and company',async()=>{
 const text=address+'\n10 container\n  11 link Description: 示例岗位, Value: unused\n  12 link Description: 示例企业, Value: unused';
 const {ui,count}=setup({text}); await ui.getState();
 await assert.rejects(ui.selectCard(11,{job:'示例岗位',company:'其他企业'}),/COMPANY/);
 await assert.rejects(ui.selectCard(11,{job:'其他岗位',company:'示例企业'}),/LABEL/);
 assert.equal(count(),0); await ui.selectCard(11,{job:'示例岗位',company:'示例企业'}); assert.equal(count(),1);
});
