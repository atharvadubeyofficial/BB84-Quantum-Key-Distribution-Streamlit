
import streamlit as st
import random
import base64

st.set_page_config(page_title="BB84 Quantum Simulator", layout="centered")

# UI HEADER
st.markdown("<h1 style='text-align: center; color: #1F51FF;'>BB84 Quantum Key Distribution Simulator🚀</h1>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center;'>🔐 Project by <b>Atharva Dubey</b></h5>", unsafe_allow_html=True)

st.markdown("---")

# MESSAGE INPUT
message = st.text_input("💬 Enter a message to encrypt and simulate using BB84 protocol:")

# SIMULATION BUTTON
run = st.button("🚀 Run Quantum Simulation")

if run and message:
    n = 200
    alice_bits = [random.randint(0, 1) for _ in range(n)]
    alice_bases = [random.choice(['X', 'Z']) for _ in range(n)]
    bob_bases = [random.choice(['X', 'Z']) for _ in range(n)]
    eve_present = random.random() < 0.65

    bob_results = []
    eve_results = []

    for i in range(n):
        bit = alice_bits[i]
        base = alice_bases[i]

        if eve_present:
            eve_base = random.choice(['X', 'Z'])
            eve_bit = bit if base == eve_base else random.randint(0, 1)
            eve_results.append(eve_bit)

            final_bit = eve_bit if eve_base == bob_bases[i] else random.randint(0, 1)
        else:
            final_bit = bit if base == bob_bases[i] else random.randint(0, 1)

        bob_results.append(final_bit)

    matching_indices = [i for i in range(n) if alice_bases[i] == bob_bases[i]]
    alice_key = [alice_bits[i] for i in matching_indices]
    bob_key = [bob_results[i] for i in matching_indices]

    error_count = sum(1 for i in range(len(alice_key)) if alice_key[i] != bob_key[i])
    error_rate = (error_count / len(alice_key)) * 100 if alice_key else 0
    key_length = len(alice_key)

    mismatch_log = [i for i in matching_indices if alice_bits[i] != bob_results[i]]

    decrypted_message = ""
    secure_status = ""

    if error_rate > 20:
        secure_status = "❌ Eavesdropping Detected! Channel Compromised."
        decrypted_message = "⚠️ Message compromised due to Eve interference."
    else:
        try:
            byte_msg = message.encode()
            bin_msg = ''.join(format(byte, '08b') for byte in byte_msg)
            key_stream = (alice_key * ((len(bin_msg) // len(alice_key)) + 1))[:len(bin_msg)]
            xor_result = ''.join(str(int(bit) ^ k) for bit, k in zip(bin_msg, key_stream))
            decrypted_bytes = [int(xor_result[i:i+8], 2) for i in range(0, len(xor_result), 8)]
            decrypted_message = bytes(decrypted_bytes).decode(errors='ignore')
            secure_status = "✅ Secure Channel Established"
        except:
            decrypted_message = "⚠️ Corrupted Message"

    # OUTPUT
    st.markdown("### 📊 Simulation Result")
    st.write("**Error Rate:**", f"{round(error_rate,2)}%")
    st.write("**Shared Key Length:**", key_length)
    st.write("**Decrypted Message:**", decrypted_message)
    st.write("**Status:**", secure_status)

    if error_rate > 20:
        st.markdown("#### 🔍 Mismatched Photon Indices")
        st.code(mismatch_log if mismatch_log else "None")

# FOOTER
st.markdown("---")
st.markdown("🔎 **Note:** This real-time simulation flags eavesdropping if error rate exceeds 20%. Random quantum noise also affects results. Accurate decryption is possible only in secure channel conditions.")

st.markdown("<p style='text-align: center; color: grey;'>🛰️ India's Q-Insight Protocol | Quantum Secure Future | Connect with me on <a href='https://www.linkedin.com/in/atharva-dubey-76b566331' target='_blank'>LinkedIn</a></p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 13px;'>🧠 Project by Atharva Dubey<br>B.Tech | SGSITS Indore<br>B.S. in Data Science | IIT Madras</p>", unsafe_allow_html=True)
