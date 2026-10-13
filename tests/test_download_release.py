import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile

spec=importlib.util.spec_from_file_location('download_release',Path(__file__).resolve().parents[1]/'tools/download_release.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class Response(io.BytesIO):url='https://release-assets.githubusercontent.com/example.zip'
class DownloadTest(unittest.TestCase):
    def setUp(self):self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name).resolve()
    def tearDown(self):self.temp.cleanup()
    def archive(self,extra=()):
        p=self.root/'bundle.zip'
        with zipfile.ZipFile(p,'w') as z:
            z.writestr('boss-apply-codex/SKILL.md','# Test input');z.writestr('boss-apply-codex/LICENSE','Test input')
            for name,value in extra:
                if isinstance(name,str):
                    member=zipfile.ZipInfo(name)
                    member.filename=name  # Preserve the deliberately malformed fixture on Windows.
                else:member=name
                z.writestr(member,value)
        return p
    def test_existing_destination_preserved(self):
        d=self.root/'existing';d.mkdir();(d/'keep').write_text('keep')
        with self.assertRaises(ValueError):m.install('codex',d)
        self.assertEqual((d/'keep').read_text(),'keep')
    def test_paths_rejected_before_extract(self):
        for name in ['boss-apply-codex/../outside','other/SKILL.md','boss-apply-codex/skill.md','boss-apply-codex/a\\b','boss-apply-codex/C:secret']:
            with self.subTest(name=name):
                p=self.archive([(name,'bad')]);stage=self.root/'stage';stage.mkdir(exist_ok=True)
                with self.assertRaises(ValueError):m.extract(p,stage,'codex')
                self.assertEqual(list(stage.iterdir()),[])
    def test_archive_symlink_rejected(self):
        info=zipfile.ZipInfo('boss-apply-codex/link');info.external_attr=0o120777<<16
        p=self.archive([(info,'/target')])
        with self.assertRaises(ValueError):m.extract(p,self.root,'codex')
    def test_bad_hash_and_size_rejected(self):
        with patch.dict(m.ARCHIVES,{'codex':{'name':'test.zip','sha256':'0'*64}}),patch.object(m.urllib.request,'build_opener') as opener:
            opener.return_value.open.return_value=Response(b'bad')
            with self.assertRaisesRegex(ValueError,'SHA-256'):m.download('codex',self.root/'bad.zip')
            opener.return_value.open.return_value=Response(b'large')
            with patch.object(m,'MAX_DOWNLOAD',2):
                with self.assertRaises(ValueError):m.download('codex',self.root/'large.zip')
    def test_https_downgrade_rejected(self):
        with self.assertRaises(ValueError):m.HTTPSRedirect().redirect_request(None,None,302,'',{},'http://example.org/a')
    def test_complete_download_only(self):
        raw=self.archive().read_bytes();sha=hashlib.sha256(raw).hexdigest();dest=self.root/'workspace'
        with patch.dict(m.ARCHIVES,{'codex':{'name':'test.zip','sha256':sha}}),patch.object(m.urllib.request,'build_opener') as opener:
            opener.return_value.open.return_value=Response(raw);receipt=m.install('codex',dest)
        self.assertEqual(receipt['sha256'],sha)
        self.assertEqual({p.name for p in dest.iterdir()},{'SKILL.md','LICENSE','INSTALLATION.json'})
    def test_destination_created_during_download_preserved(self):
        raw=self.archive().read_bytes();dest=self.root/'workspace'
        def download(client,target):target.write_bytes(raw);dest.mkdir();(dest/'keep').write_text('keep');return {}
        with patch.object(m,'download',side_effect=download):
            with self.assertRaises(FileExistsError):m.install('codex',dest)
        self.assertEqual([p.name for p in dest.iterdir()],['keep'])
    def test_real_packaged_files_checksum_and_extract(self):
        for client,item in m.ARCHIVES.items():
            p=Path(__file__).resolve().parents[1]/'dist'/item['name']
            if not p.exists():self.skipTest('run tools/package.py to validate generated ZIPs')
            self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),item['sha256'])
            dest=m.extract(p,self.root,client)
            self.assertFalse((dest/'private').exists());self.assertTrue((dest/'执行手册.md').exists())

if __name__=='__main__':unittest.main()
