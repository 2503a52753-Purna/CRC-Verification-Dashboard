"""
Generate high-resolution visual interface cards for Appendix C of the Project Report.
Uses Pillow to create clean, executive dark-themed UI mockups of the CRC Dashboard.
"""

from PIL import Image, ImageDraw, ImageFont
import os

# Colors matching dashboard theme
NAVY = "#0F172A"
CARD_BG = "#1E293B"
BORDER = "#334155"
TEXT_WHITE = "#F8FAFC"
TEXT_MUTED = "#94A3B8"
BLUE = "#38BDF8"
GREEN_BG = "#065F46"
GREEN_BORDER = "#10B981"
GREEN_TEXT = "#ECFDF5"
RED_BG = "#881337"
RED_BORDER = "#F43F5E"
RED_TEXT = "#FFF1F2"
AMBER = "#F59E0B"
CODE_BG = "#0F172A"

try:
    font_title = ImageFont.truetype("segoeui.ttf", 26)
    font_subtitle = ImageFont.truetype("segoeui.ttf", 15)
    font_heading = ImageFont.truetype("segoeui.ttf", 18)
    font_bold = ImageFont.truetype("segoeuib.ttf", 14)
    font_regular = ImageFont.truetype("segoeui.ttf", 13)
    font_code = ImageFont.truetype("consola.ttf", 13)
    font_code_bold = ImageFont.truetype("consolab.ttf", 14)
except Exception:
    font_title = ImageFont.load_default()
    font_subtitle = ImageFont.load_default()
    font_heading = ImageFont.load_default()
    font_bold = ImageFont.load_default()
    font_regular = ImageFont.load_default()
    font_code = ImageFont.load_default()
    font_code_bold = ImageFont.load_default()

def draw_rounded_rect(draw, bbox, fill, outline=None, width=1, radius=8):
    draw.rounded_rectangle(bbox, radius=radius, fill=fill, outline=outline, width=width)

# -----------------------------------------------------------------------------
# Figure C.1: Dashboard Overview & Polynomial Configuration
# -----------------------------------------------------------------------------
def create_fig_c1():
    img = Image.new("RGB", (1000, 560), NAVY)
    draw = ImageDraw.Draw(img)

    # Hero Header Banner
    draw_rounded_rect(draw, (30, 25, 970, 115), CARD_BG, outline=BORDER, radius=12)
    draw.text((50, 40), "🛡️ Cyclic Redundancy Check (CRC) & Attendance Auditor", fill=TEXT_WHITE, font=font_title)
    draw.text((50, 78), "Bitwise Polynomial Verification Dashboard | 3 Operating Modes | CSV File Tampering Detection", fill=TEXT_MUTED, font=font_subtitle)

    # Left: Sidebar Panel
    draw_rounded_rect(draw, (30, 130, 360, 530), CARD_BG, outline=BORDER, radius=10)
    draw.text((50, 150), "⚙️ Step 1: Select CRC Standard", fill=BLUE, font=font_heading)
    draw.text((50, 185), "Choose CRC Polynomial:", fill=TEXT_WHITE, font=font_regular)
    
    # Dropdown select box
    draw_rounded_rect(draw, (50, 210, 340, 248), CODE_BG, outline=BORDER, radius=6)
    draw.text((65, 222), "CRC-8 (8-bit Polynomial)     ▼", fill=TEXT_WHITE, font=font_regular)

    draw.text((50, 265), "Generator Polynomial ('gen'):", fill=TEXT_WHITE, font=font_regular)
    draw_rounded_rect(draw, (50, 290, 340, 328), CODE_BG, outline=BLUE, radius=6)
    draw.text((65, 302), "100000111", fill=BLUE, font=font_code_bold)

    # Specs Card
    draw_rounded_rect(draw, (50, 345, 340, 420), CODE_BG, outline=BORDER, radius=6)
    draw.text((60, 355), "• Standard: CRC-8 (x⁸ + x² + x + 1)", fill=TEXT_MUTED, font=font_regular)
    draw.text((60, 375), "• Generator Length: 9 bits", fill=TEXT_MUTED, font=font_regular)
    draw.text((60, 395), "• CRC Checksum Length: 8 bits", fill=AMBER, font=font_bold)

    draw.text((50, 440), "📋 Step 2: Select Input Mode", fill=BLUE, font=font_heading)
    draw.text((50, 470), "◉ Mode 1: Binary Codeword Verification", fill=TEXT_WHITE, font=font_regular)
    draw.text((50, 492), "○ Mode 2: Text CRC Comparison", fill=TEXT_MUTED, font=font_regular)
    draw.text((50, 514), "○ Mode 3: Attendance CSV Audit", fill=TEXT_MUTED, font=font_regular)

    # Right: Overview Panel
    draw_rounded_rect(draw, (380, 130, 970, 530), CARD_BG, outline=BORDER, radius=10)
    draw.text((405, 150), "🚀 Core System Architecture & Operating Principles", fill=BLUE, font=font_heading)
    draw.line((405, 180, 945, 180), fill=BORDER, width=1)

    cards = [
        ("Pure Python XOR Engine", "100% mathematical bitwise modulo-2 division without external CRC libraries (no zlib / hashlib)."),
        ("Zero Bit-Flipping Policy", "Authentic receiver verification from actual inputs and edited files rather than synthetic mutation shortcuts."),
        ("Multi-Layer Deployment", "Simultaneously running via local Streamlit (port 8501) and live 24/7 on GitHub Pages."),
        ("Attendance Record Audit Case", "Solves the academic integrity dilemma: detects altered attendance values ('Absent' vs 'Present') and missing rows.")
    ]
    for i, (ctitle, cdesc) in enumerate(cards):
        cy = 200 + i * 78
        draw_rounded_rect(draw, (405, cy, 945, cy + 66), CODE_BG, outline=BORDER, radius=8)
        draw.text((420, cy + 10), f"✔ {ctitle}", fill=AMBER, font=font_bold)
        draw.text((420, cy + 34), cdesc, fill=TEXT_MUTED, font=font_regular)

    img.save("fig_c1_dashboard_overview.png")

# -----------------------------------------------------------------------------
# Figure C.2: Mode 1 - Binary Input Codeword Verification
# -----------------------------------------------------------------------------
def create_fig_c2():
    img = Image.new("RGB", (1000, 540), NAVY)
    draw = ImageDraw.Draw(img)

    draw_rounded_rect(draw, (30, 20, 970, 85), CARD_BG, outline=BORDER, radius=10)
    draw.text((50, 32), "Mode 1: Binary Input & Codeword Modulo-2 Verification", fill=TEXT_WHITE, font=font_heading)
    draw.text((50, 60), "Sender pads data with zeros, computes CRC, and creates codeword. Receiver divides codeword to verify zero remainder.", fill=TEXT_MUTED, font=font_regular)

    # Sender Column
    draw_rounded_rect(draw, (30, 100, 485, 410), CARD_BG, outline=BORDER, radius=10)
    draw.text((50, 118), "📤 Sender Side: Codeword Generation", fill=BLUE, font=font_bold)
    draw.line((50, 142, 465, 142), fill=BORDER, width=1)
    
    draw.text((50, 155), "Raw Binary Data Input:", fill=TEXT_WHITE, font=font_regular)
    draw_rounded_rect(draw, (50, 178, 465, 212), CODE_BG, outline=BORDER, radius=6)
    draw.text((65, 188), "100100", fill=BLUE, font=font_code_bold)

    draw.text((50, 225), "Generator Polynomial ('gen'):", fill=TEXT_WHITE, font=font_regular)
    draw_rounded_rect(draw, (50, 248, 465, 282), CODE_BG, outline=BORDER, radius=6)
    draw.text((65, 258), "1101  (CRC-3, degree 3)", fill=TEXT_MUTED, font=font_code)

    draw.text((50, 295), "Padded Stream (data + '000'):", fill=TEXT_WHITE, font=font_regular)
    draw_rounded_rect(draw, (50, 318, 465, 352), CODE_BG, outline=BORDER, radius=6)
    draw.text((65, 328), "100100000", fill=TEXT_WHITE, font=font_code)

    draw.text((50, 365), "Generated Transmitted Codeword:", fill=TEXT_WHITE, font=font_regular)
    draw_rounded_rect(draw, (50, 388, 465, 424), CODE_BG, outline=AMBER, radius=6)
    draw.text((65, 398), "100100001  (Data + CRC: 001)", fill=AMBER, font=font_code_bold)

    # Receiver Column
    draw_rounded_rect(draw, (515, 100, 970, 410), CARD_BG, outline=BORDER, radius=10)
    draw.text((535, 118), "📥 Receiver Side: Modulo-2 Division", fill=BLUE, font=font_bold)
    draw.line((535, 142, 950, 142), fill=BORDER, width=1)

    draw.text((535, 155), "Received Codeword Entry:", fill=TEXT_WHITE, font=font_regular)
    draw_rounded_rect(draw, (535, 178, 950, 212), CODE_BG, outline=BORDER, radius=6)
    draw.text((550, 188), "100100001", fill=BLUE, font=font_code_bold)

    draw.text((535, 225), "Calculated Remainder [crc(received, gen)]:", fill=TEXT_WHITE, font=font_regular)
    draw_rounded_rect(draw, (535, 248, 950, 282), CODE_BG, outline=BORDER, radius=6)
    draw.text((550, 258), "000  (Integer value = 0)", fill=GREEN_BORDER, font=font_code_bold)

    # Success Verdict Badge
    draw_rounded_rect(draw, (535, 305, 950, 395), GREEN_BG, outline=GREEN_BORDER, radius=8)
    draw.text((555, 320), "✔ Status: No Error Detected", fill=GREEN_TEXT, font=font_heading)
    draw.text((555, 350), "The remainder is zero (000). Codeword was received completely intact.", fill=GREEN_TEXT, font=font_regular)
    draw.text((555, 370), "Extracted Data: 100100", fill=AMBER, font=font_code_bold)

    # Corrupted Test Case Banner (bottom)
    draw_rounded_rect(draw, (30, 440, 970, 520), RED_BG, outline=RED_BORDER, radius=8)
    draw.text((50, 452), "✖ Tested Corrupted State: Received '100101001' (Bit 5 flipped from 0 -> 1)", fill=RED_TEXT, font=font_bold)
    draw.text((50, 480), "Receiver Remainder Check: crc('100101001', '1101') = '101' != '000'. Verdict: ERROR DETECTED (Data Corrupted).", fill=RED_TEXT, font=font_regular)

    img.save("fig_c2_mode1_binary.png")

# -----------------------------------------------------------------------------
# Figure C.3: Mode 2 - Text Input CRC Comparison
# -----------------------------------------------------------------------------
def create_fig_c3():
    img = Image.new("RGB", (1000, 520), NAVY)
    draw = ImageDraw.Draw(img)

    draw_rounded_rect(draw, (30, 20, 970, 85), CARD_BG, outline=BORDER, radius=10)
    draw.text((50, 32), "Mode 2: Text Input & CRC Value Direct Comparison", fill=TEXT_WHITE, font=font_heading)
    draw.text((50, 60), "Converts ASCII strings to 8-bit binary bitstreams and computes reference checksums. Direct match confirms authenticity.", fill=TEXT_MUTED, font=font_regular)

    # Left: Sender Text
    draw_rounded_rect(draw, (30, 100, 485, 370), CARD_BG, outline=BORDER, radius=10)
    draw.text((50, 118), "📤 Sender Text Message", fill=BLUE, font=font_bold)
    draw.line((50, 142, 465, 142), fill=BORDER, width=1)

    draw.text((50, 155), "Original Input Message:", fill=TEXT_WHITE, font=font_regular)
    draw_rounded_rect(draw, (50, 178, 465, 230), CODE_BG, outline=BORDER, radius=6)
    draw.text((65, 192), "Computer Networks CRC Verification Lab", fill=TEXT_WHITE, font=font_regular)

    draw.text((50, 245), "Sender 8-Bit Binary Stream (304 bits):", fill=TEXT_WHITE, font=font_regular)
    draw_rounded_rect(draw, (50, 268, 465, 305), CODE_BG, outline=BORDER, radius=6)
    draw.text((65, 278), "010000110110111101101101...01100010", fill=BLUE, font=font_code)

    draw.text((50, 318), "Sender CRC-8 Checksum:", fill=TEXT_WHITE, font=font_regular)
    draw_rounded_rect(draw, (50, 338, 465, 370), CODE_BG, outline=AMBER, radius=6)
    draw.text((65, 346), "00001000", fill=AMBER, font=font_code_bold)

    # Right: Receiver Text with Alteration
    draw_rounded_rect(draw, (515, 100, 970, 370), CARD_BG, outline=BORDER, radius=10)
    draw.text((535, 118), "📥 Receiver Received Text (Modified)", fill=RED_BORDER, font=font_bold)
    draw.line((535, 142, 950, 142), fill=BORDER, width=1)

    draw.text((535, 155), "Received Message (Typo in 'lab'):", fill=TEXT_WHITE, font=font_regular)
    draw_rounded_rect(draw, (535, 178, 950, 230), CODE_BG, outline=RED_BORDER, radius=6)
    draw.text((550, 192), "Computer Networks CRC Verification lab  [lowercase 'l']", fill="#FDA4AF", font=font_regular)

    draw.text((535, 245), "Receiver 8-Bit Binary Stream (304 bits):", fill=TEXT_WHITE, font=font_regular)
    draw_rounded_rect(draw, (535, 268, 950, 305), CODE_BG, outline=BORDER, radius=6)
    draw.text((550, 278), "010000110110111101101101...01100010", fill=BLUE, font=font_code)

    draw.text((535, 318), "Receiver CRC-8 Checksum:", fill=TEXT_WHITE, font=font_regular)
    draw_rounded_rect(draw, (535, 338, 950, 370), CODE_BG, outline=RED_BORDER, radius=6)
    draw.text((550, 346), "01001011", fill=RED_BORDER, font=font_code_bold)

    # Comparison Verdict Card
    draw_rounded_rect(draw, (30, 395, 970, 495), RED_BG, outline=RED_BORDER, radius=8)
    draw.text((50, 410), "✖ Integrity Verdict: Error Detected (Sender CRC != Receiver CRC)", fill=RED_TEXT, font=font_heading)
    draw.text((50, 442), "Sender CRC: 00001000   !=   Receiver CRC: 01001011", fill=TEXT_WHITE, font=font_code_bold)
    draw.text((50, 468), "A single-character case difference ('L' vs 'l') produces a totally divergent checksum remainder.", fill=RED_TEXT, font=font_regular)

    img.save("fig_c3_mode2_text.png")

# -----------------------------------------------------------------------------
# Figure C.4: Mode 3 - Attendance CSV File Integrity Audit
# -----------------------------------------------------------------------------
def create_fig_c4():
    img = Image.new("RGB", (1000, 560), NAVY)
    draw = ImageDraw.Draw(img)

    draw_rounded_rect(draw, (30, 20, 970, 85), CARD_BG, outline=BORDER, radius=10)
    draw.text((50, 32), "Mode 3: Attendance Record Integrity Auditor (Instructor Case Study)", fill=TEXT_WHITE, font=font_heading)
    draw.text((50, 60), "Evaluates original instructor CSV attendance files against audited files to detect tampered values or deleted rows.", fill=TEXT_MUTED, font=font_regular)

    # Left: Original File Preview
    draw_rounded_rect(draw, (30, 100, 485, 385), CARD_BG, outline=BORDER, radius=10)
    draw.text((50, 118), "📤 Original File: sample_attendance_original.csv", fill=BLUE, font=font_bold)
    draw.text((50, 140), "Reference CRC-8: 01111001  (Generator: 100000111)", fill=AMBER, font=font_code)
    draw.line((50, 165, 465, 165), fill=BORDER, width=1)

    table_headers = ["Student_ID", "Name", "Date", "Status"]
    sample_rows = [
        ["101", "Aarav Sharma", "2026-09-14", "Present"],
        ["102", "Bhavna Patel", "2026-09-14", "Present"],
        ["103", "Chirag Reddy", "2026-09-14", "Absent"],
        ["104", "Divya Nair", "2026-09-14", "Present"],
        ["105", "Eshwar Rao", "2026-09-14", "Present"],
    ]

    # Draw table
    y = 175
    draw.text((50, y), "ID    Name             Date        Status", fill=TEXT_MUTED, font=font_code_bold)
    draw.line((50, y + 18, 465, y + 18), fill=BORDER, width=1)
    y += 24
    for r in sample_rows:
        draw.text((50, y), f"{r[0]:<5} {r[1]:<16} {r[2]:<11} {r[3]}", fill=TEXT_WHITE, font=font_code)
        y += 22

    # Right: Audited Tampered File Preview
    draw_rounded_rect(draw, (515, 100, 970, 385), CARD_BG, outline=BORDER, radius=10)
    draw.text((535, 118), "📥 Audited File: sample_attendance_modified.csv", fill=RED_BORDER, font=font_bold)
    draw.text((535, 140), "Audited CRC-8:   11101000  [MISMATCH DETECTED]", fill=RED_BORDER, font=font_code_bold)
    draw.line((535, 165, 950, 165), fill=BORDER, width=1)

    tampered_rows = [
        ["101", "Aarav Sharma", "2026-09-14", "Present"],
        ["102", "Bhavna Patel", "2026-09-14", "Present"],
        ["103", "Chirag Reddy", "2026-09-14", "Present  *TAMPERED*"],
        ["104", "Divya Nair", "2026-09-14", "Present"],
        ["105", "Eshwar Rao", "2026-09-14", "Present"],
    ]
    y = 175
    draw.text((535, y), "ID    Name             Date        Status", fill=TEXT_MUTED, font=font_code_bold)
    draw.line((535, y + 18, 950, y + 18), fill=BORDER, width=1)
    y += 24
    for r in tampered_rows:
        color = RED_BORDER if "TAMPERED" in r[3] else TEXT_WHITE
        draw.text((535, y), f"{r[0]:<5} {r[1]:<16} {r[2]:<11} {r[3]}", fill=color, font=font_code)
        y += 22

    # Audit Verdict Box
    draw_rounded_rect(draw, (30, 405, 970, 535), RED_BG, outline=RED_BORDER, radius=8)
    draw.text((50, 420), "⚖️ Official Audit Verdict: TAMPERING DETECTED (Audit Result: FAIL)", fill=RED_TEXT, font=font_heading)
    draw.text((50, 452), "Original Reference CRC: 01111001   |   Audited File CRC: 11101000", fill=TEXT_WHITE, font=font_code_bold)
    draw.text((50, 478), "Discrepancy identified! Student 103 (Chirag Reddy) attendance was illegally modified from 'Absent' to 'Present'.", fill=RED_TEXT, font=font_regular)
    draw.text((50, 502), "📥 Timestamped Official Audit Report CSV generated and certified.", fill=AMBER, font=font_regular)

    img.save("fig_c4_mode3_attendance.png")

# -----------------------------------------------------------------------------
# Figure C.5: 24/7 GitHub Pages Live Deployment Interface
# -----------------------------------------------------------------------------
def create_fig_c5():
    img = Image.new("RGB", (1000, 480), NAVY)
    draw = ImageDraw.Draw(img)

    # Browser window chrome bar
    draw_rounded_rect(draw, (30, 20, 970, 70), "#334155", radius=8)
    draw.ellipse((45, 38, 57, 50), fill="#EF4444")
    draw.ellipse((65, 38, 77, 50), fill="#F59E0B")
    draw.ellipse((85, 38, 97, 50), fill="#10B981")

    # URL bar
    draw_rounded_rect(draw, (115, 30, 950, 58), CODE_BG, outline=BORDER, radius=6)
    draw.text((130, 36), "🔒 https://2503a52753-purna.github.io/CRC-Verification-Dashboard/", fill="#38BDF8", font=font_code)

    # Main Web App Body
    draw_rounded_rect(draw, (30, 80, 970, 450), CARD_BG, outline=BORDER, radius=8)
    draw.text((55, 105), "🛡️ CRC Engine — Integrity Suite (Live 24/7 on GitHub Pages)", fill=TEXT_WHITE, font=font_heading)
    draw.text((55, 135), "Zero-installation, client-side execution powered by pure JavaScript modulo-2 polynomial engine.", fill=TEXT_MUTED, font=font_regular)

    features = [
        ("Permanent 24/7 Availability", "Hosted directly on GitHub Pages with HTTPS encryption and global CDN distribution."),
        ("100% Algorithmic Fidelity", "Executes the identical bitwise modulo-2 polynomial division algorithm as the Python engine."),
        ("Multi-Scenario Auditing", "Built-in preset loaders for testing authentic CSV files, tampered records, and row deletion."),
        ("Automated CI/CD Deployment", "Every git push to the main branch automatically builds and updates the live site in seconds.")
    ]
    for i, (ftitle, fdesc) in enumerate(features):
        fy = 175 + i * 62
        draw_rounded_rect(draw, (55, fy, 945, fy + 52), CODE_BG, outline=BORDER, radius=6)
        draw.text((70, fy + 8), f"⚡ {ftitle}", fill=AMBER, font=font_bold)
        draw.text((70, fy + 28), fdesc, fill=TEXT_MUTED, font=font_regular)

    img.save("fig_c5_github_pages.png")

if __name__ == "__main__":
    create_fig_c1()
    create_fig_c2()
    create_fig_c3()
    create_fig_c4()
    create_fig_c5()
    print("All 5 Appendix C figures generated successfully!")
