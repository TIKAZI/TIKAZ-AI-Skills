(function (global) {
  'use strict';

  const REPOSITORY = 'https://github.com/TIKAZI/TIKAZ-AI-Skills';
  const ISSUES_API = 'https://api.github.com/repos/TIKAZI/TIKAZ-AI-Skills/issues?state=all&labels=feedback&per_page=6&sort=created&direction=desc';
  const TYPE_CONFIG = {
    bug: { label: 'bug', en: 'Bug', zh: '错误' },
    improvement: { label: 'enhancement', en: 'Improvement', zh: '优化' },
    idea: { label: 'enhancement', en: 'Idea', zh: '想法' },
    other: { label: '', en: 'Feedback', zh: '反馈' },
  };
  const COPY = {
    en: {
      unspecified: 'Not specified', workflow: 'Workflow', skill: 'Skill', scope: 'Scope',
      details: 'Details', loading: 'Loading public feedback...', empty: 'No public feedback yet.',
      error: 'Public feedback could not be loaded. You can still submit or open GitHub Issues.',
      openIssue: 'Open feedback on GitHub', comments: 'comments', submitted: 'Opening GitHub...',
    },
    zh: {
      unspecified: '未指定', workflow: '工作流', skill: 'Skill', scope: '范围',
      details: '详细说明', loading: '正在加载公开反馈...', empty: '暂时还没有公开反馈。',
      error: '公开反馈暂时无法加载，你仍可提交或前往 GitHub Issues。',
      openIssue: '在 GitHub 查看反馈', comments: '条评论', submitted: '正在打开 GitHub...',
    },
  };

  function compact(value, limit) {
    return String(value || '').replace(/\s+/g, ' ').trim().slice(0, limit);
  }

  function buildFeedbackUrl(input) {
    const language = input.language === 'zh' ? 'zh' : 'en';
    const copy = COPY[language];
    const type = TYPE_CONFIG[input.type] || TYPE_CONFIG.other;
    const workflow = compact(input.workflow, 80);
    const skill = compact(input.skill, 100);
    const title = compact(input.title, 100);
    const details = String(input.details || '').trim().slice(0, 4000);
    const scopeLabel = workflow || skill ? [workflow, skill].filter(Boolean).join('/') : copy.unspecified;
    const issueTitle = `[${type[language]}][${scopeLabel}] ${title}`;
    const body = [
      `## ${copy.scope}`,
      `${copy.scope}: ${scopeLabel}`,
      `${copy.workflow}: ${workflow || copy.unspecified}`,
      `${copy.skill}: ${skill || copy.unspecified}`,
      '',
      `## ${copy.details}`,
      details,
      '',
      '---',
      'Submitted from the TIKAZ AI Skills public feedback board. Do not include credentials, cookies, private source material, or undisclosed security details.',
    ].join('\n');
    const labels = ['feedback', type.label].filter(Boolean).join(',');
    const url = new URL(`${REPOSITORY}/issues/new`);
    url.searchParams.set('title', issueTitle);
    url.searchParams.set('body', body);
    url.searchParams.set('labels', labels);
    return url.toString();
  }

  function option(value, label) {
    const node = document.createElement('option');
    node.value = value;
    node.textContent = label;
    return node;
  }

  function populateWorkflowSelect(select, data, language) {
    Object.keys(data).forEach((suite) => {
      select.appendChild(option(suite, suite));
    });
    select.setAttribute('aria-label', language === 'zh' ? '选择工作流（可选）' : 'Choose a workflow (optional)');
  }

  function populateSkillSelect(select, data, workflow, language) {
    while (select.options.length > 1) select.remove(1);
    const suites = workflow && data[workflow] ? [workflow] : Object.keys(data);
    suites.forEach((suite) => {
      const group = document.createElement('optgroup');
      group.label = suite;
      data[suite].forEach((skill) => group.appendChild(option(skill, skill)));
      select.appendChild(group);
    });
    select.setAttribute('aria-label', language === 'zh' ? '选择 Skill（可选）' : 'Choose a Skill (optional)');
  }

  function renderState(list, className, message) {
    list.replaceChildren();
    const item = document.createElement('li');
    item.className = `feedback-state ${className}`;
    item.textContent = message;
    list.appendChild(item);
  }

  function renderIssues(list, issues, language) {
    const copy = COPY[language];
    list.replaceChildren();
    issues.forEach((issue) => {
      const item = document.createElement('li');
      item.className = 'feedback-item';
      const link = document.createElement('a');
      link.href = issue.html_url;
      link.target = '_blank';
      link.rel = 'noopener noreferrer';
      link.setAttribute('aria-label', `${copy.openIssue}: ${issue.title}`);
      const title = document.createElement('strong');
      title.textContent = issue.title;
      const meta = document.createElement('span');
      const date = new Intl.DateTimeFormat(language === 'zh' ? 'zh-CN' : 'en', { dateStyle: 'medium' }).format(new Date(issue.created_at));
      meta.textContent = `#${issue.number} · ${issue.state} · ${issue.comments} ${copy.comments} · ${date}`;
      link.append(title, meta);
      item.appendChild(link);
      list.appendChild(item);
    });
  }

  async function loadIssues(list, language) {
    const copy = COPY[language];
    renderState(list, 'feedback-loading', copy.loading);
    list.setAttribute('aria-busy', 'true');
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 8000);
    try {
      const response = await fetch(ISSUES_API, {
        headers: { Accept: 'application/vnd.github+json' },
        signal: controller.signal,
      });
      if (!response.ok) throw new Error(`GitHub API ${response.status}`);
      const payload = await response.json();
      const issues = payload.filter((issue) => !issue.pull_request);
      if (issues.length) renderIssues(list, issues, language);
      else renderState(list, 'feedback-empty', copy.empty);
    } catch (_) {
      renderState(list, 'feedback-error', copy.error);
    } finally {
      clearTimeout(timeout);
      list.setAttribute('aria-busy', 'false');
    }
  }

  function initializeFeedbackBoard() {
    const form = document.getElementById('feedback-form');
    const list = document.getElementById('feedback-list');
    const data = global.TIKAZ_FEEDBACK_DATA || {};
    if (!(form instanceof HTMLFormElement) || !(list instanceof HTMLElement)) return;
    const language = form.dataset.feedbackLanguage === 'zh' ? 'zh' : 'en';
    const workflow = document.getElementById('feedback-workflow');
    const skill = document.getElementById('feedback-skill');
    const status = document.getElementById('feedback-status');
    if (!(workflow instanceof HTMLSelectElement) || !(skill instanceof HTMLSelectElement)) return;
    populateWorkflowSelect(workflow, data, language);
    populateSkillSelect(skill, data, '', language);
    workflow.addEventListener('change', () => populateSkillSelect(skill, data, workflow.value, language));
    form.addEventListener('submit', (event) => {
      event.preventDefault();
      if (!form.reportValidity()) return;
      const checkedType = form.querySelector('input[name="feedback-type"]:checked');
      const title = document.getElementById('feedback-title');
      const details = document.getElementById('feedback-details');
      if (!(checkedType instanceof HTMLInputElement) || !(title instanceof HTMLInputElement) || !(details instanceof HTMLTextAreaElement)) return;
      const url = buildFeedbackUrl({
        type: checkedType.value, workflow: workflow.value, skill: skill.value,
        title: title.value, details: details.value, language,
      });
      if (status) status.textContent = COPY[language].submitted;
      global.open(url, '_blank', 'noopener,noreferrer');
    });
    loadIssues(list, language);
  }

  const api = { buildFeedbackUrl, initializeFeedbackBoard, loadIssues };
  if (typeof module !== 'undefined') module.exports = api;
  if (typeof document !== 'undefined') {
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initializeFeedbackBoard);
    else initializeFeedbackBoard();
  }
})(typeof window !== 'undefined' ? window : globalThis);
