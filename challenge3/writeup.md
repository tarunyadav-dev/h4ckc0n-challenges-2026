# Challenge 3 — Hidden in Plain Sight

## Creator's Write-up and Intended Solve Path

**Points:** 150  
**Category:** Steganography  
**Flag:** `d4rk{fediverse}`

## Step 1 — Inspect the image

Players receive `what_was_that.png`, an image containing a numbered 9×9 board.

At first glance, it may resemble a Sudoku board or a number-placement puzzle. However, the objective is not to solve Sudoku or apply a mathematical algorithm.

The numbers represent the sequence of pen strokes needed to construct letters.

## Step 2 — Inspect the image metadata

Examining the image's EXIF metadata reveals two important pieces of information.

The first is:

> Don't Jump when there is the red, otherwise you should!

This instruction explains how to interpret the marked transitions while tracing the numbered paths:

- **Red marker:** Jump — keep the pen down and continue the current stroke.
- **No red marker:** Don't jump — lift the pen and begin a new stroke.

Small dots on the board mark the relevant diagonal transitions. Players must pay attention to these markers rather than assuming every diagonal movement should be treated the same way.

The second metadata message reads:

> nothing is inside this challenge

This is intentional. It indicates that players should not spend time searching this image for the numeric fragment used in the final challenge. The purpose of this challenge is to recover a meaningful word that directs the investigation forward.

## Step 3 — Trace the pen strokes

Players should follow the numbered sequences and use the metadata instructions to determine when to keep the pen down and when to lift it.

The board is divided conceptually into nine 3×3 sections. Each section represents one letter.

Following the indicated paths produces the following arrangement:

| F | E | D |
|---|---|---|
| I | V | E |
| R | S | E |

Players should read the resulting letters **row-wise**, from left to right, completing one row before moving to the next.

The decoded word is:

`FEDIVERSE`

## Step 4 — Submit the flag

The challenge specifies the format:

`d4rk{singleword}`

Therefore, the correct flag is:

`d4rk{fediverse}`

## Step 5 — Connection to the next challenge

The recovered word is meaningful beyond this challenge. It points toward the fediverse and provides the conceptual starting point for the next investigation.

Players must research the word and determine which online platforms are associated with it. The challenge does not explicitly name the next platform; discovering that connection is part of the intended solve path.

## Intended Learning Outcomes

- Inspecting image metadata for useful clues.
- Recognizing that a visual puzzle may encode information through paths rather than numerical calculations.
- Following a sequence of pen strokes while distinguishing between continuous strokes and pen lifts.
- Reading reconstructed letters in the intended order.
- Using a recovered word as a lead for further OSINT investigation.

---
