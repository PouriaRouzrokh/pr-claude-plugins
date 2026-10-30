#!/usr/bin/env node
// Summarize Lighthouse and axe-core JSON reports as Markdown evidence tables.
// Usage: node summarize.mjs <report.json> [more reports...]
// Read-only: never writes files. Requires Node 18+, no dependencies.

import { readFileSync } from 'node:fs';
import { basename } from 'node:path';

const PASS_SCORE = 0.9; // Lighthouse treats audit scores >= 0.9 as passing
const MAX_ITEMS = 3; // offending nodes/resources shown per finding
const SCORED_MODES = new Set(['binary', 'numeric', 'metricSavings']);
const IMPACT_ORDER = ['critical', 'serious', 'moderate', 'minor'];

// [audit id, label, good threshold, poor threshold, unit]. TBT is the lab proxy for INP.
const METRICS = [
  ['largest-contentful-paint', 'LCP', 2500, 4000, 'ms'],
  ['cumulative-layout-shift', 'CLS', 0.1, 0.25, ''],
  ['total-blocking-time', 'TBT (INP proxy)', 200, 600, 'ms'],
  ['interaction-to-next-paint', 'INP', 200, 500, 'ms'],
  ['first-contentful-paint', 'FCP', 1800, 3000, 'ms'],
  ['speed-index', 'Speed Index', 3400, 5800, 'ms'],
];

const truncate = (text, max = 110) => {
  const flat = String(text ?? '').replace(/\s+/g, ' ').replace(/\|/g, '\\|').trim();
  return flat.length > max ? `${flat.slice(0, max - 1)}…` : flat;
};

const formatMetric = (value, unit) =>
  unit === 'ms' ? `${(value / 1000).toFixed(2)} s` : value.toFixed(3);

const rate = (value, good, poor) =>
  value <= good ? 'good' : value <= poor ? 'needs improvement' : 'poor';

const median = (values) => {
  const sorted = [...values].sort((a, b) => a - b);
  const mid = Math.floor(sorted.length / 2);
  return sorted.length % 2 ? sorted[mid] : (sorted[mid - 1] + sorted[mid]) / 2;
};

// Lighthouse "list" details (used by insights) hold tables, list sections, checklists, and node items.
const tableRows = (item) => {
  if (Array.isArray(item?.value?.items)) return item.value.items; // list-section wrapping a table
  if (item?.type === 'table' && Array.isArray(item.items)) return item.items;
  return [item];
};

// Lists the first offending nodes or resources of a failing audit.
function offenders(details) {
  const items = (Array.isArray(details?.items) ? details.items : []).flatMap(tableRows);
  return items
    .map((item) => item?.node?.selector || item?.selector || item?.url || item?.sourceLocation?.url || item?.description || item?.label)
    .filter((entry) => typeof entry === 'string' && entry)
    .slice(0, MAX_ITEMS)
    .map((entry) => `\`${truncate(entry, 70)}\``);
}

function summarizeLighthouse(lhr, file) {
  const formFactor = lhr.configSettings?.formFactor ?? 'unknown';
  const out = [`## Lighthouse: ${lhr.finalDisplayedUrl ?? lhr.requestedUrl} (${formFactor})`, ''];
  out.push(`Source: \`${basename(file)}\`, Lighthouse ${lhr.lighthouseVersion}, ${lhr.fetchTime}`);
  if (lhr.runtimeError) out.push(`**Runtime error:** ${lhr.runtimeError.code}: ${lhr.runtimeError.message}`);
  for (const warning of lhr.runWarnings ?? []) out.push(`**Warning:** ${truncate(warning, 200)}`);

  out.push('', '| Category | Score |', '|---|---|');
  for (const category of Object.values(lhr.categories ?? {})) {
    const score = category.score === null ? 'n/a' : Math.round(category.score * 100);
    out.push(`| ${category.title} | ${score} |`);
  }

  out.push('', '| Metric | Value | Rating (good / poor at) |', '|---|---|---|');
  for (const [id, label, good, poor, unit] of METRICS) {
    const value = lhr.audits?.[id]?.numericValue;
    if (typeof value !== 'number') continue;
    out.push(`| ${label} | ${formatMetric(value, unit)} | ${rate(value, good, poor)} (${formatMetric(good, unit)} / ${formatMetric(poor, unit)}) |`);
  }

  for (const [categoryId, category] of Object.entries(lhr.categories ?? {})) {
    const failing = (category.auditRefs ?? [])
      .filter((ref) => ref.group !== 'metrics')
      .map((ref) => ({ ref, audit: lhr.audits?.[ref.id] }))
      .filter(({ audit }) => audit && SCORED_MODES.has(audit.scoreDisplayMode) && audit.score !== null && audit.score < PASS_SCORE)
      .sort((a, b) => b.ref.weight - a.ref.weight || a.audit.score - b.audit.score);
    if (failing.length === 0) continue;

    out.push('', `### Failing ${category.title} audits (${categoryId})`, '', '| Audit id | Score | Evidence | Examples |', '|---|---|---|---|');
    for (const { audit } of failing) {
      const savings = Object.entries(audit.metricSavings ?? {})
        .filter(([, saving]) => saving > 0)
        .map(([metric, saving]) => `${metric} -${metric === 'CLS' ? saving.toFixed(3) : `${Math.round(saving)} ms`}`);
      const evidence = [audit.title, audit.displayValue, savings.length ? `savings: ${savings.join(', ')}` : '']
        .filter(Boolean)
        .join('; ');
      out.push(`| \`${audit.id}\` | ${audit.score.toFixed(2)} | ${truncate(evidence, 160)} | ${offenders(audit.details).join(' ')} |`);
    }
  }
  return out.join('\n');
}

// Converts axe tags like "wcag1410" to "1.4.10"; level tags such as "wcag21aa" are skipped.
const wcagCriteria = (tags) =>
  tags.filter((tag) => /^wcag\d{3,}$/.test(tag)).map((tag) => `${tag[4]}.${tag[5]}.${tag.slice(6)}`);

// axe targets list one selector per frame level; a nested array is a path through shadow roots.
const axeTarget = (target) =>
  [].concat(target ?? []).map((part) => (Array.isArray(part) ? part.join(' >>> ') : part)).join(' ');

function summarizeAxe(results, file) {
  const out = [];
  for (const result of results) {
    const violations = [...(result.violations ?? [])].sort(
      (a, b) => IMPACT_ORDER.indexOf(a.impact) - IMPACT_ORDER.indexOf(b.impact),
    );
    out.push(`## axe-core ${result.testEngine?.version ?? ''}: ${result.url}`, '');
    out.push(`Source: \`${basename(file)}\`. ${violations.length} violations, ${result.incomplete?.length ?? 0} needing manual review.`, '');
    if (violations.length === 0) continue;

    out.push('| Rule id | Impact | WCAG | Nodes | Help | Examples |', '|---|---|---|---|---|---|');
    for (const violation of violations) {
      const criteria = wcagCriteria(violation.tags ?? []).join(', ') || 'best practice';
      const targets = (violation.nodes ?? []).slice(0, MAX_ITEMS).map((node) => `\`${truncate(axeTarget(node.target), 70)}\``);
      out.push(`| \`${violation.id}\` | ${violation.impact} | ${criteria} | ${violation.nodes?.length ?? 0} | ${truncate(violation.help)} | ${targets.join(' ')} |`);
    }
    out.push('');
  }
  return out.join('\n');
}

function summarizeMedians(reports) {
  const groups = new Map();
  for (const lhr of reports) {
    const key = `${lhr.finalDisplayedUrl ?? lhr.requestedUrl} (${lhr.configSettings?.formFactor ?? 'unknown'})`;
    groups.set(key, [...(groups.get(key) ?? []), lhr]);
  }
  const out = [];
  for (const [key, runs] of groups) {
    if (runs.length < 2) continue;
    out.push(`## Median of ${runs.length} Lighthouse runs: ${key}`, '', '| Metric | Median | Range | Rating |', '|---|---|---|---|');
    for (const [id, label, good, poor, unit] of METRICS) {
      const values = runs.map((lhr) => lhr.audits?.[id]?.numericValue).filter((v) => typeof v === 'number');
      if (values.length === 0) continue;
      const mid = median(values);
      const range = `${formatMetric(Math.min(...values), unit)} – ${formatMetric(Math.max(...values), unit)}`;
      out.push(`| ${label} | ${formatMetric(mid, unit)} | ${range} | ${rate(mid, good, poor)} |`);
    }
    out.push('');
  }
  return out.join('\n');
}

const files = process.argv.slice(2);
if (files.length === 0) {
  console.error('Usage: node summarize.mjs <lighthouse-or-axe-report.json> [...]');
  process.exit(2);
}

const sections = [];
const lighthouseReports = [];
for (const file of files) {
  let data;
  try {
    data = JSON.parse(readFileSync(file, 'utf8'));
  } catch (error) {
    sections.push(`## ${basename(file)}\n\nCould not read report: ${error.message}`);
    continue;
  }
  if (data?.lighthouseVersion) {
    lighthouseReports.push(data);
    sections.push(summarizeLighthouse(data, file));
  } else if (Array.isArray(data) || data?.violations) {
    sections.push(summarizeAxe([].concat(data), file));
  } else {
    sections.push(`## ${basename(file)}\n\nUnrecognized format: expected a Lighthouse or axe-core JSON report.`);
  }
}

const medians = summarizeMedians(lighthouseReports);
if (medians) sections.push(medians);
console.log(sections.join('\n\n'));
