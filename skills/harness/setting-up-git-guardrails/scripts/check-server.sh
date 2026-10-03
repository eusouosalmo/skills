#!/usr/bin/env bash
# Reports whether the default branch of the current GitHub repo is protected on the
# server: pull request required, force push blocked, deletion blocked. Reads only;
# it never changes a setting. Looks at both rulesets and classic branch protection.
#
# Usage: check-server.sh   (from inside the repo)
# Exit 0: everything protected. 1: something missing. 3: could not check.
# Needs: gh (authenticated), jq.

set -u

for dep in gh jq; do
  command -v "$dep" >/dev/null 2>&1 || { echo "check-server: $dep is required" >&2; exit 3; }
done

info=$(gh repo view --json nameWithOwner,defaultBranchRef 2>/dev/null) ||
  { echo "check-server: could not read the GitHub repo (no GitHub remote, or gh not logged in)" >&2; exit 3; }
REPO=$(jq -r .nameWithOwner <<<"$info")
BRANCH=$(jq -r .defaultBranchRef.name <<<"$info")

pr=0 force=0 del=0 classic="none"

# Rulesets that apply to the branch.
if rules=$(gh api "repos/$REPO/rules/branches/$BRANCH" 2>/dev/null); then
  jq -e 'any(.[]; .type == "pull_request")' <<<"$rules" >/dev/null && pr=1
  jq -e 'any(.[]; .type == "non_fast_forward")' <<<"$rules" >/dev/null && force=1
  jq -e 'any(.[]; .type == "deletion")' <<<"$rules" >/dev/null && del=1
fi

# Classic branch protection. 404 means none; 403 means no permission to read it.
if prot=$(gh api "repos/$REPO/branches/$BRANCH/protection" 2>&1); then
  classic="present"
  jq -e '.required_pull_request_reviews != null' <<<"$prot" >/dev/null && pr=1
  jq -e '(.allow_force_pushes.enabled // false) == false' <<<"$prot" >/dev/null && force=1
  jq -e '(.allow_deletions.enabled // false) == false' <<<"$prot" >/dev/null && del=1
elif [[ $prot == *"HTTP 403"* ]]; then
  classic="unreadable (needs admin access)"
fi

say() { if (($1)); then echo "  ok       $2"; else echo "  MISSING  $2"; fi; }
echo "Server protection for $REPO, branch $BRANCH (classic protection: $classic):"
say $pr "pull request required before merging"
say $force "force push blocked"
say $del "branch deletion blocked"

if ((pr && force && del)); then
  exit 0
fi
echo "Recommendation: add a ruleset on $BRANCH with 'Require a pull request before merging',"
echo "'Block force pushes' and 'Restrict deletions' (Settings > Rules > Rulesets)."
echo "The local hook only stops a distracted agent; this is the barrier that holds."
exit 1
