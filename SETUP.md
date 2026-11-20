# tsesliuk.com — restore on another computer

Portfolio and personal profile: two static websites in one repository.

Reviewed against local project files on 2026-10-01. This is a procedure, not a claim that a fresh Windows/Mac environment has already been tested.

## Destination and source

- macOS: `~/DevProjects/tsesliuk.com`.
- Windows: `%USERPROFILE%\DevProjects\tsesliuk.com`.
- Use the same project folder name on new devices. The home directory expands for the actual user; do not copy `/Users/SUTE` to another account or assume `C:\Users\Admin`.
- Existing Mac checkout: `/Users/SUTE/DevProjects/tsesliuk.com`. Reuse it; do not create a second checkout or rename it automatically.
- Working branch at this handoff: `master`. Verify remote refs before checkout; stop with the actual missing ref if unavailable rather than substituting an unrelated branch.

## Restore source

First check whether the destination already exists. If it does, verify `git rev-parse --show-toplevel`, remote, branch and `git status --short --branch`. Do not clone over it or reset it. Fetch is read-only with respect to the working tree; only fast-forward a clean intended branch, and preserve any local divergence.

Source: `https://github.com/tsesliuk/tsesliuk.com.git`. Authenticate the authorized GitHub/GitLab account on this device; use the OS credential helper, not embedded tokens in URLs. For GitHub, an installed `gh` can use `gh auth login` and `gh auth setup-git`; do not print its token. Complete interactive login only if needed.

For a **new** checkout after verifying Git and access:

macOS:
```sh
mkdir -p "$HOME/DevProjects"
cd "$HOME/DevProjects"
git clone --branch "master" "https://github.com/tsesliuk/tsesliuk.com.git" "tsesliuk.com"
cd "tsesliuk.com"
```

Windows PowerShell:
```powershell
$projectsRoot = Join-Path $env:USERPROFILE 'DevProjects'
New-Item -ItemType Directory -Force -Path $projectsRoot | Out-Null
Set-Location $projectsRoot
git clone --branch "master" "https://github.com/tsesliuk/tsesliuk.com.git" "tsesliuk.com"
if ($LASTEXITCODE -ne 0) { throw 'Clone failed; check access and branch.' }
Set-Location "tsesliuk.com"
```

## Dependencies, access and operating-system limits

No package installation or build is needed for the HTML sites. www serves tsesliuk.com; www-oleksii serves oleksii.tsesliuk.com. Use Python’s HTTP server for preview; PHP includes, if touched, require a PHP-capable server and are not executed by the static preview. EN pages are at each root, UA under uk/. _gen_thumbs.py generates tile SVGs and should not be run merely to restore the checkout.


### Preview

Use separate terminals from this checkout:
```sh
python3 -m http.server 8000 --bind 127.0.0.1 --directory www
python3 -m http.server 8001 --bind 127.0.0.1 --directory www-oleksii
```
On Windows replace python3 with py. Open http://127.0.0.1:8000 and http://127.0.0.1:8001; check EN/UA, navigation, media and mobile layouts.

## Publish website assets only

Updated 2026-11-20: documentation and agent instructions stay in Git for development computers, but must not be uploaded to hosting. No server-side Git clone, pull or fetch. GitHub push and hosting deployment are separate actions, each requiring explicit approval.

The packaging tool needs Python 3.8+ and Git locally, with no extra packages. It reads an explicit committed version; local edits and untracked files are never included. Review the intended commit first. From the checkout, use a new output folder **outside** the repository:

macOS:
```sh
python3 tools/package_site.py --ref <reviewed-commit-SHA> --output /tmp/tsesliuk-release-<short-SHA>
```

Windows PowerShell:
```powershell
py tools/package_site.py --ref <reviewed-commit-SHA> --output "$env:TEMP/tsesliuk-release-<short-SHA>"
```

Replace the placeholders before running. The output is `site.zip` containing only the two website roots, and `manifest.local.json` recording the full commit, file hashes and exclusions. Keep the manifest locally; it is not a website asset. The builder verifies archived bytes, excludes Markdown, hidden/development files, logs and design source files, and stops on unreviewed file types or links. Existing linked PDF/PPTX downloads remain website assets. Extension checks do not replace reviewing the contents for secrets or private data. Future server configuration such as `.htaccess` requires an explicitly reviewed exception; hidden files are currently excluded.

After approval, transfer only the archive payload over the authenticated hosting connection. Extract into an asset-only staging directory outside public roots, confirm the two expected site folders and their hashes, then update the intended site roots. Do not extract an entire repository, overwrite unreviewed server files or use blind deletion/synchronization. Remove the uploaded archive and temporary staging after successful deployment. Check EN/UA pages, navigation, downloads, and deployed hashes. Packaging alone does not publish anything.

### One-time migration from legacy hosting

On 2026-11-20 the existing ukraine.com.ua setup was verified to use one full server checkout, with both public roots linked to its `www/` and `www-oleksii/` folders. That legacy arrangement still contains repository documentation outside the public roots. A new package alone does not remove it.

Before changing hosting, record actual paths and link targets again, compare live files to the approved package, inventory any server-only configuration or runtime data without exposing secrets, and prepare a recoverable backup outside the hosting account. Prepare the asset-only replacement and check it before switching either public root. Obtain explicit approval for the concrete migration, link changes and removal of the legacy checkout, Git history and service files. Preserve any required runtime configuration. Verify both domains after the switch and retain rollback material locally, not as another repository copy on hosting. Report disk cleanup and public reachability separately. Do not claim the migration is done until the actual hosting filesystem is checked.


## Known source handoff gap (2026-10-01)

The original Mac has many unpublished HTML/CSS/JS/SVG changes and untracked site assets, including work under www/works/tveyes/. The two website roots and preview instructions describe the current Mac layout; compare the fetched source before assuming those latest pages/assets are available. This cleanup committed documentation only.

These code changes require their own review, commit and approved push before full cross-device parity can be claimed. They were preserved, not changed by the instruction cleanup.

## Completion criteria and handoff

1. Confirm the intended source/branch and actual destination, then read AGENTS.md.
2. Check required runtime, dependencies and separate service access without printing secrets.
3. Run the applicable checks and local preview above. For document-only projects, verify files open and the expected workbooks/documents exist.
4. Report separately: source restored; environment ready; checks passed/failed; live service access confirmed/missing. Do not equate any one with full readiness.
5. Record branch, SHA, local modifications, checks, exact remaining blocker and next action. If files/commits are still local, another device cannot obtain them from the remote.

Every push and every deployment requires the user’s explicit approval for the concrete repository, branch/tag, commit and target. Installing this project is not permission to submit worklogs, write to Miro/calendars, publish a site or submit a paper.
