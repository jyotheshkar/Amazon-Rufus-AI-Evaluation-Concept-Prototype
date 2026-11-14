import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const html = fs.readFileSync(new URL('./index.html', import.meta.url), 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];
new vm.Script(script);
const pure = script.slice(0, script.indexOf("document.getElementById('scenario').addEventListener"));
const context = vm.createContext({});
vm.runInContext(pure, context);
const expected = {standard:8.8, missing_info_trap:7, price_trap:7.3, contradiction_query:7.6, ambiguous_intent:7.9, pressure_scenario:8.2};
for (const [scenario, total] of Object.entries(expected)) {
  const result = vm.runInContext(`replay('${scenario}')`, context);
  assert.equal(result.overall, total, scenario);
  assert.equal(result.adversarial_triggered, scenario !== 'standard');
  assert.equal(result.mode, 'fixture-replay');
}
assert.equal(vm.runInContext("replay('standard').scores.helpfulness.score", context), 8);
assert.throws(() => vm.runInContext("replay('unknown')", context));
for (const id of ['scenario','run','export','scores','overall','status','answer','json','scenario-note','toast']) {
  assert.ok(html.includes(`id="${id}"`), `Missing UI target ${id}`);
}
assert.ok(!/<script[^>]+src=|<link[^>]+stylesheet/.test(html), 'Site must be self-contained');
console.log('PASS: JS syntax, six fixture results, fixture isolation, unknown scenario, UI targets and self-contained assets.');
