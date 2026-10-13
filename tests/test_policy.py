import copy
import importlib.util
import json
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PACKAGES=ROOT/'packages'

class PolicyTest(unittest.TestCase):
    def setUp(self):
        self.base=PACKAGES/'boss-apply-codex'
        spec=importlib.util.spec_from_file_location('check_policy',self.base/'scripts/check_policy.py')
        mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);self.validate=mod.validate
        self.p=json.loads((self.base/'templates/policy.example.json').read_text())
    def ready(self):
        p=copy.deepcopy(self.p)
        p['requirements_confirmed']=True
        p['search'].update(city='测试城市',recommendation_tabs=['测试标签'],salary_bands=['测试档位'],keywords=['测试词'])
        p['allowed_recruiter_types']=['测试来源'];p['allowed_scope']=['测试职责']
        p['scoring']['dimensions']=[{'id':'a','label':'测试维度甲','criterion':'测试条件甲','max_score':50},{'id':'b','label':'测试维度乙','criterion':'测试条件乙','max_score':50}]
        p['scoring']['default']={'operator':'>=','threshold':70}
        return p
    def test_blank_template_is_draft(self):
        self.assertFalse(self.validate(self.p));self.assertFalse(self.p['requirements_confirmed'])
        self.assertEqual(self.p['scoring']['dimensions'],[]);self.assertEqual(self.p['scoring']['special_rules'],[])
        self.assertIsNone(self.p['scoring']['default']['threshold']);self.assertEqual(self.p['search']['city'],'')
        self.assertEqual(self.p['schedule']['time'],'');self.assertFalse(self.p['schedule']['enabled'])
    def test_empty_or_unconfirmed_apply_rejected(self):
        for p in [self.p,self.ready()]:
            p['requirements_confirmed']=False;p['mode']='apply'
            with self.assertRaises(ValueError):self.validate(p)
    def test_cannot_confirm_incomplete(self):
        self.p['requirements_confirmed']=True
        with self.assertRaises(ValueError):self.validate(self.p)
    def test_ready_user_config_valid(self):
        p=self.ready();p['mode']='apply';self.assertTrue(self.validate(p))
    def test_any_user_defined_dimensions_supported(self):
        p=self.ready();p['scoring']['dimensions']=[{'id':'custom','label':'自定义维度','criterion':'自定义判断依据','max_score':100}]
        self.assertTrue(self.validate(p))
    def test_weight_validation(self):
        for n in [True,49,101]:
            p=self.ready();p['scoring']['dimensions'][0]['max_score']=n
            with self.assertRaises(ValueError):self.validate(p)
    def test_duplicate_id_rejected(self):
        p=self.ready();p['scoring']['dimensions'][1]['id']='a'
        with self.assertRaises(ValueError):self.validate(p)
    def test_special_rules_must_be_explicit(self):
        p=self.ready();p['scoring']['special_rules']=[{'name':'测试条件','scope':'当前JD明确要求测试职责时','operator':'>','threshold':75}]
        self.assertTrue(self.validate(p));p['scoring']['special_rules'][0]['scope']=''
        with self.assertRaises(ValueError):self.validate(p)
    def test_incomplete_schedule_rejected(self):
        p=self.ready();p['mode']='apply';p['schedule']['enabled']=True
        with self.assertRaises(ValueError):self.validate(p)
        p['schedule'].update(timezone='UTC',time='09:15');self.assertTrue(self.validate(p))
    def test_bad_schedule_and_old_schema_rejected(self):
        for key,value in [('time','24:30'),('enabled','true'),('pause_dates',['2026-02-30'])]:
            p=self.ready();p['schedule'][key]=value
            with self.assertRaises(ValueError):self.validate(p)
        self.p['schema_version']=1
        with self.assertRaises(ValueError):self.validate(self.p)
    def test_forbidden_recording_rejected(self):
        self.p['per_job_records']=True
        with self.assertRaises(ValueError):self.validate(self.p)
    def test_client_specific_skill_metadata(self):
        for client in ('codex','workbuddy'):
            header=(PACKAGES/('boss-apply-'+client)/'SKILL.md').read_text().split('---',2)[1]
            for key in (['name','description'] if client=='codex' else ['name','description','description_zh','description_en','version','author']):
                self.assertIn('\n'+key+':',header)
    def test_editions_match(self):
        a=PACKAGES/'boss-apply-codex';b=PACKAGES/'boss-apply-workbuddy'
        for name in ['templates/policy.example.json','templates/resume.example.md','templates/schedule-prompt.md','scripts/check_policy.py','references/matching.md','references/browser-session.md','docs/validation.md']:
            self.assertEqual((a/name).read_bytes(),(b/name).read_bytes(),name)
        self.assertEqual((a/'执行手册.md').read_text().split('## 读取与边界',1)[1],(b/'执行手册.md').read_text().split('## 读取与边界',1)[1])
    def test_additional_requirements_validate_evidence(self):
        p=self.ready();p['additional_requirements']=[{'name':'附加条件','condition':'满足本人条件','visible_evidence':'当前页面字段','unknown_action':'SKIP'}]
        self.assertTrue(self.validate(p))
        for field,value in [('visible_evidence',''),('unknown_action','ASSUME')]:
            q=copy.deepcopy(p);q['additional_requirements'][0][field]=value
            with self.assertRaises(ValueError):self.validate(q)
    def test_missing_optional_extra_field_is_compatible(self):
        p=self.ready();p.pop('additional_requirements',None);self.assertTrue(self.validate(p))
    def test_private_inputs_absent(self):
        for base in PACKAGES.iterdir():self.assertFalse((base/'private').exists())

if __name__=='__main__':unittest.main()
