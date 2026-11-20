import random
import string
import streamlit as st

st.title("🔐 Secret Code Translator")

option = st.radio("Choose an action:", ["Encode", "Decode"])
password = st.text_input("Enter secret password:", type="password")
message = st.text_input("Enter your message:")

def get_pattern(pwd):
    # Turn the password into a unique number
    key = sum(ord(char) for char in pwd)
    pad = (key % 4) + 2     # Dynamic random padding: 2 to 5 letters
    shift = (key % 15) + 1  # Dynamic character shift: 1 to 15
    return pad, shift

if st.button("Translate"):
    if not password.strip() or not message.strip():
        st.warning("Please enter both a password and a message.")
    else:
        pad, shift = get_pattern(password)
        result = []

        if option == "Encode":
            # Attach the hidden signature before encoding
            tagged_message = "OK::" + message
            words = tagged_message.split(" ")

            for word in words:
                if len(word) >= 3:
                    # 1. Move first letter to the end
                    rotated = word[1:] + word[0]
                    # 2. Shift characters using the password's shift value
                    shifted = "".join(chr(ord(c) + shift) for c in rotated)
                    # 3. Add dynamic random padding
                    r1 = "".join(random.choices(string.ascii_lowercase, k=pad))
                    r2 = "".join(random.choices(string.ascii_lowercase, k=pad))
                    result.append(r1 + shifted + r2)
                else:
                    # Reverse short words and shift characters
                    shifted = "".join(chr(ord(c) + shift) for c in word[::-1])
                    result.append(shifted)

            st.success("Encoded Message:")
            st.code(" ".join(result))

        elif option == "Decode":
            words = message.split(" ")

            for word in words:
                if len(word) >= 3:
                    # Strip dynamic padding
                    stripped = word[pad:-pad]
                    if len(stripped) > 0:
                        # Unshift characters and move last letter back to the front
                        unshifted = "".join(chr(ord(c) - shift) for c in stripped)
                        original = unshifted[-1] + unshifted[:-1]
                        result.append(original)
                else:
                    unshifted = "".join(chr(ord(c) - shift) for c in word)
                    result.append(unshifted[::-1])

            final_output = " ".join(result)

            # Verify the hidden signature
            if final_output.startswith("OK::"):
                st.success("Access Granted!")
                st.code(final_output.removeprefix("OK::"))
            else:
                st.error("❌ Wrong password or invalid code! Access denied.")
