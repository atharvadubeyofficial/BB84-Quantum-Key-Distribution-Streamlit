
import streamlit as st
import random
import base64

st.set_page_config(page_title="BB84 Quantum Simulator", layout="centered")

# Custom CSS for professional UI
st.markdown("""
    <style>
        body {
            background-color: #f5f7fa;
            font-family: 'Segoe UI', sans-serif;
        }
        .main-title {
            text-align: center;
            font-size: 40px;
            font-weight: 800;
            color: #003566;
        }
        .subtitle {
            text-align: center;
            font-size: 18px;
            color: #333;
            margin-top: -10px;
            margin-bottom: 20px;
        }
        .result-section {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.08);
            margin-top: 20px;
        }
        .footer {
            text-align: center;
            color: #666;
            font-size: 14px;
            margin-top: 40px;
        }
        .note {
            font-size: 14px;
            background-color: #e3f2fd;
            padding: 15px;
            border-left: 4px solid #2196F3;
            margin-top: 30px;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown("<div class='main-title'>🚀 BB84 Quantum Key Distribution Simulator</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'><b>Project by Atharva Dubey</b></div>", unsafe_allow_html=True)

# Input box
message = st.text_input("🔐 Enter a message to encrypt and simulate using BB84 protocol:")

# Button
run = st.button("🔁 Run Simulation")

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
        secure_status = "❌ Eavesdropping Detected! Channel compromised."
        decrypted_message = "⚠️ Message compromised due to Eve interference."
    else:
        try:
            byte_msg = message.encode()
            bin_msg = ''.join(format(byte, '08b') for byte in byte_msg)
            key_stream = (alice_key * ((len(bin_msg) // len(alice_key)) + 1))[:len(bin_msg)]
            xor_result = ''.join(str(int(bit) ^ k) for bit, k in zip(bin_msg, key_stream))
            decrypted_bytes = [int(xor_result[i:i+8], 2) for i in range(0, len(xor_result), 8)]
            decrypted_message = bytes(decrypted_bytes).decode(errors='ignore')

            if all(ord(c) < 128 for c in decrypted_message) and decrypted_message.strip() != "":
                secure_status = "✅ Secure Channel Established"
            else:
                decrypted_message = "⚠️ Corrupted Message"
                secure_status = "⚠️ Secure Channel unstable. Retry or ensure clean channel."
        except:
            decrypted_message = "⚠️ Corrupted Message"
            secure_status = "⚠️ Secure Channel unstable. Retry or ensure clean channel."

    # Results Display
    st.markdown("<div class='result-section'>", unsafe_allow_html=True)
    st.markdown("### 📊 Simulation Result")
    st.write("**Error Rate:**", f"{round(error_rate,2)}%")
    st.write("**Shared Key Length:**", key_length)
    st.write("**Decrypted Message:**", decrypted_message)
    st.write("**Status:**", secure_status)

    if error_rate > 20:
        st.markdown("#### 🔍 Mismatched Photon Indices")
        st.code(mismatch_log if mismatch_log else "None")
    st.markdown("</div>", unsafe_allow_html=True)

# Note
st.markdown("<div class='note'>🔎 <b>Note:</b> This simulation detects Eve based on an error rate threshold of 20%. Random noise and quantum base mismatches affect key accuracy. The decrypted message is only shown if the quantum channel remains secure and intact.</div>", unsafe_allow_html=True)

# Footer
st.markdown("<div class='footer'>🛰️ India's Q-Insight Protocol | Quantum Secure Future<br>Connect on <a href='https://www.linkedin.com/in/atharva-dubey-76b566331' target='_blank'>LinkedIn</a><br><br>🧠 Project by Atharva Dubey<br>B.Tech – SGSITS Indore<br>B.S. in Data Science – IIT Madras</div>", unsafe_allow_html=True)
