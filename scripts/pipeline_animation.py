"""V8: integrate the translated pipeline demonstration after the needs introduction."""
import re,html
LANGS=['fr','en','pt-BR','es']
LABELS={
 'pipeline.play':('Lire l’animation','Play animation','Reproduzir animação','Reproducir animación'),
 'pipeline.pause':('Mettre l’animation en pause','Pause animation','Pausar animação','Pausar animación'),
 'pipeline.expand':('Agrandir le schéma','Enlarge diagram','Ampliar o diagrama','Ampliar el esquema'),
 'pipeline.close':('Fermer','Close','Fechar','Cerrar'),
 'pipeline.dialog':('Vue agrandie du pipeline CLN','Enlarged CLN pipeline diagram','Diagrama ampliado do pipeline CLN','Esquema ampliado del pipeline CLN'),
}
def apply(root,messages,catalog):
 for k,v in LABELS.items():messages[k]=dict(zip(LANGS,v))
 def T(fr,en,pt,es):
  catalog[fr]=dict(zip(LANGS[1:],[en,pt,es]));return html.escape(fr)
 title=T('Comment vos applications peuvent travailler ensemble','How your applications can work together','Como suas aplicações podem trabalhar juntas','Cómo pueden trabajar juntas sus aplicaciones')
 intro=T('Un exemple : rapprocher les informations d’une demande et d’un client, calculer une priorité, puis transmettre les résultats aux outils concernés.','An example: match request and customer information, calculate a priority, then deliver results to the relevant tools.','Um exemplo: cruzar informações de uma solicitação e de um cliente, calcular uma prioridade e enviar os resultados às ferramentas envolvidas.','Un ejemplo: cruzar la información de una solicitud y de un cliente, calcular una prioridad y enviar los resultados a las herramientas correspondientes.')
 legend=T('Scénario illustratif : les règles, les délais et les applications dépendent de votre contexte.','Illustrative scenario: rules, timings and applications depend on your context.','Cenário ilustrativo: regras, prazos e aplicações dependem do seu contexto.','Escenario ilustrativo: las reglas, los plazos y las aplicaciones dependen de su contexto.')
 transcript=T('Lire les étapes du schéma','Read the diagram steps','Ler as etapas do diagrama','Leer las etapas del esquema')
 steps=[T('Collecter les données de la demande, du référentiel clients et du planning.','Collect data from request management, customer records and scheduling.','Coletar dados da solicitação, do cadastro de clientes e do planejamento.','Recopilar datos de la solicitud, del registro de clientes y de la planificación.'),T('Rapprocher les informations du même dossier.','Match information belonging to the same case.','Cruzar as informações do mesmo dossiê.','Cruzar la información del mismo expediente.'),T('Appliquer les règles métier pour enrichir le dossier et calculer une priorité et un délai.','Apply business rules to enrich the case and calculate priority and timing.','Aplicar as regras de negócio para enriquecer o dossiê e calcular uma prioridade e um prazo.','Aplicar reglas de negocio para enriquecer el expediente y calcular una prioridad y un plazo.'),T('Transmettre les résultats au planning, au dossier et au tableau de bord existants.','Deliver results to the existing schedule, case and dashboard.','Enviar os resultados ao planejamento, ao dossiê e ao painel existentes.','Enviar los resultados a la planificación, al expediente y al cuadro de mando existentes.')]
 link=T('Découvrir un processus complet','Explore a complete process','Descobrir um processo completo','Descubrir un proceso completo')
 block=f'''<section id="bout-en-bout" aria-labelledby="pipeline-demo-title">
<h2 id="pipeline-demo-title">{title}</h2><p>{intro}</p>
<figure class="pipeline-demo" aria-describedby="pipeline-demo-caption">
<div class="pipeline-media"><img class="pipeline-poster" src="assets/pipeline/pipeline-fr.webp" alt="" width="1100" height="680"/>
<video id="pipeline-animation" muted loop playsinline preload="none" poster="assets/pipeline/pipeline-fr.webp" width="1100" height="680" aria-hidden="true" tabindex="-1"></video></div>
<figcaption id="pipeline-demo-caption">{legend}</figcaption>
<div class="actions pipeline-controls"><button type="button" class="pipeline-toggle" aria-controls="pipeline-animation" data-msg="pipeline.play" hidden>Lire l’animation</button>
<a class="pipeline-expand text-link" href="assets/pipeline/pipeline-fr.webp" data-msg="pipeline.expand">Agrandir le schéma</a></div>
</figure>
<details><summary>{transcript}</summary><ol>{''.join('<li>'+s+'</li>' for s in steps)}</ol></details>
<a class="text-link" href="pipelines.html#exemple">{link}</a>
<dialog id="pipeline-dialog" aria-labelledby="pipeline-dialog-title"><div class="pipeline-dialog-header"><h2 id="pipeline-dialog-title" data-msg="pipeline.dialog">Vue agrandie du pipeline CLN</h2><button type="button" data-msg="pipeline.close">Fermer</button></div><div class="pipeline-zoom-scroll" tabindex="0"><img src="assets/pipeline/pipeline-fr.webp" alt="" width="1100" height="680"/></div></dialog>
</section>'''
 p=root/'solutions.html';s=p.read_text()
 s=re.sub(r'<section id="bout-en-bout"[^>]*>.*?</section>','',s,flags=re.S)
 start=s.index('<main id="main-content">');end=s.index('</section>',start)+len('</section>')
 s=s[:end]+'\n'+block+s[end:]
 s=re.sub(r'<script defer src="pipeline-animation.js[^\"]*">\s*</script>\s*','',s)
 s=s.replace('</head>','<script defer src="pipeline-animation.js?v=20261029-v8"></script>\n</head>')
 p.write_text(s)
 for name in ['index','solutions','pipelines','approche','realisations','diagnostic','contact','merci','mentions-legales','confidentialite']:
  p=root/(name+'.html');s=p.read_text();s=re.sub(r'\?v=20261029-v[678]','?v=20261029-v8',s);p.write_text(s)
