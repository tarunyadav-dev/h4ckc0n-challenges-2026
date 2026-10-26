# Challenge 4 — Chasing Shadows

## Creator's Write-up and Intended Solve Path

**Purpose:** This document describes the intended solution path from Challenge 3 to ECHO's GitHub account. It is for the challenge creator and organisers, not the public challenge description.

## Step 1 — Interpret the flag from Challenge 3

Players recover:

`d4rk{fediverse}`

The key word is `fediverse`. Rather than treating it as another password, players should research its meaning and identify social networking platforms built around the fediverse.

This should lead them to **Mastodon**, a decentralised social networking platform.

The challenge does not explicitly name Mastodon. Players must interpret the recovered word and research its relevance.

## Step 2 — Find Arjun Mehra's Mastodon account

The Challenge 4 description and the conversation between DCP Kabir Sharma and Agent Arjun Mehra encourage players to investigate Arjun's online identity.

Players should search for his social media presence and identify the fictional Mastodon account:

`amehraCC704`

Once they locate the profile, they should examine its posts and profile information. The objective is to investigate the account's history, not merely read its current content.

## Step 3 — Recover the edited profile information

The Mastodon profile was edited, and the current version no longer displays the GitHub link.

There are two possible approaches to recovering the previous information.

### Intended route: Mastodon's edit history

1. Locate the relevant edited post or profile-related message on Arjun's Mastodon account.
2. Open the post's edit history, using Mastodon's **edited-post history** feature where available.
3. Inspect the earlier version of the content.
4. Locate the GitHub account link that was present before the edit.
5. Follow the link to continue the investigation.

This is the intended route because it is more direct and does not depend on an external archival service. Players should be able to recover the information from the post's own history.

**Creator's testing note:** Ensure that the relevant content is actually an edited Mastodon post with accessible version history. If the GitHub link was removed only from the profile's bio, do not assume Mastodon exposes the bio's previous versions through the same feature. Place the link in an edited post if necessary, and test the exact interaction on the account used for the challenge.

### Alternative route: Wayback Machine

If the edit history is unavailable or does not expose the required information, players may use the Internet Archive.

1. Copy the relevant Mastodon post or profile URL.
2. Visit [web.archive.org](https://web.archive.org/).
3. Search for the URL and inspect available snapshots from before the content was edited.
4. Open an older snapshot and look for the GitHub link.
5. Follow the link to continue the investigation.

Mastodon pages may not render completely in archived snapshots because of their dynamic content. If a snapshot appears incomplete, inspect other available captures and the archived page's visible links.

The Wayback Machine is a fallback method, not the primary intended solution.

## Step 4 — Find ECHO's GitHub account

The recovered link leads to ECHO's GitHub account.

Players should investigate the account and identify the repository associated with the NovaVault incident.

**Intended repository:** `-`

The repository should contain the Python scripts used in the challenge. Its commit history is an important part of the evidence.

## Step 5 — Investigate the repository history

Players should examine more than the latest version of the repository.

The intended investigation involves four areas:

- **Repository files:** Read the Python scripts and understand their inputs, transformations, and outputs.
- **Commit history:** Open the commit list and inspect how the scripts changed over time.
- **Commit diffs:** Compare versions to identify data or logic introduced, removed, or modified in each commit.
- **Commit authors:** Inspect the author associated with each change. Pay attention to any commit that does not follow the established pattern.

Players should open individual file versions at specific commits instead of relying only on the latest source code.

The historical versions contain information that cannot necessarily be recovered by examining the final version alone.

## Step 6 — Recover the numeric fragments

The Python scripts change across the repository's commit history. Players can investigate them in either of two ways:

1. **Execute the scripts:** Determine the required input, run the program, and observe the output.
2. **Analyse the source code:** Trace the transformations and validation logic to understand how the program produces its output.

The intended result is a sequence of numeric fragments revealed across different commits.

Players should record each fragment alongside its corresponding commit and preserve the order in which the evidence indicates they belong.

The sixth commit reveals the required flag format. Players must combine this information with the recovered fragments to construct the final result.

**Important:** The ordering of the numbers matters. Recovering every fragment is not sufficient if the sequence is reconstructed incorrectly.

## Creator-only connection to Challenge 6

Do not explain the significance of the unusual commit author in the public-facing challenge description.

The author change is a piece of evidence that players can notice while examining the repository. Its significance should become clearer during the final challenge, when players revisit earlier evidence and question their original conclusions.

Challenge 4 should make the repository discoverable without directly explaining the identity behind the unusual commit.

## Final intended solve path

1. **Challenge 3:** Recover `d4rk{fediverse}`.
2. **Research:** Connect the fediverse to Mastodon.
3. **OSINT:** Locate Arjun Mehra's Mastodon account.
4. **Historical evidence:** Inspect the edited post's history and recover the GitHub link.
5. **Repository investigation:** Examine Python scripts, commit versions, diffs, and authors.
6. **Fragment recovery:** Extract the numeric fragments and preserve their order.
7. **Challenge 5:** Use the recovered information to proceed through the web challenge.
8. **Challenge 6:** Revisit the evidence and reconstruct the final flag.

flag : d4rk{2_3_8_7_11_16_17_23_19_13}
