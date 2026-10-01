# tsesliuk.com — agent instructions

Portfolio and personal profile: two static websites in one repository.

## Working rules

Read SETUP.md for device restoration. These instructions are self-contained; access to another computer’s private index is not required.

- Identify OS, real checkout, branch, HEAD, upstream, dirty/staged files, runtime and access before changing anything. Do not treat a failed/timed-out Git command as a clean tree.
- Preserve unrelated changes. Stage only files belonging to the assigned task. Verify Git author identity and the staged diff before a local commit. Do not silently replace an existing author identity.
- Local edits, checks and commits are autonomous within an assigned task. **Every push and every deployment requires explicit user approval for that concrete action.** Show repository, branch/tag, commit(s), target and any auto-deploy consequences. Existing approval applies only to its agreed scope.
- Do not reset, force-push, delete work, retag releases or run data-changing setup steps without the corresponding authorization. Preserve team review requirements.
- Credentials, private keys, environment values, local sessions and production data are provisioned per device, never copied into Git or chat. Git access alone does not establish backend or deployment access.
- Communicate in Ukrainian by default; concise, result first. Ask when missing information materially changes the outcome; continue independent work. English explanations should be clear at B2 level.
- New public contact: email@tsesliuk.com. Do not silently change account logins or historical Git authors.
- At handoff report branch/SHA, checks, remaining local changes, access blockers, and whether push/deploy actually completed. Do not promise another device can see an unpushed commit.

## Project-specific rules

This repository is public. Do not add private indexes, corporate access routes, client research, credentials or personal configuration. Preserve both site roots, language parity and existing page-specific styling. Review client-named cases before publishing.
