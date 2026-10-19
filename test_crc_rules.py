"""
Unit Tests verifying all CRC rules and modes using the user's exact python code.
"""

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


def test_mode_1_binary():
    print("--- Testing Mode 1: Binary Input (Codeword Method) ---")
    gen = "1101"  # CRC-3 example
    crc_len = len(gen) - 1
    binary_data = "100100"

    # Sender side
    new_data = binary_data + "0" * crc_len
    sender_crc = crc(new_data, gen)
    codeword = binary_data + sender_crc
    assert len(sender_crc) == crc_len, f"CRC length mismatch: {len(sender_crc)} != {crc_len}"
    print(f"  Sender Data: {binary_data}, Generator: {gen}, CRC: {sender_crc}, Codeword: {codeword}")

    # Receiver side (unaltered)
    remainder = crc(codeword, gen)
    assert int(remainder, 2) == 0, f"Expected 0 remainder for valid codeword, got {remainder}"
    extracted = codeword[:-crc_len]
    assert extracted == binary_data, "Extracted data does not match original binary data"
    print("  [PASS] Unaltered codeword verified successfully. No error detected.")

    # Receiver side (altered manually, e.g. '100100001' -> '100101001')
    altered_codeword = "100101" + sender_crc
    remainder_err = crc(altered_codeword, gen)
    assert int(remainder_err, 2) != 0, f"Expected non-zero remainder for altered codeword, got {remainder_err}"
    print(f"  [PASS] Altered codeword correctly flagged: Remainder = {remainder_err}. Error detected.")


def test_mode_2_text():
    print("\n--- Testing Mode 2: Text Input (CRC Value Comparison) ---")
    gen = "100000111"  # CRC-8 generator
    crc_len = len(gen) - 1

    sender_text = "Computer Networks CRC Lab"
    sender_binary = text_to_binary(sender_text)
    sender_crc = crc(sender_binary + "0" * crc_len, gen)

    # Receiver with identical text
    receiver_text_match = "Computer Networks CRC Lab"
    receiver_binary_match = text_to_binary(receiver_text_match)
    receiver_crc_match = crc(receiver_binary_match + "0" * crc_len, gen)
    assert sender_crc == receiver_crc_match, "CRCs should match for identical text"
    print(f"  [PASS] Matching text: Sender CRC {sender_crc} == Receiver CRC {receiver_crc_match}")

    # Receiver with altered text
    receiver_text_diff = "Computer Networks CRC lab"  # small 'l'
    receiver_binary_diff = text_to_binary(receiver_text_diff)
    receiver_crc_diff = crc(receiver_binary_diff + "0" * crc_len, gen)
    assert sender_crc != receiver_crc_diff, "CRCs should not match for altered text"
    print(f"  [PASS] Altered text: Sender CRC {sender_crc} != Receiver CRC {receiver_crc_diff}")


def test_mode_3_file():
    print("\n--- Testing Mode 3: File Input (Attendance CSV Audit) ---")
    gen = "100000111"  # CRC-8
    crc_len = len(gen) - 1

    with open("sample_attendance_original.csv", "r", encoding="utf-8") as f:
        orig_text = f.read()
    with open("sample_attendance_modified.csv", "r", encoding="utf-8") as f:
        mod_text = f.read()
    with open("sample_attendance_deleted_row.csv", "r", encoding="utf-8") as f:
        del_text = f.read()

    orig_crc = crc(text_to_binary(orig_text) + "0" * crc_len, gen)
    orig_copy_crc = crc(text_to_binary(orig_text) + "0" * crc_len, gen)
    mod_crc = crc(text_to_binary(mod_text) + "0" * crc_len, gen)
    del_crc = crc(text_to_binary(del_text) + "0" * crc_len, gen)

    assert orig_crc == orig_copy_crc, "Original file CRC must match itself"
    print(f"  [PASS] Original CSV CRC match: {orig_crc} == {orig_copy_crc} (Integrity Verified)")

    assert orig_crc != mod_crc, "Modified CSV must produce different CRC"
    print(f"  [PASS] Modified attendance value detected: {orig_crc} != {mod_crc} (Tampering Detected)")

    assert orig_crc != del_crc, "Deleted row CSV must produce different CRC"
    print(f"  [PASS] Deleted row detected: {orig_crc} != {del_crc} (Row Deletion Detected)")


if __name__ == "__main__":
    test_mode_1_binary()
    test_mode_2_text()
    test_mode_3_file()
    print("\nALL CRC TESTS PASSED SUCCESSFULLY!")
