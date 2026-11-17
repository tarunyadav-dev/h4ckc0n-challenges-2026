# **Challenge 1 — The SetUp**

**Category:** Cryptography\
**Objective:** Recover the credentials required to access Challenge 2 — Digital Footprints.

## **1. Challenge Overview**

The challenge provides two files:

- `audio.wav` — a stereo audio file containing a Morse-code message.
- `ciphertext.txt` — a Base64-encoded RSA ciphertext.

The objective is to recover the credentials hidden inside the ciphertext. However, the private key required for decryption is not directly provided. Players must first analyse the audio file to discover a shortened URL, retrieve the RSA private key from it, and then decrypt the ciphertext.

The challenge combines audio steganography, Morse-code decoding, URL analysis, and RSA cryptography.

## **2. Step-by-Step Solution**

### **Step 1: Analyse the audio file**

Start by inspecting the provided `audio.wav` file.

The audio contains Morse code, so the first step is to decode the signals using an audio-based Morse-code decoder.

One of the tools that can be used is:

\- [Morse Code Audio Decoder](https://themorselab.com/morse-code-audio-decoder/?utm_source=chatgpt.com)

However, there is an additional detail in the audio that is important for recovering the correct message.

The audio is divided into two separate channels:

- **Left channel:** Contains lowercase letters.
- **Right channel:** Contains uppercase letters.

Therefore, decoding the entire audio without examining the individual channels can make it difficult to identify the correct capitalization.

### **Step 2: Decode the left and right channels separately**

Open the audio in a tool that allows you to inspect or isolate its left and right channels.

Decode the Morse-code signals from each channel independently.

The decoded signals are:

| Audio channel | Morse-decoded letters | Required case |
| ------------- | --------------------- | ------------- |
| Left          | `TXT`                 | Lowercase     |
| Right         | `VB`                  | Uppercase     |

The next step is to reconstruct the original sequence.

Read the decoded letters in their chronological order of appearance:

1. `T` — Left channel
2. `V` — Right channel
3. `B` — Right channel
4. `X` — Left channel
5. `T` — Left channel

Combining these letters gives:

```
TVBXT
```

Now apply the capitalization rule:

- Letters from the left channel are lowercase.
- Letters from the right channel are uppercase.

The final result is:

RECOVERED STRING

# **tVBxt**

**Important:** The capitalization is essential. The recovered string is not simply `TVBXT`; it is `tVBxt`.

### **Step 3: Identify the shortened URL**

The recovered string is:

```
tVBxt
```

At this point, the hint provided in the challenge becomes relevant:

> A short address can lead to somewhere much longer.

This suggests that the recovered string is not a normal word or password, but a URL identifier.

URL-shortening services generate compact identifiers that redirect users to longer web addresses. These identifiers are often case-sensitive, meaning that changing even one letter's capitalization can lead to a different destination or an invalid link.

Using the shortened URL service, construct the address:

```
https://shorturl.at/tVBxt
```

Opening this URL redirects to a hosted text file containing the RSA private key.

Private key:

[Retrieve the RSA private key](https://www.image2url.com/r2/default/files/1792782290262-cb6dabe0-3e6d-4a4e-bf23-d03d888ab133.txt?utm_source=chatgpt.com)

This is the key required for the next stage.

### **Step 4: Understand the ciphertext**

Now inspect the second provided file, `ciphertext.txt`.

Its contents look like a long sequence of seemingly random characters. Before attempting decryption, identify its encoding.

The ciphertext is Base64-encoded.

Base64 is an encoding format, not an encryption algorithm. It represents binary data using printable characters. In this case, decoding the Base64 representation produces the encrypted RSA data.

The decoded ciphertext is 256 bytes long, which is consistent with encryption using a 2048-bit RSA key.

At this stage, we have both required components:

1. The encrypted ciphertext from the provided file.
2. The RSA private key recovered through the shortened URL.

### **Step 5: Decrypt using RSA**

The next step is to decrypt the ciphertext using the recovered private key.

You can use the following online tool:

[RSA Decryption Tool — Kordu](https://www.kordu.tools/tools/encryption/rsa-decrypt?utm_source=chatgpt.com)

Configure the decryption tool as follows:

| Parameter            | Value                        |
| -------------------- | ---------------------------- |
| Operation            | Decryption                   |
| Ciphertext           | Contents of `ciphertext.txt` |
| Input encoding       | Base64                       |
| Private key          | Recovered PEM private key    |
| Encryption algorithm | RSA-OAEP                     |
| Hash algorithm       | SHA-256                      |

Make sure that you select **RSA-OAEP with SHA-256**. Selecting a different padding scheme or hash algorithm will result in decryption failure.

After entering the ciphertext and private key, execute the decryption operation.

If everything is configured correctly, the decrypted plaintext reveals the credentials for the next challenge.

### **Step 6: Recover the credentials**

The decrypted message contains:

```
Username: a.mehraCC704
Password: drower4648
```

These credentials are required to access Challenge 2 — Digital Footprints.

The corresponding flag is:

```
d4rk{username_a.mehraCC704_password_drower4648}
```

## **3. Tools Used**

| Purpose                   | Tool                                                                                                |
| ------------------------- | --------------------------------------------------------------------------------------------------- |
| Morse-code audio decoding | [The Morse Lab](https://themorselab.com/morse-code-audio-decoder/?utm_source=chatgpt.com)           |
| Audio channel inspection  | Any audio editor supporting stereo channel separation                                               |
| URL redirection           | [ShortURL](https://shorturl.at/?utm_source=chatgpt.com)                                             |
| Private-key hosting       | [Image2URL](https://www.image2url.com/?utm_source=chatgpt.com)                                      |
| RSA decryption            | [Kordu RSA Decryption](https://www.kordu.tools/tools/encryption/rsa-decrypt?utm_source=chatgpt.com) |

## **4. Cryptographic Concepts Involved**

**Morse Code:** A communication system that represents characters using sequences of dots and dashes. In this challenge, the signals are distributed across the left and right audio channels.

**Stereo Audio Channels:** A stereo audio file contains two independent audio channels. Analysing them separately reveals information that may not be obvious when listening to the combined audio.

**URL Shortening:** A URL-shortening service maps a short identifier to a longer destination URL. The recovered Morse-code message provides the identifier needed to locate the private key.

**Base64 Encoding:** The ciphertext is represented using Base64. Decoding it converts the printable representation into the original encrypted binary data.

**RSA Encryption:** RSA is an asymmetric cryptographic algorithm that uses a public key for encryption and a private key for decryption. The recovered private key is necessary to retrieve the original plaintext.

**RSA-OAEP with SHA-256:** OAEP is a padding scheme used with RSA encryption. The decryption operation must use the same padding configuration and hash algorithm that were used during encryption.

## **5. Story and Narrative Purpose**

NovaVault, presented as India's biggest cryptocurrency exchange, suffers a breach at 3:14 AM, resulting in the disappearance of ₹50 crore.

DCP Kabir Sharma assigns Agent Arjun Mehra to investigate the incident. Arjun was supposedly off-duty during the breach, although remote access was active.

The player begins by recovering the credentials required to access the internal investigation system. The audio file contains the first lead, while the encrypted text contains the actual credentials.

This challenge establishes the initial entry point into the investigation. It introduces the player to the encrypted information and the first set of credentials needed to proceed.

**Transition:** With the credentials recovered, the player can access Challenge 2 — Digital Footprints and begin examining the internal records.
