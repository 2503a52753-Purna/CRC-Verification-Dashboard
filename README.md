# CRC Verification & Attendance Audit Dashboard

An interactive dashboard that strictly implements the fundamental bitwise Cyclic Redundancy Check (CRC) algorithm and polynomial division without any external CRC libraries (`zlib`, `hashlib`, etc.).

### 🌐 Live 24/7 Deployments
* **GitHub Pages Web App (Instant 24/7):** [https://2503a52753-Purna.github.io/CRC-Verification-Dashboard/](https://2503a52753-Purna.github.io/CRC-Verification-Dashboard/)
* **Streamlit Community Cloud:** Can be launched with 1-click via [Streamlit Cloud](https://share.streamlit.io/).

---

## Key Highlights

1. **Strictly Uses Provided Python Code**:
   - `def crc(data, gen)`: Bitwise XOR modulo-2 division.
   - `def text_to_binary(text)`: Converts characters to standard 8-bit ASCII binary.
2. **Zero Bit-Flipping**:
   - No artificial bit-flipping buttons, random mutations, or synthetic corruption.
   - The receiver directly validates natural input, pasted codewords, modified text, or audited files.
3. **Solves the Attendance File Audit Problem (Slide Case Study)**:
   - Evaluates original instructor CSV attendance files against received files.
   - Detects any modified attendance statuses (`Absent` vs `Present`) or deleted rows with 100% precision.

---

## Supported Modes & Rules

### Step 1: Select CRC Type & Generator
- **CRC-3**: Generator polynomial `1011` ($x^3 + x + 1$)
- **CRC-4**: Generator polynomial `10011` ($x^4 + x + 1$)
- **CRC-8**: Generator polynomial `100000111` ($x^8 + x^2 + x + 1$)
- **CRC-32**: Generator polynomial `100000100110000010001110110110111` (IEEE 802.3)
- Fully supports custom binary generator strings `gen` (`crc_len = len(gen) - 1`).

### Step 2: Input Modes
- **Mode 1: Binary Input (Codeword Verification)**:
  - **Sender**: Padds data with `crc_len` zeros, computes `sender_crc = crc(new_data, gen)`, generates codeword `data + sender_crc`.
  - **Receiver**: Divides received codeword by generator `remainder = crc(received_codeword, gen)`. If remainder is zero (`int(remainder, 2) == 0`), status is **No Error Detected** and extracts original data. Otherwise, flags **Error Detected (Data Corrupted)**.
- **Mode 2: Text Input (CRC Value Comparison)**:
  - **Sender**: Converts text to 8-bit binary and calculates `sender_crc`.
  - **Receiver**: Converts received text to 8-bit binary and calculates `receiver_crc`.
  - **Comparison**: If `sender_crc == receiver_crc`, status is **No Error Detected**; otherwise **Error Detected**.
- **Mode 3: File Input (Attendance CSV Integrity Audit)**:
  - **Sender**: Reads original instructor attendance CSV file, converts to binary, computes reference CRC.
  - **Receiver / Auditor**: Reads file to audit, converts to binary, computes audited CRC.
  - **Audit Verdict**: Verifies whether the attendance record is intact or has been tampered with/deleted during storage or transfer. Provides downloadable audit reports.

---

## How to Run

1. Open PowerShell or Terminal and navigate to this folder:
   ```bash
   cd "C:\Users\Purna Chandar Reddy\.gemini\antigravity-ide\scratch\crc_dashboard"
   ```
2. Run the Streamlit dashboard:
   ```bash
   streamlit run app.py
   ```
3. The dashboard will automatically open in your browser at `http://localhost:8501`.

---

## Included Sample Files

- `sample_attendance_original.csv`: Pristine 5-student attendance file.
- `sample_attendance_modified.csv`: Attendance status tampered (`Absent` -> `Present`).
- `sample_attendance_deleted_row.csv`: Missing student record row.
