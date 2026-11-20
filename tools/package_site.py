#!/usr/bin/env python3
"""Package committed public assets only; never uploads or modifies the checkout."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import subprocess
import tempfile
import zipfile

ROOTS = ('www', 'www-oleksii')
EXTENSIONS = {'.html', '.css', '.js', '.json', '.xml', '.svg', '.png', '.jpg',
              '.jpeg', '.gif', '.webp', '.avif', '.ico', '.mp4', '.webm', '.pdf',
              '.pptx', '.php', '.woff', '.woff2', '.ttf', '.eot'}
EXCLUDED = {'.md', '.markdown', '.log', '.sketch', '.py', '.sh', '.bat', '.ps1',
            '.bak', '.tmp', '.pem', '.key', '.zip', '.tar', '.gz'}


def eligible(name):
    path = PurePosixPath(name)
    if path.parts[0] not in ROOTS or '..' in path.parts:
        raise ValueError('Unexpected path: ' + name)
    if any(p.startswith('.') or p in ('node_modules', '__pycache__') for p in path.parts):
        return False
    if path.suffix.lower() in EXCLUDED:
        return False
    if path.suffix.lower() in EXTENSIONS or name in ('www/robots.txt', 'www-oleksii/robots.txt'):
        return True
    raise ValueError('Unreviewed file type; review before extending the allowlist: ' + name)


def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ref', required=True, help='Reviewed commit or ref; resolved to a full SHA')
    parser.add_argument('--output', required=True, type=Path, help='New local directory outside the checkout')
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[1]
    commit = git(repo, 'rev-parse', '--verify', args.ref + '^{commit}').decode().strip()
    output = args.output.expanduser().resolve()
    if output == repo or repo in output.parents:
        parser.error('Keep packages outside the repository.')
    if output.exists():
        parser.error('Output directory already exists; use a new path.')
    files, excluded = [], []
    for record in git(repo, 'ls-tree', '-rz', commit, '--', *ROOTS).split(b'\0'):
        if not record:
            continue
        meta, raw_name = record.split(b'\t', 1)
        mode, kind, oid = meta.decode().split()
        name = raw_name.decode('utf-8')
        if mode not in ('100644', '100755') or kind != 'blob':
            raise ValueError('Links and submodules cannot be deployed: ' + name)
        if eligible(name):
            files.append((name, oid))
        else:
            excluded.append(name)
    names = {name for name, _ in files}
    for root in ROOTS:
        for page in ('index.html', 'uk/index.html'):
            if root + '/' + page not in names:
                raise ValueError('Missing language homepage: ' + root + '/' + page)
    # Build privately; publish the completed local directory only after validation.
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=output.parent, prefix='.site-package-') as temp:
        staging = Path(temp)
        archive = staging / 'site.zip'
        manifest = {'commit': commit, 'excluded': excluded, 'files': []}
        with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED) as z:
            for name, oid in files:
                data = git(repo, 'cat-file', 'blob', oid)
                info = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
                info.create_system = 3
                info.external_attr = 0o100644 << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                z.writestr(info, data)
                manifest['files'].append({'path': name, 'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)})
        with zipfile.ZipFile(archive) as z:
            if z.namelist() != [entry['path'] for entry in manifest['files']]:
                raise ValueError('Archive contents mismatch')
            for entry in manifest['files']:
                if hashlib.sha256(z.read(entry['path'])).hexdigest() != entry['sha256']:
                    raise ValueError('Archive verification failed: ' + entry['path'])
        manifest['archive_sha256'] = hashlib.sha256(archive.read_bytes()).hexdigest()
        (staging / 'manifest.local.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
        staging.rename(output)
    print('Verified commit:', commit)
    print('Website files:', len(files), '| Excluded:', len(excluded))
    print('Package:', output / 'site.zip')
    print('Local-only verification record:', output / 'manifest.local.json')
    print('Nothing uploaded. Transfer only the site.zip payload after deployment approval.')


if __name__ == '__main__':
    main()
