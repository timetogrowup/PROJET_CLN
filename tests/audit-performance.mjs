import vm from 'node:vm';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
const messages=JSON.parse(readFileSync('i18n/messages.json'));
for(const lang of ['fr','en','pt-BR','es']){
 const window={CLN:{t:key=>messages[key]?.[lang]||key}};
 vm.runInNewContext(readFileSync('case-data.js','utf8'),{window});
 const data=window.CLNCase;
 const raw={approach:['audit','existing','compare'],situation:'Texte libre <sans modification>'};
 const answers=data.clean(raw);
 assert.deepEqual(Array.from(answers.approach),['audit','existing','compare']);
 for(const code of answers.approach) assert(data.summary(answers).includes(messages['case.choice.approach.'+code][lang]));
 assert.deepEqual(Array.from(data.clean({approach:['audit','audit','invalid']}).approach),['audit']);
 assert.deepEqual(Array.from(data.clean({approach:['audit','inconnu']}).approach),['inconnu']);
 assert.deepEqual(Array.from(data.clean({approach:'audit'}).approach),['audit']);
 assert.equal(answers.situation,raw.situation);
 assert(data.summary(answers).includes(messages['case.choice.approach.audit'][lang]));
 assert(data.valid({version:11,id:'audit-test',generatedAt:new Date().toISOString(),answers}));
 assert(data.valid({version:11,id:'legacy-test',generatedAt:new Date().toISOString(),answers:data.clean({approach:'existing'})}));
 assert.deepEqual(Array.from(data.clean({approach:'invalid'}).approach),['inconnu']);
 assert(data.valid({version:11,id:'legacy-string',generatedAt:new Date().toISOString(),answers:{...answers,approach:'audit'}}));
}
console.log('PASS audit: four-language summary, schema validation, free text, legacy transfer and invalid choice.');
