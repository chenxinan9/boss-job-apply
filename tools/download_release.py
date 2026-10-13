#!/usr/bin/env python3
"""Download and verify an independent skill workspace; never run BOSS or register a task."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import shutil
import stat
import tempfile
import unicodedata
import urllib.parse
import urllib.request
import zipfile

VERSION='v0.1.2'
REPOSITORY='https://github.com/chenxinan9/boss-job-apply'
ARCHIVES={'codex': {'name': 'boss-apply-codex-0.1.2.zip', 'sha256': '06870bc3503a52d033c72105272b5820ee67bad23e66009c20782dedcb0b8d2b'}, 'workbuddy': {'name': 'boss-apply-workbuddy-0.1.2.zip', 'sha256': 'cf5e4d44e250e2fc94bf927f77677c67f5c0f2bf3c63d945f06203dac408a4fa'}}
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
    digest=hashlib.sha256();size=0
    with opener.open(request,timeout=45) as response,Path(target).open('xb') as out:
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
            name=info.filename.rstrip('/') if info.is_dir() else info.filename
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
    (dest/'INSTALLATION.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
    return receipt

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--client',required=True,choices=tuple(ARCHIVES))
    parser.add_argument('--destination',type=Path)
    args=parser.parse_args();dest=args.destination or Path.cwd()/('boss-apply-'+args.client)
    try:receipt=install(args.client,dest)
    except (ValueError,OSError,RuntimeError,zipfile.BadZipFile) as e:parser.exit(1,'下载未完成：'+str(e)+'\n')
    print('已校验并下载 '+VERSION+'：'+str(dest.absolute()))
    print('SHA-256：'+receipt['sha256'])
    print('请在对应客户端打开此目录并读取SKILL.md；本人条件与简历未提供前不得投递。')
    print('仅下载工作区；未注册技能、设置定时、连接浏览器或发送。')

if __name__=='__main__':main()
