// WhatsApp CRM dashboard - plain JavaScript, no build step.
const $ = (sel, el = document) => el.querySelector(sel);
const $$ = (sel, el = document) => [...el.querySelectorAll(sel)];
const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const fromSql = (s) => (s ? new Date(s.replace(' ', 'T') + 'Z') : null);
const fmtTime = (s) => { const d = fromSql(s); return d ? d.toLocaleString([], { dateStyle: 'short', timeStyle: 'short' }) : ''; };
const money = (v) => Number(v || 0).toLocaleString(undefined, { style: 'currency', currency: 'USD', maximumFractionDigits: 0 });
const tagsOf = (c) => (c.tags || '').split(',').map((t) => t.trim()).filter(Boolean);

const state = { view: 'inbox', activeId: null, search: '', lastMsgSig: '' };

async function api(path, { method = 'GET', body } = {}) {
  const res = await fetch('/api' + path, {
    method,
    headers: body ? { 'Content-Type': 'application/json' } : {},
    body: body ? JSON.stringify(body) : undefined,
  });
  if (res.status === 204) return null;
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || `Request failed (${res.status})`);
  return data;
}

function toast(text, isError = false) {
  const t = $('#toast');
  t.textContent = text;
  t.className = 'toast' + (isError ? ' error' : '');
  clearTimeout(toast.timer);
  toast.timer = setTimeout(() => t.classList.add('hidden'), 3500);
}

// Run an async action and show any error as a toast
const safe = (fn) => async (...args) => { try { await fn(...args); } catch (e) { toast(e.message, true); } };

// Generic modal: fields = [{ name, label, type, value, options }]
function openModal(title, fields, submitLabel = 'Save') {
  return new Promise((resolve) => {
    const dlg = $('#modal');
    const form = $('#modalForm');
    form.innerHTML = `<h2>${esc(title)}</h2>` + fields.map((f) => {
      if (f.type === 'select') {
        return `<label>${esc(f.label)}</label><select name="${f.name}">${f.options.map((o) =>
          `<option value="${esc(o.value)}" ${String(o.value) === String(f.value ?? '') ? 'selected' : ''}>${esc(o.label)}</option>`).join('')}</select>`;
      }
      if (f.type === 'textarea') return `<label>${esc(f.label)}</label><textarea name="${f.name}">${esc(f.value)}</textarea>`;
      if (f.type === 'checkbox') return `<label class="inline"><input type="checkbox" name="${f.name}" ${f.value ? 'checked' : ''}> ${esc(f.label)}</label>`;
      return `<label>${esc(f.label)}</label><input name="${f.name}" type="${f.type || 'text'}" value="${esc(f.value)}" ${f.placeholder ? `placeholder="${esc(f.placeholder)}"` : ''}>`;
    }).join('') + `<div class="actions"><button class="btn secondary" value="cancel">Cancel</button><button class="btn" value="ok">${esc(submitLabel)}</button></div>`;
    dlg.onclose = () => {
      if (dlg.returnValue !== 'ok') return resolve(null);
      const out = {};
      for (const f of fields) {
        const el = form.elements[f.name];
        out[f.name] = f.type === 'checkbox' ? el.checked : el.value;
      }
      resolve(out);
    };
    dlg.returnValue = '';
    dlg.showModal();
  });
}

// ---------------- Navigation ----------------
function go(view) {
  state.view = view;
  $$('#nav button').forEach((b) => b.classList.toggle('active', b.dataset.view === view));
  views[view]();
}
$('#nav').addEventListener('click', (e) => { const b = e.target.closest('button'); if (b) go(b.dataset.view); });

async function refreshStatus() {
  try {
    const s = await api('/status');
    $('#modeBadge').textContent = s.live ? '● Live' : '● Mock mode';
    $('#modeBadge').title = s.live ? 'Connected to WhatsApp Cloud API' : 'No WhatsApp credentials - messages are not really sent';
    const b = $('#unreadBadge');
    b.textContent = s.stats.unread;
    b.classList.toggle('hidden', !s.stats.unread);
    return s;
  } catch { return null; }
}

// ---------------- Inbox ----------------
async function renderInbox() {
  $('#view').innerHTML = `
    <div class="inbox ${state.activeId ? 'has-chat' : ''}" id="inbox">
      <div class="convlist">
        <div class="search"><input id="convSearch" placeholder="Search name, phone…" value="${esc(state.search)}"></div>
        <div class="convs" id="convs"></div>
      </div>
      <div class="chat" id="chat"><div class="empty">Select a conversation<br><span class="muted">New WhatsApp messages appear here automatically.</span></div></div>
      <div class="side" id="side"></div>
    </div>`;
  $('#convSearch').addEventListener('input', (e) => { state.search = e.target.value; loadConvs(); });
  await loadConvs();
  if (state.activeId) await openChat(state.activeId);
}

async function loadConvs() {
  const list = await api('/contacts' + (state.search ? `?q=${encodeURIComponent(state.search)}` : ''));
  const el = $('#convs');
  if (!el) return;
  el.innerHTML = list.length ? list.map((c) => `
    <div class="conv ${c.id === state.activeId ? 'active' : ''}" data-id="${c.id}">
      <div class="top"><span class="name">${esc(c.name || '+' + c.phone)}</span>
        <span class="muted" style="font-size:11px">${fmtTime(c.last_message_at)}</span></div>
      <div class="top"><span class="preview">${esc(c.last_message || 'No messages yet')}</span>
        ${c.unread ? `<span class="badge">${c.unread}</span>` : ''}</div>
    </div>`).join('') : '<div class="empty">No contacts yet.<br>Use Settings → Simulator to test.</div>';
  $$('.conv', el).forEach((n) => n.addEventListener('click', () => openChat(Number(n.dataset.id))));
}

async function openChat(id) {
  state.activeId = id;
  state.lastMsgSig = '';
  $('#inbox')?.classList.add('has-chat');
  $$('.conv').forEach((n) => n.classList.toggle('active', Number(n.dataset.id) === id));
  const c = await api(`/contacts/${id}`);

  $('#chat').innerHTML = `
    <div class="chathead">
      <div class="row"><button class="btn secondary small" id="backBtn" title="Back">←</button>
        <div><b>${esc(c.name || '+' + c.phone)}</b><div class="muted" style="font-size:12px">+${esc(c.phone)}</div></div></div>
      <label class="inline" title="When paused, the bot will not auto-reply to this contact">
        <input type="checkbox" id="botToggle" ${c.bot_paused ? '' : 'checked'}> 🤖 Bot</label>
    </div>
    <div class="msgs" id="msgs"></div>
    <div class="composer">
      <div class="warnbar ${c.in_window ? 'hidden' : ''}">⚠️ More than 24h since this contact last messaged you. WhatsApp only allows
        <b>approved templates</b> now. <a href="#" id="tplLink">Send a template</a></div>
      <div class="row"><textarea id="composer" class="grow" placeholder="Type a message… (Enter to send, Shift+Enter for new line). {name} is replaced with the contact's name"></textarea>
        <button class="btn" id="sendBtn">Send</button></div>
    </div>`;
  $('#backBtn').onclick = () => { state.activeId = null; $('#inbox').classList.remove('has-chat'); };
  $('#botToggle').onchange = safe(async (e) => {
    await api(`/contacts/${id}`, { method: 'PATCH', body: { bot_paused: !e.target.checked } });
    toast(e.target.checked ? 'Bot resumed for this contact' : 'Bot paused - you are handling this chat');
  });
  const send = safe(async () => {
    const body = $('#composer').value;
    if (!body.trim()) return;
    $('#composer').value = '';
    try { await api(`/contacts/${id}/messages`, { method: 'POST', body: { body } }); }
    finally {
      await loadMessages(id);
      loadConvs();
      // Replying can auto-pause the bot (see Bot settings), so re-sync the toggle
      const fresh = await api(`/contacts/${id}`);
      if ($('#botToggle')) $('#botToggle').checked = !fresh.bot_paused;
    }
  });
  $('#sendBtn').onclick = send;
  $('#composer').addEventListener('keydown', (e) => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(); } });
  $('#tplLink').onclick = (e) => { e.preventDefault(); sendTemplateDialog(id); };

  await Promise.all([loadMessages(id), renderSide(c)]);
}

async function loadMessages(id) {
  const msgs = await api(`/contacts/${id}/messages`);
  const sig = msgs.map((m) => m.id + m.status).join();
  const el = $('#msgs');
  if (!el || sig === state.lastMsgSig) return;
  state.lastMsgSig = sig;
  api(`/contacts/${id}/read`, { method: 'POST' }).then(() => { refreshStatus(); loadConvs(); }).catch(() => {}); // you're looking at it, so it's read
  const tick = { queued: '🕓', sent: '✓', delivered: '✓✓', read: '✓✓ read', failed: '⚠️ failed' };
  el.innerHTML = msgs.map((m) => `
    <div class="msg ${m.direction} ${m.status === 'failed' ? 'failed' : ''}" ${m.error ? `title="${esc(m.error)}"` : ''}>
      <div class="body">${esc(m.body)}</div>
      <div class="meta">${m.sent_by && m.sent_by !== 'agent' ? (m.sent_by === 'bot' ? '🤖 bot · ' : '⏰ follow-up · ') : ''}${fmtTime(m.created_at)}
        ${m.direction === 'out' ? ' ' + (tick[m.status] || '') : ''}</div>
    </div>`).join('') || '<div class="empty">No messages yet. Say hello 👋</div>';
  el.scrollTop = el.scrollHeight;
}

async function renderSide(c) {
  const [deals, fus] = await Promise.all([api(`/deals?contactId=${c.id}`), api(`/followups?contactId=${c.id}&status=pending`)]);
  const social = JSON.parse(c.social || '{}');
  $('#side').innerHTML = `
    <div class="row"><b class="grow">Contact</b><button class="btn secondary small" id="editC">Edit</button></div>
    <div>${esc(c.name || '—')}</div><div class="muted">+${esc(c.phone)}${c.email ? ' · ' + esc(c.email) : ''}</div>
    <div>${tagsOf(c).map((t) => `<span class="tag">${esc(t)}</span>`).join('')}</div>
    ${c.notes ? `<h3>Notes</h3><div style="white-space:pre-wrap">${esc(c.notes)}</div>` : ''}
    ${Object.values(social).some(Boolean) ? `<h3>Social</h3>${Object.entries(social).filter(([, v]) => v).map(([k, v]) => `<div>${esc(k)}: ${esc(v)}</div>`).join('')}` : ''}
    <h3>Deals</h3>
    ${deals.map((d) => `<div class="deal" style="cursor:default">${esc(d.title)} <span class="v">${money(d.value)}</span></div>`).join('') || '<div class="muted">No deals</div>'}
    <button class="btn secondary small" id="addDealC" style="margin-top:6px">+ Deal</button>
    <h3>Pending follow-ups</h3>
    ${fus.map((f) => `<div class="muted" style="font-size:12px">⏰ ${fmtTime(f.send_at)} — ${esc(f.template_name ? 'template: ' + f.template_name : f.body).slice(0, 80)}</div>`).join('') || '<div class="muted">None</div>'}
    <button class="btn secondary small" id="addFuC" style="margin-top:6px">+ Follow-up</button>`;
  $('#editC').onclick = safe(async () => { if (await editContactDialog(c)) openChat(c.id); });
  $('#addDealC').onclick = safe(async () => { if (await dealDialog({ contact_id: c.id, title: `${c.name || c.phone} deal` })) renderSide(c); });
  $('#addFuC').onclick = safe(async () => { if (await followupDialog(c.id)) renderSide(c); });
}

async function sendTemplateDialog(contactId) {
  const v = await openModal('Send WhatsApp template', [
    { name: 'templateName', label: 'Template name (as approved in Meta WhatsApp Manager)', placeholder: 'hello_world' },
    { name: 'templateLang', label: 'Language code', value: 'en_US' },
    { name: 'templateParams', label: 'Body parameters {{1}}, {{2}}… one per line ({name} allowed)', type: 'textarea' },
  ], 'Send');
  if (!v || !v.templateName) return;
  await safe(async () => {
    await api(`/contacts/${contactId}/messages`, { method: 'POST', body: { ...v, templateParams: v.templateParams.split('\n').map((s) => s.trim()).filter(Boolean) } });
    toast('Template sent');
  })();
  loadMessages(contactId);
}

// ---------------- Contacts ----------------
async function editContactDialog(c = {}) {
  const social = JSON.parse(c.social || '{}');
  const v = await openModal(c.id ? 'Edit contact' : 'New contact', [
    ...(c.id ? [] : [{ name: 'phone', label: 'WhatsApp number (with country code, e.g. 6591234567)' }]),
    { name: 'name', label: 'Name', value: c.name },
    { name: 'email', label: 'Email', value: c.email },
    { name: 'tags', label: 'Tags (comma separated)', value: c.tags },
    { name: 'notes', label: 'Notes', type: 'textarea', value: c.notes },
    { name: 'instagram', label: 'Instagram handle', value: social.instagram },
    { name: 'facebook', label: 'Facebook profile', value: social.facebook },
    { name: 'tiktok', label: 'TikTok handle', value: social.tiktok },
  ]);
  if (!v) return null;
  const { instagram, facebook, tiktok, ...rest } = v;
  const body = { ...rest, tags: rest.tags.split(',').map((t) => t.trim()).filter(Boolean).join(',') };
  let saved;
  if (c.id) saved = await api(`/contacts/${c.id}`, { method: 'PATCH', body: { ...body, social: { instagram, facebook, tiktok } } });
  else {
    saved = await api('/contacts', { method: 'POST', body });
    await api(`/contacts/${saved.id}`, { method: 'PATCH', body: { social: { instagram, facebook, tiktok } } });
  }
  toast('Contact saved');
  return saved;
}

async function renderContacts() {
  $('#view').innerHTML = `
    <div class="card">
      <div class="row wrap">
        <input id="cSearch" class="grow" placeholder="Search…" style="max-width:320px" value="${esc(state.search)}">
        <input id="cTag" placeholder="Filter by tag" style="max-width:180px">
        <span class="grow"></span>
        <a class="btn secondary" href="/api/contacts/export.csv">Export CSV</a>
        <button class="btn" id="newC">+ New contact</button>
      </div>
    </div>
    <div class="card tablewrap"><table><thead><tr><th>Name</th><th>Phone</th><th>Tags</th><th>Deals</th><th>Bot</th><th>Last message</th><th></th></tr></thead>
      <tbody id="cRows"></tbody></table></div>`;
  const load = safe(async () => {
    const params = new URLSearchParams();
    if ($('#cSearch').value) params.set('q', $('#cSearch').value);
    if ($('#cTag').value) params.set('tag', $('#cTag').value.trim());
    const list = await api('/contacts?' + params);
    $('#cRows').innerHTML = list.map((c) => `
      <tr class="click" data-id="${c.id}">
        <td><b>${esc(c.name || '—')}</b>${c.email ? `<div class="muted">${esc(c.email)}</div>` : ''}</td>
        <td>+${esc(c.phone)}</td>
        <td>${tagsOf(c).map((t) => `<span class="tag">${esc(t)}</span>`).join('')}</td>
        <td>${c.deal_count}</td>
        <td>${c.bot_paused ? '⏸ paused' : '🤖 on'}</td>
        <td class="muted">${fmtTime(c.last_message_at)}</td>
        <td><button class="btn danger small" data-del="${c.id}">Delete</button></td>
      </tr>`).join('') || '<tr><td colspan="7" class="muted">No contacts found.</td></tr>';
  });
  $('#cSearch').addEventListener('input', load);
  $('#cTag').addEventListener('input', load);
  $('#newC').onclick = safe(async () => { if (await editContactDialog()) load(); });
  $('#cRows').addEventListener('click', safe(async (e) => {
    const del = e.target.closest('[data-del]');
    if (del) {
      if (confirm('Delete this contact and all of their messages and follow-ups?')) { await api(`/contacts/${del.dataset.del}`, { method: 'DELETE' }); load(); }
      return;
    }
    const tr = e.target.closest('tr[data-id]');
    if (tr) { state.activeId = Number(tr.dataset.id); go('inbox'); }
  }));
  load();
}

// ---------------- Pipeline ----------------
async function contactOptions() {
  const list = await api('/contacts');
  return [{ value: '', label: '— none —' }, ...list.map((c) => ({ value: c.id, label: `${c.name || 'Unnamed'} (+${c.phone})` }))];
}

async function dealDialog(d = {}) {
  const [stages, contacts] = await Promise.all([api('/stages'), contactOptions()]);
  const v = await openModal(d.id ? 'Edit deal' : 'New deal', [
    { name: 'title', label: 'Title', value: d.title },
    { name: 'value', label: 'Value', type: 'number', value: d.value ?? 0 },
    { name: 'contact_id', label: 'Contact', type: 'select', value: d.contact_id, options: contacts },
    { name: 'stage_id', label: 'Stage', type: 'select', value: d.stage_id ?? stages[0]?.id, options: stages.map((s) => ({ value: s.id, label: s.name })) },
    { name: 'notes', label: 'Notes', type: 'textarea', value: d.notes },
  ]);
  if (!v) return null;
  const body = { ...v, value: Number(v.value) || 0, contact_id: v.contact_id ? Number(v.contact_id) : null, stage_id: Number(v.stage_id) };
  const saved = d.id ? await api(`/deals/${d.id}`, { method: 'PATCH', body }) : await api('/deals', { method: 'POST', body });
  toast('Deal saved');
  return saved;
}

async function renderPipeline() {
  const [stages, deals, status] = await Promise.all([api('/stages'), api('/deals'), api('/status')]);
  $('#view').innerHTML = `
    <div class="stats">
      <div class="stat"><span class="muted">Open deals</span><b>${status.stats.openDeals.n}</b></div>
      <div class="stat"><span class="muted">Open pipeline value</span><b>${money(status.stats.openDeals.v)}</b></div>
      <div class="stat"><span class="muted">Won</span><b>${money(status.stats.wonValue)}</b></div>
      <div class="stat"><span class="muted">Contacts</span><b>${status.stats.contacts}</b></div>
    </div>
    <div class="row" style="margin-bottom:12px"><button class="btn" id="newDeal">+ New deal</button>
      <button class="btn secondary" id="newStage">+ Stage</button>
      <span class="muted">Drag deals between stages · click a stage name to rename it</span></div>
    <div class="board" id="board">${stages.map((s) => {
      const items = deals.filter((d) => d.stage_id === s.id);
      return `<div class="col" data-stage="${s.id}">
        <div class="colhead" style="border-color:${esc(s.color)}">
          <span class="t" data-rename="${s.id}">${esc(s.name)}</span>
          <span class="muted" style="font-size:12px">${items.length} · ${money(items.reduce((a, d) => a + d.value, 0))}
            <button class="btn secondary small" data-delstage="${s.id}" title="Delete stage">×</button></span>
        </div>
        <div class="colbody">${items.map((d) => `
          <div class="deal" draggable="true" data-deal="${d.id}">
            <div><b>${esc(d.title)}</b></div>
            <div class="row"><span class="v grow">${money(d.value)}</span>
              ${d.contact_id ? `<a href="#" data-chat="${d.contact_id}" title="Open chat">💬</a>` : ''}</div>
            ${d.contact_name || d.contact_phone ? `<div class="muted" style="font-size:12px">${esc(d.contact_name || '+' + d.contact_phone)}</div>` : ''}
          </div>`).join('')}</div>
      </div>`;
    }).join('')}</div>`;

  const board = $('#board');
  board.addEventListener('dragstart', (e) => { const d = e.target.closest('[data-deal]'); if (d) e.dataTransfer.setData('text/plain', d.dataset.deal); });
  $$('.col', board).forEach((col) => {
    col.addEventListener('dragover', (e) => { e.preventDefault(); col.classList.add('dragover'); });
    col.addEventListener('dragleave', () => col.classList.remove('dragover'));
    col.addEventListener('drop', safe(async (e) => {
      e.preventDefault();
      col.classList.remove('dragover');
      const id = e.dataTransfer.getData('text/plain');
      if (id) { await api(`/deals/${id}`, { method: 'PATCH', body: { stage_id: Number(col.dataset.stage) } }); renderPipeline(); }
    }));
  });
  board.addEventListener('click', safe(async (e) => {
    const chat = e.target.closest('[data-chat]');
    if (chat) { e.preventDefault(); state.activeId = Number(chat.dataset.chat); return go('inbox'); }
    const ren = e.target.closest('[data-rename]');
    if (ren) {
      const s = stages.find((x) => x.id === Number(ren.dataset.rename));
      const v = await openModal('Edit stage', [{ name: 'name', label: 'Name', value: s.name }, { name: 'color', label: 'Color', type: 'color', value: s.color }]);
      if (v) { await api(`/stages/${s.id}`, { method: 'PATCH', body: v }); renderPipeline(); }
      return;
    }
    const del = e.target.closest('[data-delstage]');
    if (del) { if (confirm('Delete this stage?')) { await api(`/stages/${del.dataset.delstage}`, { method: 'DELETE' }); renderPipeline(); } return; }
    const card = e.target.closest('[data-deal]');
    if (card) {
      const d = deals.find((x) => x.id === Number(card.dataset.deal));
      if (await dealDialog(d)) renderPipeline();
    }
  }));
  $('#newDeal').onclick = safe(async () => { if (await dealDialog()) renderPipeline(); });
  $('#newStage').onclick = safe(async () => {
    const v = await openModal('New stage', [{ name: 'name', label: 'Name' }, { name: 'color', label: 'Color', type: 'color', value: '#64748b' }]);
    if (v?.name) { await api('/stages', { method: 'POST', body: v }); renderPipeline(); }
  });
}

// ---------------- Follow-ups ----------------
function localInputValue(date) {
  const d = new Date(date.getTime() - date.getTimezoneOffset() * 60000);
  return d.toISOString().slice(0, 16);
}

async function followupDialog(contactId = null) {
  const contacts = (await contactOptions()).slice(1);
  const v = await openModal('Schedule follow-up', [
    contactId
      ? { name: 'contactId', label: 'Contact', type: 'select', value: contactId, options: contacts }
      : { name: 'contactId', label: 'Contact (or leave empty and use a tag below)', type: 'select', value: '', options: [{ value: '', label: '— by tag —' }, ...contacts] },
    ...(contactId ? [] : [{ name: 'tag', label: 'Send to every contact with tag', placeholder: 'e.g. interested-pricing' }]),
    { name: 'sendAt', label: 'Send at', type: 'datetime-local', value: localInputValue(new Date(Date.now() + 24 * 3600 * 1000)) },
    { name: 'body', label: 'Message ({name}, {first_name} allowed)', type: 'textarea', value: 'Hi {first_name}, just following up on our chat. Any questions I can help with?' },
    { name: 'templateName', label: 'OR approved template name (required if >24h since their last message)', placeholder: 'optional' },
    { name: 'templateLang', label: 'Template language', value: 'en_US' },
    { name: 'templateParams', label: 'Template body parameters, one per line', type: 'textarea' },
    { name: 'cancelOnReply', label: 'Cancel automatically if the contact replies first', type: 'checkbox', value: true },
  ], 'Schedule');
  if (!v) return null;
  const r = await api('/followups', {
    method: 'POST',
    body: { ...v, contactId: v.contactId ? Number(v.contactId) : null, sendAt: new Date(v.sendAt).toISOString() },
  });
  toast(`Scheduled ${r.scheduled} follow-up(s)`);
  return r;
}

async function renderFollowups() {
  $('#view').innerHTML = `
    <div class="card"><div class="row wrap">
      <select id="fuFilter" style="max-width:200px">
        <option value="">All</option><option value="pending" selected>Pending</option><option value="sent">Sent</option>
        <option value="failed">Failed</option><option value="cancelled">Cancelled</option></select>
      <span class="grow"></span>
      <button class="btn secondary" id="runNow" title="Send everything that is due right now">Run due now</button>
      <button class="btn" id="newFu">+ Schedule follow-up</button></div>
      <p class="muted" style="margin:10px 0 0">Tip: WhatsApp allows free-text only within 24h of the contact's last message. For older chats, use an approved <b>template</b>.</p>
    </div>
    <div class="card tablewrap"><table><thead><tr><th>When</th><th>Contact</th><th>Message</th><th>Status</th><th></th></tr></thead><tbody id="fuRows"></tbody></table></div>`;
  const load = safe(async () => {
    const list = await api('/followups' + ($('#fuFilter').value ? `?status=${$('#fuFilter').value}` : ''));
    $('#fuRows').innerHTML = list.map((f) => `
      <tr><td>${fmtTime(f.send_at)}</td>
        <td><a href="#" data-chat="${f.contact_id}">${esc(f.contact_name || '+' + f.contact_phone)}</a></td>
        <td style="white-space:pre-wrap">${f.template_name ? `<span class="tag">template: ${esc(f.template_name)}</span>` : esc(f.body)}</td>
        <td><span class="pill ${esc(f.status)}">${esc(f.status)}</span>${f.error ? `<div class="muted" style="font-size:12px">${esc(f.error)}</div>` : ''}</td>
        <td>${f.status === 'pending' ? `<button class="btn secondary small" data-cancel="${f.id}">Cancel</button>` : ''}</td></tr>`).join('')
      || '<tr><td colspan="5" class="muted">Nothing here.</td></tr>';
  });
  $('#fuFilter').onchange = load;
  $('#newFu').onclick = safe(async () => { if (await followupDialog()) load(); });
  $('#runNow').onclick = safe(async () => { const r = await api('/followups/run', { method: 'POST' }); toast(`Sent ${r.sent} follow-up(s)`); load(); });
  $('#fuRows').addEventListener('click', safe(async (e) => {
    const c = e.target.closest('[data-cancel]');
    if (c) { await api(`/followups/${c.dataset.cancel}`, { method: 'DELETE' }); load(); }
    const chat = e.target.closest('[data-chat]');
    if (chat) { e.preventDefault(); state.activeId = Number(chat.dataset.chat); go('inbox'); }
  }));
  load();
}

// ---------------- Bot ----------------
async function ruleDialog(r = {}) {
  const v = await openModal(r.id ? 'Edit rule' : 'New bot rule', [
    { name: 'keyword', label: 'Keyword', value: r.keyword, placeholder: 'e.g. price' },
    { name: 'match_type', label: 'Match', type: 'select', value: r.match_type || 'contains', options: [
      { value: 'contains', label: 'Message contains the word' }, { value: 'exact', label: 'Message is exactly the keyword' }] },
    { name: 'reply', label: 'Bot reply ({name}, {first_name} allowed)', type: 'textarea', value: r.reply },
    { name: 'add_tag', label: 'Add tag to contact (optional)', value: r.add_tag },
    { name: 'priority', label: 'Priority (higher wins when several rules match)', type: 'number', value: r.priority ?? 0 },
    { name: 'handoff', label: 'Hand off to a human (pause the bot for this contact)', type: 'checkbox', value: r.handoff },
    { name: 'enabled', label: 'Enabled', type: 'checkbox', value: r.enabled ?? 1 },
  ]);
  if (!v) return null;
  return r.id ? api(`/bot/rules/${r.id}`, { method: 'PATCH', body: v }) : api('/bot/rules', { method: 'POST', body: v });
}

async function renderBot() {
  const { settings, rules } = await api('/bot');
  $('#view').innerHTML = `
    <div class="grid2">
      <div class="card"><h2>🤖 Bot settings</h2>
        <label class="inline"><input type="checkbox" id="bEnabled" ${settings.bot_enabled === '1' ? 'checked' : ''}> Bot enabled</label>
        <label class="inline"><input type="checkbox" id="bPause" ${settings.pause_bot_on_agent_reply === '1' ? 'checked' : ''}> Pause bot for a contact when a human replies</label>
        <label>Welcome message (sent to brand-new contacts)</label><textarea id="bWelcome">${esc(settings.welcome_message)}</textarea>
        <label>Fallback message (when no rule matches; leave empty to stay silent)</label><textarea id="bFallback">${esc(settings.fallback_message)}</textarea>
        <div class="actions"><button class="btn" id="bSave">Save settings</button></div>
      </div>
      <div class="card"><h2>How the bot decides</h2>
        <ol class="muted" style="padding-left:18px;margin:0">
          <li>If the bot is off, or paused for that contact → do nothing.</li>
          <li>Brand-new contact → send the welcome message.</li>
          <li>Find the highest-priority keyword rule that matches → send its reply, add its tag, and optionally hand off to a human.</li>
          <li>No match → send the fallback message (if set).</li>
        </ol>
        <p class="muted">Test it under <b>Settings → Simulator</b>.</p>
      </div>
    </div>
    <div class="card"><div class="row"><h2 class="grow" style="margin:0">Keyword rules</h2><button class="btn" id="newRule">+ Rule</button></div>
      <div class="tablewrap"><table><thead><tr><th>Keyword</th><th>Match</th><th>Reply</th><th>Tag</th><th>Handoff</th><th>Priority</th><th>On</th><th></th></tr></thead>
      <tbody>${rules.map((r) => `<tr class="click" data-rule="${r.id}">
        <td><b>${esc(r.keyword)}</b></td><td>${esc(r.match_type)}</td><td style="white-space:pre-wrap">${esc(r.reply)}</td>
        <td>${r.add_tag ? `<span class="tag">${esc(r.add_tag)}</span>` : ''}</td><td>${r.handoff ? '👤 yes' : ''}</td>
        <td>${r.priority}</td><td>${r.enabled ? '✅' : '—'}</td>
        <td><button class="btn danger small" data-delrule="${r.id}">Delete</button></td></tr>`).join('') || '<tr><td colspan="8" class="muted">No rules yet.</td></tr>'}</tbody></table></div>
    </div>`;
  $('#bSave').onclick = safe(async () => {
    await api('/bot/settings', { method: 'PUT', body: {
      bot_enabled: $('#bEnabled').checked ? '1' : '0',
      pause_bot_on_agent_reply: $('#bPause').checked ? '1' : '0',
      welcome_message: $('#bWelcome').value,
      fallback_message: $('#bFallback').value,
    } });
    toast('Bot settings saved');
  });
  $('#newRule').onclick = safe(async () => { if (await ruleDialog()) renderBot(); });
  $('#view > .card:last-child').addEventListener('click', safe(async (e) => {
    const del = e.target.closest('[data-delrule]');
    if (del) { e.stopPropagation(); if (confirm('Delete rule?')) { await api(`/bot/rules/${del.dataset.delrule}`, { method: 'DELETE' }); renderBot(); } return; }
    const row = e.target.closest('[data-rule]');
    if (row) { if (await ruleDialog(rules.find((r) => r.id === Number(row.dataset.rule)))) renderBot(); }
  }));
}

// ---------------- Settings ----------------
async function renderSettings() {
  const s = await api('/status');
  const webhookUrl = `${location.origin}/webhook`;
  $('#view').innerHTML = `
    <div class="grid2">
      <div class="card"><h2>WhatsApp connection</h2>
        <p>Status: <b>${s.live ? '🟢 Live - connected to WhatsApp Cloud API' : '🟡 Mock mode - messages are logged, not sent'}</b></p>
        <ol style="padding-left:18px">
          <li>Create an app at <a href="https://developers.facebook.com/apps" target="_blank" rel="noopener">developers.facebook.com</a> → add the <b>WhatsApp</b> product.</li>
          <li>Copy the <b>access token</b> and <b>Phone number ID</b> into <code>.env</code> (<code>WHATSAPP_TOKEN</code>, <code>WHATSAPP_PHONE_NUMBER_ID</code>), and the App Secret into <code>WHATSAPP_APP_SECRET</code>.</li>
          <li>In WhatsApp → Configuration, set the webhook URL to <code>${esc(webhookUrl)}</code> and the verify token to the value of <code>WHATSAPP_VERIFY_TOKEN</code>.</li>
          <li>Subscribe to the <b>messages</b> webhook field, then restart this app.</li>
        </ol>
        <p class="muted">The webhook must be reachable over public HTTPS. For local testing use a tunnel such as ngrok or Cloudflare Tunnel.</p>
      </div>
      <div class="card"><h2>🧪 Simulator</h2>
        <p class="muted">Pretend a customer sent you a WhatsApp message. Useful for testing contacts, the bot and follow-ups before going live.</p>
        <label>From phone</label><input id="simPhone" value="15551234567">
        <label>Name</label><input id="simName" value="Test Customer">
        <label>Message</label><input id="simBody" value="Hi, what is the price?">
        <div class="actions"><button class="btn" id="simSend">Simulate incoming message</button></div>
      </div>
    </div>
    <div class="card"><h2>Coming next: social media channels</h2>
      <p class="muted">Contacts already store Instagram / Facebook / TikTok handles, and every message records its channel.
      Instagram DMs and Facebook Messenger use the same Meta webhook system as WhatsApp, so they can be added as new adapters in
      <code>src/channels/</code> without changing the rest of the CRM. See the README.</p>
    </div>`;
  $('#simSend').onclick = safe(async () => {
    const r = await api('/simulate', { method: 'POST', body: { phone: $('#simPhone').value, name: $('#simName').value, body: $('#simBody').value } });
    toast('Message received - check the Inbox');
    if (r?.contact) state.activeId = r.contact.id;
    refreshStatus();
  });
}

const views = { inbox: renderInbox, contacts: renderContacts, pipeline: renderPipeline, followups: renderFollowups, bot: renderBot, settings: renderSettings };

// Poll for new messages every few seconds (simple and reliable; no websockets needed)
setInterval(() => {
  refreshStatus();
  if (state.view === 'inbox' && !$('#modal').open) {
    loadConvs().catch(() => {});
    if (state.activeId && $('#msgs')) loadMessages(state.activeId).catch(() => {});
  }
}, 4000);

refreshStatus();
go('inbox');
