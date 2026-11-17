# The Mirror Investigation

## A story about evidence, assumptions, and the person behind the story

I did not want to create a sequence of unrelated CTF challenges where each stage simply presents a puzzle, hides a flag, and asks the player to find it. I wanted to create an investigation—one that gradually changes the way the player thinks about what they are seeing.

The Mirror Investigation begins as a fictional incident involving NovaVault. It introduces people, records, accounts, technical systems, and conflicting pieces of evidence. As the investigation progresses, the player is encouraged to form explanations, trust certain sources, question others, and connect details that initially appear unrelated.

But the case has another purpose. Beneath the technical tasks is a question about human behaviour: **How much of what we believe comes from the evidence itself, and how much comes from the story we have built around that evidence?**

This is the idea that connects every stage.

---

## The investigation begins with a person

The first part of the story establishes a world that feels like a real investigation. There is an incident, there are records to examine, and there are people whose actions appear to matter.

Arjun Mehra becomes an important part of the trail. The player follows his digital footprint, examines the information associated with him, and begins to construct a picture of what might have happened. Kabir Sharma provides another perspective and helps move the investigation forward. ECHO, meanwhile, remains a presence behind the events—an identity that is difficult to place and whose intentions are not immediately clear.

I wanted the player to experience something familiar from real investigations: the moment when a collection of disconnected facts begins to look like a coherent explanation.

That moment is useful, but it is also dangerous.

Once we begin to believe that we understand a case, we tend to interpret new information in ways that support our existing theory. We give more weight to details that fit, overlook details that do not, and sometimes mistake a plausible explanation for a proven one.

The early stages encourage the player to investigate carefully, but they also create the conditions in which assumptions can form.

## Digital Footprints — the ordinary detail

Digital Footprints asks players to examine records and relationships rather than accept a single account of events. The evidence is deliberately not a simple declaration of who is responsible. Different records have different levels of reliability, and a connection between two events does not automatically establish that the same person caused both.

This distinction matters to me. In a real investigation, a valid session is not necessarily proof of the human being operating it. A badge record is not absolute proof of who physically carried the badge. A timestamp, a network connection, or a system-generated claim may establish a relationship without establishing identity or intent.

The player has to decide what the evidence supports, what it merely suggests, and what remains unknown.

There is also a small detail in the terminal that is easy to ignore: the unusual prefix appearing before the NovaVault prompt. It is visible repeatedly, almost as if it were simply part of the interface. It does not look like the main evidence. It does not demand attention. It is the kind of detail a person may stop noticing precisely because it is always there.

That detail becomes important much later.

I wanted it to represent a simple habit of investigation: do not automatically discard something because it looks like decoration, a default value, or an unimportant part of the environment. Familiarity can make us careless. Sometimes the thing we stop seeing is the thing we should have questioned.

## Hidden in Plain Sight — changing the way we look

The next stage shifts the player away from conventional records and towards a visual encoding. The board initially resembles a familiar number-placement puzzle, but the numbers are not asking to be solved mathematically. They describe paths and pen movements. The metadata provides the instructions needed to distinguish between continuous strokes and separate strokes.

The answer is FEDIVERSE.

This stage is intentionally a change in perspective. The information is present, but the player must stop applying the first interpretation that comes to mind. A Sudoku-like board does not necessarily require Sudoku logic. A sequence of numbers does not necessarily represent a calculation. The form of an object can suggest one way of reading it while its actual purpose is something else.

That is another recurring idea in the investigation: the first interpretation is not always the correct one.

The recovered word also moves the player beyond the immediate artifact. It becomes a lead towards Mastodon and the next part of Arjun's online identity. The investigation expands from a technical environment into the wider world of public information.

## Chasing Shadows — history is part of the evidence

In Chasing Shadows, the player follows the connection from the Fediverse to Mastodon, locates Arjun's account, and examines its history to recover a GitHub link that is no longer visible in the current content.

The important idea here is that the present version of a page is not necessarily the whole story. Online identities change. Posts are edited. Links disappear. Repositories evolve. A current snapshot can conceal the path by which it came to exist.

The player then reaches ECHO's GitHub repository and examines its scripts and commit history. The repository is not treated as a static collection of files; its history becomes part of the evidence. Changes, earlier versions, and authorship all matter.

This is also where the investigation begins to leave a trail that is larger than the fictional characters. At first, the player is looking for information about ECHO. Later, the player may notice that the repository contains an unexpected connection to the person who created the challenge.

At this point, that connection is only a clue. Its full significance is not yet explained.

## ECHO: The Three Systems — separate evidence, one conclusion

The next stage brings together three different technical investigations. Each system has its own method and its own kind of evidence: a cache inconsistency, a weakness in a signed session construction, and a device-evidence reconstruction involving process information, input events, screen state, and clock calibration.

These are different technical disciplines, but they share a common investigative requirement: do not rely on one surface-level observation when the underlying system tells a more complicated story.

A cache response may not mean what its URL appears to request. A signed value may not provide the integrity guarantee its designers assume. An event's arrival time may not be the same as the time at which it occurred. A keyboard event, a screen click, and a process record may each be incomplete on their own, yet become meaningful when correlated correctly.

The player has to separate the evidence, understand what each source actually records, and then combine the results.

This stage is deliberately technical, but it still serves the larger theme. Systems produce data; people interpret it. A mistake in that interpretation can be just as consequential as a flaw in the system itself.

By completing the three systems, the player has gathered the information needed to move towards the final stage. But the central question—who is ECHO?—has not yet been answered.

---

## WHOAMI — when the investigation turns around

The final stage changes the direction of the investigation.

Until now, the player has been looking outward: at NovaVault, at Arjun, at Kabir, at ECHO, at accounts, repositories, sessions, and records. WHOAMI asks the player to look back at the trail itself.

It brings together three fragments.

The first was present in Digital Footprints from the beginning. The terminal prompt contained the prefix `NHGUBE`. It looked like an ordinary part of the interface, but ROT13 transforms it into:

`AUTHOR`

The second fragment is found by revisiting ECHO's GitHub repository from Chasing Shadows. Among the commits is one attributed to Tarun Yadav—the author of the challenge. Its first-person commit message, “I forget to add this one,” is not written in the voice of a fictional operator. It is a trace of the person constructing the challenge.

The third fragment takes the player beyond the fictional environment and into the social connections around the event. The event is hosted by D4rkC0de, the cybersecurity club at IIIT Delhi. Following that real-world connection leads to the Instagram account `with_tarunyadav`. Its first post contains the final wording needed for the flag.

Individually, these clues may look like unrelated details. Together, they reveal that the trail has been pointing outside the fictional case.

ECHO is not another fictional suspect waiting to be uncovered. The final identity is the author himself: Tarun Yadav.

This is the fourth-wall break. The player is no longer only investigating the fictional incident. The player is investigating the construction of the incident—and the person who designed the path through it.

## Why make the author the answer?

The reveal is not meant to say that every fictional event was real, or that the technical evidence inside the story should be treated as proof about a real-world incident. The fictional case and its characters are part of a constructed investigation.

The point is that the player has spent the entire experience trusting a frame: a world with its own identities, motives, records, and apparent boundaries. The final stage asks the player to question that frame.

Who created the records? Who chose which details would be visible? Who decided which identities would appear trustworthy? Who placed the clues, and who guided the order in which they would be discovered?

The author was outside the world the player was investigating, but traces of the author were inside it all along.

That is why the final answer is not simply another name. It changes the meaning of the earlier clues. The terminal prefix becomes more than a strange prompt. The GitHub commit becomes more than a repository change. The social-media connection becomes more than an OSINT lead. Together, they reveal the hand behind the investigation.

## What I hoped players would take away

I wanted the challenges to reward technical skill, but technical skill alone is not the central lesson. The larger lessons are about how we investigate and how we think.

**Question what looks ordinary.** Repeated details can become invisible through familiarity. A default prompt, a small label, a timestamp, or a commit message may carry meaning precisely because nobody expects it to.

**Separate observation from interpretation.** “This record exists” is an observation. “This person must have performed the action” is an interpretation. The distance between those statements is where careful investigation happens.

**Do not confuse correlation with attribution.** Two records that match in time or device information may be connected without proving that the same person was responsible. Evidence should be allowed to support only the conclusions it can actually justify.

**Revisit old evidence with new questions.** A clue can be visible from the beginning and still go unnoticed until the investigator has the right context. Returning to an earlier source is not wasted effort; it is often how a new interpretation becomes possible.

**Understand the system, not just the output.** Whether the subject is a cache, a signature, a repository, or a device trace, the investigator should ask how the result was produced and what assumptions are built into that process.

**Be willing to question your own theory.** A convincing narrative can make a weak conclusion feel certain. Good investigation requires the willingness to revise an explanation when new evidence changes the picture.

And finally: **look beyond the frame when the evidence gives you a reason to do so.** Sometimes the most important question is not only what happened inside the system, but who designed the system you are examining.

---

## A note from the author

I designed The Mirror Investigation to feel like one continuous case rather than a set of disconnected technical exercises. Each challenge changes the kind of evidence the player must understand, but the underlying question remains connected: what can we really know from the information in front of us?

The story begins by asking players to identify a suspicious actor. It ends by asking them to identify the person who created the investigation. Between those points, the player has to move through digital forensics, steganography, OSINT, web security, cryptography, and evidence correlation. Those disciplines are not there only for variety. Each one offers a different way to examine information, and each one contributes to the larger idea that appearances, records, and identities need to be questioned.

I also wanted the final reveal to reward curiosity rather than brute force. The last answer is not obtained by finding a hidden file in the final environment. It comes from remembering details, revisiting earlier work, recognising an inconsistency, and being willing to investigate beyond the fictional boundary.

If there is one thing I hope players remember, it is this:

**Do not stop at the explanation that first makes sense. Look again. Question the details. Question the source. And when the evidence asks you to, question the frame itself.**

The Mirror Investigation was built to make the player follow the trail.

In the end, the trail leads back to the person who made it.

**The case is closed.**
