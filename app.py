"""
================================================================================
Cyclic Redundancy Check (CRC) Interactive Dashboard & Attendance Auditor
--------------------------------------------------------------------------------
Built strictly using the fundamental CRC bitwise XOR algorithm without any
external CRC libraries. Strictly follows all 3 modes and rules without bit-flipping.
================================================================================
"""

import streamlit as st
import pandas as pd
import io
import datetime
import os

# -----------------------------------------------------------------------------
# CORE ALGORITHMS (EXACT USER SPECIFIED CODE)
# -----------------------------------------------------------------------------
def crc(data, gen):
    data = list(data)

    for i in range(len(data) - len(gen) + 1):
        if data[i] == "1":
            for j in range(len(gen)):
                data[i + j] = str(int(data[i + j]) ^ int(gen[j]))

    return "".join(data[-(len(gen) - 1) :])


def text_to_binary(text):
    # Converts text to 8-bit ASCII binary
    return "".join(format(ord(char), "08b") for char in text)


# -----------------------------------------------------------------------------
# PAGE CONFIGURATION & STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="CRC Verification & Attendance Auditor Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Styling for modern, premium appearance
st.markdown(
    """
    <style>
    /* Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }

    code, pre, .mono-text {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Hero header styling */
    .hero-container {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 24px 32px;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.2);
    }
    .hero-title {
        color: #F8FAFC;
        font-size: 1.9rem;
        font-weight: 700;
        margin: 0 0 8px 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .hero-subtitle {
        color: #94A3B8;
        font-size: 1.05rem;
        margin: 0;
        line-height: 1.5;
    }

    /* Card Panels */
    .panel-card {
        background-color: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .panel-header {
        font-size: 1.15rem;
        font-weight: 600;
        color: #38BDF8;
        margin-bottom: 14px;
        border-bottom: 1px solid #334155;
        padding-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Result Badges */
    .status-badge-success {
        background: linear-gradient(135deg, #065F46 0%, #047857 100%);
        color: #ECFDF5;
        padding: 16px 20px;
        border-radius: 10px;
        border-left: 6px solid #10B981;
        font-weight: 600;
        margin: 12px 0;
    }
    .status-badge-error {
        background: linear-gradient(135deg, #881337 0%, #9F1239 100%);
        color: #FFF1F2;
        padding: 16px 20px;
        border-radius: 10px;
        border-left: 6px solid #F43F5E;
        font-weight: 600;
        margin: 12px 0;
    }

    .binary-pill {
        background-color: #0F172A;
        color: #38BDF8;
        padding: 8px 14px;
        border-radius: 8px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.95rem;
        word-break: break-all;
        border: 1px solid #334155;
        margin: 6px 0 12px 0;
    }

    .crc-highlight {
        color: #F59E0B;
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# HERO HEADER
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero-container">
        <div class="hero-title">🛡️ Cyclic Redundancy Check (CRC) Dashboard</div>
        <div class="hero-subtitle">
            Bitwise polynomial verification engine & attendance record audit suite.
            Computes authentic checksums strictly using binary polynomial division without flipping.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# SIDEBAR: STEP 1 - CRC TYPE & GENERATOR SELECTION
# -----------------------------------------------------------------------------
st.sidebar.markdown("### ⚙️ Step 1: Select CRC Type")

crc_type_options = {
    "CRC-3": "1011",
    "CRC-4": "10011",
    "CRC-8": "100000111",
    "CRC-32": "100000100110000010001110110110111",
}

selected_crc_name = st.sidebar.selectbox(
    "Choose CRC Standard:",
    options=list(crc_type_options.keys()),
    index=2,  # Default to CRC-8
    help="Select the CRC polynomial degree (CRC-3, CRC-4, CRC-8, CRC-32).",
)

default_generator = crc_type_options[selected_crc_name]

generator_input = st.sidebar.text_input(
    "Generator Polynomial (Binary 'gen'):",
    value=default_generator,
    help="Enter binary generator divisor. Degree equals length - 1.",
)

# Validate generator
gen = generator_input.strip()
if not gen or not set(gen).issubset({"0", "1"}) or len(gen) < 2:
    st.sidebar.error("❌ Generator must be a binary string with at least 2 bits (e.g. '100000111')")
    st.stop()

crc_len = len(gen) - 1

st.sidebar.markdown(
    f"""
    **Polynomial Details:**
    - **Standard:** `{selected_crc_name}`
    - **Generator Length:** `{len(gen)} bits`
    - **CRC Length (len(gen) - 1):** `{crc_len} bits`
    """
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📋 Step 2: Select Input Mode")

mode_choice = st.sidebar.radio(
    "Input Mode:",
    [
        "1. Binary Input (Codeword Verification)",
        "2. Text Input (CRC Value Comparison)",
        "3. File Input (Attendance CSV Audit)",
    ],
    index=0,
)

st.sidebar.markdown("---")
st.sidebar.info(
    "ℹ️ **Integrity Rule**: No synthetic bit-flipping is used. Receiver tests authentic input directly from user entries or audited files."
)

# -----------------------------------------------------------------------------
# MODE 1: BINARY INPUT (CODEWORD METHOD)
# -----------------------------------------------------------------------------
if mode_choice.startswith("1."):
    st.subheader("Mode 1: Binary Input (Codeword Verification)")
    st.markdown(
        "Sender appends `0 * crc_len` to binary data, generates CRC, and transmits the codeword. "
        "Receiver performs modulo-2 division on received codeword. A zero remainder confirms zero errors."
    )

    col_sender, col_receiver = st.columns(2)

    with col_sender:
        st.markdown("#### 📤 Sender Side")
        sender_bin_data = st.text_input(
            "Enter Binary Data String:",
            value="100100",
            help="Enter binary string consisting only of 0s and 1s.",
            key="m1_bin_input",
        ).strip()

        if sender_bin_data and set(sender_bin_data).issubset({"0", "1"}):
            # Sender Calculations
            new_data = sender_bin_data + "0" * crc_len
            sender_crc = crc(new_data, gen)
            codeword = sender_bin_data + sender_crc

            st.markdown(f"**Generator:** <span class='mono-text'>{gen}</span>", unsafe_allow_html=True)
            st.markdown(
                f"**Padded Data (data + 0*{crc_len}):** <div class='binary-pill'>{new_data}</div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"**Sender CRC ({crc_len} bits):** <div class='binary-pill crc-highlight'>{sender_crc}</div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"**Generated Transmitted Codeword:** <div class='binary-pill'>{codeword}</div>",
                unsafe_allow_html=True,
            )

            # Store default codeword in session state for easy receiver testing
            if "last_codeword" not in st.session_state:
                st.session_state.last_codeword = codeword
        else:
            st.warning("Please enter a valid binary string (containing only '0' and '1').")
            codeword = ""

    with col_receiver:
        st.markdown("#### 📥 Receiver Side")
        default_rcv = codeword if codeword else "100100001"
        received_codeword = st.text_input(
            "Enter Received Binary Codeword:",
            value=default_rcv,
            help="Enter the received codeword to verify. You can modify any bit manually to test error detection!",
            key="m1_rcv_input",
        ).strip()

        if received_codeword and set(received_codeword).issubset({"0", "1"}):
            if len(received_codeword) >= len(gen):
                # Calculate remainder using crc()
                remainder = crc(received_codeword, gen)

                st.markdown(
                    f"**Remainder Check:** <div class='binary-pill'>{remainder}</div>",
                    unsafe_allow_html=True,
                )

                if int(remainder, 2) == 0:
                    extracted_binary = received_codeword[:-crc_len]
                    st.markdown(
                        f"""
                        <div class="status-badge-success">
                            <div style="font-size: 1.25rem;">✔ Status: No Error Detected</div>
                            <div style="margin-top: 6px; font-weight: 400;">
                                The remainder is zero. Transmission was error-free.<br>
                                <strong>Extracted Data:</strong> <code>{extracted_binary}</code>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f"""
                        <div class="status-badge-error">
                            <div style="font-size: 1.25rem;">✖ Status: Error Detected (Data Corrupted)</div>
                            <div style="margin-top: 6px; font-weight: 400;">
                                Remainder is non-zero (<code>{remainder}</code>). One or more bits were corrupted during transmission.
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
            else:
                st.warning(f"Codeword must be at least {len(gen)} bits long to divide by generator.")
        else:
            st.warning("Please enter a valid binary string for the received codeword.")

# -----------------------------------------------------------------------------
# MODE 2: TEXT INPUT (CRC VALUE COMPARISON METHOD)
# -----------------------------------------------------------------------------
elif mode_choice.startswith("2."):
    st.subheader("Mode 2: Text Input (CRC Value Comparison)")
    st.markdown(
        "Sender converts text into 8-bit ASCII binary and computes the CRC. "
        "Receiver converts received text into binary and computes its CRC. Direct CRC comparison verifies authenticity."
    )

    col_txt_send, col_txt_recv = st.columns(2)

    with col_txt_send:
        st.markdown("#### 📤 Sender Side")
        sender_text = st.text_area(
            "Enter Sender Text:",
            value="Computer Networks CRC Verification Lab",
            height=110,
            key="m2_sender_txt",
        )

        sender_binary = text_to_binary(sender_text)
        sender_crc = crc(sender_binary + "0" * crc_len, gen) if sender_binary else "0" * crc_len

        st.markdown(f"**Generator:** <span class='mono-text'>{gen}</span>", unsafe_allow_html=True)
        st.markdown(
            f"**Sender Binary ({len(sender_binary)} bits):** <div class='binary-pill' style='max-height: 80px; overflow-y: auto;'>{sender_binary}</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"**Sender CRC:** <div class='binary-pill crc-highlight'>{sender_crc}</div>",
            unsafe_allow_html=True,
        )

    with col_txt_recv:
        st.markdown("#### 📥 Receiver Side")
        receiver_text = st.text_area(
            "Enter Received Text (Modify text to test error detection):",
            value=sender_text,
            height=110,
            key="m2_receiver_txt",
        )

        receiver_binary = text_to_binary(receiver_text)
        receiver_crc = crc(receiver_binary + "0" * crc_len, gen) if receiver_binary else "0" * crc_len

        st.markdown(
            f"**Receiver Binary ({len(receiver_binary)} bits):** <div class='binary-pill' style='max-height: 80px; overflow-y: auto;'>{receiver_binary}</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"**Receiver CRC:** <div class='binary-pill crc-highlight'>{receiver_crc}</div>",
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("#### 🔍 CRC Comparison & Integrity Verdict")

    if sender_crc == receiver_crc:
        st.markdown(
            f"""
            <div class="status-badge-success">
                <div style="font-size: 1.25rem;">✔ Status: No Error Detected (Sender CRC == Receiver CRC)</div>
                <div style="margin-top: 6px; font-weight: 400;">
                    Both checksums match perfectly (<code>{sender_crc}</code>). The text message is completely intact and authentic.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div class="status-badge-error">
                <div style="font-size: 1.25rem;">✖ Status: Error Detected (Sender CRC != Receiver CRC)</div>
                <div style="margin-top: 6px; font-weight: 400;">
                    Checksum discrepancy detected! <br>
                    <strong>Sender CRC:</strong> <code>{sender_crc}</code> &nbsp;|&nbsp;
                    <strong>Receiver CRC:</strong> <code>{receiver_crc}</code>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# -----------------------------------------------------------------------------
# MODE 3: FILE INPUT (ATTENDANCE CSV INTEGRITY AUDIT)
# -----------------------------------------------------------------------------
elif mode_choice.startswith("3."):
    st.subheader("Mode 3: File Input (Attendance Record Integrity Auditor)")
    st.markdown(
        """
        > 💡 **Scenario from Instructor Case Study**:
        > *An instructor generates a CSV attendance file after completing a class. During storage, transfer, or handling, 
        > some attendance values or rows may be accidentally changed or deleted. 
        > CRC comparison audits the file to guarantee it remains identical to the original record.*
        """
    )

    # Pre-load sample files if present
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    orig_sample_path = os.path.join(curr_dir, "sample_attendance_original.csv")
    mod_sample_path = os.path.join(curr_dir, "sample_attendance_modified.csv")
    del_sample_path = os.path.join(curr_dir, "sample_attendance_deleted_row.csv")

    col_file_s, col_file_r = st.columns(2)

    with col_file_s:
        st.markdown("#### 📤 1. Sender Side (Original Reference File)")
        uploaded_sender_file = st.file_uploader(
            "Upload Instructor's Original CSV / Text File:",
            type=["csv", "txt"],
            key="m3_orig_upload",
        )

        sender_file_content = ""
        sender_file_name = "sample_attendance_original.csv"

        if uploaded_sender_file is not None:
            sender_file_content = uploaded_sender_file.getvalue().decode("utf-8")
            sender_file_name = uploaded_sender_file.name
            st.success(f"Loaded: `{sender_file_name}`")
        elif os.path.exists(orig_sample_path):
            with open(orig_sample_path, "r", encoding="utf-8") as f:
                sender_file_content = f.read()
            st.info(f"Using default: `{sender_file_name}`")

        # Compute Sender CRC
        sender_binary = text_to_binary(sender_file_content)
        sender_crc = crc(sender_binary + "0" * crc_len, gen) if sender_binary else "0" * crc_len

        st.markdown(f"**Generator:** <span class='mono-text'>{gen}</span>", unsafe_allow_html=True)
        st.markdown(
            f"**Sender File CRC:** <div class='binary-pill crc-highlight'>{sender_crc}</div>",
            unsafe_allow_html=True,
        )

        # Preview Dataframe
        if sender_file_content:
            try:
                df_orig = pd.read_csv(io.StringIO(sender_file_content))
                st.caption(f"Preview: `{sender_file_name}` ({len(df_orig)} rows)")
                st.dataframe(df_orig, use_container_width=True, height=180)
            except Exception:
                st.text_area("File Content Preview", sender_file_content, height=180)

    with col_file_r:
        st.markdown("#### 📥 2. Receiver Side (Audited / Received File)")
        
        # Quick-load scenario helpers
        preset_choice = st.radio(
            "Audit Source:",
            [
                "Upload Audited File",
                "Load Sample: Identical (Authentic)",
                "Load Sample: Modified Attendance Status (Tampered)",
                "Load Sample: Missing Student Row (Row Deleted)",
            ],
            index=0,
            horizontal=False,
        )

        receiver_file_content = ""
        receiver_file_name = "audited_attendance.csv"

        if preset_choice == "Upload Audited File":
            uploaded_rx_file = st.file_uploader(
                "Upload File to Audit:",
                type=["csv", "txt"],
                key="m3_recv_upload",
            )
            if uploaded_rx_file is not None:
                receiver_file_content = uploaded_rx_file.getvalue().decode("utf-8")
                receiver_file_name = uploaded_rx_file.name
            else:
                receiver_file_content = sender_file_content
                receiver_file_name = f"Copy of {sender_file_name}"
        elif preset_choice == "Load Sample: Identical (Authentic)" and os.path.exists(orig_sample_path):
            with open(orig_sample_path, "r", encoding="utf-8") as f:
                receiver_file_content = f.read()
            receiver_file_name = "sample_attendance_original.csv"
        elif preset_choice == "Load Sample: Modified Attendance Status (Tampered)" and os.path.exists(mod_sample_path):
            with open(mod_sample_path, "r", encoding="utf-8") as f:
                receiver_file_content = f.read()
            receiver_file_name = "sample_attendance_modified.csv"
        elif preset_choice == "Load Sample: Missing Student Row (Row Deleted)" and os.path.exists(del_sample_path):
            with open(del_sample_path, "r", encoding="utf-8") as f:
                receiver_file_content = f.read()
            receiver_file_name = "sample_attendance_deleted_row.csv"

        # Compute Receiver CRC
        receiver_binary = text_to_binary(receiver_file_content)
        receiver_crc = crc(receiver_binary + "0" * crc_len, gen) if receiver_binary else "0" * crc_len

        st.markdown(
            f"**Receiver File CRC:** <div class='binary-pill crc-highlight'>{receiver_crc}</div>",
            unsafe_allow_html=True,
        )

        # Preview Receiver Dataframe
        if receiver_file_content:
            try:
                df_recv = pd.read_csv(io.StringIO(receiver_file_content))
                st.caption(f"Preview: `{receiver_file_name}` ({len(df_recv)} rows)")
                st.dataframe(df_recv, use_container_width=True, height=180)
            except Exception:
                st.text_area("File Content Preview", receiver_file_content, height=180)

    # -------------------------------------------------------------------------
    # AUDIT VERDICT & REPORT GENERATION
    # -------------------------------------------------------------------------
    st.markdown("---")
    st.markdown("#### ⚖️ Official File Audit Verdict")

    is_file_intact = (sender_crc == receiver_crc)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if is_file_intact:
        st.markdown(
            f"""
            <div class="status-badge-success">
                <div style="font-size: 1.3rem;">✔ Status: No Error Detected (Sender CRC == Receiver CRC)</div>
                <div style="margin-top: 8px; font-weight: 400; line-height: 1.5;">
                    <strong>Audit Result: PASS</strong><br>
                    The audited attendance record is 100% identical to the original instructor copy.<br>
                    Checksum Match: <code>{sender_crc}</code> == <code>{receiver_crc}</code>.
                    No attendance values or rows were changed or deleted during storage or transfer.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div class="status-badge-error">
                <div style="font-size: 1.3rem;">✖ Status: Error Detected (Sender CRC != Receiver CRC)</div>
                <div style="margin-top: 8px; font-weight: 400; line-height: 1.5;">
                    <strong>Audit Result: TAMPERING / CORRUPTION DETECTED</strong><br>
                    Discrepancy identified between the original attendance record and the audited file.<br>
                    <strong>Original File CRC:</strong> <code>{sender_crc}</code><br>
                    <strong>Audited File CRC:</strong> <code>{receiver_crc}</code><br>
                    One or more student attendance values, names, or rows have been altered or deleted!
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Downloadable Audit Report
    report_data = {
        "Audit Timestamp": [timestamp],
        "Original File": [sender_file_name],
        "Audited File": [receiver_file_name],
        "CRC Standard": [selected_crc_name],
        "Generator": [gen],
        "Original CRC": [sender_crc],
        "Audited CRC": [receiver_crc],
        "Audit Status": ["No Error Detected (AUTHENTIC)" if is_file_intact else "Error Detected (TAMPERED)"],
        "Details": ["Identical file content." if is_file_intact else "Discrepancy in file content or missing rows."],
    }
    audit_df = pd.DataFrame(report_data)

    csv_buffer = io.StringIO()
    audit_df.to_csv(csv_buffer, index=False)
    csv_bytes = csv_buffer.getvalue().encode("utf-8")

    st.download_button(
        label="📥 Download Official Audit Report (CSV)",
        data=csv_bytes,
        file_name=f"crc_audit_report_{selected_crc_name.lower()}.csv",
        mime="text/csv",
    )
