# Challenge 6 — WHOAMI

## Player Write-up and Intended Solve Path

**Category:** OSINT / Meta Investigation  
**Flag:** `d4rk{AUTHOR_Tarun_Yadav_is_the_hacker_you_are_looking_for_what_you_guessed}`

This is the final challenge of **The Mirror Investigation**.

Unlike the previous stages, the answer is not hidden in another fictional identity, a server, or a conventional evidence file. The investigation eventually crosses the boundary between the story and the real world.

The objective is to collect three fragments from earlier challenges, recognise what they imply, and identify the person behind the challenge itself.

The central question is simple:

**Who is ECHO?**

---

## Step 1 — Collect Fragment 1 from Digital Footprints

Return to **Challenge 2 — Digital Footprints** and look carefully at the NovaVault terminal.

When connecting to the terminal, you may have noticed that the command prompt does not begin with the expected application name. Instead, it repeatedly displays:

```text
NHGUBE:NovaVault>
```

It is easy to dismiss this as a default prompt or an arbitrary label. However, the unusual prefix is deliberate.

The important fragment is:

```text
NHGUBE
```

### Decode it with ROT13

Use any ROT13 decoder, such as CyberChef:

1. Open CyberChef.
2. Paste `NHGUBE` into the input panel.
3. Add the **ROT13** operation.
4. Read the output.

Alternatively, use Python:

```python
import codecs

print(codecs.decode("NHGUBE", "rot_13"))
```

The output is:

```text
AUTHOR
```

This is **Fragment 1**.

The clue was visible throughout the terminal session. It was not hidden in a complicated record or behind a difficult exploit. The challenge tests whether you pay attention to details that appear so routinely that you stop questioning them.

A prompt is part of the interface, but that does not mean it is meaningless.

---

## Step 2 — Collect Fragment 2 from Chasing Shadows

Now return to **Challenge 4 — Chasing Shadows**.

During that challenge, you discovered ECHO's GitHub account and investigated its repository. You examined the Python scripts, commit history, file changes, and commit authors to recover the numeric fragments.

This time, revisit the repository with a different question in mind:

**Does every commit really belong to the identity you think is behind this account?**

### Inspect the commit history again

1. Open the ECHO GitHub account discovered in Challenge 4.
2. Open the repository you investigated earlier.
3. Above the file list, select the commit-history link (usually displayed as the number of commits).
4. Browse the commit list and inspect the author associated with each commit.
5. Look for the commit attributed to **Tarun Yadav**.
6. Open that commit and read its commit message.

One commit is attributed to the author of this challenge: Tarun Yadav.

That is unusual. Until this point, the investigation has presented ECHO as an entity operating inside the fictional NovaVault storyline. Why, then, does a commit in ECHO's repository carry the name of the person who created the challenge?

The commit message makes the clue more direct:

> I forget to add this one

Pay attention to the first-person wording. The message no longer sounds like an operational note from an anonymous fictional hacker. It reads like a remark from the person constructing the challenge.

This is the second break in the boundary between the fictional investigation and its creator.

The commit is not simply another code change to analyse. Its author and wording are themselves evidence.

**Fragment 2 points you towards the person who created the investigation.**

---

## Step 3 — Follow the real-world social trail

The description of the final challenge asks you to reconsider who ECHO might be and to investigate the identity behind the account.

At this stage, stop treating ECHO as only a fictional character.

You already have two clues:

- The first fragment explicitly decodes to `AUTHOR`.
- The second reveals the challenge creator's name in ECHO's GitHub commit history.

The next step is to connect that identity to the real-world social accounts associated with the event.

### Start with the D4rkC0de club

The event is hosted by **D4rkC0de**, the cybersecurity club of IIIT Delhi.

If you want to reach the person behind the challenge, investigate the club's social-media connections.

1. Find the official D4rkC0de social-media account.
2. Open its **Following** list.
3. Examine the accounts connected to the club.
4. Look for the account associated with the name discovered in the GitHub commit.

The clue is not asking you to search randomly across the entire internet. It asks you to use the social connections of the event organiser to narrow down the identity.

### Identify the Instagram account

The social-media trail leads to Instagram.

Search for:

```text
with_tarunyadav
```

Open the profile and inspect its posts. Do not stop at the profile name or biography. The first post contains the final fragment and explains how the flag should be assembled.

The final fragment is:

```text
Tarun_Yadav_is_the_hacker_you_are_looking_for_what_you_guessed
```

Read the post carefully and preserve the wording and order.

This gives you the final piece needed to complete the investigation.

---

## Step 4 — Combine the three fragments

At this point, the clues connect:

| Source | Finding | Meaning |
|---|---|---|
| Challenge 2 — Digital Footprints | `NHGUBE` → ROT13 → `AUTHOR` | Look for the author |
| Challenge 4 — Chasing Shadows | Tarun Yadav appears as a GitHub commit author; the message uses first-person wording | The fictional trail points outside the story |
| D4rkC0de social connections and Instagram | `with_tarunyadav` and the first post | Identifies the person and provides the final wording |

The three fragments are not independent passwords. They form a sequence of increasingly direct hints:

1. **AUTHOR** tells you what kind of identity to search for.
2. The GitHub commit gives you the author's name and breaks the fictional voice.
3. The social-media trail connects that name to the real-world account and supplies the final flag wording.

The answer is no longer another character hidden inside NovaVault.

The person you are looking for is the author of the challenge.

---

## Step 5 — Understand the final reveal

The final flag is:

```text
d4rk{AUTHOR_Tarun_Yadav_is_the_hacker_you_are_looking_for_what_you_guessed}
```

The reveal changes how the entire investigation should be understood.

Throughout the earlier challenges, the evidence encouraged you to follow a trail through fictional identities:

- Arjun Mehra appeared to be connected to the suspicious activity.
- Kabir Sharma guided the investigation and supplied the investigative perspective.
- ECHO remained the anonymous entity behind the events.

Each stage encouraged you to form a theory about the person responsible. The evidence was deliberately arranged to make you follow identities, accounts, records, and relationships.

But the final challenge asks you to question the boundary of that investigation.

What if the person behind the fictional identity is not another character in the story?

What if the clues have been pointing towards the person who created the story all along?

ECHO is revealed not as another fictional suspect to be discovered inside NovaVault, but as the challenge author himself: **Tarun Yadav**.

---

## Closing — The Mirror Investigation

The Mirror Investigation was designed around a recurring idea: people do not always examine evidence objectively. They form assumptions, trust familiar labels, follow convincing narratives, and sometimes overlook the smallest details because those details appear ordinary.

The investigation uses that behaviour at every stage.

- In **Digital Footprints**, the terminal prompt was visible throughout the investigation, but its unusual prefix could easily be dismissed as decoration.
- In **Hidden in Plain Sight**, the solution depended on interpreting visual instructions rather than treating the board as an ordinary puzzle.
- In **Chasing Shadows**, social-media history and repository commits provided a trail beyond the current public identity.
- In **ECHO: The Three Systems**, the investigation required combining separate technical weaknesses and evidence sources rather than trusting a single explanation.
- In **WHOAMI**, the trail finally leaves the fictional world and points towards the person who built it.

The final twist is a deliberate fourth-wall break. The investigator is no longer simply asking who manipulated NovaVault. The investigator is being asked to reconsider who constructed the evidence, who created the trail, and who has been guiding the investigation from the beginning.

The answer was not another name hidden in the fictional case.

It was the author.

**The Mirror Investigation ends here.**
