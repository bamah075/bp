// Languages the CRM can talk to customers in.
// To add one: add an entry here (code -> display name + WhatsApp template language code),
// then add the dashboard translations in public/i18n.js.
const LANGUAGES = {
  en: { name: 'English', template: 'en_US' },
  zh: { name: '中文 (简体)', template: 'zh_CN' },
};
const DEFAULT_LANGUAGE = 'en';

const isLanguage = (code) => Object.hasOwn(LANGUAGES, code);

// Lightweight detection that is reliable for the supported languages:
// any CJK character -> Chinese, any Latin letter -> English, otherwise unknown.
function detectLanguage(text) {
  const s = String(text || '');
  if (/[㐀-鿿豈-﫿]/.test(s)) return 'zh';
  if (/[a-z]/i.test(s)) return 'en';
  return null;
}

// Settings like welcome_message are stored per language as welcome_message_zh, etc.
// The default language uses the plain key. Falls back to the default language if empty.
const settingKey = (key, lang) => (lang && lang !== DEFAULT_LANGUAGE ? `${key}_${lang}` : key);
function localizedSetting(settings, key, lang) {
  return settings[settingKey(key, lang)] || settings[key] || '';
}

function templateLanguage(lang) {
  return (LANGUAGES[lang] || LANGUAGES[DEFAULT_LANGUAGE]).template;
}

module.exports = { LANGUAGES, DEFAULT_LANGUAGE, isLanguage, detectLanguage, settingKey, localizedSetting, templateLanguage };
