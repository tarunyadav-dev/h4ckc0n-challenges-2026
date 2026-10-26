# Challenge 1 — The SetUp

**Category:** Cryptography  
**Objective:** Recover the credentials required to access Challenge 2: Digital Footprints.

## 1. How to Solve the Challenge

1. **Inspect the provided audio.** The audio contains a Morse-code clue. Decode it using the [Morse Code Audio Decoder](https://themorselab.com/morse-code-audio-decoder/).

2. **Recover the private-key URL.** Use the decoded clue to identify the shortened URL leading to the RSA private key. You have to make combination, which letter is caps and which one is small.

   - Short URL: https://shorturl.at/tVBxt
   - Private-key file: https://www.image2url.com/r2/default/files/1792782290262-cb6dabe0-3e6d-4a4e-bf23-d03d888ab133.txt

3. **Decrypt the ciphertext.** Open the [RSA Decryption Tool](https://www.kordu.tools/tools/encryption/rsa-decrypt), select decryption mode, provide the supplied Base64 ciphertext and recovered PEM private key, and select RSA-OAEP with SHA-256.

4. **Recover the plaintext.** Successful decryption reveals the credentials needed for the next challenge.

### Recovered Credentials

- **Username:** `a.mehraCC704`
- **Password:** `drower4648`

**Flag:**

`d4rk{username_a.mehraCC704_password_drower4648}`

## 2. How the Challenge Was Created

The challenge combines Morse-code audio with RSA encryption to create a short, multi-step cryptographic puzzle.

- **Audio clue:** Morse code is used to direct players towards the private-key URL.
- **Private key:** The RSA private key is hosted separately and linked through a shortened URL.
- **Encryption:** The credentials are encrypted using RSA-OAEP with SHA-256.
- **Decryption:** Players use the recovered private key and the provided ciphertext to obtain the plaintext credentials.
- **Flag:** The recovered username and password are included in the flag, which also establishes the expected credential format.

### Tools Used

| Purpose | Tool |
|---|---|
| RSA decryption | https://www.kordu.tools/tools/encryption/rsa-decrypt |
| Private-key hosting | https://www.image2url.com/ |
| Shortened URL | https://shorturl.at/tVBxt |
| Morse-code generation | https://opentoollab.com/tools/morse-code-translator-audio/ |
| Morse-code audio decoding | https://themorselab.com/morse-code-audio-decoder/ |

## 3. Story and Narrative Purpose

NovaVault, presented as India's biggest cryptocurrency exchange, suffers a breach at 3:14 AM, resulting in the disappearance of ₹50 crore.

DCP Kabir Sharma assigns Agent Arjun Mehra to investigate. Arjun was off-duty during the incident, but remote access was active.

Kabir provides the credentials required to begin the investigation. The player must recover them from the encrypted material before accessing NovaVault's internal system in Challenge 2.

This challenge establishes the setting, introduces the incident, and provides the entry point for the larger investigation. It does not yet introduce the deception or the hidden authorship messages; those elements emerge in subsequent challenges.

**Transition:** The recovered credentials unlock Challenge 2 — Digital Footprints, where the player begins investigating NovaVault's internal records.
