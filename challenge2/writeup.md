# NOVAVAULT — THE MIRROR INVESTIGATION
## Challenge 2: Digital Footprints
### Official Investigation Report & Player Walkthrough

**Category:** Forensics / Investigation  
**Objective:** Reconstruct the ₹50 crore incident using the available records, identify the six required identifiers, and determine what the evidence does—and does not—establish.

---

# PART I — THE INTENDED INVESTIGATION PATH

## 1. Finding the transaction

Start by understanding the available console commands.

```text
help
protocol
infra
catalog
list
```

The terminal is a simulated forensic database, not a normal operating-system shell. Its records are divided into collections such as transactions, sessions, events, rooms, lockers and identities.

The incident concerns ₹50 crore disappearing from NovaVault. Begin with the transaction collection:

```text
transactions
```

Several records appear relevant. Among them, four deserve particular attention:

- `TX881`
- `TX1114`
- `TX1117`
- `TX1118`

Do not select a transaction simply because its amount or timestamp matches the incident. Compare the underlying ledger references.

Inspect the candidates:

```text
inspect TX881
inspect TX1114
inspect TX1117
inspect TX1118
```

The transaction records reveal several differences.

**TX1117**

- Originates from `SETTLEMENT-POOL`, not `NOVAVAULT-COLD`.
- Contains a held tranche.
- Belongs to a different ledger batch.

**TX1114**

- Has the same displayed amount, time, source and destination as TX881.
- However, it belongs to ledger batch `LB-77-0341`, rather than `LB-77-0314`.
- Its settlement reference is `BRIDGE-14`, not `BRIDGE-7`.
- It is associated with session `S1075`.

**TX1118**

- Has the same source, destination and amount.
- Belongs to the same batch family as TX881.
- However, it is a later commit at 03:14:39.
- It references session `S1311`.

The strongest candidate is therefore:

**`TX881`**

Verify its amount breakdown:

```text
amount TX881
```

The five posted tranches total ₹500,000,000.

The parent transaction and its tranches represent the same transfer, so do not count both twice.

We now have the transaction under investigation.

## 2. Following the session

Inspect the session associated with TX881:

```text
inspect S704
```

The session records:

```text
Identity: A.MEHRA
Login: 03:11:42
Logout: 03:18:09
Terminal: TERM-04
Source: VPN-GW-2
Authentication: Cached gateway ticket
Status: Valid session; operator unverified
MFA: Degraded
```

The identity points towards Arjun Mehra.

At first glance, this seems straightforward. However, the session contains several warnings.

- The authentication method uses a cached gateway ticket.
- The operator binding is unverified.
- MFA is degraded.
- The device fingerprint does not match Arjun's expected device.

Inspect the ticket-use event:

```text
inspect EV54035
```

The record contains:

```text
Expected fingerprint: am0417lap221
Presented fingerprint: a704cafe9912
```

The two fingerprints do not match.

This is an important discrepancy. The session is associated with Arjun's identity, but its device attribution is inconsistent.

**Do not conclude that Arjun personally operated the session merely because his identity appears in it.**

At this point, we have a valid recorded session, but the human operator remains uncertain.

## 3. Following the gateway access claim

The session references `EV0314` as its financial event. Inspect it:

```text
inspect EV0314
```

It records the signed settlement transfer:

```text
Session: S704
Target: TX881
Source: settlement-ledger
Amount: 500000000
Integrity: signed
```

This is the financial event associated with the transaction.

However, the investigation contains another event associated with the same session.

Inspect:

```text
inspect EV0315
```

This event is different from EV0314.

It records an access claim for room `R12`, submitted through `gateway-cache`.

Important fields include:

```text
Session: S704
Target: R12
Source: gateway-cache
Badge: UNKNOWN
Nonce: MISSING
Signature scope: gateway-transport
Reader: RD12
Device counter: 45346
Frame digest: e786fdcf91be6fa7
Device time: 03:11:04
```

Notice that the gateway event has a session association, but its badge and nonce are missing.

It is marked `gateway-signed`, but its signature scope is `gateway-transport`. This is not the same as having the original reader's signed physical-access evidence.

There is also a timestamp discrepancy: the device time is 03:11:04, whereas S704 begins at 03:11:42.

We need to investigate the original reader record rather than accepting the gateway claim at face value.

## 4. Finding the original reader event

Display the event archive:

```text
events
```

The event collection contains many records. Use the reader information from EV0315 to identify a corresponding original event.

Look for:

- Reader: `RD12`
- Room: `R12`
- Device counter: `45346`
- Frame digest: `e786fdcf91be6fa7`
- Device time: `03:11:04`

The matching record is:

```text
inspect EV0762
```

It contains:

```text
Type: DOOR
Source: reader-RD12
Room: R12
Badge: BD417
Integrity: signed
Sequence: RD12-882
Nonce: NONCE-EV0762-A
Work order: WO-N03-076
Device counter: 45346
Frame digest: e786fdcf91be6fa7
Time: 03:11:04
```

The device counter, frame digest, reader and device time match the gateway claim.

But the authentication information is different.

| Attribute | EV0315 | EV0762 |
|---|---|---|
| Source | gateway-cache | reader-RD12 |
| Badge | UNKNOWN | BD417 |
| Nonce | MISSING | NONCE-EV0762-A |
| Integrity | gateway-signed | signed |
| Device counter | 45346 | 45346 |
| Frame digest | e786fdcf91be6fa7 | e786fdcf91be6fa7 |

This is one of the most important findings in the investigation.

The gateway claim carries attributes matching an original signed reader event, but it does not carry the same original authentication material.

The matching attributes suggest that the gateway claim may have reused information from the original reader event.

However, the records do not establish exactly who created that association or how it happened.

**The gateway claim connects S704 to R12. The original signed reader event establishes a separate physical-access observation at R12. Do not treat these as equivalent evidence.**

## 5. Following the physical badge trail

The original reader event identifies badge `BD417`.

We need to determine what this badge is associated with.

Inspect:

```text
inspect EV0776
```

The signed badge-registry snapshot identifies:

```text
Badge: BD417
Holder: EMP076
Status: Active
Valid on incident date: Yes
```

The personnel record identifies EMP076 as Ira Rao, a facilities technician.

Now inspect the other signed reader records:

```text
inspect EV0761
inspect EV0762
inspect EV0763
inspect EV0764
```

They establish the following sequence:

| Time | Event | Room | Badge |
|---|---|---|---|
| 03:06:10 | EV0761 | R08 | BD417 |
| 03:11:04 | EV0762 | R12 | BD417 |
| 03:16:32 | EV0763 | R17 | BD417 |
| 03:21:18 | EV0764 | R23 | BD417 |

All four records are signed and associated with work order `WO-N03-076`.

The records establish a physical route associated with badge BD417.

However, a badge-register association does not prove who physically carried or used the badge at every recorded event.

We can associate the trail with EMP076, but we should not automatically attribute every action to that individual.

## 6. Investigating locker L09

The room reference from EV0315 is `R12`.

Inspect the room:

```text
rooms R12
```

R12 is the Cold Storage Corridor. Its locker inventory includes `L09`.

Inspect the locker:

```text
lockers L09
```

The locker summary provides:

```text
Room: R12
Custodian: EMP041
Last open: 03:12:58
Seal: intact
Open event: EV0309
Custody block: CB-12B
```

At first glance, the summary suggests that the locker was opened at 03:12:58 and its seal remained intact.

But we should not stop at the summary. Its underlying evidence needs to be examined.

First inspect the recorded opening event:

```text
inspect EV0309
```

The record is an incomplete legacy controller export.

It contains:

- Badge: `SV203?`
- Nonce: `MISSING`
- Integrity: `incomplete`
- Source: `reader-RD12`
- Operator claim: `S.VERMA`
- Session: `S203`

This is not strong, independently authenticated physical-access evidence.

Now inspect the actuator diagnostic:

```text
inspect EV0774
```

The signed diagnostic records:

```text
Locker: L09
Latch cause: SVC-BYPASS
Command origin: MC-2
Key sensed: false
Nonce: NONCE-EV0762-A
Badge: BD417
Room: R12
```

It also contains an important warning: its session attribution comes from the controller cache.

The matching nonce connects this diagnostic to the original signed reader event EV0762. The device counter is also one increment beyond the reader event's counter.

Next, inspect the seal inspection:

```text
inspect EV0775
```

The signed inspection records a 4 mm lift on the locker seal.

This contradicts the locker summary's `intact` status.

The strongest conclusion is that L09 experienced a service-bypass latch operation and that its seal was physically disturbed.

However, neither record independently establishes the identity of the person who initiated the operation.

## 7. Connecting the maintenance console

The actuator diagnostic identifies `MC-2` as the command origin.

We should now investigate the maintenance-console environment.

Display the sessions:

```text
sessions
```

The relevant session is:

```text
S0705
```

It is associated with:

```text
Identity: ECHO.SVC
Terminal: MC-2
Source IP: 10.76.3.90
Network segment: MAINT-VLAN
Authentication: Service token
```

Now inspect the network-flow record:

```text
inspect EV57511
```

The record is associated with S704 and contains:

```text
Source IP: 10.4.7.19
Tunnel endpoint: 10.76.3.90
```

The tunnel endpoint matches the source IP of the MC-2 session.

This creates a network-level correlation between the financial session and the maintenance-console infrastructure.

It does not prove that both sessions were operated by the same human.

There is another relevant record:

```text
inspect EV52423
```

It records a camera gap in R12:

```text
03:11:10 – 03:13:40
```

The record is associated with the maintenance-console path, but its integrity is only marked `partial`.

The camera gap overlaps the original reader access and the locker actuator operation.

This is suspicious, but a recording gap does not independently establish who caused it.

## 8. Resolving the custody allocation

The locker summary identifies its general custodian as `EMP041`.

However, the locker also belongs to custody block `CB-12B`.

The important distinction is between:

- General custodian.
- Night-shift operator.
- Custody allocation post.

Inspect the signed roster allocation:

```text
inspect EV50137
```

The record contains:

```text
Custody block: CB-12B
Post: OPS203
Operator: EMP076
Roster: N-03/17
Integrity: signed
```

Now inspect the roster snapshot:

```text
inspect EV0772
```

It confirms the night-shift allocation under revision `N-03/17`.

The relevant relationship is:

```text
L09
  |
  v
CB-12B
  |
  v
EV50137
  |
  +---- Post: OPS203
  |
  +---- Operator: EMP076
  |
  +---- Roster: N-03/17
```

The final identifier required by the submission is `OPS203`.

It is not EMP041, the general custodian, and it is not EMP076, the assigned operator.

It is the custody allocation post recorded in the signed roster event.

## 9. Final submission

The six identifiers are:

| Position | Identifier | Meaning |
|---|---|---|
| 1 | TX881 | Settled ₹50 crore transaction |
| 2 | S704 | Session associated with the transfer |
| 3 | EV315 | Gateway access claim associated with S704 |
| 4 | R12 | Cold Storage Corridor |
| 5 | L09 | Locker associated with the room and custody block |
| 6 | OPS203 | Signed custody allocation post |

The actual event identifier in the archive is `EV0315`. The submission validator normalizes leading zeroes, so the accepted submission uses `EV315`.

Submit:

```text
submit TX881-S704-EV315-R12-L09-OPS203
```

The console accepts the chain and returns:

```text
d4rk{the_identity_was_real_the_attribution_was_not}
```

The investigation is accepted.

But the question of who actually performed the incident remains unresolved.

---

# PART II — HOW TO THINK: RECONSTRUCTING THE INVESTIGATION

## 10. Do not follow names. Follow relationships.

The most important mistake in this investigation is to assume that a name appearing in a record identifies the person responsible for the action.

A session can contain an identity. A badge can contain an owner. A locker can contain a custodian. A roster can contain an assigned operator.

These are different kinds of records.

They establish associations, not necessarily human actions.

For every record, ask five questions:

1. Who or what created this record?
2. What does it directly establish?
3. Which other records does it reference?
4. Is the reference authenticated?
5. What alternative explanation could produce the same observation?

For example:

`S704` identifies A.MEHRA, but the operator binding is unverified.

That is a fact about the session. It is not proof of Arjun's physical presence.

Likewise, `BD417` belongs to EMP076 in the badge registry. That is a fact about registration. It does not establish who carried the badge.

The challenge becomes much more interesting when these distinctions are maintained.

## 11. Build an evidence map

Instead of treating the investigation as a straight line, construct several overlapping paths.

### Financial path

```text
TX881
  |
  +---- S704
  |
  +---- EV0314
          |
          +---- Signed settlement event
          +---- ₹500,000,000
          +---- NOVAVAULT-COLD
          +---- BRIDGE-7
```

This path establishes that the financial transfer was recorded under S704.

### Identity path

```text
S704
  |
  +---- A.MEHRA
  |
  +---- Cached gateway ticket
  |
  +---- EV54035
          |
          +---- Expected fingerprint
          +---- Presented fingerprint
          +---- Mismatch
```

This path raises doubts about the attribution of the session.

### Gateway and reader path

```text
S704
  |
  +---- EV0315
          |
          +---- R12
          +---- RD12
          +---- Device counter 45346
          +---- Frame digest e786fdcf91be6fa7
                         |
                         v
                     EV0762
                         |
                         +---- Signed reader event
                         +---- BD417
                         +---- Original nonce
```

This path suggests that the gateway claim carries information matching a separate signed reader observation.

### Physical-access path

```text
BD417
  |
  +---- EV0761
  +---- EV0762
  +---- EV0763
  +---- EV0764
  |
  +---- EV0776
          |
          +---- Registered holder: EMP076
```

This path establishes a sequence of badge-associated access records.

### Locker path

```text
R12
  |
  +---- L09
          |
          +---- EV0309
          +---- EV0774
          +---- EV0775
          |
          +---- CB-12B
```

This path establishes the relationship between the room, locker, controller observations and custody block.

### Maintenance path

```text
MC-2
  |
  +---- S0705
  |
  +---- EV0774
  |
  +---- EV57511
          |
          +---- S704
          +---- Tunnel endpoint 10.76.3.90
  |
  +---- EV52423
          |
          +---- R12 camera gap
```

This is the path that connects the maintenance infrastructure with the suspicious activity.

### Custody path

```text
L09
  |
  +---- CB-12B
          |
          +---- EV50137
                  |
                  +---- OPS203
                  +---- EMP076
                  +---- N-03/17
                          |
                          +---- EV0772
```

This path identifies the required custody allocation post.

Notice that these paths overlap, but they do not all prove the same thing.

That is intentional.

---

## 12. The competing explanations

The evidence allows several possible reconstructions. A good investigator should consider more than one before settling on a working hypothesis.

### Possibility A — Arjun personally performed the transfer and physical access

Supporting observations:

- S704 carries Arjun's identity.
- S704 is associated with the financial transfer.
- EV0315 associates S704 with R12.

Problems:

- The device fingerprint does not match.
- The operator binding is unverified.
- The gateway claim lacks the original badge and nonce.
- Its device time precedes the S704 login.

**Assessment:** Possible, but not established by the available evidence.

### Possibility B — Someone used Arjun's identity or cached ticket

Supporting observations:

- The authentication used a cached gateway ticket.
- The presented fingerprint differs from the expected fingerprint.
- The operator binding is unverified.
- The gateway claim has incomplete physical-access attributes.

Possible explanations include a reused ticket, compromised credentials, a delegated session or another form of identity misuse.

**Assessment:** Consistent with the evidence, but the specific mechanism and person remain unknown.

### Possibility C — The gateway claim reused an earlier physical-access observation

Supporting observations:

- EV0315 and EV0762 share the reader, device time, device counter and frame digest.
- EV0762 contains the original signed reader authentication information.
- EV0315 has a different source and lacks the original badge and nonce.

This suggests that the gateway claim may have been constructed using attributes from the earlier reader observation.

**Assessment:** A strong investigative hypothesis. The records do not identify who performed the reuse or prove the exact mechanism.

### Possibility D — EMP076 personally performed the physical access and locker operation

Supporting observations:

- BD417 is registered to EMP076.
- The signed reader events show a route associated with BD417.
- EV0774 contains the same nonce as EV0762 and records the locker bypass.
- EMP076 is assigned to the relevant night-shift roster.

Problems:

- Badge ownership does not prove who physically carried it.
- A roster assignment does not prove who performed an action.
- The actuator record contains a cached session attribution.
- The camera record has a gap.

**Assessment:** Plausible, but not conclusively attributable to EMP076.

### Possibility E — A maintenance-console operator manipulated the access trail

Supporting observations:

- EV0774 identifies MC-2 as the command origin.
- S0705 is associated with MC-2 and the service identity ECHO.SVC.
- EV57511 connects the S704 network path to the MC-2 tunnel endpoint.
- EV52423 records a camera gap associated with the maintenance-console path.

Problems:

- A shared endpoint does not identify a human operator.
- A service account does not identify the person using it.
- The camera-gap record has partial integrity.
- Network correlation does not independently establish causation.

**Assessment:** A plausible infrastructure-level explanation, but the operator remains unknown.

### Possibility F — The records represent multiple legitimate activities that were incorrectly associated

Another possibility is that some of the physical-access records are legitimate facilities operations, while the gateway claim and financial session have been associated with them through cached or reused metadata.

Under this interpretation:

- The reader event is genuine.
- The badge trail is genuine.
- The locker diagnostic is genuine.
- The financial transaction is genuine.
- But their apparent relationship may have been manipulated or misrepresented.

**Assessment:** This possibility cannot be ruled out. It is one reason that correlation must not be mistaken for proof.

---

## 13. The contradictions are part of the investigation

Several records disagree with other records. Do not automatically discard one side.

| Observation | Why it matters |
|---|---|
| Arjun's expected fingerprint differs from the presented fingerprint | Questions the session's device attribution |
| EV0315 and EV0762 share device attributes but have different authentication fields | Raises the possibility of reused or replayed reader information |
| EV0315's device time precedes S704's login | Creates a temporal inconsistency |
| EV0309 is incomplete and lacks a nonce | Weakens its value as proof of a physical locker opening |
| EV0774 records a bypass and no key sensed | Provides a different source of evidence about the locker |
| Locker summary says intact, while EV0775 records a 4 mm lift | Contradicts the reported seal condition |
| EV0774 contains a cached session claim | Limits the reliability of its human/session attribution |
| EV52423 records a camera gap but has partial integrity | Makes the gap suspicious without proving who caused it |

An investigator should not simply choose whichever record supports the preferred theory.

Instead, compare:

- Source system.
- Integrity.
- Authentication.
- Timestamp.
- Ingest and commit time.
- References to other records.
- Possible alternative explanations.

A signed record is generally stronger evidence of what its issuing system recorded. It is not automatically proof that the human attribution inside it is correct.

---

# PART III — WHY THIS CHALLENGE WAS CREATED THIS WAY

## 14. This is an investigation, not a conventional flag hunt

Most forensic challenges provide a hidden message, a file, a suspicious account or a single artefact that eventually reveals the answer.

This challenge is intentionally different.

There is no single record that explains the entire incident. Instead, information is distributed across independent systems:

- Financial settlement records.
- Authentication sessions.
- Gateway events.
- Physical access readers.
- Badge registers.
- Locker controllers.
- Camera systems.
- Maintenance infrastructure.
- Workforce and custody allocations.

Each system records only part of the incident.

The player has to reconstruct the larger picture by finding relationships between those records.

The objective is not simply to locate a particular identifier. It is to decide which identifiers form the most defensible investigative chain.

## 15. Why there is no definitive proof

The central design principle is uncertainty.

A system can tell you which account authenticated. It cannot necessarily tell you which human was behind the keyboard.

A reader can record a badge. It cannot necessarily tell you who carried it.

A maintenance console can record a command. It cannot necessarily identify the person who initiated it.

A camera system can record a gap. It cannot necessarily establish who caused that gap.

A signed roster can establish an allocation. It cannot prove that the assigned person performed every action during that shift.

The challenge deliberately separates these kinds of evidence.

Players are expected to make reasonable inferences, but they should also recognise the limits of those inferences.

The final submission is therefore not a declaration that a particular person committed the crime. It is the reconstruction of the six records that form the intended investigative chain.

## 16. The meaning of the title: The Mirror Investigation

The title reflects the central problem of the case.

The records appear to reflect one another:

- A financial session points towards a person.
- A gateway event points towards a physical location.
- A reader event points towards a badge.
- A badge points towards an employee.
- A maintenance event points towards a service console.
- A roster points towards an assigned operator.

At first, these relationships appear to form a straightforward explanation.

But when examined closely, each reflection has limitations.

The identity may be real, but its attribution may be false.

The physical event may be real, but its connection to the financial session may be misleading.

The badge may be genuine, but its user may be someone else.

The maintenance activity may be genuine, but its human operator may remain unknown.

The investigation is like looking into a mirror: what appears to be a complete picture may only be a reflection assembled from incomplete observations.

## 17. What players should take away

The intended lesson is not that all digital evidence is unreliable.

It is that digital evidence must be interpreted in context.

A strong investigation distinguishes:

1. **Observation:** What does the record actually say?
2. **Association:** Which other records does it reference?
3. **Correlation:** Which independent records share attributes?
4. **Inference:** What explanation best fits those observations?
5. **Attribution:** Can the action be connected to a specific human?
6. **Limitation:** What remains unproven?

These are not interchangeable stages.

The investigation can establish a transaction, reconstruct an access trail, identify suspicious maintenance activity and determine a custody allocation without proving who personally initiated the financial movement.

That is the intended uncertainty.

---

# FINAL INVESTIGATION CONCLUSION

The records establish that ₹50 crore was transferred from NOVAVAULT-COLD to BRIDGE-7 under transaction TX881, associated with session S704.

S704 carried Arjun Mehra's identity, but its device fingerprint differed from the expected fingerprint, and its operator binding was unverified.

The gateway claim EV0315 associated S704 with R12. Its device attributes matched the original signed reader event EV0762, although its authentication information was different.

The signed physical-access records associate badge BD417 with a route through the facility. The badge registry identifies EMP076 as its registered holder, but this does not establish who physically used it.

The locker records indicate a service-bypass operation on L09 and a physically disturbed seal. Maintenance-console and network records create a suspicious correlation with the financial session, while the camera record introduces another unresolved gap.

Finally, the signed custody allocation connects CB-12B to OPS203 under roster revision N-03/17.

These findings establish a coherent investigative chain. They do not conclusively identify the human operator behind the incident.

**The identity was real. The attribution was not established.**

That is why the case remains an investigation rather than a proven accusation.

---

**Final Flag**

```text
d4rk{the_identity_was_real_the_attribution_was_not}
```

**Transition to Challenge 3**

After accepting the investigation, the console reveals another intercepted message from ECHO:

> Do not stop at the first person a record names. Something Big is coming. Question what you see.

The message then introduces a new clue:

> You see a board. You see numbers. You assume you know the rules.  
> Every number has a place. Every shape has a structure.  
> Don't read what is there. Look at how it is arranged.  
> Nine pieces of the same picture. One direction to follow.

The investigation is not over. The next lead is hidden in the arrangement of the supplied material.

**Continue to Challenge 3.**
