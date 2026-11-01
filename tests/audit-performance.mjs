import vm from 'node:vm';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
const messages=JSON.parse(readFileSync('i18n/messages.json'));
for(const lang of ['fr','en','pt-BR','es']){
 const window={CLN:{t:key=>messages[key]?.[lang]||key}};
 vm.runInNewContext(readFileSync('case-data.js','utf8'),{window});
 const data=window.CLNCase;
 const raw={approach:'audit',situation:'Texte libre <sans modification>'};
 const answers=data.clean(raw);
 assert.equal(answers.approach,'audit');
 assert.equal(answers.situation,raw.situation);
 assert(data.summary(answers).includes(messages['case.choice.approach.audit'][lang]));
 assert(data.valid({version:11,id:'audit-test',generatedAt:new Date().toISOString(),answers}));
 assert(data.valid({version:11,id:'legacy-test',generatedAt:new Date().toISOString(),answers:data.clean({approach:'existing'})}));
 assert.equal(data.clean({approach:'invalid'}).approach,'inconnu');
}
console.log('PASS audit: four-language summary, schema validation, free text, legacy transfer and invalid choice.');
