# Removing the organisation name from past commits (owner action)

The current files no longer carry the real organisation's name in plain text: it lives base64-encoded in
`scripts/blocked-text.b64`, and `scripts/qa/claims_lint.py` fails if it comes back. Past commits on `main` still
contain it (older versions of `scripts/sync-agentic.sh`, `scripts/agentic-neutral.mjs`, `scripts/qa/` and the
`agentic/` pages). The owner chose on 2026-11-18 to leave history as it is for now. If that changes, these are the
steps. They rewrite every commit hash, so every clone, fork and open branch must be re-cloned afterwards, and
GitHub may keep old commits reachable through cached views and pull requests until GitHub Support removes them.

1. Merge or close every open pull request first; their branches will no longer apply.
2. In a fresh mirror clone:
   ```bash
   git clone --mirror https://github.com/Tamoura/system-design-for-vibe-coders.git
   cd system-design-for-vibe-coders.git
   python3 ../system-design-for-vibe-coders/scripts/blocked_text.py --show   # from a normal checkout
   ```
   Write a `replacements.txt` for `git filter-repo --replace-text` with one line per form of the name shown by
   `--show` (the regex in `name_regex` and the strings in `blocked`), each mapped to a neutral word, for example
   `literal:<the name>==>the organisation`. Keep that file outside the repository.
3. `git filter-repo --replace-text ../replacements.txt` (install with `pip install git-filter-repo`).
4. Check: `git log --all -p | grep -c -i -E '<the forms>'` returns 0.
5. `git push --force --mirror` (needs branch protection on `main` lifted for the push, then restored).
6. Ask GitHub Support to purge cached views and dangling commits; tell anyone with a clone to re-clone.
