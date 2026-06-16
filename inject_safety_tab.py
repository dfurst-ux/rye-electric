#!/usr/bin/env python3
"""
Rye Electric — Safety Tab Injector
====================================
Run this script from the root of your rye-electric repo.
It will inject the Safety tab (button + panel + CSS + JS) into all 11 trackers.

Usage:
    python3 inject_safety_tab.py

Each file is backed up as filename.html.bak before modification.
"""

import os
import re
import shutil

# ── Files to patch ────────────────────────────────────────────────────────────
TRACKERS = [
    "rye-electric-field-tracker-24001-biola.html",
    "rye-electric-field-tracker-24002-sepulveda.html",
    "rye-electric-field-tracker-24005-vnv.html",
    "rye-electric-field-tracker-24006-vf.html",
    "rye-electric-field-tracker-24010-commons.html",
    "rye-electric-field-tracker-25001-decena.html",
    "rye-electric-field-tracker-25002-bah.html",
    "rye-electric-field-tracker-26002-wilshire.html",
    "rye-electric-field-tracker-sp25018-cdc.html",
    "rye-electric-field-tracker-26003-carina.html",
    "rye-electric-field-tracker-26005-marina-shores.html",
]

# ── Safety tab button ─────────────────────────────────────────────────────────
TAB_BUTTON = """
    <button class="tab-btn safety-tab-btn" onclick="showTab('safety')" id="tab-btn-safety">
      🛡️ Safety
      <span class="safety-friday-badge" id="safetyFridayBadge" style="display:none;">Required</span>
    </button>"""

# ── Safety tab panel ──────────────────────────────────────────────────────────
TAB_PANEL = """
  <!-- ═══════════════ SAFETY TAB PANEL ═══════════════ -->
  <div id="tab-safety" class="tab-panel" style="display:none;">

    <div class="safety-header">
      <h2>Safety Documentation</h2>
      <div class="safety-meta">
        <span id="safetyDateDisplay"></span>
        <span id="safetyFridayNotice" class="safety-required-badge" style="display:none;">📋 Friday — All 3 forms required</span>
        <span id="safetyOptionalNotice" class="safety-optional-badge" style="display:none;">Optional today — required on Fridays</span>
      </div>
      <div id="safetySubmittedBanner" class="safety-submitted-banner" style="display:none;">
        ✅ Safety forms submitted for this week — <span id="safetySubmittedBy"></span>
      </div>
    </div>

    <!-- WJSI -->
    <div class="safety-form-card" id="wjsiCard">
      <div class="safety-form-header" onclick="toggleSafetySection('wjsi')">
        <span class="safety-form-icon">📋</span>
        <div>
          <div class="safety-form-title">Weekly Jobsite Safety Inspection</div>
          <div class="safety-form-subtitle">WJSI · Required at start of job and weekly thereafter</div>
        </div>
        <span class="safety-check-status" id="wjsiStatus">—</span>
        <span class="safety-chevron" id="wjsiChevron">▼</span>
      </div>
      <div class="safety-form-body" id="wjsiBody">
        <div class="safety-checklist-grid">
          <div class="safety-checklist-section">
            <div class="safety-section-label">General Conditions</div>
            <label class="safety-check-item"><input type="checkbox" name="wjsi" value="gc_fire"> Fire Protection Equipment</label>
            <label class="safety-check-item"><input type="checkbox" name="wjsi" value="gc_firstaid"> First Aid &amp; Emergency Equipment</label>
            <label class="safety-check-item"><input type="checkbox" name="wjsi" value="gc_phone"> Emergency Phone Numbers Posted</label>
            <label class="safety-check-item"><input type="checkbox" name="wjsi" value="gc_sanitary"> Sanitary Toilets &amp; Wash Water</label>
            <label class="safety-check-item"><input type="checkbox" name="wjsi" value="gc_water"> Drinking Water</label>
            <label class="safety-check-item"><input type="checkbox" name="wjsi" value="gc_lighting"> Task Lighting</label>
            <label class="safety-check-item"><input type="checkbox" name="wjsi" value="gc_cranes"> Cranes, Rigging, Forklifts, Scissor &amp; Aerial Lifts</label>
          </div>
          <div class="safety-checklist-section">
            <div class="safety-section-label">Access, Egress &amp; Walking Surfaces</div>
            <label class="safety-check-item"><input type="checkbox" name="wjsi" value="ae_access"> Safe access and egress to all work areas</label>
            <label class="safety-check-item"><input type="checkbox" name="wjsi" value="ae_ladders"> Ladders and stairs safe and used correctly</label>
            <label class="safety-check-item"><input type="checkbox" name="wjsi" value="ae_aisles"> Aisles and passageways free from hazards</label>
            <label class="safety-check-item"><input type="checkbox" name="wjsi" value="ae_scaffolds"> Scaffolds — proper construction and free from hazards</label>
          </div>
          <div class="safety-checklist-section">
            <div class="safety-section-label">Fall Protection</div>
            <label class="safety-check-item"><input type="checkbox" name="wjsi" value="fp_ppe"> Personal Protective Equipment is safe</label>
            <label class="safety-check-item"><input type="checkbox" name="wjsi" value="fp_rigging"> Rigging and Anchors are safe</label>
            <label class="safety-check-item"><input type="checkbox" name="wjsi" value="fp_compliance"> Workers in compliance with fall protection rules</label>
            <label class="safety-check-item"><input type="checkbox" name="wjsi" value="fp_guardrails"> Guardrails and Handrails are safe</label>
            <label class="safety-check-item"><input type="checkbox" name="wjsi" value="fp_holes"> Floor holes and openings are covered or guarded</label>
            <label class="safety-check-item"><input type="checkbox" name="wjsi" value="fp_walls"> Wall openings or open-sided floors are guarded</label>
          </div>
          <div class="safety-checklist-section">
            <div class="safety-section-label">Tools, Cords &amp; Hoses</div>
            <label class="safety-check-item"><input type="checkbox" name="wjsi" value="tc_electrical"> Electrical tools and cords</label>
            <label class="safety-check-item"><input type="checkbox" name="wjsi" value="tc_pneumatic"> Pneumatic (air) hoses and connections</label>
            <label class="safety-check-item"><input type="checkbox" name="wjsi" value="tc_oxyacetylene"> Oxy-Acetylene gauges, cylinders, hoses &amp; torch</label>
          </div>
          <div class="safety-checklist-section">
            <div class="safety-section-label">Personal Protective Equipment</div>
            <label class="safety-check-item"><input type="checkbox" name="wjsi" value="ppe_clothing"> Proper work clothing and footwear</label>
            <label class="safety-check-item"><input type="checkbox" name="wjsi" value="ppe_head"> Head Protection</label>
            <label class="safety-check-item"><input type="checkbox" name="wjsi" value="ppe_eye"> Eye Protection</label>
            <label class="safety-check-item"><input type="checkbox" name="wjsi" value="ppe_hearing"> Hearing Protection</label>
            <label class="safety-check-item"><input type="checkbox" name="wjsi" value="ppe_task"> Task Specific PPE (gloves, face shield, respirator)</label>
          </div>
        </div>
        <div class="safety-section-label" style="margin-top:20px;">Inspection Observations &amp; Findings</div>
        <div class="safety-obs-hint">Include positive comments and note corrective action for any unsafe conditions.</div>
        <div class="safety-obs-table" id="wjsiObsTable"></div>
        <button class="safety-add-row-btn" onclick="addWjsiObsRow()">+ Add observation</button>
        <div class="safety-signatories">
          <div class="safety-sig-row">
            <div class="safety-sig-field"><label>Field Representative Name</label><input type="text" id="wjsiFieldRep" placeholder="Print name"></div>
            <div class="safety-sig-field"><label>Initials</label><input type="text" id="wjsiFieldRepInitials" placeholder="Initials" maxlength="4" style="width:80px;"></div>
          </div>
          <div class="safety-sig-row">
            <div class="safety-sig-field"><label>Management Representative Name</label><input type="text" id="wjsiMgmtRep" placeholder="Print name"></div>
            <div class="safety-sig-field"><label>Initials</label><input type="text" id="wjsiMgmtRepInitials" placeholder="Initials" maxlength="4" style="width:80px;"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- JHA -->
    <div class="safety-form-card" id="jhaCard">
      <div class="safety-form-header" onclick="toggleSafetySection('jha')">
        <span class="safety-form-icon">⚠️</span>
        <div>
          <div class="safety-form-title">Job Hazard Analysis</div>
          <div class="safety-form-subtitle">JHA · Identify task steps, hazards, and controls</div>
        </div>
        <span class="safety-check-status" id="jhaStatus">—</span>
        <span class="safety-chevron" id="jhaChevron">▼</span>
      </div>
      <div class="safety-form-body" id="jhaBody">
        <div class="safety-field-row">
          <div class="safety-field"><label>Job Position</label><input type="text" id="jhaPosition" placeholder="e.g. Foreman, Electrician"></div>
          <div class="safety-field"><label>Division</label><input type="text" id="jhaDivision" placeholder="e.g. Electrical"></div>
          <div class="safety-field"><label>Supervisor</label><input type="text" id="jhaSupervisor" placeholder="Supervisor name"></div>
          <div class="safety-field"><label>Approved By</label><input type="text" id="jhaApprovedBy" placeholder="Name"></div>
        </div>
        <div class="safety-section-label" style="margin-top:16px;">Required / Recommended PPE</div>
        <div class="safety-checklist-grid" style="grid-template-columns:repeat(auto-fill,minmax(200px,1fr));">
          <label class="safety-check-item"><input type="checkbox" name="jhaPPE" value="hard_hat"> Hard Hat</label>
          <label class="safety-check-item"><input type="checkbox" name="jhaPPE" value="safety_glasses"> Safety Glasses</label>
          <label class="safety-check-item"><input type="checkbox" name="jhaPPE" value="hi_vis"> Hi-Vis Vest</label>
          <label class="safety-check-item"><input type="checkbox" name="jhaPPE" value="gloves"> Gloves</label>
          <label class="safety-check-item"><input type="checkbox" name="jhaPPE" value="steel_toe"> Steel-Toe Boots</label>
          <label class="safety-check-item"><input type="checkbox" name="jhaPPE" value="face_shield"> Face Shield</label>
          <label class="safety-check-item"><input type="checkbox" name="jhaPPE" value="respirator"> Respirator</label>
          <label class="safety-check-item"><input type="checkbox" name="jhaPPE" value="hearing_prot"> Hearing Protection</label>
          <label class="safety-check-item"><input type="checkbox" name="jhaPPE" value="fall_arrest"> Fall Arrest Equipment</label>
        </div>
        <div class="safety-section-label" style="margin-top:20px;">Task Analysis</div>
        <div class="safety-obs-hint">Break down each task step with its potential hazards and safety controls.</div>
        <div class="jha-table-wrapper">
          <table class="jha-table">
            <thead><tr><th style="width:32px;">#</th><th>Job Task Step</th><th>Potential Hazards</th><th>Safety Controls</th><th style="width:32px;"></th></tr></thead>
            <tbody id="jhaTableBody"></tbody>
          </table>
        </div>
        <button class="safety-add-row-btn" onclick="addJhaRow()">+ Add task step</button>
      </div>
    </div>

    <!-- PTP -->
    <div class="safety-form-card" id="ptpCard">
      <div class="safety-form-header" onclick="toggleSafetySection('ptp')">
        <span class="safety-form-icon">📝</span>
        <div>
          <div class="safety-form-title">Pre-Task Plan</div>
          <div class="safety-form-subtitle">PTP · Complete before starting work each day</div>
        </div>
        <span class="safety-check-status" id="ptpStatus">—</span>
        <span class="safety-chevron" id="ptpChevron">▼</span>
      </div>
      <div class="safety-form-body" id="ptpBody">
        <div class="safety-field-row">
          <div class="safety-field"><label>Task Location</label><input type="text" id="ptpTaskLocation" placeholder="Floor, area, or unit"></div>
          <div class="safety-field">
            <label>Weather</label>
            <div class="safety-weather-toggle">
              <button class="weather-btn" data-val="under80" onclick="setWeather(this)">Under 80°</button>
              <button class="weather-btn" data-val="80plus" onclick="setWeather(this)">80°+</button>
              <button class="weather-btn" data-val="95plus" onclick="setWeather(this)">95°+</button>
            </div>
          </div>
          <div class="safety-field"><label>Time</label><input type="time" id="ptpTime"></div>
        </div>
        <div class="safety-field" style="margin-top:12px;">
          <label>Task Description</label>
          <textarea id="ptpTaskDesc" rows="3" placeholder="Brief description of the task to be performed..."></textarea>
        </div>
        <div class="safety-section-label" style="margin-top:16px;">Task Steps</div>
        <div id="ptpTaskSteps">
          <div class="ptp-numbered-row"><span>1</span><input type="text" placeholder="Step 1"></div>
          <div class="ptp-numbered-row"><span>2</span><input type="text" placeholder="Step 2"></div>
          <div class="ptp-numbered-row"><span>3</span><input type="text" placeholder="Step 3"></div>
          <div class="ptp-numbered-row"><span>4</span><input type="text" placeholder="Step 4"></div>
          <div class="ptp-numbered-row"><span>5</span><input type="text" placeholder="Step 5"></div>
        </div>
        <div class="safety-section-label" style="margin-top:16px;">Tools, Equipment &amp; Material</div>
        <div class="ptp-tools-grid">
          <input type="text" placeholder="1."><input type="text" placeholder="6.">
          <input type="text" placeholder="2."><input type="text" placeholder="7.">
          <input type="text" placeholder="3."><input type="text" placeholder="8.">
          <input type="text" placeholder="4."><input type="text" placeholder="9.">
          <input type="text" placeholder="5."><input type="text" placeholder="10.">
        </div>
        <div class="safety-section-label" style="margin-top:16px;">Hazardous Chemicals</div>
        <div class="safety-hz-row">
          <label class="safety-radio-item"><input type="radio" name="ptpHazChem" value="no" checked> No</label>
          <label class="safety-radio-item"><input type="radio" name="ptpHazChem" value="yes"> Yes</label>
          <label class="safety-check-item" id="ptpSdsLabel" style="display:none;margin-left:16px;"><input type="checkbox" id="ptpSdsAvail"> SDS Sheet available for review</label>
        </div>
        <div class="safety-section-label" style="margin-top:16px;">Certifications, Inspections, Training &amp; Permits</div>
        <div class="safety-checklist-grid" style="grid-template-columns:repeat(auto-fill,minmax(240px,1fr));">
          <label class="safety-check-item"><input type="checkbox" name="ptpCert" value="forklift_cert"> Forklift Operator Certification</label>
          <label class="safety-check-item"><input type="checkbox" name="ptpCert" value="forklift_pre"> Forklift Pre-Use Inspection</label>
          <label class="safety-check-item"><input type="checkbox" name="ptpCert" value="mewp_cert"> MEWP Certification</label>
          <label class="safety-check-item"><input type="checkbox" name="ptpCert" value="mewp_pre"> MEWP Pre-Use Inspection</label>
          <label class="safety-check-item"><input type="checkbox" name="ptpCert" value="fall_training"> Personal Fall Arrest Equipment Training</label>
          <label class="safety-check-item"><input type="checkbox" name="ptpCert" value="fall_pre"> Personal Fall Arrest Equipment Pre-Use Inspection</label>
          <label class="safety-check-item"><input type="checkbox" name="ptpCert" value="ladder_pre"> Portable Ladder Pre-Use Inspection</label>
          <label class="safety-check-item"><input type="checkbox" name="ptpCert" value="trench_training"> Trench &amp; Excavation Awareness Training</label>
          <label class="safety-check-item"><input type="checkbox" name="ptpCert" value="scaffold_training"> Scaffold User Training</label>
          <label class="safety-check-item"><input type="checkbox" name="ptpCert" value="silica_training"> Silica Awareness Training</label>
          <label class="safety-check-item"><input type="checkbox" name="ptpCert" value="loto_training"> LOTO Exposed Employee Training</label>
          <label class="safety-check-item"><input type="checkbox" name="ptpCert" value="hot_work"> Hot Work Permit</label>
        </div>
        <div class="safety-section-label" style="margin-top:16px;">Additional PPE Required</div>
        <div class="safety-checklist-grid" style="grid-template-columns:repeat(auto-fill,minmax(200px,1fr));">
          <label class="safety-check-item"><input type="checkbox" name="ptpAddPPE" value="face_shield"> Face Shield or Goggles</label>
          <label class="safety-check-item"><input type="checkbox" name="ptpAddPPE" value="fall_arrest"> Personal Fall Arrest Equipment</label>
          <label class="safety-check-item"><input type="checkbox" name="ptpAddPPE" value="leather_gloves"> Leather Gloves</label>
          <label class="safety-check-item"><input type="checkbox" name="ptpAddPPE" value="hearing"> Hearing Protection</label>
        </div>
        <div class="safety-section-label" style="margin-top:20px;">Hazards &amp; Controls</div>
        <div class="safety-obs-hint">Identify hazards present and a control for each. List highest-risk hazards first.</div>
        <div class="jha-table-wrapper">
          <table class="jha-table">
            <thead><tr><th style="width:32px;">#</th><th>Hazard</th><th>Hazard Control</th><th style="width:32px;"></th></tr></thead>
            <tbody id="ptpHazardBody"></tbody>
          </table>
        </div>
        <button class="safety-add-row-btn" onclick="addPtpHazardRow()">+ Add hazard</button>
        <div class="safety-section-label" style="margin-top:20px;">Crew Signatures</div>
        <div class="safety-obs-hint">All employees involved must sign before starting the task.</div>
        <div class="ptp-sig-grid" id="ptpSigGrid"></div>
        <button class="safety-add-row-btn" onclick="addPtpSigRow()">+ Add crew member</button>
        <div class="safety-section-label" style="margin-top:20px;">Supervisor Review</div>
        <div class="safety-field"><label>Supervisor Notes</label><textarea id="ptpSupervisorNotes" rows="2" placeholder="Review notes and feedback to the team..."></textarea></div>
        <div class="safety-field" style="margin-top:8px;"><label>Supervisor Name</label><input type="text" id="ptpSupervisorName" placeholder="Supervisor name"></div>
      </div>
    </div>

    <!-- Submit -->
    <div class="safety-submit-area">
      <div class="safety-submitter-row">
        <label>Submitted by</label>
        <input type="text" id="safetySubmittedByInput" placeholder="Your name">
      </div>
      <button class="safety-submit-btn" id="safetySubmitBtn" onclick="submitSafetyForms()">Submit Safety Forms</button>
      <div id="safetySubmitStatus" class="safety-submit-status"></div>
    </div>

  </div>
  <!-- END SAFETY TAB PANEL -->"""

# ── CSS ───────────────────────────────────────────────────────────────────────
SAFETY_CSS = """
  /* ── Safety Tab ── */
  .safety-tab-btn{position:relative}
  .safety-friday-badge{position:absolute;top:-6px;right:-6px;background:#e53e3e;color:#fff;font-size:9px;font-weight:700;padding:2px 5px;border-radius:8px;text-transform:uppercase;letter-spacing:.4px}
  .safety-header{padding:16px 0 8px;border-bottom:2px solid #e2e8f0;margin-bottom:20px}
  .safety-header h2{margin:0 0 4px;font-size:20px;font-weight:700;color:#1a202c}
  .safety-meta{display:flex;align-items:center;gap:12px;font-size:13px;color:#718096;flex-wrap:wrap}
  .safety-required-badge{background:#fff5f5;border:1px solid #feb2b2;color:#c53030;padding:2px 8px;border-radius:6px;font-size:12px;font-weight:600}
  .safety-optional-badge{background:#f7fafc;border:1px solid #cbd5e0;color:#718096;padding:2px 8px;border-radius:6px;font-size:12px}
  .safety-submitted-banner{margin-top:10px;background:#f0fff4;border:1px solid #9ae6b4;color:#276749;padding:8px 14px;border-radius:8px;font-size:13px;font-weight:600}
  .safety-form-card{background:#fff;border:1px solid #e2e8f0;border-radius:10px;margin-bottom:16px;overflow:hidden}
  .safety-form-header{display:flex;align-items:center;gap:12px;padding:14px 16px;cursor:pointer;background:#f7fafc;border-bottom:1px solid #e2e8f0;user-select:none}
  .safety-form-header:hover{background:#edf2f7}
  .safety-form-icon{font-size:20px;flex-shrink:0}
  .safety-form-title{font-size:15px;font-weight:700;color:#1a202c}
  .safety-form-subtitle{font-size:11px;color:#718096;margin-top:1px}
  .safety-check-status{margin-left:auto;font-size:18px;min-width:28px;text-align:center}
  .safety-chevron{font-size:12px;color:#a0aec0;flex-shrink:0;transition:transform .2s}
  .safety-chevron.open{transform:rotate(180deg)}
  .safety-form-body{padding:16px;display:none}
  .safety-form-body.open{display:block}
  .safety-checklist-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:4px 20px;margin-top:8px}
  .safety-checklist-section{margin-bottom:12px}
  .safety-section-label{font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.6px;color:#4a5568;margin-bottom:6px}
  .safety-check-item{display:flex;align-items:center;gap:8px;font-size:13px;color:#2d3748;padding:3px 0;cursor:pointer;line-height:1.3}
  .safety-check-item input[type="checkbox"]{flex-shrink:0;accent-color:#2b6cb0}
  .safety-obs-hint{font-size:12px;color:#718096;margin-bottom:10px}
  .safety-obs-row{display:grid;grid-template-columns:28px 1fr 100px 1fr;gap:6px;align-items:center;margin-bottom:6px}
  .safety-obs-num{font-size:12px;color:#718096;text-align:center;font-weight:600}
  .safety-yesno{display:flex;gap:6px;justify-content:center}
  .safety-yesno label{display:flex;align-items:center;gap:3px;font-size:12px;font-weight:600;cursor:pointer}
  .safety-yesno input[type="radio"]{accent-color:#2b6cb0}
  .safety-signatories{margin-top:20px;border-top:1px dashed #e2e8f0;padding-top:16px}
  .safety-sig-row{display:flex;gap:12px;margin-bottom:10px;align-items:flex-end;flex-wrap:wrap}
  .safety-sig-field{display:flex;flex-direction:column;gap:4px;flex:1;min-width:140px}
  .safety-sig-field label{font-size:12px;font-weight:600;color:#4a5568}
  .safety-sig-field input{font-size:13px}
  .safety-field-row{display:flex;flex-wrap:wrap;gap:12px}
  .safety-field{display:flex;flex-direction:column;gap:4px;flex:1;min-width:140px}
  .safety-field label{font-size:12px;font-weight:600;color:#4a5568}
  .safety-field input,.safety-field textarea,.safety-field select{padding:7px 10px;border:1px solid #cbd5e0;border-radius:6px;font-size:13px;color:#2d3748;background:#fff}
  .safety-field textarea{resize:vertical;font-family:inherit}
  .safety-weather-toggle{display:flex;gap:4px}
  .weather-btn{flex:1;padding:7px 6px;border:1px solid #cbd5e0;border-radius:6px;background:#fff;font-size:12px;font-weight:600;color:#4a5568;cursor:pointer;transition:all .15s}
  .weather-btn.active{background:#2b6cb0;color:#fff;border-color:#2b6cb0}
  .ptp-numbered-row{display:flex;align-items:center;gap:10px;margin-bottom:6px}
  .ptp-numbered-row span{font-size:12px;font-weight:700;color:#718096;width:18px;text-align:right;flex-shrink:0}
  .ptp-numbered-row input{flex:1;padding:7px 10px;border:1px solid #cbd5e0;border-radius:6px;font-size:13px}
  .ptp-tools-grid{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-top:8px}
  .ptp-tools-grid input{padding:7px 10px;border:1px solid #cbd5e0;border-radius:6px;font-size:13px}
  .safety-hz-row{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-top:6px}
  .safety-radio-item{display:flex;align-items:center;gap:6px;font-size:13px;font-weight:600;cursor:pointer}
  .jha-table-wrapper{overflow-x:auto;margin-top:10px}
  .jha-table{width:100%;border-collapse:collapse;font-size:13px}
  .jha-table th{background:#edf2f7;color:#4a5568;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;padding:8px 10px;text-align:left;border-bottom:2px solid #e2e8f0}
  .jha-table td{padding:5px 6px;border-bottom:1px solid #f0f0f0;vertical-align:middle}
  .jha-table input[type="text"],.jha-table textarea{width:100%;padding:5px 8px;border:1px solid #e2e8f0;border-radius:5px;font-size:13px;resize:vertical;font-family:inherit}
  .jha-table input[type="text"]:focus,.jha-table textarea:focus{border-color:#63b3ed;outline:none}
  .jha-del-btn{background:none;border:none;color:#fc8181;cursor:pointer;font-size:16px;padding:2px 6px}
  .ptp-sig-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:8px;margin-top:8px}
  .ptp-sig-entry{display:flex;flex-direction:column;gap:4px;background:#f7fafc;border:1px solid #e2e8f0;border-radius:6px;padding:8px}
  .ptp-sig-entry label{font-size:11px;font-weight:600;color:#718096}
  .ptp-sig-entry input{padding:5px 8px;border:1px solid #cbd5e0;border-radius:5px;font-size:13px}
  .safety-add-row-btn{background:none;border:1px dashed #a0aec0;color:#4a5568;padding:6px 14px;border-radius:6px;font-size:12px;font-weight:600;cursor:pointer;margin-top:8px;transition:all .15s}
  .safety-add-row-btn:hover{border-color:#2b6cb0;color:#2b6cb0;background:#ebf8ff}
  .safety-submit-area{background:#f7fafc;border:1px solid #e2e8f0;border-radius:10px;padding:16px;margin-top:8px;display:flex;flex-wrap:wrap;gap:12px;align-items:flex-end}
  .safety-submitter-row{display:flex;flex-direction:column;gap:4px;flex:1;min-width:180px}
  .safety-submitter-row label{font-size:12px;font-weight:600;color:#4a5568}
  .safety-submitter-row input{padding:8px 12px;border:1px solid #cbd5e0;border-radius:6px;font-size:13px}
  .safety-submit-btn{background:#2b6cb0;color:#fff;border:none;padding:10px 24px;border-radius:8px;font-size:14px;font-weight:700;cursor:pointer;transition:background .15s}
  .safety-submit-btn:hover{background:#2c5282}
  .safety-submit-btn:disabled{background:#90cdf4;cursor:not-allowed}
  .safety-submit-status{font-size:13px;font-weight:600;width:100%}
  .safety-submit-status.success{color:#276749}
  .safety-submit-status.error{color:#c53030}
  @media(max-width:600px){
    .safety-obs-row{grid-template-columns:28px 1fr}
    .ptp-tools-grid{grid-template-columns:1fr}
  }"""

# ── JS ────────────────────────────────────────────────────────────────────────
SAFETY_JS = """
  // ── Safety Tab ────────────────────────────────────────
  (function initSafetyTab(){
    var SUPABASE_URL='https://okesnavkxmqucgvvhncx.supabase.co';
    var SUPABASE_KEY='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im9rZXNuYXZreG1xdWNndnZobmN4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Nzk3MzY2ODUsImV4cCI6MjA5NTMxMjY4NX0.-FCoWt0B7Eb60bcGzTMhT0TRIsqd6Vk-2XfVhbsEK7c';
    function isFriday(){return new Date().getDay()===5}
    function getWeekEnding(){var n=new Date(),day=n.getDay(),diff=day<=5?5-day:5-day+7,f=new Date(n);f.setDate(n.getDate()+diff);return f.toISOString().slice(0,10)}
    function getJobId(){if(typeof JOB_ID!=='undefined')return JOB_ID;var m=window.location.pathname.match(/field-tracker-([^.]+)\\.html/);return m?m[1].toUpperCase():'UNKNOWN'}
    function formatDate(d){return d.toLocaleDateString('en-US',{weekday:'long',month:'short',day:'numeric',year:'numeric'})}
    window.addEventListener('load',function(){
      var el=document.getElementById('safetyDateDisplay');if(el)el.textContent=formatDate(new Date());
      if(isFriday()){
        var b=document.getElementById('safetyFridayBadge');if(b)b.style.display='inline-block';
        var n=document.getElementById('safetyFridayNotice');if(n)n.style.display='inline-block';
        var o=document.getElementById('safetyOptionalNotice');if(o)o.style.display='none';
      } else {
        var o=document.getElementById('safetyOptionalNotice');if(o)o.style.display='inline-block';
      }
      var t=document.getElementById('ptpTime');if(t){var now=new Date();t.value=now.toTimeString().slice(0,5)}
      for(var i=0;i<5;i++)addWjsiObsRow();
      for(var i=0;i<5;i++)addJhaRow();
      for(var i=0;i<10;i++)addPtpHazardRow();
      for(var i=0;i<5;i++)addPtpSigRow();
      document.querySelectorAll('input[name="ptpHazChem"]').forEach(function(r){r.addEventListener('change',function(){var l=document.getElementById('ptpSdsLabel');if(l)l.style.display=this.value==='yes'?'flex':'none'})});
      checkExistingSubmission();
    });
    window.toggleSafetySection=function(id){var b=document.getElementById(id+'Body'),c=document.getElementById(id+'Chevron');if(!b)return;var open=b.classList.contains('open');b.classList.toggle('open',!open);if(c)c.classList.toggle('open',!open)};
    window.setWeather=function(btn){document.querySelectorAll('.weather-btn').forEach(function(b){b.classList.remove('active')});btn.classList.add('active')};
    window.addWjsiObsRow=function(){var c=document.getElementById('wjsiObsTable');if(!c)return;var n=c.querySelectorAll('.safety-obs-row').length;if(n>=10)return;var i=n+1,row=document.createElement('div');row.className='safety-obs-row';row.innerHTML='<div class="safety-obs-num">'+i+'</div><input type="text" placeholder="Observation..."><div class="safety-yesno"><label><input type="radio" name="wjsiObs'+i+'" value="yes"> YES</label><label><input type="radio" name="wjsiObs'+i+'" value="no"> NO</label></div><input type="text" placeholder="Person responsible (if NO)">';c.appendChild(row)};
    window.addJhaRow=function(){var t=document.getElementById('jhaTableBody');if(!t)return;var n=t.querySelectorAll('tr').length+1,tr=document.createElement('tr');tr.innerHTML='<td class="safety-obs-num">'+n+'</td><td><input type="text" placeholder="Task step..."></td><td><input type="text" placeholder="Potential hazard..."></td><td><input type="text" placeholder="Safety control..."></td><td><button class="jha-del-btn" onclick="this.closest(\'tr\').remove()">×</button></td>';t.appendChild(tr)};
    window.addPtpHazardRow=function(){var t=document.getElementById('ptpHazardBody');if(!t)return;var n=t.querySelectorAll('tr').length+1,tr=document.createElement('tr');tr.innerHTML='<td class="safety-obs-num">'+n+'</td><td><input type="text" placeholder="Hazard..."></td><td><input type="text" placeholder="Control..."></td><td><button class="jha-del-btn" onclick="this.closest(\'tr\').remove()">×</button></td>';t.appendChild(tr)};
    window.addPtpSigRow=function(){var g=document.getElementById('ptpSigGrid');if(!g)return;var n=g.querySelectorAll('.ptp-sig-entry').length+1,d=document.createElement('div');d.className='ptp-sig-entry';d.innerHTML='<label>Employee '+n+'</label><input type="text" placeholder="Full name"><label style="margin-top:4px;">MSR Initials</label><input type="text" placeholder="Mid-shift initials" maxlength="6">';g.appendChild(d)};
    function getChecked(name){var v=[];document.querySelectorAll('input[name="'+name+'"]:checked').forEach(function(c){v.push(c.value)});return v}
    function getWjsiObs(){return Array.from(document.querySelectorAll('#wjsiObsTable .safety-obs-row')).map(function(r,i){var t=r.querySelectorAll('input[type="text"]'),cor=r.querySelector('input[value="yes"]:checked')?'yes':r.querySelector('input[value="no"]:checked')?'no':null;return{n:i+1,observation:t[0]?t[0].value:'',corrected:cor,responsible:t[1]?t[1].value:''}}).filter(function(r){return r.observation})}
    function getJhaRows(){return Array.from(document.querySelectorAll('#jhaTableBody tr')).map(function(tr){var i=tr.querySelectorAll('input[type="text"]');return{step:i[0]?i[0].value:'',hazard:i[1]?i[1].value:'',control:i[2]?i[2].value:''}}).filter(function(r){return r.step||r.hazard})}
    function getPtpHazards(){return Array.from(document.querySelectorAll('#ptpHazardBody tr')).map(function(tr){var i=tr.querySelectorAll('input[type="text"]');return{hazard:i[0]?i[0].value:'',control:i[1]?i[1].value:''}}).filter(function(r){return r.hazard})}
    function getPtpSigs(){return Array.from(document.querySelectorAll('#ptpSigGrid .ptp-sig-entry')).map(function(d){var i=d.querySelectorAll('input');return{name:i[0]?i[0].value:'',msr:i[1]?i[1].value:''}}).filter(function(r){return r.name})}
    function v(id){var e=document.getElementById(id);return e?e.value:''}
    function collectData(){return{wjsi:{checklist:(function(){var o={};document.querySelectorAll('input[name="wjsi"]').forEach(function(c){o[c.value]=c.checked});return o})(),observations:getWjsiObs(),field_rep:v('wjsiFieldRep'),field_rep_initials:v('wjsiFieldRepInitials'),mgmt_rep:v('wjsiMgmtRep'),mgmt_rep_initials:v('wjsiMgmtRepInitials')},jha:{position:v('jhaPosition'),division:v('jhaDivision'),supervisor:v('jhaSupervisor'),approved_by:v('jhaApprovedBy'),ppe:getChecked('jhaPPE'),tasks:getJhaRows()},ptp:{task_location:v('ptpTaskLocation'),weather:(function(){var b=document.querySelector('.weather-btn.active');return b?b.dataset.val:''})(),time:v('ptpTime'),task_description:v('ptpTaskDesc'),task_steps:Array.from(document.querySelectorAll('#ptpTaskSteps input')).map(function(i){return i.value}).filter(Boolean),tools:Array.from(document.querySelectorAll('.ptp-tools-grid input')).map(function(i){return i.value}).filter(Boolean),hazardous_chemicals:(function(){var r=document.querySelector('input[name="ptpHazChem"]:checked');return r?r.value:'no'})(),sds_available:(function(){var e=document.getElementById('ptpSdsAvail');return e?e.checked:false})(),certifications:getChecked('ptpCert'),additional_ppe:getChecked('ptpAddPPE'),hazards:getPtpHazards(),signatures:getPtpSigs(),supervisor_notes:v('ptpSupervisorNotes'),supervisor_name:v('ptpSupervisorName')}}}
    function updateStatusIcons(){var wjsiOk=document.querySelectorAll('input[name="wjsi"]:checked').length>0,jhaOk=getJhaRows().length>0,ptpOk=v('ptpTaskDesc').trim().length>0;var map={wjsi:'wjsiStatus',jha:'jhaStatus',ptp:'ptpStatus'};var vals={wjsi:wjsiOk,jha:jhaOk,ptp:ptpOk};Object.keys(map).forEach(function(k){var e=document.getElementById(map[k]);if(e)e.textContent=vals[k]?'✅':'—'})}
    document.addEventListener('change',updateStatusIcons);
    document.addEventListener('input',updateStatusIcons);
    async function checkExistingSubmission(){try{var r=await fetch(SUPABASE_URL+'/rest/v1/safety_logs?job_id=eq.'+getJobId()+'&week_ending=eq.'+getWeekEnding()+'&select=submitted_by,submitted_at&limit=1',{headers:{'apikey':SUPABASE_KEY,'Authorization':'Bearer '+SUPABASE_KEY}});var d=await r.json();if(d&&d.length>0){var ban=document.getElementById('safetySubmittedBanner'),by=document.getElementById('safetySubmittedBy'),btn=document.getElementById('safetySubmitBtn');if(ban)ban.style.display='block';if(by)by.textContent=d[0].submitted_by+' · '+new Date(d[0].submitted_at).toLocaleDateString();if(btn)btn.textContent='Re-submit (Update)'}}catch(e){console.warn('Safety check:',e)}}
    window.submitSafetyForms=async function(){var by=document.getElementById('safetySubmittedByInput')?document.getElementById('safetySubmittedByInput').value.trim():'';var statusEl=document.getElementById('safetySubmitStatus');var btn=document.getElementById('safetySubmitBtn');if(!by){if(statusEl){statusEl.textContent='Please enter your name before submitting.';statusEl.className='safety-submit-status error'}return}if(btn){btn.disabled=true;btn.textContent='Submitting…'}if(statusEl){statusEl.textContent='';statusEl.className='safety-submit-status'}var data=collectData();var payload={job_id:getJobId(),submitted_by:by,week_ending:getWeekEnding(),friday_required:isFriday(),wjsi:data.wjsi,jha:data.jha,ptp:data.ptp};try{var r=await fetch(SUPABASE_URL+'/rest/v1/safety_logs',{method:'POST',headers:{'apikey':SUPABASE_KEY,'Authorization':'Bearer '+SUPABASE_KEY,'Content-Type':'application/json','Prefer':'return=minimal'},body:JSON.stringify(payload)});if(r.ok||r.status===201){if(statusEl){statusEl.textContent='✅ Safety forms submitted successfully.';statusEl.className='safety-submit-status success'}if(btn){btn.disabled=false;btn.textContent='Re-submit (Update)'}var ban=document.getElementById('safetySubmittedBanner'),byEl=document.getElementById('safetySubmittedBy');if(ban)ban.style.display='block';if(byEl)byEl.textContent=by+' · Today'}else{var err=await r.text();if(statusEl){statusEl.textContent='Error: '+err;statusEl.className='safety-submit-status error'}if(btn){btn.disabled=false;btn.textContent='Submit Safety Forms'}}}catch(e){if(statusEl){statusEl.textContent='Network error — check connection and try again.';statusEl.className='safety-submit-status error'}if(btn){btn.disabled=false;btn.textContent='Submit Safety Forms'}}};
    window.getSafetyStatusForReport=async function(){if(!isFriday())return{submitted:false,required:false};try{var r=await fetch(SUPABASE_URL+'/rest/v1/safety_logs?job_id=eq.'+getJobId()+'&week_ending=eq.'+getWeekEnding()+'&select=submitted_by&limit=1',{headers:{'apikey':SUPABASE_KEY,'Authorization':'Bearer '+SUPABASE_KEY}});var d=await r.json();return{submitted:d&&d.length>0,required:true,by:d&&d.length>0?d[0].submitted_by:null}}catch(e){return{submitted:false,required:true,error:true}}};
  })();"""


def inject(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    original = html

    # ── 1. Tab button — insert before </nav> or before the last tab-btn group closer
    # Look for the Tasks tab button as anchor point
    tasks_btn_pattern = re.compile(
        r'(<button[^>]*onclick=["\']showTab\(\'tasks\'\)["\'][^>]*>.*?</button>)',
        re.DOTALL | re.IGNORECASE
    )
    if 'tab-btn-safety' in html:
        print(f"  ⏭  Already patched: {filepath}")
        return False

    match = tasks_btn_pattern.search(html)
    if match:
        html = html[:match.end()] + TAB_BUTTON + html[match.end():]
    else:
        # Fallback: look for any last tab-btn before </nav>
        nav_close = html.rfind('</nav>')
        if nav_close == -1:
            print(f"  ⚠  Could not find tab nav in {filepath} — skipping button injection")
        else:
            html = html[:nav_close] + TAB_BUTTON + '\n  ' + html[nav_close:]

    # ── 2. Tab panel — insert before </main> or before </body>
    # Find tasks panel end as anchor
    tasks_panel_pattern = re.compile(
        r'(id=["\']tab-tasks["\'].*?</div>\s*)(<!--\s*end|</main|</body)',
        re.DOTALL | re.IGNORECASE
    )
    # Simpler: find the closing of the last tab panel by looking for </main> or </body>
    main_close = html.rfind('</main>')
    if main_close != -1:
        html = html[:main_close] + TAB_PANEL + '\n\n' + html[main_close:]
    else:
        body_close = html.rfind('</body>')
        if body_close != -1:
            html = html[:body_close] + TAB_PANEL + '\n\n' + html[body_close:]
        else:
            print(f"  ⚠  Could not find </main> or </body> in {filepath} — skipping panel injection")

    # ── 3. CSS — insert before </style>
    style_close = html.rfind('</style>')
    if style_close != -1:
        html = html[:style_close] + SAFETY_CSS + '\n' + html[style_close:]
    else:
        print(f"  ⚠  No </style> found in {filepath}")

    # ── 4. JS — insert before </script> (last one)
    script_close = html.rfind('</script>')
    if script_close != -1:
        html = html[:script_close] + SAFETY_JS + '\n' + html[script_close:]
    else:
        print(f"  ⚠  No </script> found in {filepath}")

    if html == original:
        print(f"  ⚠  No changes made to {filepath}")
        return False

    # Backup original
    shutil.copy2(filepath, filepath + '.bak')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

    return True


def main():
    print("Rye Electric — Safety Tab Injector")
    print("=" * 40)
    found = 0
    patched = 0
    missing = []

    for filename in TRACKERS:
        if not os.path.exists(filename):
            missing.append(filename)
            print(f"  ❌ Not found: {filename}")
            continue
        found += 1
        print(f"  🔧 Patching: {filename}")
        if inject(filename):
            patched += 1
            print(f"     ✅ Done — backup saved as {filename}.bak")

    print()
    print(f"Results: {patched}/{found} files patched.")
    if missing:
        print(f"Missing files ({len(missing)}):")
        for m in missing:
            print(f"  - {m}")
        print("Check filenames in the TRACKERS list at the top of this script.")


if __name__ == '__main__':
    main()
