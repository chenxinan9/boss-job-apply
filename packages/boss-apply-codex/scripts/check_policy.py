#!/usr/bin/env python3
"""Validate user-owned configuration only; no browser or network operations."""
import argparse
import json
import re
from datetime import date
from pathlib import Path


def text_list(value):
    return isinstance(value, list) and all(isinstance(v,str) and v.strip() for v in value)


def gate(value, allow_empty=False):
    if not isinstance(value,dict) or value.get('operator') not in ('>','>='):
        raise ValueError('评分比较符须为 > 或 >=')
    n=value.get('threshold')
    if allow_empty and n is None: return
    if type(n) is not int or not 0<=n<=100: raise ValueError('评分门槛须为0到100整数')


def validate(p):
    if p.get('schema_version') != 2: raise ValueError('请按当前空白模板准备配置并由本人确认')
    if p.get('mode') not in ('review','apply'): raise ValueError('mode 必须是 review/apply')
    if type(p.get('requirements_confirmed')) is not bool: raise ValueError('requirements_confirmed 必须为布尔值')
    s=p['search']
    if not isinstance(s['city'],str): raise ValueError('city 必须为文本')
    for key in ('recommendation_tabs','salary_bands','keywords'):
        if not text_list(s[key]): raise ValueError(key+' 必须为文本列表')
    salary=s['monthly_salary_upper_min_k']
    if salary is not None and (type(salary) not in (int,float) or not 0<salary<10000): raise ValueError('薪资额外门槛须为正数或null')
    for key in ('allowed_recruiter_types','exclude_companies','exclude_titles','exclude_primary_duties','allowed_scope'):
        if not text_list(p[key]): raise ValueError(key+' 必须为文本列表')
    extra=p.get('additional_requirements',[])
    if not isinstance(extra,list): raise ValueError('additional_requirements 必须为列表')
    for requirement in extra:
        if not isinstance(requirement,dict) or any(not isinstance(requirement.get(k),str) or not requirement[k].strip() for k in ('name','condition','visible_evidence')):
            raise ValueError('附加要求需要名称、条件和可见证据说明')
        if requirement.get('unknown_action')!='SKIP': raise ValueError('附加条件不明时跳过，不猜测')
    if p.get('unknown_recruiter_action')!='SKIP': raise ValueError('来源不明时应跳过')
    scoring=p['scoring']; dims=scoring['dimensions']
    if not isinstance(dims,list): raise ValueError('评分维度必须为列表')
    ids=[]
    for d in dims:
        if not isinstance(d,dict) or any(not isinstance(d.get(k),str) or not d[k].strip() for k in ('id','label','criterion')):
            raise ValueError('每个维度需要id、label和criterion')
        if type(d.get('max_score')) is not int or not 0<d['max_score']<=100: raise ValueError('维度权重须为正整数')
        ids.append(d['id'])
    if len(set(ids))!=len(ids): raise ValueError('维度id不能重复')
    if dims and sum(d['max_score'] for d in dims)!=100: raise ValueError('维度权重须合计100')
    gate(scoring['default'],allow_empty=True)
    rules=scoring['special_rules']
    if not isinstance(rules,list): raise ValueError('特殊评分规则必须为列表')
    for rule in rules:
        gate(rule)
        if any(not isinstance(rule.get(k),str) or not rule[k].strip() for k in ('name','scope')): raise ValueError('特殊规则需要name与scope')
    sch=p['schedule']
    if type(sch['enabled']) is not bool: raise ValueError('schedule.enabled 必须为布尔值')
    if not isinstance(sch['timezone'],str) or not isinstance(sch['time'],str): raise ValueError('时区和时间必须为文本')
    if sch['time'] and not re.fullmatch(r'(?:[01][0-9]|2[0-3]):[0-5][0-9]',sch['time']): raise ValueError('时间必须为HH:MM')
    if not isinstance(sch['pause_dates'],list): raise ValueError('暂停日期必须为列表')
    for day in sch['pause_dates']:
        if not isinstance(day,str) or date.fromisoformat(day).isoformat()!=day: raise ValueError('暂停日期须为YYYY-MM-DD')
    for key in ('historical_dedupe','post_send_verification','per_job_records'):
        if p.get(key) is not False: raise ValueError(key+' 与本流程不符')
    if p.get('completion')!='CURRENT_PLATFORM_DAILY_CAP': raise ValueError('完成依据须为平台当前满额提示')
    ready=bool(p['requirements_confirmed'] and s['city'].strip() and all(s[k] for k in ('recommendation_tabs','salary_bands','keywords')) and p['allowed_recruiter_types'] and p['allowed_scope'] and dims and scoring['default']['threshold'] is not None)
    if p['requirements_confirmed'] and not ready: raise ValueError('本人确认之前必须补齐条件与评分')
    if p['mode']=='apply' and not ready: raise ValueError('空白或未确认的配置不能apply')
    if sch['enabled'] and (p['mode']!='apply' or not ready or not sch['timezone'].strip() or not sch['time']): raise ValueError('启用定时前须完成本人条件、apply模式、时区与时间')
    return ready


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('policy',type=Path);args=parser.parse_args()
    try:
        p=json.loads(args.policy.read_text(encoding='utf-8-sig'));ready=validate(p)
        print(json.dumps({'status':'READY' if ready else 'DRAFT','mode':p['mode'],'boundary':'配置状态不是本人外发授权，也不证明浏览器已连接'},ensure_ascii=False))
    except (ValueError,KeyError,TypeError,OSError) as error:
        print(json.dumps({'status':'FAIL','error':str(error)},ensure_ascii=False));raise SystemExit(1)
