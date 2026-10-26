import base64

# DON'T DECODE THIS FILE!
# This file is only here to verify whether your flag is correct or not.
# Don't try to decode the Base64 flag.
# I made the decoder for you. Just run this program and paste your flag.
# It will show whether your flag is correct or wrong.
#
# If it is wrong, don't decode this file. Solve the whole challenge!

ENCODED_FLAG = "ZDRya3tBVVRIT1JfVGFydW5fWWFkYXZfd3JvdGVfdGhlX3Bsb3R9"


def check_flag(user_flag):
    correct_flag = base64.b64decode(ENCODED_FLAG).decode("utf-8")
    return user_flag.strip().casefold() == correct_flag.casefold()


def main():
    print("=" * 50)
    print("       THE MIRROR INVESTIGATION")
    print("                 WHOAMI")
    print("=" * 50)

    flag = input("\nEnter your flag: ")

    if check_flag(flag):
        print("\n[+] FLAG ACCEPTED!")
        print("You found the truth.")
        print("ECHO was the author all along.")
        print("\n" + "=" * 50)
        print("       THANK YOU FOR PLAYING!")
        print("=" * 50)

        print("\nHow was THE MIRROR INVESTIGATION?")
        print("Did you enjoy the challenges and storyline?")
        print("Did you like the clues and the final reveal?")
        print("How much time did it take you to solve everything?")
        print("Which challenge was your favourite?")
        print("Which challenge was the hardest?")
        print("Did you suspect the truth before the final challenge?")
        print("Was anything confusing or unfair?")
        print("\nYour feedback would mean a lot to me!")
        print("Suggestions and honest criticism are welcome.")
        print("\nSix challenges. One investigation.")
        print("Question what you see.")

    else:
        print("\n[-] INCORRECT FLAG!")
        print("Don't guess. Investigate.")
        print("Retrace your steps and connect the evidence.")


if __name__ == "__main__":
    main()
