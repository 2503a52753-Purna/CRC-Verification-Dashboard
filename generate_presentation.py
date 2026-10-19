"""
Generate a professional 8-slide PowerPoint presentation summarizing the
CRC Verification & Attendance File Integrity Audit Dashboard.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Color definitions
    NAVY = RGBColor(15, 23, 42)        # #0F172A
    CARD_BG = RGBColor(30, 41, 59)     # #1E293B
    LIGHT_BG = RGBColor(248, 250, 252) # #F8FAFC
    LIGHT_CARD = RGBColor(255, 255, 255)
    BORDER_COLOR = RGBColor(203, 213, 225) # #CBD5E1
    
    TEXT_MAIN = RGBColor(15, 23, 42)
    TEXT_MUTED = RGBColor(100, 116, 139)
    ACCENT_BLUE = RGBColor(2, 132, 199)    # #0284C7
    ACCENT_GREEN = RGBColor(16, 185, 129)  # #10B981
    ACCENT_RED = RGBColor(239, 68, 68)     # #EF4444
    ACCENT_AMBER = RGBColor(245, 158, 11)  # #F59E0B
    WHITE = RGBColor(255, 255, 255)

    blank_layout = prs.slide_layouts[6]

    def add_header(slide, title_text, category_text="CRC DASHBOARD SUMMARY"):
        # Header background banner
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(1.1))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p_cat = tf.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = ACCENT_BLUE
        
        p_title = tf.add_paragraph()
        p_title.text = title_text
        p_title.font.size = Pt(24)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_MAIN

    # -------------------------------------------------------------------------
    # SLIDE 1: Title Slide (Dark Theme)
    # -------------------------------------------------------------------------
    slide1 = prs.slides.add_slide(blank_layout)
    bg1 = slide1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = NAVY
    bg1.line.fill.background()

    # Title Card container
    title_box = slide1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(3.8))
    tf1 = title_box.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "NETWORK SECURITY & DATA INTEGRITY"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = ACCENT_BLUE

    p1 = tf1.add_paragraph()
    p1.text = "Cyclic Redundancy Check (CRC)\n& Attendance File Auditor"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = WHITE
    p1.space_before = Pt(12)

    p2 = tf1.add_paragraph()
    p2.text = "Bitwise Polynomial Verification Dashboard | 3 Operating Modes | CSV File Tampering Detection"
    p2.font.size = Pt(16)
    p2.font.color.rgb = RGBColor(148, 163, 184)
    p2.space_before = Pt(16)

    # 3 Badges at the bottom
    badges = [
        ("Pure Python XOR Engine", "Zero external CRC libraries"),
        ("Zero Bit-Flipping", "Natural verification testing"),
        ("Attendance Audit Case", "Detects row deletion & edits")
    ]
    for i, (b_title, b_sub) in enumerate(badges):
        bx = Inches(1.0 + i * 3.9)
        by = Inches(5.6)
        card = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, bx, by, Inches(3.5), Inches(1.1))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = RGBColor(51, 65, 85)
        
        ctf = card.text_frame
        ctf.word_wrap = True
        ctf.margin_top = Inches(0.18)
        cp1 = ctf.paragraphs[0]
        cp1.text = b_title
        cp1.font.bold = True
        cp1.font.size = Pt(13)
        cp1.font.color.rgb = WHITE
        
        cp2 = ctf.add_paragraph()
        cp2.text = b_sub
        cp2.font.size = Pt(11)
        cp2.font.color.rgb = RGBColor(148, 163, 184)

    # -------------------------------------------------------------------------
    # SLIDE 2: Problem Statement & Case Study Context
    # -------------------------------------------------------------------------
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(slide2, "The Real-World Challenge: Attendance Record Integrity", "BACKGROUND & CONTEXT")

    # Left Box: Problem
    card_prob = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
    card_prob.fill.solid()
    card_prob.fill.fore_color.rgb = LIGHT_BG
    card_prob.line.color.rgb = BORDER_COLOR
    
    tf_p = card_prob.text_frame
    tf_p.word_wrap = True
    tf_p.margin_left = tf_p.margin_right = Inches(0.4)
    tf_p.margin_top = Inches(0.4)
    
    p = tf_p.paragraphs[0]
    p.text = "⚠️ The Dilemma (Classroom Scenario)"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = ACCENT_RED
    
    items_prob = [
        "Instructor generates a CSV attendance file immediately after class.",
        "During storage, network transfer, or handling by intermediaries, values or rows may be altered or deleted.",
        "Manual line-by-line inspection is tedious, error-prone, and unscalable for large student cohorts.",
        "How can the instructor audit the file to determine whether it remains 100% identical to the original?"
    ]
    for it in items_prob:
        pi = tf_p.add_paragraph()
        pi.text = "• " + it
        pi.font.size = Pt(13)
        pi.font.color.rgb = TEXT_MAIN
        pi.space_before = Pt(12)

    # Right Box: Solution
    card_sol = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0))
    card_sol.fill.solid()
    card_sol.fill.fore_color.rgb = LIGHT_BG
    card_sol.line.color.rgb = BORDER_COLOR
    
    tf_s = card_sol.text_frame
    tf_s.word_wrap = True
    tf_s.margin_left = tf_s.margin_right = Inches(0.4)
    tf_s.margin_top = Inches(0.4)
    
    p = tf_s.paragraphs[0]
    p.text = "🛡️ The Solution: Cyclic Redundancy Check (CRC)"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN
    
    items_sol = [
        "Cryptographic-like mathematical fingerprint generated using bitwise polynomial modulo-2 division.",
        "Reference CRC: Computed on pristine original attendance file right after generation.",
        "Audited CRC: Computed on received file at any point during later storage or audit.",
        "Instant Verification: CRC match proves file authenticity; any bit mismatch immediately flags tampering!"
    ]
    for it in items_sol:
        pi = tf_s.add_paragraph()
        pi.text = "• " + it
        pi.font.size = Pt(13)
        pi.font.color.rgb = TEXT_MAIN
        pi.space_before = Pt(12)

    # -------------------------------------------------------------------------
    # SLIDE 3: What is CRC & How Does It Work?
    # -------------------------------------------------------------------------
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(slide3, "Core Mechanics of Cyclic Redundancy Check (CRC)", "THEORETICAL FOUNDATION")

    col_w = Inches(3.7)
    gap = Inches(0.3)
    y_pos = Inches(1.8)
    h_pos = Inches(5.0)

    steps = [
        ("1. Modulo-2 XOR Arithmetic",
         "Binary Division Without Carries",
         [
             "CRC uses binary modulo-2 arithmetic.",
             "Addition and subtraction are identical to bitwise XOR (^).",
             "1 ^ 1 = 0,  0 ^ 0 = 0",
             "1 ^ 0 = 1,  0 ^ 1 = 1",
             "Eliminates complex carries, making hardware and software execution ultrafast."
         ], ACCENT_BLUE),
        ("2. The Polynomial Formula",
         "D(x) · 2^k + R(x) = C(x)",
         [
             "Data bits D are padded with k zeros, where k = len(G) - 1.",
             "The padded stream is divided by Generator Polynomial G(x).",
             "The division remainder R(x) is the CRC checksum.",
             "Transmitted Codeword = Data + Remainder."
         ], ACCENT_AMBER),
        ("3. Receiver Verification",
         "Remainder Check Condition",
         [
             "Receiver receives the codeword and divides by the exact same G(x).",
             "If Remainder == 0:",
             "  -> No error detected! Codeword is authentic.",
             "If Remainder != 0:",
             "  -> Corrupted! Flag tampering immediately."
         ], ACCENT_GREEN),
    ]

    for i, (title, sub, bullet_list, accent) in enumerate(steps):
        cx = Inches(0.8 + i * (3.7 + 0.3))
        card = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, y_pos, col_w, h_pos)
        card.fill.solid()
        card.fill.fore_color.rgb = LIGHT_BG
        card.line.color.rgb = BORDER_COLOR
        
        ctf = card.text_frame
        ctf.word_wrap = True
        ctf.margin_left = ctf.margin_right = Inches(0.3)
        ctf.margin_top = Inches(0.3)
        
        p = ctf.paragraphs[0]
        p.text = title
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = accent
        
        p_sub = ctf.add_paragraph()
        p_sub.text = sub
        p_sub.font.size = Pt(11)
        p_sub.font.bold = True
        p_sub.font.color.rgb = TEXT_MUTED
        p_sub.space_before = Pt(4)
        
        for b in bullet_list:
            pb = ctf.add_paragraph()
            pb.text = "• " + b if not b.startswith("  ") else b
            pb.font.size = Pt(12)
            pb.font.color.rgb = TEXT_MAIN
            pb.space_before = Pt(8)

    # -------------------------------------------------------------------------
    # SLIDE 4: CRC Standard Types & Generators
    # -------------------------------------------------------------------------
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(slide4, "Supported CRC Standards & Generator Polynomials", "SYSTEM CONFIGURATION")

    crc_cards = [
        ("CRC-3", "3 Bits", "1011", "x³ + x + 1", "Educational / Telemetry",
         "Compact 3-bit checksum used for demonstrating polynomial division fundamentals."),
        ("CRC-4", "4 Bits", "10011", "x⁴ + x + 1", "ITU G.704 Framing",
         "4-bit CRC standard widely used in digital telecommunications and framing systems."),
        ("CRC-8", "8 Bits", "100000111", "x⁸ + x² + x + 1", "ATM / Sensor Protocols",
         "1-byte checksum delivering robust burst error detection for text and structured files."),
        ("CRC-32", "32 Bits", "100000100110000010001110110110111", "IEEE 802.3 Standard", "Ethernet / ZIP / PNG",
         "Industry-standard 32-bit polynomial detecting 99.9999999% of all transmission errors.")
    ]

    for i, (name, length, gen_str, poly, usage, desc) in enumerate(crc_cards):
        cx = Inches(0.8 + (i % 2) * 5.9)
        cy = Inches(1.8 + (i // 2) * 2.6)
        card = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, cy, Inches(5.6), Inches(2.3))
        card.fill.solid()
        card.fill.fore_color.rgb = LIGHT_BG
        card.line.color.rgb = BORDER_COLOR
        
        ctf = card.text_frame
        ctf.word_wrap = True
        ctf.margin_left = ctf.margin_right = Inches(0.3)
        ctf.margin_top = Inches(0.2)
        
        p = ctf.paragraphs[0]
        p.text = f"{name}  ({length} Checksum)"
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = ACCENT_BLUE
        
        p2 = ctf.add_paragraph()
        p2.text = f"Polynomial: {poly}  |  Standard: {usage}"
        p2.font.size = Pt(11)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_MUTED
        p2.space_before = Pt(3)
        
        p3 = ctf.add_paragraph()
        p3.text = f"Generator 'gen': {gen_str}"
        p3.font.size = Pt(11)
        p3.font.color.rgb = ACCENT_AMBER
        p3.space_before = Pt(4)

        p4 = ctf.add_paragraph()
        p4.text = desc
        p4.font.size = Pt(11)
        p4.font.color.rgb = TEXT_MAIN
        p4.space_before = Pt(4)

    # -------------------------------------------------------------------------
    # SLIDE 5: Mode 1 - Binary Input (Codeword Method)
    # -------------------------------------------------------------------------
    slide5 = prs.slides.add_slide(blank_layout)
    add_header(slide5, "Mode 1: Binary Input & Codeword Verification", "OPERATING MODE 1")

    # Left column: Sender
    c_s = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(5.6), Inches(5.0))
    c_s.fill.solid()
    c_s.fill.fore_color.rgb = LIGHT_BG
    c_s.line.color.rgb = BORDER_COLOR
    
    tf = c_s.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.4)
    tf.margin_top = Inches(0.3)
    
    p = tf.paragraphs[0]
    p.text = "📤 Sender Side: Codeword Generation"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = ACCENT_BLUE

    steps_s = [
        "Input: User provides raw binary string, e.g. 100100.",
        "Zero Padding: Padded with k zeros: new_data = data + '0'*crc_len.",
        "CRC Generation: Calculated using pure bitwise XOR: sender_crc = crc(new_data, gen).",
        "Transmitted Codeword: Formed by appending CRC: codeword = data + sender_crc.",
        "Example Output:",
        "  • Data: 100100  |  Gen: 1101 (CRC-3)",
        "  • Sender CRC: 001",
        "  • Codeword: 100100001"
    ]
    for s in steps_s:
        p_item = tf.add_paragraph()
        p_item.text = s
        p_item.font.size = Pt(12)
        p_item.font.color.rgb = TEXT_MAIN
        p_item.space_before = Pt(6)

    # Right column: Receiver
    c_r = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.8), Inches(5.6), Inches(5.0))
    c_r.fill.solid()
    c_r.fill.fore_color.rgb = LIGHT_BG
    c_r.line.color.rgb = BORDER_COLOR
    
    tf2 = c_r.text_frame
    tf2.word_wrap = True
    tf2.margin_left = tf2.margin_right = Inches(0.4)
    tf2.margin_top = Inches(0.3)
    
    p = tf2.paragraphs[0]
    p.text = "📥 Receiver Side: Remainder Verification"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN

    steps_r = [
        "Input: Receives binary codeword (manual entry or direct test).",
        "Remainder Division: remainder = crc(received_codeword, gen).",
        "Deterministic Error Check:",
        "  • If int(remainder, 2) == 0:",
        "     ✔ Status: No Error Detected",
        "     Extracted Data: received_codeword[:-crc_len]",
        "  • If int(remainder, 2) != 0:",
        "     ✖ Status: Error Detected (Data Corrupted)",
        "Strict Policy: No artificial flipping! Receiver evaluates authentic input."
    ]
    for s in steps_r:
        p_item = tf2.add_paragraph()
        p_item.text = s
        p_item.font.size = Pt(12)
        p_item.font.color.rgb = ACCENT_RED if "Error Detected (Data Corrupted)" in s else (ACCENT_GREEN if "No Error Detected" in s else TEXT_MAIN)
        p_item.space_before = Pt(6)

    # -------------------------------------------------------------------------
    # SLIDE 6: Mode 2 - Text Input (CRC Value Comparison)
    # -------------------------------------------------------------------------
    slide6 = prs.slides.add_slide(blank_layout)
    add_header(slide6, "Mode 2: Text Input & CRC Value Comparison", "OPERATING MODE 2")

    top_banner = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.8), Inches(11.7), Inches(1.3))
    top_banner.fill.solid()
    top_banner.fill.fore_color.rgb = LIGHT_BG
    top_banner.line.color.rgb = BORDER_COLOR
    
    tb_tf = top_banner.text_frame
    tb_tf.word_wrap = True
    tb_tf.margin_left = Inches(0.3)
    tb_tf.margin_top = Inches(0.18)
    
    p = tb_tf.paragraphs[0]
    p.text = "🔤 Text to 8-Bit Binary Conversion: text_to_binary(text)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_BLUE

    p2 = tb_tf.add_paragraph()
    p2.text = "Converts every character into an 8-bit ASCII bitstream: ''.join(format(ord(char), '08b') for char in text). Enables arbitrary natural language strings to be mathematically processed by polynomial division."
    p2.font.size = Pt(12)
    p2.font.color.rgb = TEXT_MAIN
    p2.space_before = Pt(4)

    # Left Card: Matching text
    c1 = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.3), Inches(5.6), Inches(3.5))
    c1.fill.solid()
    c1.fill.fore_color.rgb = LIGHT_BG
    c1.line.color.rgb = RGBColor(16, 185, 129)
    
    ctf1 = c1.text_frame
    ctf1.word_wrap = True
    ctf1.margin_left = ctf1.margin_right = Inches(0.3)
    ctf1.margin_top = Inches(0.25)
    
    p = ctf1.paragraphs[0]
    p.text = "✔ Case A: Identical Text (No Error)"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_GREEN

    pts1 = [
        "Sender Text: 'Computer Networks CRC Lab'",
        "Receiver Text: 'Computer Networks CRC Lab'",
        "Sender CRC: 00001000",
        "Receiver CRC: 00001000",
        "Verdict: Sender CRC == Receiver CRC",
        "Result: No Error Detected (Data authentic)"
    ]
    for pt in pts1:
        pi = ctf1.add_paragraph()
        pi.text = "• " + pt
        pi.font.size = Pt(12)
        pi.font.color.rgb = TEXT_MAIN
        pi.space_before = Pt(4)

    # Right Card: Mismatched text
    c2 = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(3.3), Inches(5.6), Inches(3.5))
    c2.fill.solid()
    c2.fill.fore_color.rgb = LIGHT_BG
    c2.line.color.rgb = RGBColor(239, 68, 68)
    
    ctf2 = c2.text_frame
    ctf2.word_wrap = True
    ctf2.margin_left = ctf2.margin_right = Inches(0.3)
    ctf2.margin_top = Inches(0.25)
    
    p = ctf2.paragraphs[0]
    p.text = "✖ Case B: Single Typo / Alteration"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = ACCENT_RED

    pts2 = [
        "Sender Text: 'Computer Networks CRC Lab'",
        "Receiver Text: 'Computer Networks CRC lab' (lowercase 'l')",
        "Sender CRC: 00001000",
        "Receiver CRC: 01001011",
        "Verdict: Sender CRC != Receiver CRC",
        "Result: Error Detected! 1-bit text shift creates completely different remainder."
    ]
    for pt in pts2:
        pi = ctf2.add_paragraph()
        pi.text = "• " + pt
        pi.font.size = Pt(12)
        pi.font.color.rgb = TEXT_MAIN
        pi.space_before = Pt(4)

    # -------------------------------------------------------------------------
    # SLIDE 7: Mode 3 - File Input & Attendance CSV Audit
    # -------------------------------------------------------------------------
    slide7 = prs.slides.add_slide(blank_layout)
    add_header(slide7, "Mode 3: File Input & Attendance CSV Audit", "OPERATING MODE 3")

    cards_m3 = [
        ("Test 1: Pristine Original Record", "AUTHENTIC RECORD VERIFICATION",
         "Original file compared against itself or uncorrupted copy.",
         "Original CRC: 01111001\nAudited CRC:  01111001",
         "Verdict: PASS (No Error Detected)", ACCENT_GREEN),
        ("Test 2: Attendance Status Tampered", "DETECTING ACCIDENTAL MODIFICATION",
         "Student 103 status changed from 'Absent' to 'Present'.",
         "Original CRC: 01111001\nAudited CRC:  11101000",
         "Verdict: FAIL (Tampering Detected)", ACCENT_RED),
        ("Test 3: Student Row Deleted", "DETECTING ACCIDENTAL ROW REMOVAL",
         "Student 105 row removed during transfer.",
         "Original CRC: 01111001\nAudited CRC:  10011110",
         "Verdict: FAIL (Row Deletion Detected)", ACCENT_AMBER),
    ]

    for i, (m_title, m_cat, m_desc, m_crc, m_verdict, m_color) in enumerate(cards_m3):
        cx = Inches(0.8 + i * 4.0)
        card = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, Inches(1.8), Inches(3.7), Inches(4.0))
        card.fill.solid()
        card.fill.fore_color.rgb = LIGHT_BG
        card.line.color.rgb = m_color
        
        ctf = card.text_frame
        ctf.word_wrap = True
        ctf.margin_left = ctf.margin_right = Inches(0.25)
        ctf.margin_top = Inches(0.25)
        
        p = ctf.paragraphs[0]
        p.text = m_title
        p.font.size = Pt(15)
        p.font.bold = True
        p.font.color.rgb = m_color
        
        p2 = ctf.add_paragraph()
        p2.text = m_cat
        p2.font.size = Pt(9)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_MUTED
        p2.space_before = Pt(3)

        p3 = ctf.add_paragraph()
        p3.text = m_desc
        p3.font.size = Pt(11)
        p3.font.color.rgb = TEXT_MAIN
        p3.space_before = Pt(8)

        p4 = ctf.add_paragraph()
        p4.text = m_crc
        p4.font.size = Pt(11)
        p4.font.bold = True
        p4.font.color.rgb = NAVY
        p4.space_before = Pt(12)

        p5 = ctf.add_paragraph()
        p5.text = m_verdict
        p5.font.size = Pt(12)
        p5.font.bold = True
        p5.font.color.rgb = m_color
        p5.space_before = Pt(12)

    # Bottom Callout: Audit Report
    b_card = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(6.0), Inches(11.7), Inches(0.9))
    b_card.fill.solid()
    b_card.fill.fore_color.rgb = NAVY
    b_card.line.fill.background()
    
    b_tf = b_card.text_frame
    b_tf.word_wrap = True
    b_tf.margin_left = Inches(0.4)
    b_tf.margin_top = Inches(0.18)
    
    bp1 = b_tf.paragraphs[0]
    bp1.text = "📊 Audit Trail & CSV Report Generation"
    bp1.font.size = Pt(13)
    bp1.font.bold = True
    bp1.font.color.rgb = WHITE

    bp2 = b_tf.add_paragraph()
    bp2.text = "Instructors can download timestamped verification reports (CSV) certifying file integrity for administrative compliance."
    bp2.font.size = Pt(11)
    bp2.font.color.rgb = RGBColor(148, 163, 184)

    # -------------------------------------------------------------------------
    # SLIDE 8: Architecture, Rules & Summary
    # -------------------------------------------------------------------------
    slide8 = prs.slides.add_slide(blank_layout)
    add_header(slide8, "Architecture Summary & Key Takeaways", "CONCLUSION & HIGHLIGHTS")

    pillars = [
        ("Strict Implementation Rules",
         [
             "100% Pure Python XOR Engine: Zero external CRC libraries (no zlib / hashlib).",
             "Strict adherence to provided crc() and text_to_binary() functions.",
             "No Bit-Flipping Controls: Evaluates natural user inputs and authentic files without synthetic flipping shortcuts."
         ], ACCENT_BLUE),
        ("Dashboard Features",
         [
             "Dynamic CRC selection (CRC-3, CRC-4, CRC-8, CRC-32) + Custom generator input.",
             "Multi-mode switching: Binary Codeword, Text Comparison, and File Attendance Audit.",
             "Live tabular preview of CSV records & instant visual audit verdicts."
         ], ACCENT_GREEN),
        ("Key Educational Takeaways",
         [
             "CRC provides mathematical certainty for detecting accidental transmission errors.",
             "Solves the instructor's classroom dilemma: audits files reliably without manual overhead.",
             "All 3 modes verified with automated unit tests (test_crc_rules.py)."
         ], ACCENT_AMBER)
    ]

    for i, (p_title, p_bullets, p_col) in enumerate(pillars):
        cx = Inches(0.8 + i * 4.0)
        card = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx, Inches(1.8), Inches(3.7), Inches(5.0))
        card.fill.solid()
        card.fill.fore_color.rgb = LIGHT_BG
        card.line.color.rgb = BORDER_COLOR
        
        ctf = card.text_frame
        ctf.word_wrap = True
        ctf.margin_left = ctf.margin_right = Inches(0.3)
        ctf.margin_top = Inches(0.3)
        
        p = ctf.paragraphs[0]
        p.text = p_title
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = p_col
        
        for b in p_bullets:
            pb = ctf.add_paragraph()
            pb.text = "• " + b
            pb.font.size = Pt(12)
            pb.font.color.rgb = TEXT_MAIN
            pb.space_before = Pt(10)

    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "crc_dashboard_summary.pptx")
    prs.save(output_path)
    print(f"Presentation successfully created at: {output_path}")

if __name__ == "__main__":
    create_presentation()
