#!/usr/bin/env node
/**
 * Record 3 vertical (9:16) Cursor demo screencasts.
 */
import { chromium } from 'playwright-core';
import path from 'path';
import fs from 'fs';
import { spawnSync } from 'child_process';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = __dirname;
const OUT = path.join(ROOT, 'out');
const ART = '/opt/cursor/artifacts';
fs.mkdirSync(OUT, { recursive: true });
fs.mkdirSync(ART, { recursive: true });

const demos = [
  { file: '01-tab.html', name: 'screencast_01_tab_complete', maxMs: 12000 },
  { file: '02-context.html', name: 'screencast_02_repo_context_v2', maxMs: 12000 },
  { file: '03-agent.html', name: 'screencast_03_ai_partner_v2', maxMs: 13000 },
];

async function recordOne(browser, demo) {
  const videoDir = path.join(OUT, demo.name + '_raw');
  fs.rmSync(videoDir, { recursive: true, force: true });
  fs.mkdirSync(videoDir, { recursive: true });

  const context = await browser.newContext({
    viewport: { width: 1080, height: 1920 },
    deviceScaleFactor: 1,
    recordVideo: { dir: videoDir, size: { width: 1080, height: 1920 } },
  });
  const page = await context.newPage();
  const url = 'file://' + path.join(ROOT, demo.file);
  await page.goto(url, { waitUntil: 'networkidle' });

  const started = Date.now();
  while (Date.now() - started < demo.maxMs) {
    const done = await page.evaluate(() => document.body.dataset.done === '1');
    if (done) break;
    await page.waitForTimeout(200);
  }
  await page.waitForTimeout(400);
  await context.close();

  const files = fs.readdirSync(videoDir).filter(f => f.endsWith('.webm'));
  if (!files.length) throw new Error('No webm for ' + demo.name);
  const webm = path.join(videoDir, files[0]);
  const mp4 = path.join(OUT, demo.name + '.mp4');
  const ff = spawnSync('ffmpeg', [
    '-y', '-i', webm,
    '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
    '-movflags', '+faststart',
    '-an',
    mp4,
  ], { encoding: 'utf8' });
  if (ff.status !== 0) {
    console.error(ff.stderr);
    throw new Error('ffmpeg failed for ' + demo.name);
  }
  const artPath = path.join(ART, demo.name + '.mp4');
  fs.copyFileSync(mp4, artPath);
  const thumb = path.join(ART, demo.name + '_preview.jpg');
  spawnSync('ffmpeg', ['-y', '-ss', '2', '-i', mp4, '-frames:v', '1', '-q:v', '3', thumb], { encoding: 'utf8' });
  console.log('OK', mp4, '->', artPath);
  return artPath;
}

const browser = await chromium.launch({
  executablePath: '/usr/bin/google-chrome-stable',
  headless: true,
  args: ['--no-sandbox', '--disable-dev-shm-usage'],
});
try {
  for (const demo of demos) {
    await recordOne(browser, demo);
  }
} finally {
  await browser.close();
}
console.log('All screencasts ready');
