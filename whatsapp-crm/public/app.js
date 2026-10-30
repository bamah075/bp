// WhatsApp CRM dashboard - plain JavaScript, no build step.
const $ = (sel, el = document) => el.querySelector(sel);
const $$ = (sel, el = document) => [...el.querySelectorAll(sel)];
const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const fromSql = (s) => (s ? new Date(s.replace(' ', 'T') + 'Z') : null);
const tagsOf = (c) => (c.tags || '').split(',').map((t) => t.trim()).filter(Boolean);

// ---------------- Language ----------------
// Dashboard language is a per-browser preference. Customer languages come from the server (/api/status).
const storage = {
  get: (k) => { try { return localStorage.getItem(k); } catch { return null; } },
  set: (k, v) => { try { localStorage.setItem(k, v); } catch { /* private mode: not remembered */ } },
};
let uiLang = storage.get('crm.uiLang') || (navigator.language?.toLowerCase().startsWith('zh') ? 'zh' : 'en');
if (!I18N[uiLang]) uiLang = 'en';

// t('fu.scheduled', { n: 3 }) -> "Scheduled 3 follow-up(s)". Unknown {placeholders} are left as-is.
function t(key, vars = {}) {
  const text = I18N[uiLang][key] ?? I18N.en[key] ?? key;
  return text.replace(/\{(\w+)\}/g, (m, k) => (k in vars ? vars[k] : m));
}
const locale = () => (uiLang === 'zh' ? 'zh-CN' : 'en');
const fmtTime = (s) => { const d = fromSql(s); return d ? d.toLocaleString(locale(), { dateStyle: 'short', timeStyle: 'short' }) : ''; };
const money = (v) => Number(v || 0).toLocaleString(locale(), { style: 'currency', currency: 'USD', maximumFractionDigits: 0 });

// Starting text for new follow-ups, per customer language
const FOLLOWUP_DEFAULTS = {
  en: 'Hi {first_name}, just following up on our chat. Any questions I can help with?',
  zh: '您好 {first_name}，跟进一下我们之前的对话。请问还有什么可以帮您的吗？',
};

const state = { view: 'inbox', activeId: null, search: '', lastMsgSig: '', languages: { en: { name: 'English' } }, defaultLang: 'en' };
const langName = (code) => state.languages[code]?.name || code;
const otherLanguages = () => Object.keys(state.languages).filter((c) => c !== state.defaultLang);

function applyStaticText() {
  document.documentElement.lang = uiLang === 'zh' ? 'zh-CN' : 'en';
  $$('[data-i18n]').forEach((el) => { el.textContent = t(el.dataset.i18n); });
  const pick = $('#uiLang');
  pick.innerHTML = Object.entries(I18N).map(([code, d]) => `<option value="${code}" ${code === uiLang ? 'selected' : ''}>${esc(d._name)}</option>`).join('');
  pick.title = t('common.uiLanguage');
}
$('#uiLang').addEventListener('change', (e) => {
  uiLang = e.target.value;
  storage.set('crm.uiLang', uiLang);
  applyStaticText();
  refreshStatus();
  go(state.view);
});

async function api(path, { method = 'GET', body } = {}) {
  const res = await fetch('/api' + path, {
    method,
    headers: body ? { 'Content-Type': 'application/json' } : {},
    body: body ? JSON.stringify(body) : undefined,
  });
  if (res.status === 204) return null;
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || t('common.requestFailed', { status: res.status }));
  return data;
}

function toast(text, isError = false) {
  const el = $('#toast');
  el.textContent = text;
  el.className = 'toast' + (isError ? ' error' : '');
  clearTimeout(toast.timer);
  toast.timer = setTimeout(() => el.classList.add('hidden'), 3500);
}

// Run an async action and show any error as a toast
const safe = (fn) => async (...args) => { try { await fn(...args); } catch (e) { toast(e.message, true); } };

// Generic modal: fields = [{ name, label, type, value, options }]
function openModal(title, fields, submitLabel = t('common.save')) {
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
    }).join('') + `<div class="actions"><button class="btn secondary" value="cancel">${t('common.cancel')}</button><button class="btn" value="ok">${esc(submitLabel)}</button></div>`;
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
    state.languages = s.languages;
    state.defaultLang = s.defaultLanguage;
    $('#modeBadge').textContent = s.live ? t('mode.live') : t('mode.mock');
    $('#modeBadge').title = s.live ? t('mode.liveTitle') : t('mode.mockTitle');
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
        <div class="search"><input id="convSearch" placeholder="${esc(t('inbox.search'))}" value="${esc(state.search)}"></div>
        <div class="convs" id="convs"></div>
      </div>
      <div class="chat" id="chat"><div class="empty">${t('inbox.select')}<br><span class="muted">${t('inbox.selectHint')}</span></div></div>
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
      <div class="top"><span class="preview">${esc(c.last_message || t('inbox.noMessagesYet'))}</span>
        ${c.unread ? `<span class="badge">${c.unread}</span>` : ''}</div>
    </div>`).join('') : `<div class="empty">${t('inbox.noContacts')}<br>${t('inbox.noContactsHint')}</div>`;
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
      <div class="row"><button class="btn secondary small" id="backBtn" title="${esc(t('inbox.back'))}">←</button>
        <div><b>${esc(c.name || '+' + c.phone)}</b>${c.language ? `<span class="langpill">${esc(langName(c.language))}</span>` : ''}
          <div class="muted" style="font-size:12px">+${esc(c.phone)}</div></div></div>
      <label class="inline" title="${esc(t('inbox.botTitle'))}">
        <input type="checkbox" id="botToggle" ${c.bot_paused ? '' : 'checked'}> 🤖 ${t('inbox.bot')}</label>
    </div>
    <div class="msgs" id="msgs"></div>
    <div class="composer">
      <div class="warnbar ${c.in_window ? 'hidden' : ''}">${t('inbox.windowWarning')} <a href="#" id="tplLink">${t('inbox.sendTemplate')}</a></div>
      <div class="row"><textarea id="composer" class="grow" placeholder="${esc(t('inbox.composer'))}"></textarea>
        <button class="btn" id="sendBtn">${t('common.send')}</button></div>
    </div>`;
  $('#backBtn').onclick = () => { state.activeId = null; $('#inbox').classList.remove('has-chat'); };
  $('#botToggle').onchange = safe(async (e) => {
    await api(`/contacts/${id}`, { method: 'PATCH', body: { bot_paused: !e.target.checked } });
    toast(e.target.checked ? t('inbox.botResumed') : t('inbox.botPaused'));
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
  el.innerHTML = msgs.map((m) => `
    <div class="msg ${m.direction} ${m.status === 'failed' ? 'failed' : ''}" ${m.error ? `title="${esc(m.error)}"` : ''}>
      <div class="body">${esc(m.body)}</div>
      <div class="meta">${m.sent_by && m.sent_by !== 'agent' ? (m.sent_by === 'bot' ? t('inbox.byBot') : t('inbox.byFollowup')) : ''}${fmtTime(m.created_at)}
        ${m.direction === 'out' ? ' ' + t('status.' + m.status) : ''}</div>
    </div>`).join('') || `<div class="empty">${t('inbox.sayHello')}</div>`;
  el.scrollTop = el.scrollHeight;
}

async function renderSide(c) {
  const [deals, fus] = await Promise.all([api(`/deals?contactId=${c.id}`), api(`/followups?contactId=${c.id}&status=pending`)]);
  const social = JSON.parse(c.social || '{}');
  $('#side').innerHTML = `
    <div class="row"><b class="grow">${t('side.contact')}</b><button class="btn secondary small" id="editC">${t('common.edit')}</button></div>
    <div>${esc(c.name || '—')}</div><div class="muted">+${esc(c.phone)}${c.email ? ' · ' + esc(c.email) : ''}</div>
    <div class="muted">${t('common.language')}: ${esc(c.language ? langName(c.language) : t('side.languageNotSet'))}</div>
    <div>${tagsOf(c).map((tag) => `<span class="tag">${esc(tag)}</span>`).join('')}</div>
    ${c.notes ? `<h3>${t('common.notes')}</h3><div style="white-space:pre-wrap">${esc(c.notes)}</div>` : ''}
    ${Object.values(social).some(Boolean) ? `<h3>${t('side.social')}</h3>${Object.entries(social).filter(([, v]) => v).map(([k, v]) => `<div>${esc(k)}: ${esc(v)}</div>`).join('')}` : ''}
    <h3>${t('side.deals')}</h3>
    ${deals.map((d) => `<div class="deal" style="cursor:default">${esc(d.title)} <span class="v">${money(d.value)}</span></div>`).join('') || `<div class="muted">${t('side.noDeals')}</div>`}
    <button class="btn secondary small" id="addDealC" style="margin-top:6px">${t('side.addDeal')}</button>
    <h3>${t('side.pendingFollowups')}</h3>
    ${fus.map((f) => `<div class="muted" style="font-size:12px">⏰ ${fmtTime(f.send_at)} — ${esc(f.template_name ? t('side.template', { name: f.template_name }) : (JSON.parse(f.translations || '{}')[c.language] || f.body)).slice(0, 80)}</div>`).join('') || `<div class="muted">${t('common.none')}</div>`}
    <button class="btn secondary small" id="addFuC" style="margin-top:6px">${t('side.addFollowup')}</button>`;
  $('#editC').onclick = safe(async () => { if (await editContactDialog(c)) openChat(c.id); });
  $('#addDealC').onclick = safe(async () => { if (await dealDialog({ contact_id: c.id, title: t('side.dealTitle', { who: c.name || c.phone }) })) renderSide(c); });
  $('#addFuC').onclick = safe(async () => { if (await followupDialog(c.id)) renderSide(c); });
}

async function sendTemplateDialog(contactId) {
  const v = await openModal(t('tpl.title'), [
    { name: 'templateName', label: t('tpl.name'), placeholder: 'hello_world' },
    { name: 'templateLang', label: t('tpl.lang'), placeholder: 'en_US / zh_CN' },
    { name: 'templateParams', label: t('tpl.params'), type: 'textarea' },
  ], t('common.send'));
  if (!v || !v.templateName) return;
  await safe(async () => {
    await api(`/contacts/${contactId}/messages`, { method: 'POST', body: { ...v, templateParams: v.templateParams.split('\n').map((s) => s.trim()).filter(Boolean) } });
    toast(t('tpl.sent'));
  })();
  loadMessages(contactId);
}

// ---------------- Contacts ----------------
const languageOptions = (emptyLabel) => [
  { value: '', label: emptyLabel },
  ...Object.keys(state.languages).map((code) => ({ value: code, label: langName(code) })),
];

async function editContactDialog(c = {}) {
  const social = JSON.parse(c.social || '{}');
  const v = await openModal(c.id ? t('contact.edit') : t('contact.new'), [
    ...(c.id ? [] : [{ name: 'phone', label: t('contact.phone') }]),
    { name: 'name', label: t('common.name'), value: c.name },
    { name: 'language', label: t('contact.language'), type: 'select', value: c.language || '', options: languageOptions(t('common.autoDetect')) },
    { name: 'email', label: t('common.email'), value: c.email },
    { name: 'tags', label: t('contact.tags'), value: c.tags },
    { name: 'notes', label: t('common.notes'), type: 'textarea', value: c.notes },
    { name: 'instagram', label: t('contact.instagram'), value: social.instagram },
    { name: 'facebook', label: t('contact.facebook'), value: social.facebook },
    { name: 'tiktok', label: t('contact.tiktok'), value: social.tiktok },
  ]);
  if (!v) return null;
  const { instagram, facebook, tiktok, ...rest } = v;
  const body = { ...rest, tags: rest.tags.split(',').map((tag) => tag.trim()).filter(Boolean).join(',') };
  let saved;
  if (c.id) saved = await api(`/contacts/${c.id}`, { method: 'PATCH', body: { ...body, social: { instagram, facebook, tiktok } } });
  else {
    saved = await api('/contacts', { method: 'POST', body });
    await api(`/contacts/${saved.id}`, { method: 'PATCH', body: { social: { instagram, facebook, tiktok } } });
  }
  toast(t('contact.saved'));
  return saved;
}

async function renderContacts() {
  $('#view').innerHTML = `
    <div class="card">
      <div class="row wrap">
        <input id="cSearch" class="grow" placeholder="${esc(t('contacts.search'))}" style="max-width:320px" value="${esc(state.search)}">
        <input id="cTag" placeholder="${esc(t('contacts.filterTag'))}" style="max-width:180px">
        <span class="grow"></span>
        <a class="btn secondary" href="/api/contacts/export.csv">${t('contacts.export')}</a>
        <button class="btn" id="newC">${t('contacts.new')}</button>
      </div>
    </div>
    <div class="card tablewrap"><table><thead><tr><th>${t('common.name')}</th><th>${t('common.phone')}</th><th>${t('common.language')}</th><th>${t('common.tags')}</th>
      <th>${t('contacts.deals')}</th><th>${t('contacts.bot')}</th><th>${t('contacts.lastMessage')}</th><th></th></tr></thead>
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
        <td>${c.language ? esc(langName(c.language)) : '<span class="muted">—</span>'}</td>
        <td>${tagsOf(c).map((tag) => `<span class="tag">${esc(tag)}</span>`).join('')}</td>
        <td>${c.deal_count}</td>
        <td>${c.bot_paused ? t('contacts.paused') : t('contacts.on')}</td>
        <td class="muted">${fmtTime(c.last_message_at)}</td>
        <td><button class="btn danger small" data-del="${c.id}">${t('common.delete')}</button></td>
      </tr>`).join('') || `<tr><td colspan="8" class="muted">${t('contacts.empty')}</td></tr>`;
  });
  $('#cSearch').addEventListener('input', load);
  $('#cTag').addEventListener('input', load);
  $('#newC').onclick = safe(async () => { if (await editContactDialog()) load(); });
  $('#cRows').addEventListener('click', safe(async (e) => {
    const del = e.target.closest('[data-del]');
    if (del) {
      if (confirm(t('contacts.confirmDelete'))) { await api(`/contacts/${del.dataset.del}`, { method: 'DELETE' }); load(); }
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
  return [{ value: '', label: t('common.noneOption') }, ...list.map((c) => ({ value: c.id, label: `${c.name || t('common.unnamed')} (+${c.phone})` }))];
}

async function dealDialog(d = {}) {
  const [stages, contacts] = await Promise.all([api('/stages'), contactOptions()]);
  const v = await openModal(d.id ? t('deal.edit') : t('deal.new'), [
    { name: 'title', label: t('deal.title'), value: d.title },
    { name: 'value', label: t('deal.value'), type: 'number', value: d.value ?? 0 },
    { name: 'contact_id', label: t('deal.contact'), type: 'select', value: d.contact_id, options: contacts },
    { name: 'stage_id', label: t('deal.stage'), type: 'select', value: d.stage_id ?? stages[0]?.id, options: stages.map((s) => ({ value: s.id, label: s.name })) },
    { name: 'notes', label: t('common.notes'), type: 'textarea', value: d.notes },
  ]);
  if (!v) return null;
  const body = { ...v, value: Number(v.value) || 0, contact_id: v.contact_id ? Number(v.contact_id) : null, stage_id: Number(v.stage_id) };
  const saved = d.id ? await api(`/deals/${d.id}`, { method: 'PATCH', body }) : await api('/deals', { method: 'POST', body });
  toast(t('deal.saved'));
  return saved;
}

async function renderPipeline() {
  const [stages, deals, status] = await Promise.all([api('/stages'), api('/deals'), api('/status')]);
  $('#view').innerHTML = `
    <div class="stats">
      <div class="stat"><span class="muted">${t('pipe.openDeals')}</span><b>${status.stats.openDeals.n}</b></div>
      <div class="stat"><span class="muted">${t('pipe.openValue')}</span><b>${money(status.stats.openDeals.v)}</b></div>
      <div class="stat"><span class="muted">${t('pipe.won')}</span><b>${money(status.stats.wonValue)}</b></div>
      <div class="stat"><span class="muted">${t('pipe.contacts')}</span><b>${status.stats.contacts}</b></div>
    </div>
    <div class="row wrap" style="margin-bottom:12px"><button class="btn" id="newDeal">${t('pipe.newDeal')}</button>
      <button class="btn secondary" id="newStage">${t('pipe.newStage')}</button>
      <span class="muted">${t('pipe.hint')}</span></div>
    <div class="board" id="board">${stages.map((s) => {
      const items = deals.filter((d) => d.stage_id === s.id);
      return `<div class="col" data-stage="${s.id}">
        <div class="colhead" style="border-color:${esc(s.color)}">
          <span class="t" data-rename="${s.id}">${esc(s.name)}</span>
          <span class="muted" style="font-size:12px">${items.length} · ${money(items.reduce((a, d) => a + d.value, 0))}
            <button class="btn secondary small" data-delstage="${s.id}" title="${esc(t('pipe.deleteStage'))}">×</button></span>
        </div>
        <div class="colbody">${items.map((d) => `
          <div class="deal" draggable="true" data-deal="${d.id}">
            <div><b>${esc(d.title)}</b></div>
            <div class="row"><span class="v grow">${money(d.value)}</span>
              ${d.contact_id ? `<a href="#" data-chat="${d.contact_id}" title="${esc(t('pipe.openChat'))}">💬</a>` : ''}</div>
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
      const v = await openModal(t('pipe.editStage'), [{ name: 'name', label: t('common.name'), value: s.name }, { name: 'color', label: t('common.color'), type: 'color', value: s.color }]);
      if (v) { await api(`/stages/${s.id}`, { method: 'PATCH', body: v }); renderPipeline(); }
      return;
    }
    const del = e.target.closest('[data-delstage]');
    if (del) { if (confirm(t('pipe.confirmDeleteStage'))) { await api(`/stages/${del.dataset.delstage}`, { method: 'DELETE' }); renderPipeline(); } return; }
    const card = e.target.closest('[data-deal]');
    if (card) {
      const d = deals.find((x) => x.id === Number(card.dataset.deal));
      if (await dealDialog(d)) renderPipeline();
    }
  }));
  $('#newDeal').onclick = safe(async () => { if (await dealDialog()) renderPipeline(); });
  $('#newStage').onclick = safe(async () => {
    const v = await openModal(t('pipe.newStageTitle'), [{ name: 'name', label: t('common.name') }, { name: 'color', label: t('common.color'), type: 'color', value: '#64748b' }]);
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
  // One message box per extra language; each contact receives the version for their language
  const translationFields = otherLanguages().map((code) => ({
    name: `tr_${code}`, label: t('fu.translation', { lang: langName(code) }), type: 'textarea', value: FOLLOWUP_DEFAULTS[code] || '',
  }));
  const v = await openModal(t('fu.title'), [
    contactId
      ? { name: 'contactId', label: t('fu.contact'), type: 'select', value: contactId, options: contacts }
      : { name: 'contactId', label: t('fu.contactOrTag'), type: 'select', value: '', options: [{ value: '', label: t('fu.byTag') }, ...contacts] },
    ...(contactId ? [] : [{ name: 'tag', label: t('fu.tag'), placeholder: t('fu.tagPlaceholder') }]),
    { name: 'sendAt', label: t('fu.sendAt'), type: 'datetime-local', value: localInputValue(new Date(Date.now() + 24 * 3600 * 1000)) },
    { name: 'body', label: `${t('fu.body')} — ${langName(state.defaultLang)}`, type: 'textarea', value: FOLLOWUP_DEFAULTS[state.defaultLang] },
    ...translationFields,
    { name: 'templateName', label: t('fu.templateName'), placeholder: t('fu.optional') },
    { name: 'templateLang', label: t('fu.templateLang'), placeholder: 'en_US / zh_CN' },
    { name: 'templateParams', label: t('fu.templateParams'), type: 'textarea' },
    { name: 'cancelOnReply', label: t('fu.cancelOnReply'), type: 'checkbox', value: true },
  ], t('fu.schedule'));
  if (!v) return null;
  const translations = Object.fromEntries(otherLanguages().map((code) => [code, v[`tr_${code}`]]));
  const r = await api('/followups', {
    method: 'POST',
    body: { ...v, translations, contactId: v.contactId ? Number(v.contactId) : null, sendAt: new Date(v.sendAt).toISOString() },
  });
  toast(t('fu.scheduled', { n: r.scheduled }));
  return r;
}

async function renderFollowups() {
  const statuses = ['pending', 'sent', 'failed', 'cancelled'];
  $('#view').innerHTML = `
    <div class="card"><div class="row wrap">
      <select id="fuFilter" style="max-width:200px">
        <option value="">${t('fu.all')}</option>
        ${statuses.map((s) => `<option value="${s}" ${s === 'pending' ? 'selected' : ''}>${t('fu.' + s)}</option>`).join('')}</select>
      <span class="grow"></span>
      <button class="btn secondary" id="runNow" title="${esc(t('fu.runNowTitle'))}">${t('fu.runNow')}</button>
      <button class="btn" id="newFu">${t('fu.new')}</button></div>
      <p class="muted" style="margin:10px 0 0">${t('fu.tip')}</p>
    </div>
    <div class="card tablewrap"><table><thead><tr><th>${t('fu.when')}</th><th>${t('fu.contact')}</th><th>${t('fu.message')}</th><th>${t('fu.status')}</th><th></th></tr></thead><tbody id="fuRows"></tbody></table></div>`;
  const load = safe(async () => {
    const list = await api('/followups' + ($('#fuFilter').value ? `?status=${$('#fuFilter').value}` : ''));
    $('#fuRows').innerHTML = list.map((f) => {
      // Show the version this contact will actually receive (same rule as the server's scheduler)
      const translated = JSON.parse(f.translations || '{}')[f.contact_language];
      const text = translated?.trim() ? translated : f.body;
      const lang = f.contact_language ? `<span class="langpill" style="margin:0 6px 0 0">${esc(langName(f.contact_language))}</span>` : '';
      return `
      <tr><td>${fmtTime(f.send_at)}</td>
        <td><a href="#" data-chat="${f.contact_id}">${esc(f.contact_name || '+' + f.contact_phone)}</a></td>
        <td style="white-space:pre-wrap">${lang}${f.template_name ? `<span class="tag">${esc(t('side.template', { name: f.template_name }))}</span>` : esc(text)}</td>
        <td><span class="pill ${esc(f.status)}">${esc(t('fu.' + f.status))}</span>${f.error ? `<div class="muted" style="font-size:12px">${esc(f.error)}</div>` : ''}</td>
        <td>${f.status === 'pending' ? `<button class="btn secondary small" data-cancel="${f.id}">${t('common.cancel')}</button>` : ''}</td></tr>`;
    }).join('') || `<tr><td colspan="5" class="muted">${t('fu.empty')}</td></tr>`;
  });
  $('#fuFilter').onchange = load;
  $('#newFu').onclick = safe(async () => { if (await followupDialog()) load(); });
  $('#runNow').onclick = safe(async () => { const r = await api('/followups/run', { method: 'POST' }); toast(t('fu.sentN', { n: r.sent })); load(); });
  $('#fuRows').addEventListener('click', safe(async (e) => {
    const c = e.target.closest('[data-cancel]');
    if (c) { await api(`/followups/${c.dataset.cancel}`, { method: 'DELETE' }); load(); }
    const chat = e.target.closest('[data-chat]');
    if (chat) { e.preventDefault(); state.activeId = Number(chat.dataset.chat); go('inbox'); }
  }));
  load();
}

// ---------------- Bot ----------------
// Per-language setting keys mirror src/i18n.js: welcome_message (default language), welcome_message_zh, ...
const settingKey = (key, code) => (code === state.defaultLang ? key : `${key}_${code}`);

async function ruleDialog(r = {}) {
  const v = await openModal(r.id ? t('rule.edit') : t('rule.new'), [
    { name: 'keyword', label: t('rule.keyword'), value: r.keyword, placeholder: t('rule.keywordPlaceholder') },
    { name: 'language', label: t('rule.language'), type: 'select', value: r.language || '', options: languageOptions(t('common.anyLanguage')) },
    { name: 'match_type', label: t('rule.match'), type: 'select', value: r.match_type || 'contains', options: [
      { value: 'contains', label: t('rule.contains') }, { value: 'exact', label: t('rule.exact') }] },
    { name: 'reply', label: t('rule.reply'), type: 'textarea', value: r.reply },
    { name: 'add_tag', label: t('rule.addTag'), value: r.add_tag },
    { name: 'priority', label: t('rule.priority'), type: 'number', value: r.priority ?? 0 },
    { name: 'handoff', label: t('rule.handoff'), type: 'checkbox', value: r.handoff },
    { name: 'enabled', label: t('rule.enabled'), type: 'checkbox', value: r.enabled ?? 1 },
  ]);
  if (!v) return null;
  return r.id ? api(`/bot/rules/${r.id}`, { method: 'PATCH', body: v }) : api('/bot/rules', { method: 'POST', body: v });
}

async function renderBot() {
  const { settings, rules } = await api('/bot');
  const codes = Object.keys(state.languages);
  const perLang = (key, labelKey) => codes.map((code) => `
    <label>${t(labelKey, { lang: langName(code) })}</label>
    <textarea data-setting="${settingKey(key, code)}">${esc(settings[settingKey(key, code)])}</textarea>`).join('');
  $('#view').innerHTML = `
    <div class="grid2">
      <div class="card"><h2>${t('bot.settings')}</h2>
        <label class="inline"><input type="checkbox" id="bEnabled" ${settings.bot_enabled === '1' ? 'checked' : ''}> ${t('bot.enabled')}</label>
        <label class="inline"><input type="checkbox" id="bPause" ${settings.pause_bot_on_agent_reply === '1' ? 'checked' : ''}> ${t('bot.pauseOnReply')}</label>
        ${perLang('welcome_message', 'bot.welcome')}
        ${perLang('fallback_message', 'bot.fallback')}
        <div class="actions"><button class="btn" id="bSave">${t('bot.save')}</button></div>
      </div>
      <div class="card"><h2>${t('bot.how')}</h2>
        <ol class="muted" style="padding-left:18px;margin:0">
          <li>${t('bot.step1')}</li><li>${t('bot.step2')}</li><li>${t('bot.step3')}</li><li>${t('bot.step4')}</li>
        </ol>
        <p class="muted">🌐 ${t('bot.langNote')}</p>
        <p class="muted">${t('bot.test')}</p>
      </div>
    </div>
    <div class="card"><div class="row"><h2 class="grow" style="margin:0">${t('bot.rules')}</h2><button class="btn" id="newRule">${t('bot.newRule')}</button></div>
      <div class="tablewrap"><table><thead><tr><th>${t('rule.keyword')}</th><th>${t('common.language')}</th><th>${t('rule.match')}</th><th>${t('bot.reply')}</th>
        <th>${t('bot.tag')}</th><th>${t('bot.handoff')}</th><th>${t('bot.priority')}</th><th>${t('bot.on')}</th><th></th></tr></thead>
      <tbody>${rules.map((r) => `<tr class="click" data-rule="${r.id}">
        <td><b>${esc(r.keyword)}</b></td><td>${r.language ? esc(langName(r.language)) : `<span class="muted">${t('common.anyLanguage')}</span>`}</td>
        <td>${t('bot.' + r.match_type)}</td><td style="white-space:pre-wrap">${esc(r.reply)}</td>
        <td>${r.add_tag ? `<span class="tag">${esc(r.add_tag)}</span>` : ''}</td><td>${r.handoff ? t('bot.yes') : ''}</td>
        <td>${r.priority}</td><td>${r.enabled ? '✅' : '—'}</td>
        <td><button class="btn danger small" data-delrule="${r.id}">${t('common.delete')}</button></td></tr>`).join('') || `<tr><td colspan="9" class="muted">${t('bot.noRules')}</td></tr>`}</tbody></table></div>
    </div>`;
  $('#bSave').onclick = safe(async () => {
    const body = {
      bot_enabled: $('#bEnabled').checked ? '1' : '0',
      pause_bot_on_agent_reply: $('#bPause').checked ? '1' : '0',
    };
    $$('[data-setting]').forEach((el) => { body[el.dataset.setting] = el.value; });
    await api('/bot/settings', { method: 'PUT', body });
    toast(t('bot.saved'));
  });
  $('#newRule').onclick = safe(async () => { if (await ruleDialog()) renderBot(); });
  $('#view > .card:last-child').addEventListener('click', safe(async (e) => {
    const del = e.target.closest('[data-delrule]');
    if (del) { e.stopPropagation(); if (confirm(t('bot.confirmDelete'))) { await api(`/bot/rules/${del.dataset.delrule}`, { method: 'DELETE' }); renderBot(); } return; }
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
      <div class="card"><h2>${t('settings.connection')}</h2>
        <p>${t('settings.status')}: <b>${s.live ? t('settings.live') : t('settings.mock')}</b></p>
        <ol style="padding-left:18px">
          <li>${t('settings.step1')}</li><li>${t('settings.step2')}</li>
          <li>${t('settings.step3', { url: esc(webhookUrl) })}</li><li>${t('settings.step4')}</li>
        </ol>
        <p class="muted">${t('settings.https')}</p>
        <p class="muted">📘 ${t('settings.guide')}</p>
      </div>
      <div class="card"><h2>${t('sim.title')}</h2>
        <p class="muted">${t('sim.hint')}</p>
        <label>${t('sim.from')}</label><input id="simPhone" value="15551234567">
        <label>${t('common.name')}</label><input id="simName" value="Test Customer">
        <label>${t('sim.message')}</label><input id="simBody" value="${uiLang === 'zh' ? '你好，请问价格是多少？' : 'Hi, what is the price?'}">
        <div class="actions"><button class="btn" id="simSend">${t('sim.send')}</button></div>
      </div>
    </div>
    <div class="card"><h2>${t('settings.socialTitle')}</h2><p class="muted">${t('settings.social')}</p></div>`;
  $('#simSend').onclick = safe(async () => {
    const r = await api('/simulate', { method: 'POST', body: { phone: $('#simPhone').value, name: $('#simName').value, body: $('#simBody').value } });
    toast(t('sim.received'));
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

applyStaticText();
refreshStatus().then(() => go('inbox'));
