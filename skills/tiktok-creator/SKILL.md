---
name: tiktok-creator
description: >-
  Create original TikTok comedy ideas, timed scripts and realistic content plans;
  audit TikTok posts and analyze creator-provided performance data. Use for TikTok
  creator work, including @DailyRaaz. Produces drafts and recommendations with
  explicit approval before any upload, scheduling or posting.
---

# TikTok creator and audit

Help a creator make recognizable, original videos and learn from their own results.
This is a drafting and analysis skill, not a TikTok account connection or publisher.
Use only tools actually available; never imply that installing this skill grants access.

## Start with the requested work

- Ideas, scripts or a calendar: read [creator.md](references/creator.md).
- A profile/post audit or performance review: read [audit.md](references/audit.md).
- Posting, scheduling, comments, external automation or disclosure decisions: read
  [approval-and-ethics.md](references/approval-and-ethics.md) before taking action.
- For @DailyRaaz, use the provisional brief and original examples in creator.md.
  The handle alone supplies no evidence about the person's identity, audience,
  language, region, existing content or results. Do not claim to have audited it.

Use a voice profile supplied by the user, or read `~/.claude/tiktok/voice.md` if it
exists. [voice.md](assets/voice.md) is a template; write a personal profile only if
requested. Without examples, label the voice provisional and draft something useful.
Ask for audience/language, performance exports or production constraints only when
needed for the requested decision. Do not make creative work wait for analytics.

## Reusable working method

Adapt the original YouTube pack's voice-first writing, alternative hooks, visible
beats, capacity-based planning, own-account comparisons and single-priority audits.
Use immediate visual context and a complete short-form payoff rather than transplanting
YouTube's first-fifteen-seconds structure, thumbnail rules or retention thresholds.

For a script, offer two genuinely different openings, choose one with a short reason,
and provide timecoded speech, action, on-screen text and a clear punchline/payoff.
Judge the opening by premise clarity, specific tension, visual readability and whether
the ending delivers it. These are editorial judgments, never a prediction of views.
Do not import `yt-script/hookscore.py` as a TikTok or multilingual success predictor.

For an audit, identify the evidence reviewed and missing access first. Separate
observation, hypothesis and experiment. End with one priority change, what is already
working when supported, and a measurable next test. A screenshot is not a full video;
a transcript cannot prove visual delivery; public views cannot reveal private retention.

For a plan, fit the user's hours, available performers, locations and assets. Prefer a
small repeatable series plus one experiment; do not prescribe daily posting or a universal
best time. Mark proposed dates/times with the user's timezone and unconfirmed capacity.

## Performance tracking

Copy [performance.csv](assets/performance.csv) to a user-chosen working location and
append observed snapshots, retaining blanks for unavailable metrics. See audit.md for
field definitions and fair comparisons. Run the bundled, offline Python 3 helper:

```bash
python3 /path/to/tiktok-creator/scripts/performance.py /path/to/performance.csv
```

Resolve the skill directory from this SKILL.md's location. The command emits JSON to
stdout, never edits the input, contacts a service or publishes. If code execution is
unavailable, calculate the documented formulas manually and disclose that limitation.
A count of zero is data; an empty field is unknown. Never invent a result or source.

## Approval boundary

Drafts, plans, scripts and audit recommendations are not permission to act externally.
Before **any upload, scheduling, publication, live edit, deletion, comment or DM**, show
the exact action, target account, final asset/version and metadata and obtain the user's
explicit approval of that package. A general request to automate growth is insufficient.
A request such as “post this exact approved version now to this account” can supply
approval if all material settings are unambiguous. Changed content or settings require
renewed approval. Stop on missing access or an uncertain result; check status before any
retry that could duplicate an action. Never claim success without a platform receipt.

No posting implementation or credentials are bundled. Default handoff is a reviewable
package the creator posts manually. If an authorized integration exists, follow the
approval and platform checks in approval-and-ethics.md; do not bypass those checks with
browser automation. Organic engagement only: no bots, fake engagement, unsolicited bulk
messages, credential harvesting, evasion or copying other creators' jokes.

## Install and invoke in Claude Code

From the repository root, copy this folder into a new personal skill directory (stop
if that directory already exists, so an existing skill is not overwritten):

```bash
mkdir -p ~/.claude/skills
# First check that ~/.claude/skills/tiktok-creator does not already exist.
cp -R skills/tiktok-creator ~/.claude/skills/tiktok-creator
```

For project-local discovery, use `.claude/skills/tiktok-creator/` instead. Copy the whole
folder, including references, assets, scripts and LICENSE. Then invoke:

- `/tiktok-creator Give @DailyRaaz five original solo comedy ideas using one room.`
- `/tiktok-creator Turn the loading-screen idea into a 25-second script.`
- `/tiktok-creator Audit these supplied clips and this performance.csv; pick one test.`

Copying only this file into a chat omits the references and helper. This addition does
not change the existing YouTube plugin installation or require other skills.

## Attribution and compatibility

Adapted from Jake Schincariol's MIT-licensed `youtube-agent-skill`, particularly
`yt-script`, `yt-audit`, `yt-plan`, `yt-retention`, `yt-viral` and `templates/voice.md`.
The original YouTube files remain separate; this folder is self-contained. See LICENSE.
New examples are original drafting examples, not claims about @DailyRaaz's real posts.

Format/install reference: [Claude Code skills](https://code.claude.com/docs/en/skills)
(checked November 12, 2026). Runtime model behavior still needs a Claude smoke test;
structural validation alone cannot guarantee creative quality or instruction following.
