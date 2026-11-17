# Challenge 4 — Chasing Shadows

## Player Write-up and Intended Solve Path

**Points:** 150  
**Category:** OSINT / Investigation  
**Flag:** `d4rk{2_3_8_7_11_16_17_23_19_13}`

### Step 1 — Follow the clue from Challenge 3

The previous challenge gives us the flag:

`d4rk{fediverse}`

The important part is the word **Fediverse**. It refers to a network of interconnected social platforms. Researching the term leads to platforms such as **Mastodon**.

This is the first lead in the investigation.

### Step 2 — Locate Arjun Mehra's Mastodon account

Using the context provided in the challenge description and the conversation between DCP Kabir Sharma and Agent Arjun Mehra, investigate Arjun's online presence.

The search leads to the Mastodon account:

`amehraCC704`

Once you locate the profile, examine its information and posts carefully. Do not limit your investigation to the content currently visible on the profile. Earlier versions of online content can sometimes reveal information that is no longer publicly displayed.

### Step 3 — Recover the GitHub link

The Mastodon content has been edited, and the current version no longer displays the GitHub link.

To recover the original information:

1. Locate the relevant edited post on Arjun's Mastodon account.
2. Open the post's edit history.
3. Compare the available versions of the post.
4. Inspect the earlier version and look for the GitHub link.
5. Open the recovered link.

The important detail is that the information was not necessarily deleted from every historical version. Examining the edit history can reveal content that is absent from the current post.

### Step 4 — Explore the GitHub account

The recovered link leads to ECHO's GitHub account.

Explore the account and locate the repository associated with the NovaVault incident.

Do not rely exclusively on the latest version of the repository. The repository's history is an important part of the investigation, and some relevant information may only be visible in earlier versions.

### Step 5 — Investigate the commit history

Open the repository's commit history and examine how its Python scripts changed over time.

Pay attention to the following:

- **Repository files:** Read the Python scripts and understand what they do.
- **Commit history:** Examine the sequence of changes made to the repository.
- **Commit diffs:** Compare file versions to identify what was added, removed, or modified.
- **Commit authors:** Check who is associated with each change.

You should inspect individual file versions at specific commits rather than looking only at the current source code.

The historical changes contain information that may no longer be visible in the latest version.

### Step 6 — Recover the numeric fragments

The Python scripts change across multiple commits. There are two useful ways to investigate them:

1. **Execute the scripts:** Understand their expected inputs, run them, and observe their outputs.
2. **Analyse the source code:** Trace the transformations and validation logic to determine how the outputs are generated.

By examining the relevant versions, you can recover a sequence of numeric fragments.

Record each fragment alongside the commit from which it was obtained. The order matters: collecting all the numbers is not enough if they are assembled incorrectly.

The sixth commit also provides the required flag format. Use that information together with the recovered fragments to construct the final flag.

### Step 7 — Submit the flag

Combining the fragments in the correct order gives:

`d4rk{2_3_8_7_11_16_17_23_19_13}`

<badge color="success">Flag recovered</badge>

## Key Takeaways

- A word recovered from one challenge can become the starting point for an OSINT investigation.
- Social media edit histories can preserve information that is no longer visible in the current version of a post.
- GitHub repositories contain more than their latest source code; commit history and diffs can reveal important historical information.
- Running a script and understanding its source code are complementary approaches to reverse-engineering its behaviour.
- Commit authorship and the sequence of changes can provide useful investigative context beyond the code itself.
