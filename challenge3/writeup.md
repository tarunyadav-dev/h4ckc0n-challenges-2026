# Challenge 3 — Hidden in Plain Sight

## Creator's Write-up and Intended Solve Path

**Points:** 150  
**Category:** Steganography  
**Flag:** `d4rk{fediverse}`

### Step 1 — Inspect the image

Players are provided with an image named `what_was_that.png`, which contains a numbered 9×9 board.

At first glance, the board may resemble a Sudoku grid or a number-placement puzzle. However, solving it as a conventional mathematical puzzle is not the objective.

Instead, the numbers indicate the sequence of pen movements required to trace letters. The challenge is to interpret these sequences as strokes rather than perform calculations on the numbers.

### Step 2 — Examine the image metadata

Inspecting the image's EXIF metadata reveals two important messages.

The first message reads:

> Don't Jump when there is the red, otherwise you should!

This serves as an instruction for interpreting the marked transitions along the numbered paths:

- **Red marker:** Do not lift the pen; continue the current stroke.
- **No red marker:** Lift the pen and begin a new stroke.

The small dots on the board indicate the relevant diagonal transitions. Players must use these markers to distinguish between continuous strokes and separate strokes, rather than treating every diagonal movement identically.

The second metadata message reads:

> nothing is inside this challenge

This is an intentional hint. Players do not need to search the image for the numeric fragment used in the final challenge. Instead, the objective here is to recover a meaningful word that will serve as a lead for the next stage of the investigation.

### Step 3 — Reconstruct the letters

Players must follow the numbered sequences on the board, applying the metadata instructions to determine when a stroke continues and when the pen must be lifted.

The 9×9 board can be viewed as nine separate 3×3 sections, with each section encoding one letter.

Tracing the paths and applying the pen-lift instructions produces the following arrangement:

| F | E | D |
|---|---|---|
| I | V | E |
| R | S | E |

The resulting letters must be read **row-wise**, from left to right, completing each row before moving to the next.

This reveals the word:

`FEDIVERSE`

### Step 4 — Submit the flag

The expected flag format is:

`d4rk{singleword}`

Replacing `singleword` with the decoded result gives the correct flag:

`d4rk{fediverse}`

### Step 5 — Connection to the next challenge

The decoded word is not merely the answer to this challenge. It also provides a conceptual lead for the next stage.

The term *Fediverse* refers to a network of interconnected social platforms. Players are expected to research the term and identify the online platforms associated with it.

The next platform is not explicitly named in this challenge. Discovering the relevant connection through independent research is part of the intended progression.

## Intended Learning Outcomes

- Examining image metadata to identify embedded instructions.
- Recognizing visual encodings that rely on paths and stroke sequences rather than numerical calculations.
- Interpreting markers to distinguish continuous pen strokes from separate strokes.
- Reconstructing letters and reading them in the intended order.
- Using a decoded term as a starting point for further OSINT investigation.
