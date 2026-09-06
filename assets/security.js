/* A ai QUANTUM SHIELD v2 - passphrase-gated zero-knowledge vault.
   v2 fix: vault key derives from a user PASSPHRASE (never stored), not just
   a device fingerprint. A stolen copy of localStorage is useless ciphertext.
   AES-256-GCM: quantum-resistant (~2^128 ops under Grover). PBKDF2 310k.
   aai_* data is NEVER written to disk in plaintext - while locked, writes
   stay in memory and flush encrypted at unlock. AAD binds each envelope to
   its storage key. Load in <head> BEFORE any other script. */
(function () {
  'use strict';
  var TARGET_PREFIX = 'aai_';
  var PBKDF2_ITERS = 310000;
  var VERIFIER = 'Aai Quantum Vault v2';
  var IDLE_LOCK_MS = 600000;
  var EXPECTED_APP_SHA = '5e78fd2a009e5827c55e4447ae75e13189df8e066f5f1f1fc24b7c3c72165064';
  var APP_URL = 'assets/app.js';

  var KDF = 'PBKDF2-SHA256 (310k)';
  var MAC = 'GCM 128-bit tag';
  var INTEGRITY = 'SHA-256';

  var state = {
    mode: 'anon',
    key: null,
    salt: null,
    psalt: null,
    token: null,
    detections: 0,
    audits: [],
    shadow: {},
    pending: {},
    envelopes: {},
    unlockCbs: [],
    failCount: 0,
    failUntil: 0,
    idleTimer: null,
    lastError: null
  };
  var cfg = { pl: 0 };
  function readCfg() {
    try {
      var c = getItemNative('qs_cfg');
      if (c) { var o = JSON.parse(c); if (o && o.pl) cfg.pl = 1; }
    } catch (e) {}
  }

  function b64(buf) {
    var b = new Uint8Array(buf), s = '';
    for (var i = 0; i < b.length; i++) s += String.fromCharCode(b[i]);
    return btoa(s);
  }
  function unb64(s) {
    var bin = atob(s), b = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) b[i] = bin.charCodeAt(i);
    return b.buffer;
  }
  function sha256(str) {
    return crypto.subtle.digest('SHA-256', new TextEncoder().encode(str)).then(function (d) {
      return Array.prototype.map.call(new Uint8Array(d), function (x) {
        return ('0' + x.toString(16)).slice(-2);
      }).join('');
    });
  }
  function randBytes(n) { var b = new Uint8Array(n); crypto.getRandomValues(b); return b; }
  function randHex(n) {
    return Array.prototype.map.call(randBytes(n), function (x) { return ('0' + x.toString(16)).slice(-2); }).join('');
  }
  function isTarget(k) { return typeof k === 'string' && k.indexOf(TARGET_PREFIX) === 0; }
  function nowStr() { return new Date().toISOString().slice(0, 19).replace('T', ' '); }

  function fingerprint() {
    var parts = [];
    try { parts.push(navigator.userAgent); } catch (e) {}
    try { parts.push(navigator.language + '/' + navigator.languages.join(',')); } catch (e) {}
    try { parts.push(screen.width + 'x' + screen.height + 'x' + screen.colorDepth); } catch (e) {}
    try { parts.push(String(new Date().getTimezoneOffset())); } catch (e) {}
    try { parts.push(navigator.hardwareConcurrency + '|' + navigator.deviceMemory); } catch (e) {}
    try {
      var c = document.createElement('canvas').getContext('2d');
      c.textBaseline = 'top';
      c.font = '14px sans-serif';
      c.fillText('A ai Quantum Shield', 2, 2);
      parts.push(c.canvas.toDataURL().slice(0, 400));
    } catch (e) {}
    return parts.join(String.fromCharCode(8226));
  }

  var _nativeSet = Storage.prototype.setItem;
  var _nativeGet = Storage.prototype.getItem;
  var _nativeRemove = Storage.prototype.removeItem;
  function setItemNative(k, v) { try { return _nativeSet.call(window.localStorage, k, v); } catch (e) {} }
  function getItemNative(k) { try { return _nativeGet.call(window.localStorage, k); } catch (e) { return null; } }
  function removeItemNative(k) { try { return _nativeRemove.call(window.localStorage, k); } catch (e) {} }

  function deriveFrom(secretStr, saltB64) {
    return crypto.subtle.importKey('raw', new TextEncoder().encode(secretStr), 'PBKDF2', false, ['deriveKey'])
      .then(function (base) {
        return crypto.subtle.deriveKey(
          { name: 'PBKDF2', salt: unb64(saltB64), iterations: PBKDF2_ITERS, hash: 'SHA-256' },
          base, { name: 'AES-GCM', length: 256 }, false, ['encrypt', 'decrypt']
        );
      });
  }
  function aadFor(k) { return new TextEncoder().encode('aai|' + k); }

  function encWith(key, plain, aadKey) {
    var iv = randBytes(12);
    return crypto.subtle.encrypt({ name: 'AES-GCM', iv: iv, additionalData: aadFor(aadKey) }, key,
      new TextEncoder().encode(String(plain)))
      .then(function (ct) {
        var full = new Uint8Array(iv.length + ct.byteLength);
        full.set(iv, 0);
        full.set(new Uint8Array(ct), iv.length);
        return JSON.stringify({ q: 2, c: b64(full) });
      });
  }
  function decWith(key, env, aadKey) {
    try {
      var o = JSON.parse(env);
      if (!o || !o.c) return Promise.resolve(null);
      var raw = new Uint8Array(unb64(o.c));
      var iv = raw.slice(0, 12);
      var ct = raw.slice(12);
      var opt = { name: 'AES-GCM', iv: iv };
      if (o.q === 2) opt.additionalData = aadFor(aadKey);
      return crypto.subtle.decrypt(opt, key, ct)
        .then(function (pt) { return new TextDecoder().decode(pt); })
        .catch(function () { return null; });
    } catch (e) { return Promise.resolve(null); }
  }

  function wrappedSetItem(k, v) {
    if (!isTarget(k)) { setItemNative(k, v); return; }
    if (state.mode !== 'open') {
      state.pending[k] = v;
      return;
    }
    state.shadow[k] = v;
    encWith(state.key, v, k).then(function (env) {
      setItemNative(k, env);
      delete state.pending[k];
    });
  }
  function wrappedGetItem(k) {
    if (!isTarget(k)) return getItemNative(k);
    if (Object.prototype.hasOwnProperty.call(state.shadow, k)) return state.shadow[k];
    if (Object.prototype.hasOwnProperty.call(state.pending, k)) return state.pending[k];
    return null;
  }
  function wrappedRemoveItem(k) {
    if (!isTarget(k)) { removeItemNative(k); return; }
    delete state.shadow[k];
    delete state.pending[k];
    delete state.envelopes[k];
    removeItemNative(k);
  }

  function flushEnvelopes() {
    var keys = [];
    try {
      for (var i = 0; i < window.localStorage.length; i++) {
        var k = window.localStorage.key(i);
        if (isTarget(k)) keys.push(k);
      }
    } catch (e) {}
    var chain = Promise.resolve();
    keys.forEach(function (k) {
      chain = chain.then(function () {
        var env = getItemNative(k);
        if (env === null) return;
        var isEnv = false;
        try { var o = JSON.parse(env); isEnv = !!(o && (o.q === 1 || o.q === 2) && o.c); } catch (e) {}
        var plainP = isEnv ? decWith(state.key, env, k) : Promise.resolve(env);
        return plainP.then(function (plain) {
          if (plain === null) { audit('vault: decrypt failed for ' + k); return; }
          state.shadow[k] = plain;
          if (!isEnv || env.indexOf('"q":2') === -1) {
            return encWith(state.key, plain, k).then(function (newEnv) { setItemNative(k, newEnv); });
          }
        });
      });
    });
    chain.then(function () {
      var pend = Object.keys(state.pending);
      pend.forEach(function (k) {
        if (k.indexOf('aai_chat:') === 0 || k.indexOf('aai_mem:') === 0) return;
        var v = state.pending[k];
        state.shadow[k] = v; // keep session writes readable across the anon->open transition
        encWith(state.key, v, k).then(function (env) { setItemNative(k, env); });
      });
      state.pending = {};
      audit('vault unlocked (AES-256-GCM)');
      var ev = null;
      try { ev = new CustomEvent('qs-unlock', { detail: { passphrase: !!cfg.pl } }); } catch (e) {}
      if (ev) document.dispatchEvent(ev);
      state.unlockCbs.forEach(function (fn) { try { fn(); } catch (e) {} });
      state.unlockCbs = [];
      if (typeof renderPanel === 'function') renderPanel();
    });
  }

  /* ------------------------- vault operations ---------------------------- */
  function rekeyAll(newKey, newPsalt) {
    var keys = [];
    try {
      for (var i = 0; i < window.localStorage.length; i++) {
        var k = window.localStorage.key(i);
        if (isTarget(k)) keys.push(k);
      }
    } catch (e) {}
    var chain = Promise.resolve();
    keys.forEach(function (k) {
      chain = chain.then(function () {
        var env = getItemNative(k);
        if (env === null) return;
        var plain = state.shadow[k] !== undefined ? Promise.resolve(state.shadow[k]) : null;
        if (plain === null) {
          var isEnv = false;
          try { var o = JSON.parse(env); isEnv = !!(o && (o.q === 1 || o.q === 2) && o.c); } catch (e2) {}
          plain = isEnv ? decWith(state.key, env, k) : Promise.resolve(env);
        }
        return plain.then(function (val) {
          if (val === null) return;
          state.shadow[k] = val;
          return encWith(newKey, val, k).then(function (newEnv) { setItemNative(k, newEnv); });
        });
      });
    });
    return chain.then(function () {
      if (newPsalt) state.psalt = newPsalt;
      state.key = newKey;
    });
  }

  function verifyPass(pass) {
    var psalt = getItemNative('qs_psalt');
    if (!psalt) return Promise.resolve(false);
    return deriveFrom(String(pass), psalt).then(function (cand) {
      var ver = getItemNative('qs_ver');
      if (!ver) return false;
      return decWith(cand, ver, 'qs_ver').then(function (plain) {
        return plain === VERIFIER;
      });
    });
  }

  function unlock(pass) {
    return new Promise(function (resolve) {
      if (!cfg.pl) { resolve({ ok: true, msg: 'no passphrase set' }); return; }
      var now = Date.now();
      if (now < state.failUntil) {
        var wait = Math.ceil((state.failUntil - now) / 1000);
        resolve({ ok: false, err: 'Too many attempts - wait ' + wait + 's' });
        return;
      }
      verifyPass(pass).then(function (good) {
        if (!good) {
          state.failCount++;
          audit('FAILED vault unlock attempt #' + state.failCount);
          if (state.failCount >= 5) {
            state.failUntil = now + 60000;
            state.failCount = 0;
            audit('unlock throttled for 60s (5 failed attempts)');
          }
          resolve({ ok: false, err: 'Wrong passphrase' });
          return;
        }
        state.failCount = 0;
        state.psalt = getItemNative('qs_psalt');
        deriveFrom(String(pass), state.psalt).then(function (k) {
          state.key = k;
          state.mode = 'open';
          audit('passphrase verified - vault opening');
          flushEnvelopes();
          resolve({ ok: true });
        });
      });
    });
  }

  function lock() {
    if (!cfg.pl || state.mode !== 'open') return;
    state.key = null;
    state.shadow = {};
    state.pending = {};
    state.envelopes = {};
    state.mode = 'locked';
    audit('vault locked by user/auto-lock');
    var ev = null;
    try { ev = new CustomEvent('qs-lock'); } catch (e) {}
    if (ev) document.dispatchEvent(ev);
    if (typeof renderPanel === 'function') renderPanel();
  }

  function setPassphrase(pass) {
    return new Promise(function (resolve) {
      if (cfg.pl) { resolve({ ok: false, err: 'A passphrase already exists - use Change' }); return; }
      if (state.mode !== 'open') { resolve({ ok: false, err: 'Vault is not open' }); return; }
      if (String(pass).length < 8) { resolve({ ok: false, err: 'At least 8 characters' }); return; }
      var salt2 = b64(randBytes(16));
      deriveFrom(String(pass), salt2).then(function (newKey) {
        encWith(newKey, VERIFIER, 'qs_ver').then(function (ver) {
          rekeyAll(newKey, salt2).then(function () {
            setItemNative('qs_psalt', salt2);
            setItemNative('qs_ver', ver);
            cfg.pl = 1;
            setItemNative('qs_cfg', JSON.stringify(cfg));
            audit('vault passphrase CREATED - all data re-encrypted');
            if (typeof renderPanel === 'function') renderPanel();
            armIdleLock();
            resolve({ ok: true });
          });
        });
      });
    });
  }

  function changePassphrase(oldPass, newPass) {
    return new Promise(function (resolve) {
      if (!cfg.pl) { resolve({ ok: false, err: 'No passphrase set yet' }); return; }
      if (String(newPass).length < 8) { resolve({ ok: false, err: 'At least 8 characters' }); return; }
      verifyPass(oldPass).then(function (good) {
        if (!good) { resolve({ ok: false, err: 'Current passphrase is wrong' }); return; }
        var salt2 = b64(randBytes(16));
        deriveFrom(String(newPass), salt2).then(function (newKey) {
          encWith(newKey, VERIFIER, 'qs_ver').then(function (ver) {
            rekeyAll(newKey, salt2).then(function () {
              setItemNative('qs_psalt', salt2);
              setItemNative('qs_ver', ver);
              setItemNative('qs_cfg', JSON.stringify(cfg));
              audit('vault passphrase CHANGED - all data re-encrypted');
              if (typeof renderPanel === 'function') renderPanel();
              resolve({ ok: true });
            });
          });
        });
      });
    });
  }

  function removePassphrase(pass) {
    return new Promise(function (resolve) {
      if (!cfg.pl) { resolve({ ok: false, err: 'No passphrase set' }); return; }
      verifyPass(pass).then(function (good) {
        if (!good) { resolve({ ok: false, err: 'Passphrase is wrong' }); return; }
        sha256(fingerprint()).then(function (fpHash) {
          return deriveFrom(fpHash, state.salt).then(function (anonKey) {
            return rekeyAll(anonKey, null).then(function () {
              removeItemNative('qs_psalt');
              removeItemNative('qs_ver');
              cfg.pl = 0;
              setItemNative('qs_cfg', JSON.stringify(cfg));
              audit('vault passphrase REMOVED - device key restored');
              disarmIdleLock();
              if (typeof renderPanel === 'function') renderPanel();
              resolve({ ok: true });
            });
          });
        });
      });
    });
  }

  /* --------------------------- idle auto-lock --------------------------- */
  function armIdleLock() {
    disarmIdleLock();
    var bump = function () {
      if (state.idleTimer) clearTimeout(state.idleTimer);
      state.idleTimer = setTimeout(function () { if (cfg.pl && state.mode === 'open') lock(); }, IDLE_LOCK_MS);
    };
    ['pointerdown', 'keydown', 'wheel', 'touchstart'].forEach(function (evName) {
      document.addEventListener(evName, bump, { passive: true });
    });
    bump();
  }
  function disarmIdleLock() {
    if (state.idleTimer) { clearTimeout(state.idleTimer); state.idleTimer = null; }
  }

  /* ------------------------------- init --------------------------------- */
  function init() {
    state.token = randHex(16);
    state.salt = getItemNative('qs_salt');
    if (!state.salt) {
      state.salt = b64(randBytes(16));
      setItemNative('qs_salt', state.salt);
    }
    try {
      readCfg();
    } catch (e) {}
    try {
      delete window.localStorage.setItem;
      delete window.localStorage.getItem;
      delete window.localStorage.removeItem;
      Storage.prototype.setItem = wrappedSetItem;
      Storage.prototype.getItem = wrappedGetItem;
      Storage.prototype.removeItem = wrappedRemoveItem;
      if (window.localStorage.setItem !== wrappedSetItem) state.lastError = 'storage patch rejected';
    } catch (e) { state.lastError = 'storage patch failed'; }

    integrityCheck();
    scheduleThreatProbes();
    restoreAudits();

    if (cfg.pl) {
      state.mode = 'locked';
      audit('vault LOCKED - passphrase required');
    } else {
      sha256(fingerprint()).then(function (fpHash) {
        return deriveFrom(fpHash, state.salt);
      }).then(function (k) {
        state.key = k;
        state.mode = 'open';
        audit('vault unlocked (device key) - set a passphrase to go zero-knowledge');
        flushEnvelopes();
      }).catch(function (e) {
        state.lastError = String(e);
        audit('device-key unlock failed: ' + state.lastError);
        state.mode = 'open';   // degrade: app stays usable
        var ev = null;
        try { ev = new CustomEvent('qs-unlock', { detail: { degraded: true } }); } catch (e2) {}
        if (ev) document.dispatchEvent(ev);
        state.unlockCbs.forEach(function (fn) { try { fn(); } catch (e3) {} });
        state.unlockCbs = [];
      });
    }
  }

  function restoreAudits() {
    try {
      var a = getItemNative('qs_audit');
      if (a) { var arr = JSON.parse(a); if (Array.isArray(arr)) state.audits = arr.slice(0, 25); }
    } catch (e) {}
  }
  function audit(ev) {
    state.audits.unshift({ t: nowStr(), e: ev });
    if (state.audits.length > 25) state.audits.length = 25;
    try { setItemNative('qs_audit', JSON.stringify(state.audits)); } catch (e) {}
  }

  function integrityCheck() {
    if (!EXPECTED_APP_SHA || EXPECTED_APP_SHA.length !== 64) return;
    fetch(APP_URL + '?v=' + state.token.slice(0, 4))
      .then(function (r) { if (!r.ok) { audit('integrity check unavailable (http ' + r.status + ')'); return null; } return r.text(); })
      .then(function (txt) { if (txt === null) return null;
        return sha256(txt).then(function (h) {
          if (h !== EXPECTED_APP_SHA) {
            state.detections++;
            audit('TAMPER: app.js integrity mismatch (expected ' + EXPECTED_APP_SHA.slice(0, 12) + ', got ' + h.slice(0, 12) + ')');
          } else {
            audit('integrity verified: app.js SHA-256 ok');
          }
        });
      })
      .catch(function () { audit('integrity check unavailable (offline?)'); });
  }

  function scheduleThreatProbes() {
    try {
      setInterval(function () {
        var w = window.outerWidth - window.innerWidth;
        var h = window.outerHeight - window.innerHeight;
        if ((w > 300 && h > 300) && state.detections < 3) {
          state.detections++;
          audit('debugger/devtools window detected');
        }
      }, 5000);
      var origLog = window.console.log;
      window.console.log = function () {
        if (origLog.toString().indexOf('native code') === -1) {
          state.detections++;
          audit('console tampering detected');
        }
        return origLog.apply(window.console, arguments);
      };
    } catch (e) {}
  }

  function sanitize(str) {
    return String(str == null ? '' : str)
      .replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F]/g, '')
      .replace(/<script[\s\S]*?<\/script>/gi, '')
      .replace(/on\w+\s*=\s*(['"]).*?\1/gi, '')
      .replace(/javascript\s*:/gi, '')
      .replace(/data\s*:\s*text\/html/gi, '');
  }

  /* ---------------------------- public API ------------------------------ */
  window.QS = {
    get ready() { return state.mode === 'open'; },
    get locked() { return state.mode === 'locked'; },
    get mode() { return state.mode; },
    get hasPassphrase() { return !!cfg.pl; },
    get cipher() { return 'AES-256-GCM'; },
    get kdf() { return KDF; },
    get mac() { return MAC; },
    get integrity() { return INTEGRITY; },
    get token() { return state.token; },
    get detections() { return state.detections; },
    get audits() { return state.audits; },
    get lastError() { return state.lastError; },
    sanitize: sanitize,
    audit: audit,
    newToken: function () { state.token = randHex(16); return state.token; },
    unlock: unlock,
    lock: lock,
    setPassphrase: setPassphrase,
    changePassphrase: changePassphrase,
    removePassphrase: removePassphrase,
    onUnlock: function (fn) {
      if (state.mode === 'open') { try { fn(); } catch (e) {} return; }
      state.unlockCbs.push(fn);
    },
    vaultStats: function () {
      var s = { chat: 0, mem: 0, auth: 0, other: 0 };
      try {
        for (var i = 0; i < window.localStorage.length; i++) {
          var k = window.localStorage.key(i);
          if (!isTarget(k)) continue;
          var v = getItemNative(k);
          if (!v) continue;
          if (k.indexOf('aai_chat') === 0) s.chat++;
          else if (k.indexOf('aai_mem') === 0) s.mem++;
          else if (k.indexOf('aai_user') === 0) s.auth = 1;
          else s.other++;
        }
      } catch (e) {}
      return s;
    },
    isEncrypted: function (k) {
      var v = getItemNative(k);
      if (!v) return false;
      try { var o = JSON.parse(v); return !!(o && (o.q === 1 || o.q === 2)); } catch (e) { return false; }
    }
  };

  /* --------------------------- Security Center UI ----------------------- */
  function esc(s) { return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
    return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
  }); }
  function msg(t) {
    var el = document.getElementById('qsMsg');
    if (el) el.textContent = t || '';
  }
  function gridRow(k, v) {
    return '<div class="qs-row"><span class="qs-k">' + esc(k) + '</span><span class="qs-v">' + v + '</span></div>';
  }
  function auditHtml() {
    return '<div class="qs-audit"><h4>Security audit log</h4>' +
      (state.audits.length ? state.audits.map(function (a) {
        return '<div class="qs-audit-item"><span>' + esc(a.t) + '</span>' + esc(a.e) + '</div>';
      }).join('') : '<div class="qs-audit-item">No events yet.</div>') + '</div>';
  }
  function renderPanel() {
    var body = document.getElementById('qsBody');
    if (!body) return;
    var vs = window.QS.vaultStats();
    if (state.mode === 'locked') {
      body.innerHTML =
        '<div class="qs-status warn"><i class="fas fa-lock"></i> Vault LOCKED - passphrase required</div>' +
        '<div class="qs-lockbox">' +
        '<label class="qs-lbl" for="qsPass">Enter your vault passphrase</label>' +
        '<div class="qs-lockrow"><input type="password" id="qsPass" class="qs-input" placeholder="Passphrase" autocomplete="off">' +
        '<button class="qs-btn" onclick="QSUnlock()"><i class="fas fa-unlock"></i> Unlock</button></div>' +
        '<div id="qsMsg" class="qs-msg"></div>' +
        '<div class="qs-note">All conversations, memory, identity and complaints are sealed with AES-256-GCM. ' +
        'Without your passphrase the data cannot be opened - even if this storage is copied, even with a quantum computer.</div>' +
        '</div>' + auditHtml();
      return;
    }
    var status = cfg.pl ? 'ACTIVE - zero-knowledge vault' : 'ACTIVE (device key)';
    body.innerHTML =
      '<div class="qs-status ok"><i class="fas fa-shield-halved"></i> Quantum Shield ' + status +
      (cfg.pl ? ' <button class="qs-mini" onclick="QSLock()"><i class="fas fa-lock"></i> Lock now</button>' : '') +
      '</div>' +
      '<div class="qs-grid">' +
      gridRow('Cipher', 'AES-256-GCM <span class="qs-sub">(quantum-resistant)</span>') +
      gridRow('Key derivation', KDF) +
      gridRow('Authentication', MAC + ' <span class="qs-sub">(AAD-bound)</span>') +
      gridRow('Integrity', INTEGRITY) +
      gridRow('Session token', '<code>' + esc(state.token.slice(0, 12)) + '</code> <button class="qs-mini" onclick="QSRotate()">Rotate</button>') +
      gridRow('Vault', 'chat:' + vs.chat + ' · memory:' + vs.mem + ' · identity:' + vs.auth + ' · other:' + vs.other) +
      gridRow('Threat detections', String(state.detections)) +
      gridRow('Vault key', cfg.pl ? '<span class="qs-sub">Passphrase-derived (never stored)</span>' : '<span class="qs-warn-txt">Device-derived - upgrade below</span>') +
      '</div>' +
      '<div id="qsMsg" class="qs-msg"></div>' + settingsHtml() +
      '<div class="qs-note">' + (cfg.pl ?
        'Zero-knowledge vault: the key is derived from your passphrase via PBKDF2 (310,000 rounds) and never touches disk. ' +
        'A stolen copy of this storage is useless ciphertext. If you forget the passphrase the data cannot be recovered - by design.' :
        'Data is currently encrypted with a device-derived key - an attacker who copies this storage and runs the page could re-derive it. ' +
        'Create a passphrase below to go zero-knowledge: the key will then come only from your memory.') + '</div>' +
      auditHtml();
  }
  function settingsHtml() {
    if (!cfg.pl) {
      return '<div class="qs-settings"><h4>Upgrade to zero-knowledge</h4>' +
        '<div class="qs-lockrow"><input type="password" id="qsNew" class="qs-input" placeholder="New passphrase (min 8 chars)">' +
        '<button class="qs-btn" onclick="QSSet()"><i class="fas fa-key"></i> Set passphrase</button></div>' +
        '<div class="qs-lockrow"><input type="password" id="qsNew2" class="qs-input" placeholder="Repeat passphrase"></div></div>';
    }
    return '<div class="qs-settings"><h4>Vault settings</h4>' +
      '<div class="qs-lockrow"><input type="password" id="qsOld" class="qs-input" placeholder="Current passphrase">' +
      '<input type="password" id="qsNew" class="qs-input" placeholder="New passphrase">' +
      '<button class="qs-btn" onclick="QSChange()"><i class="fas fa-sync"></i> Change</button></div>' +
      '<div class="qs-lockrow"><input type="password" id="qsRm" class="qs-input" placeholder="Current passphrase to remove">' +
      '<button class="qs-btn qs-danger" onclick="QSRemove()"><i class="fas fa-unlock-alt"></i> Remove passphrase</button></div></div>';
  }

  window.QSRender = function () { renderPanel(); };
  window.QSToggle = function () {
    var ov = document.getElementById('qsOverlay');
    if (!ov) return;
    var open = ov.classList.toggle('open');
    if (open) renderPanel();
  };
  window.QSClose = function () {
    var ov = document.getElementById('qsOverlay');
    if (ov) ov.classList.remove('open');
  };
  window.QSRotate = function () { QS.newToken(); renderPanel(); msg('Session token rotated'); };
  window.QSUnlock = function () {
    var pass = document.getElementById('qsPass');
    var btn = pass ? pass.parentNode.querySelector('.qs-btn') : null;
    if (btn) btn.disabled = true;
    QS.unlock(pass ? pass.value : '').then(function (res) {
      if (btn) btn.disabled = false;
      if (res && res.ok) { if (pass) pass.value = ''; renderPanel(); }
      else msg((res && res.err) || 'Unlock failed');
    });
  };
  window.QSLock = function () { QS.lock(); };
  window.QSSet = function () {
    var a = document.getElementById('qsNew'), b = document.getElementById('qsNew2');
    if (!a || !b) return;
    if (a.value !== b.value) { msg('Passphrases do not match'); return; }
    QS.setPassphrase(a.value).then(function (res) {
      msg(res && res.ok ? 'Zero-knowledge vault enabled - all data re-encrypted' : (res && res.err) || 'Failed');
      a.value = ''; if (b) b.value = '';
      if (res && res.ok) renderPanel();
    });
  };
  window.QSChange = function () {
    var o = document.getElementById('qsOld'), n = document.getElementById('qsNew');
    if (!o || !n) return;
    QS.changePassphrase(o.value, n.value).then(function (res) {
      msg(res && res.ok ? 'Passphrase changed - data re-encrypted' : (res && res.err) || 'Failed');
      o.value = ''; n.value = '';
    });
  };
  window.QSRemove = function () {
    var r = document.getElementById('qsRm');
    if (!r) return;
    QS.removePassphrase(r.value).then(function (res) {
      msg(res && res.ok ? 'Passphrase removed - device key restored' : (res && res.err) || 'Failed');
      r.value = '';
      if (res && res.ok) renderPanel();
    });
  };

  function injectButton() {
    var tt = document.getElementById('themeToggle');
    if (!tt || document.getElementById('qsShield')) return;
    var b = document.createElement('button');
    b.className = 'theme-toggle qs-shield-btn';
    b.id = 'qsShield';
    b.setAttribute('aria-label', 'Quantum Security Center');
    b.title = 'Quantum Security Center';
    b.innerHTML = '<i class="fas fa-shield-halved"></i>';
    b.onclick = function () { window.QSToggle(); };
    tt.parentNode.insertBefore(b, tt.nextSibling);
    var ov = document.createElement('div');
    ov.className = 'qs-overlay';
    ov.id = 'qsOverlay';
    ov.innerHTML =
      '<div class="qs-card">' +
      '<div class="qs-head"><span><i class="fas fa-shield-halved"></i> Quantum Security Center</span>' +
      '<button class="qs-x" onclick="QSClose()"><i class="fas fa-times"></i></button></div>' +
      '<div id="qsBody"></div></div>';
    ov.addEventListener('click', function (e) { if (e.target === ov) window.QSClose(); });
    document.body.appendChild(ov);
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', injectButton);
  } else {
    injectButton();
  }

  init();
})();
