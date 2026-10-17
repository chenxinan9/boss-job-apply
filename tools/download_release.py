#!/usr/bin/env python3
"""Download and verify an independent skill workspace; never run BOSS or register a task."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import stat
import sys
import tempfile
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import zipfile

VERSION='v0.4.0-rc.15'
REPOSITORY='https://github.com/chenxinan9/boss-job-apply'
RELEASE_AVAILABLE=False  # Re-enable only after independent live acceptance.
ARCHIVES={'codex': {'name': 'boss-apply-codex-0.4.0-rc.15.zip', 'sha256': 'd95667c6297351e3f730be3ba3819d71c204959385c28e34f235a4d0499a421c'}, 'workbuddy-macos': {'name': 'boss-apply-workbuddy-macos-0.4.0-rc.15.zip', 'sha256': '4df78c8fb7619eb03d5854bd52a6f5070c0789e910ec0a20a4be4b408f471f0d'}, 'workbuddy-windows': {'name': 'boss-apply-workbuddy-windows-0.4.0-rc.15.zip', 'sha256': '4f765a67bfcbfa56e5e60bb2ba8160fe2aa91706ca32059dc63ffd2eb285b6f1'}}
MAX_DOWNLOAD=10*1024*1024
MAX_UNPACKED=30*1024*1024

class HTTPSRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,request,file,code,message,headers,newurl):
        if urllib.parse.urlsplit(newurl).scheme.lower()!='https':raise ValueError('拒绝非HTTPS跳转')
        return super().redirect_request(request,file,code,message,headers,newurl)

def download(client,target):
    item=ARCHIVES[client];expected=item['sha256']
    if len(expected)!=64:raise ValueError('该版本校验未准备好')
    url=REPOSITORY+'/releases/download/'+VERSION+'/'+item['name']
    opener=urllib.request.build_opener(HTTPSRedirect())
    request=urllib.request.Request(url,headers={'User-Agent':'boss-skill-download/1'})
    try: response=opener.open(request,timeout=45)
    except urllib.error.URLError:
        # Some networks cannot reach release URLs; keep the version, asset and hash pinned.
        api='https://api.github.com/repos/chenxinan9/boss-job-apply/releases/'
        with opener.open(urllib.request.Request(api+'tags/'+VERSION,headers={'User-Agent':'boss-skill-download/1'}),timeout=45) as metadata:
            raw=metadata.read(MAX_DOWNLOAD+1)
        if len(raw)>MAX_DOWNLOAD:raise ValueError('发行元数据大小超限')
        release=json.loads(raw)
        assets=release.get('assets',[]) if isinstance(release,dict) else []
        matches=[a for a in assets if isinstance(a,dict) and a.get('name')==item['name']]
        if len(matches)!=1 or type(matches[0].get('id')) is not int or matches[0]['id']<=0:raise ValueError('固定版本缺少唯一同名附件')
        url=api+'assets/'+str(matches[0]['id'])
        response=opener.open(urllib.request.Request(url,headers={'User-Agent':'boss-skill-download/1','Accept':'application/octet-stream'}),timeout=45)
    digest=hashlib.sha256();size=0
    with response,Path(target).open('xb') as out:
        if urllib.parse.urlsplit(response.url).scheme.lower()!='https':raise ValueError('拒绝非HTTPS下载')
        while chunk:=response.read(65536):
            size+=len(chunk)
            if size>MAX_DOWNLOAD:raise ValueError('下载大小超限')
            digest.update(chunk);out.write(chunk)
    if digest.hexdigest()!=expected:raise ValueError('SHA-256不匹配，不解压')
    return {'version':VERSION,'client':client,'url':url,'sha256':expected}

def extract(archive,staging,client):
    package='boss-apply-'+client
    with zipfile.ZipFile(archive) as z:
        infos=z.infolist();seen=set();files=[]
        if len(infos)>1000 or sum(i.file_size for i in infos)>MAX_UNPACKED:raise ValueError('解包大小超限')
        for info in infos:
            # ZipInfo may normalize backslashes on Windows; validate the original member name.
            raw_name=info.orig_filename
            name=raw_name.rstrip('/') if info.is_dir() else raw_name
            parts=name.split('/');path=PurePosixPath(name);key=unicodedata.normalize('NFC',name).casefold()
            kind=stat.S_IFMT(info.external_attr>>16)
            if ('\\' in name or '\x00' in name or path.is_absolute() or any(p in ('','.','..') or ':' in p for p in parts) or parts[0]!=package or key in seen or info.flag_bits&1 or kind not in (0,stat.S_IFREG,stat.S_IFDIR)):
                raise ValueError('压缩包含不安全或重复路径')
            seen.add(key)
            if not info.is_dir():
                if len(parts)<2:raise ValueError('压缩包目录结构错误')
                files.append((info,Path(*parts[1:])))
        names={p.as_posix() for _,p in files}
        if not {'SKILL.md','LICENSE'}<=names:raise ValueError('缺少技能或许可证')
        root=Path(staging)/package;root.mkdir()
        for info,path in files:
            dest=root/path;dest.parent.mkdir(parents=True,exist_ok=True)
            with z.open(info) as src,dest.open('xb') as out:
                remaining=info.file_size
                while chunk:=src.read(min(65536,remaining+1)):
                    remaining-=len(chunk)
                    if remaining<0:raise ValueError('内容超出声明大小')
                    out.write(chunk)
                if remaining:raise ValueError('内容长度不符')
            dest.chmod(0o644)
    return root

def install(client,destination):
    dest=Path(destination).expanduser().absolute()
    if any(p.is_symlink() for p in (dest,*dest.parents)):raise ValueError('目标及父目录不能为符号链接')
    if dest.exists():raise ValueError('已有目录不覆盖：'+str(dest))
    if not dest.parent.is_dir():raise ValueError('请先建立目标父目录')
    with tempfile.TemporaryDirectory(prefix='boss-download-') as t:
        staging=Path(t);archive=staging/'release.zip'
        receipt=download(client,archive);root=extract(archive,staging,client)
        shutil.copytree(root,dest)
    receipt['scope']='downloaded workspace only; no private data, client registration, schedule or BOSS action'
    (dest/'INSTALLATION.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n', encoding='utf-8', newline='\n')
    return receipt

def main():
    # PowerShell pipes may default to a legacy code page even when files are UTF-8.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="backslashreplace")
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--client',required=True,choices=tuple(ARCHIVES))
    parser.add_argument('--destination',type=Path)
    parser.add_argument('--candidate',action='store_true',help='明确下载未验收候选，仅供本人授权的独立实站测试')
    args=parser.parse_args();dest=args.destination or Path.cwd()/('boss-apply-'+args.client)
    if not RELEASE_AVAILABLE and not args.candidate: parser.exit(1,'当前没有通过独立实站验收的公开安装包，下载已暂停；请勿使用旧包。\n')
    if args.candidate: print('未验收候选：下载不代表投递通过；不覆盖生产或私人资料。')
    try:receipt=install(args.client,dest)
    except (ValueError,OSError,RuntimeError,zipfile.BadZipFile) as e:parser.exit(1,'下载未完成：'+str(e)+'\n')
    print('已校验并下载 '+VERSION+'：'+str(dest.absolute()))
    print('SHA-256：'+receipt['sha256'])
    print('请在对应客户端打开此目录并读取SKILL.md；本人条件与简历未提供前不得投递。')
    print('仅下载工作区；未注册技能、设置定时、连接浏览器或发送。')

if __name__=='__main__':main()
