/**
 * ============================================================================
 * CRC Dashboard - Client-Side Engine (Pure JavaScript)
 * Strictly adheres to the provided bitwise polynomial modulo-2 XOR algorithm.
 * No external libraries, no bit-flipping controls.
 * ============================================================================
 */

// ----------------------------------------------------------------------------
// 1. CORE ALGORITHMS (EXACT SAME LOGIC AS USER'S PYTHON CODE)
// ----------------------------------------------------------------------------

/**
 * Computes the CRC remainder using bitwise Modulo-2 XOR division.
 * Directly mirrors the user's Python crc(data, gen) function.
 */
function crc(data, gen) {
  const dataArr = data.split("");
  const limit = dataArr.length - gen.length + 1;

  for (let i = 0; i < limit; i++) {
    if (dataArr[i] === "1") {
      for (let j = 0; j < gen.length; j++) {
        dataArr[i + j] = String(Number(dataArr[i + j]) ^ Number(gen[j]));
      }
    }
  }

  const remainderLen = gen.length - 1;
  return dataArr.slice(-remainderLen).join("");
}

/**
 * Converts text into 8-bit ASCII binary string.
 * Directly mirrors the user's Python text_to_binary(text) function.
 */
function text_to_binary(text) {
  return Array.from(text)
    .map(char => char.charCodeAt(0).toString(2).padStart(8, "0"))
    .join("");
}

// ----------------------------------------------------------------------------
// 2. STANDARD GENERATOR POLYNOMIALS & STATE
// ----------------------------------------------------------------------------

const CRC_STANDARDS = {
  "CRC-3": "1011",
  "CRC-4": "10011",
  "CRC-8": "100000111",
  "CRC-32": "100000100110000010001110110110111",
};

// Baseline attendance dataset samples for Mode 3
const SAMPLE_CSV_ORIGINAL = `StudentID,Name,Course,Date,Status
101,Aarav Sharma,Computer Networks,2026-09-11,Present
102,Bhavna Patel,Computer Networks,2026-09-11,Present
103,Chirag Reddy,Computer Networks,2026-09-11,Absent
104,Divya Rao,Computer Networks,2026-09-11,Present
105,Eshwar Kumar,Computer Networks,2026-09-11,Present`;

const SAMPLE_CSV_TAMPERED = `StudentID,Name,Course,Date,Status
101,Aarav Sharma,Computer Networks,2026-09-11,Present
102,Bhavna Patel,Computer Networks,2026-09-11,Present
103,Chirag Reddy,Computer Networks,2026-09-11,Present
104,Divya Rao,Computer Networks,2026-09-11,Present
105,Eshwar Kumar,Computer Networks,2026-09-11,Present`;

const SAMPLE_CSV_DELETED = `StudentID,Name,Course,Date,Status
101,Aarav Sharma,Computer Networks,2026-09-11,Present
102,Bhavna Patel,Computer Networks,2026-09-11,Present
103,Chirag Reddy,Computer Networks,2026-09-11,Absent
104,Divya Rao,Computer Networks,2026-09-11,Present`;

let state = {
  selectedStandard: "CRC-8",
  gen: "100000111",
  crcLen: 8,
  
  // Mode 3 files state
  m3SenderName: "sample_attendance_original.csv",
  m3SenderContent: SAMPLE_CSV_ORIGINAL,
  m3ReceiverName: "sample_attendance_original.csv",
  m3ReceiverContent: SAMPLE_CSV_ORIGINAL,
  m3CustomReceiverContent: "",
  m3CustomReceiverName: "",
};

// ----------------------------------------------------------------------------
// 3. INITIALIZATION & SIDEBAR HANDLERS
// ----------------------------------------------------------------------------

document.addEventListener("DOMContentLoaded", () => {
  setupNavigation();
  setupSidebarControls();
  
  // Initialize calculations across all modes
  updateAllCalculations();
  
  // Setup Mode 1 listeners
  document.getElementById("m1SenderInput").addEventListener("input", updateMode1);
  document.getElementById("m1ReceiverInput").addEventListener("input", updateMode1Receiver);
  document.getElementById("m1SyncBtn").addEventListener("click", () => {
    const codeword = document.getElementById("m1CodewordDisplay").textContent;
    document.getElementById("m1ReceiverInput").value = codeword;
    updateMode1Receiver();
  });

  // Setup Mode 2 listeners
  document.getElementById("m2SenderText").addEventListener("input", updateMode2);
  document.getElementById("m2ReceiverText").addEventListener("input", updateMode2);

  // Setup Mode 3 listeners
  setupMode3Listeners();
});

function setupNavigation() {
  const tabs = document.querySelectorAll(".nav-tab");
  tabs.forEach(tab => {
    tab.addEventListener("click", () => {
      tabs.forEach(t => t.classList.remove("active"));
      tab.classList.add("active");

      const modeNum = tab.getAttribute("data-mode");
      document.querySelectorAll(".mode-view").forEach(v => v.classList.remove("active"));
      document.getElementById(`viewMode${modeNum}`).classList.add("active");
    });
  });
}

function setupSidebarControls() {
  const standardSelect = document.getElementById("crcStandardSelect");
  const generatorInput = document.getElementById("generatorInput");

  standardSelect.addEventListener("change", (e) => {
    state.selectedStandard = e.target.value;
    state.gen = CRC_STANDARDS[state.selectedStandard];
    generatorInput.value = state.gen;
    validateAndUpdateGenerator();
  });

  generatorInput.addEventListener("input", () => {
    validateAndUpdateGenerator();
  });
}

function validateAndUpdateGenerator() {
  const generatorInput = document.getElementById("generatorInput");
  const hint = document.getElementById("genValidationHint");
  const cleanVal = generatorInput.value.trim();

  // Validate: only 0 and 1, length >= 2
  const isValid = /^[01]{2,}$/.test(cleanVal);
  if (!isValid) {
    hint.textContent = "❌ Must be a binary string with at least 2 bits";
    hint.style.color = "#F43F5E";
    return;
  }

  hint.textContent = "Binary divisor string";
  hint.style.color = "#64748B";

  state.gen = cleanVal;
  state.crcLen = state.gen.length - 1;

  // Update spec card
  document.getElementById("specStandard").textContent = state.selectedStandard;
  document.getElementById("specGenLen").textContent = `${state.gen.length} bits`;
  document.getElementById("specCrcLen").textContent = `${state.crcLen} bits`;

  // Recalculate all 3 modes with the new generator
  updateAllCalculations();
}

function updateAllCalculations() {
  updateMode1();
  updateMode2();
  updateMode3();
}

// ----------------------------------------------------------------------------
// 4. MODE 1: BINARY INPUT (CODEWORD VERIFICATION)
// ----------------------------------------------------------------------------

function updateMode1() {
  const senderInput = document.getElementById("m1SenderInput").value.trim();
  const genDisplay = document.getElementById("m1GenDisplay");
  const paddedDisplay = document.getElementById("m1PaddedDisplay");
  const crcDisplay = document.getElementById("m1CrcDisplay");
  const codewordDisplay = document.getElementById("m1CodewordDisplay");

  genDisplay.textContent = state.gen;

  if (!/^[01]+$/.test(senderInput)) {
    paddedDisplay.textContent = "Invalid binary input";
    crcDisplay.textContent = "-";
    codewordDisplay.textContent = "-";
    return;
  }

  // Sender calculations
  const paddedData = senderInput + "0".repeat(state.crcLen);
  const senderCrc = crc(paddedData, state.gen);
  const codeword = senderInput + senderCrc;

  paddedDisplay.textContent = paddedData;
  crcDisplay.textContent = senderCrc;
  codewordDisplay.textContent = codeword;

  updateMode1Receiver();
}

function updateMode1Receiver() {
  const receiverInput = document.getElementById("m1ReceiverInput").value.trim();
  const remainderDisplay = document.getElementById("m1RemainderDisplay");
  const statusBanner = document.getElementById("m1StatusBanner");
  const statusText = document.getElementById("m1StatusText");
  const statusDetail = document.getElementById("m1StatusDetail");

  if (!/^[01]+$/.test(receiverInput) || receiverInput.length < state.gen.length) {
    remainderDisplay.textContent = "Requires at least " + state.gen.length + " bits";
    statusBanner.className = "status-banner error";
    statusText.textContent = "Status: Invalid / Incomplete Codeword";
    statusDetail.textContent = `Codeword must be a valid binary sequence of at least ${state.gen.length} bits.`;
    return;
  }

  const remainder = crc(receiverInput, state.gen);
  remainderDisplay.textContent = remainder;

  const isZeroRemainder = !remainder.includes("1"); // remainder is all zeros

  if (isZeroRemainder) {
    statusBanner.className = "status-banner success";
    statusText.textContent = "Status: No Error Detected";
    const extractedData = receiverInput.slice(0, -state.crcLen);
    statusDetail.innerHTML = `The remainder is zero. Transmission was completely error-free.<br><strong>Extracted Data:</strong> <code>${extractedData}</code>`;
  } else {
    statusBanner.className = "status-banner error";
    statusText.textContent = "Status: Error Detected (Data Corrupted)";
    statusDetail.innerHTML = `Remainder is non-zero (<code>${remainder}</code>). One or more bits were corrupted during transmission.`;
  }
}

// ----------------------------------------------------------------------------
// 5. MODE 2: TEXT INPUT (CRC COMPARISON)
// ----------------------------------------------------------------------------

function updateMode2() {
  const senderText = document.getElementById("m2SenderText").value;
  const receiverText = document.getElementById("m2ReceiverText").value;

  document.getElementById("m2GenDisplay").textContent = state.gen;

  // Sender calculations
  const senderBinary = text_to_binary(senderText);
  const senderCrc = senderBinary ? crc(senderBinary + "0".repeat(state.crcLen), state.gen) : "0".repeat(state.crcLen);

  document.getElementById("m2SenderBits").textContent = senderBinary.length;
  document.getElementById("m2SenderBinary").textContent = senderBinary || "Empty";
  document.getElementById("m2SenderCrc").textContent = senderCrc;

  // Receiver calculations
  const receiverBinary = text_to_binary(receiverText);
  const receiverCrc = receiverBinary ? crc(receiverBinary + "0".repeat(state.crcLen), state.gen) : "0".repeat(state.crcLen);

  document.getElementById("m2ReceiverBits").textContent = receiverBinary.length;
  document.getElementById("m2ReceiverBinary").textContent = receiverBinary || "Empty";
  document.getElementById("m2ReceiverCrc").textContent = receiverCrc;

  // Comparison Verdict
  const statusBanner = document.getElementById("m2StatusBanner");
  const statusText = document.getElementById("m2StatusText");
  const statusDetail = document.getElementById("m2StatusDetail");

  if (senderCrc === receiverCrc) {
    statusBanner.className = "status-banner success";
    statusText.textContent = "Status: No Error Detected (Sender CRC == Receiver CRC)";
    statusDetail.innerHTML = `Both checksums match perfectly (<code>${senderCrc}</code>). The text message is authentic and completely intact.`;
  } else {
    statusBanner.className = "status-banner error";
    statusText.textContent = "Status: Error Detected (Sender CRC != Receiver CRC)";
    statusDetail.innerHTML = `Checksum discrepancy detected!<br><strong>Sender CRC:</strong> <code>${senderCrc}</code> &nbsp;|&nbsp; <strong>Receiver CRC:</strong> <code>${receiverCrc}</code>`;
  }
}

// ----------------------------------------------------------------------------
// 6. MODE 3: FILE INPUT (ATTENDANCE CSV INTEGRITY AUDIT)
// ----------------------------------------------------------------------------

function setupMode3Listeners() {
  // Sender file upload
  document.getElementById("m3SenderFileInput").addEventListener("change", (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (event) => {
      state.m3SenderName = file.name;
      state.m3SenderContent = event.target.result;
      document.getElementById("m3SenderFileName").textContent = file.name;
      updateMode3();
    };
    reader.readAsText(file);
  });

  // Scenario presets
  const scenarioRadios = document.querySelectorAll("input[name='m3Scenario']");
  const customUploadArea = document.getElementById("m3CustomUploadArea");

  scenarioRadios.forEach(radio => {
    radio.addEventListener("change", (e) => {
      const choice = e.target.value;
      if (choice === "authentic") {
        state.m3ReceiverName = state.m3SenderName;
        state.m3ReceiverContent = state.m3SenderContent;
        customUploadArea.style.display = "none";
      } else if (choice === "tampered") {
        state.m3ReceiverName = "sample_attendance_modified.csv";
        state.m3ReceiverContent = SAMPLE_CSV_TAMPERED;
        customUploadArea.style.display = "none";
      } else if (choice === "deleted") {
        state.m3ReceiverName = "sample_attendance_deleted_row.csv";
        state.m3ReceiverContent = SAMPLE_CSV_DELETED;
        customUploadArea.style.display = "none";
      } else if (choice === "custom") {
        customUploadArea.style.display = "block";
        if (state.m3CustomReceiverContent) {
          state.m3ReceiverName = state.m3CustomReceiverName;
          state.m3ReceiverContent = state.m3CustomReceiverContent;
        }
      }
      document.getElementById("m3ReceiverFileName").textContent = state.m3ReceiverName;
      updateMode3();
    });
  });

  // Custom receiver file upload
  document.getElementById("m3ReceiverFileInput").addEventListener("change", (e) => {
    const file = e.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (event) => {
      state.m3CustomReceiverName = file.name;
      state.m3CustomReceiverContent = event.target.result;
      state.m3ReceiverName = file.name;
      state.m3ReceiverContent = event.target.result;
      document.getElementById("m3ReceiverFileName").textContent = file.name;
      updateMode3();
    };
    reader.readAsText(file);
  });

  // Download official audit report
  document.getElementById("m3DownloadBtn").addEventListener("click", downloadAuditReport);
}

function updateMode3() {
  // 1. Calculate Sender CRC
  const senderBinary = text_to_binary(state.m3SenderContent);
  const senderCrc = senderBinary ? crc(senderBinary + "0".repeat(state.crcLen), state.gen) : "0".repeat(state.crcLen);
  document.getElementById("m3SenderCrc").textContent = senderCrc;
  renderCsvTable(state.m3SenderContent, "m3SenderTableContainer");

  // 2. Calculate Receiver CRC
  const receiverBinary = text_to_binary(state.m3ReceiverContent);
  const receiverCrc = receiverBinary ? crc(receiverBinary + "0".repeat(state.crcLen), state.gen) : "0".repeat(state.crcLen);
  document.getElementById("m3ReceiverCrc").textContent = receiverCrc;
  renderCsvTable(state.m3ReceiverContent, "m3ReceiverTableContainer");

  // 3. Verdict
  const isMatch = (senderCrc === receiverCrc);
  const statusBanner = document.getElementById("m3StatusBanner");
  const statusText = document.getElementById("m3StatusText");
  const statusDetail = document.getElementById("m3StatusDetail");

  if (isMatch) {
    statusBanner.className = "status-banner success";
    statusText.textContent = "Official Audit Result: PASS (Authentic)";
    statusDetail.innerHTML = `The audited attendance record is 100% identical to the original instructor copy.<br>
      Checksum Match: <code>${senderCrc}</code> == <code>${receiverCrc}</code>.<br>
      No attendance values or rows were changed or deleted during storage or transfer.`;
  } else {
    statusBanner.className = "status-banner error";
    statusText.textContent = "Official Audit Result: FAIL (Tampering / Row Deletion Detected)";
    statusDetail.innerHTML = `Checksum discrepancy detected between the original record and the audited file!<br>
      <strong>Original CRC:</strong> <code>${senderCrc}</code> &nbsp;|&nbsp; <strong>Audited CRC:</strong> <code>${receiverCrc}</code><br>
      One or more student attendance values, names, or rows have been altered or deleted!`;
  }
}

function renderCsvTable(csvText, containerId) {
  const container = document.getElementById(containerId);
  if (!csvText || !csvText.trim()) {
    container.innerHTML = "<div style='padding: 10px; color: #64748B;'>Empty file</div>";
    return;
  }

  const lines = csvText.trim().split("\n");
  if (lines.length === 0) return;

  let html = "<table class='preview-table'><thead><tr>";
  const headers = lines[0].split(",");
  headers.forEach(h => {
    html += `<th>${escapeHtml(h.trim())}</th>`;
  });
  html += "</tr></thead><tbody>";

  for (let i = 1; i < lines.length; i++) {
    if (!lines[i].trim()) continue;
    html += "<tr>";
    const cols = lines[i].split(",");
    cols.forEach(c => {
      html += `<td>${escapeHtml(c.trim())}</td>`;
    });
    html += "</tr>";
  }
  html += "</tbody></table>";
  container.innerHTML = html;
}

function downloadAuditReport() {
  const senderCrc = document.getElementById("m3SenderCrc").textContent;
  const receiverCrc = document.getElementById("m3ReceiverCrc").textContent;
  const isMatch = (senderCrc === receiverCrc);
  const timestamp = new Date().toISOString().replace("T", " ").substring(0, 19);

  const reportCsv = [
    "Audit Timestamp,Original File,Audited File,CRC Standard,Generator,Original CRC,Audited CRC,Audit Verdict,Details",
    `"${timestamp}","${state.m3SenderName}","${state.m3ReceiverName}","${state.selectedStandard}","${state.gen}","${senderCrc}","${receiverCrc}","${isMatch ? "PASS (Authentic)" : "FAIL (Tampered)"}","${isMatch ? "File content 100% identical." : "Discrepancy in file content or missing rows."}"`
  ].join("\n");

  const blob = new Blob([reportCsv], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.setAttribute("href", url);
  link.setAttribute("download", `crc_audit_report_${state.selectedStandard.toLowerCase()}.csv`);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

function escapeHtml(text) {
  const map = {
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#039;",
  };
  return text.replace(/[&<>"']/g, m => map[m]);
}
