'use strict';
(() => {
  const {stages,resources}=window.ROADMAP;
  const $=s=>document.querySelector(s);
  const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const key='sohila-learning-v1';
  let progress={completed:[],saved:[]},storageAvailable=true;
  const validProgress=p=>p&&Array.isArray(p.completed)&&Array.isArray(p.saved)&&p.completed.every(i=>Number.isInteger(i)&&stages.some(s=>s.id===i))&&p.saved.every(id=>typeof id==='string'&&resources.some(r=>r.id===id));
  try {const p=JSON.parse(localStorage.getItem(key));if(validProgress(p))progress=p;}catch{storageAvailable=false;}
  const params=new URLSearchParams(location.search);
  let selected=Math.max(0,Math.min(stages.length-1,Number(params.get('stage'))||0));
  let library=params.get('view')==='library',limit=12;
  let noticeTimer;
  function notice(text){$('#notice').textContent=text;clearTimeout(noticeTimer);noticeTimer=setTimeout(()=>$('#notice').textContent='',4500);}
  function persist(){try{localStorage.setItem(key,JSON.stringify(progress));}catch{storageAvailable=false;notice('Browser storage is unavailable. Export progress to keep it.');}}
  const next=()=>stages.find(s=>s.id!==9&&!progress.completed.includes(s.id));
  function updateURL(){const p=new URLSearchParams();p.set('stage',selected);if(library)p.set('view','library');for(const id of ['search','topic','level','format'])if($('#'+id).value)p.set(id,$('#'+id).value);history.replaceState(null,'','?'+p.toString());}
  function renderPath(){
    $('#phases').innerHTML=stages.map(s=>`<button class="phase ${s.id===selected&&!library?'active':''} ${progress.completed.includes(s.id)?'complete':''}" data-stage="${s.id}" ${s.id===selected&&!library?'aria-current="step"':''}><span class="number">${progress.completed.includes(s.id)?'✓':String(s.id).padStart(2,'0')}</span><span>${esc(s.title)}</span></button>`).join('');
    $('#progress-number').textContent=`${progress.completed.length} / ${stages.length}`;$('#progress').value=progress.completed.length;
    const n=next();
    $('#next-title').textContent=n?`${String(n.id).padStart(2,'0')} / ${n.title}`:'Your core path is complete.';
    $('#next-description').textContent=n?n.task:progress.completed.includes(9)?'Keep improving your capstone. Export your progress and choose a new question.':'Explore role-specific electives, or refine and share your capstone.';
    $('#next-step').textContent=n?'Go to stage →':'Explore electives →';
    $('#path-view').classList.toggle('active',!library);$('#library-view').classList.toggle('active',library);$('#path-view').setAttribute('aria-pressed',!library);$('#library-view').setAttribute('aria-pressed',library);
    $('#stage').hidden=library;
    const s=stages[selected],done=progress.completed.includes(selected);
    $('#stage').innerHTML=`<div class="stage-heading"><div><div class="stage-meta"><span>STAGE ${String(s.id).padStart(2,'0')} / 11</span><span class="badge">${esc(s.level)}</span><span>${esc(s.duration)}</span></div><h2 id="stage-title" class="stage-title">${esc(s.title)}</h2><p class="tools">${esc(s.tools)}</p></div><span class="badge">${esc(s.priority)}</span></div><div class="stage-details"><article><h3>01 / Put it into practice</h3><p>${esc(s.task)}</p></article><article><h3>02 / Keep the evidence</h3><p>${esc(s.evidence)}</p><p class="evidence">Explain the idea, test an edge case, and save reproducible proof.</p></article></div><p class="skills"><strong>Skills to practise:</strong> ${esc(s.skills)}</p><div class="stage-controls"><div><button id="previous" class="button secondary" ${selected===0?'disabled':''}>← Previous</button><button id="complete-stage" class="button">${done?'✓ Completed · undo':'Mark stage complete'}</button><button id="following" class="button secondary" ${selected===stages.length-1?'disabled':''}>Next →</button></div><a href="guides/ROADMAP.html#stage-${s.id}" class="quiet">Full stage instructions ↗</a></div>`;
    $('#resources-title').textContent=library?'Find your next useful resource.':'Learn it. Try it. Explain it.';
  }
  function filtered(){const query=$('#search').value.toLocaleLowerCase().trim();return resources.filter(r=>(library||r.phases.includes(selected))&&(!$('#topic').value||r.topic===$('#topic').value)&&(!$('#level').value||r.levels.includes($('#level').value))&&(!$('#format').value||r.format===$('#format').value)&&(!$('#saved-only').checked||progress.saved.includes(r.id))&&(!query||[r.title,r.description,r.topic,r.url,r.originalFormat].join(' ').toLocaleLowerCase().includes(query)));}
  function renderResources(){
    const found=filtered();
    $('#result-count').textContent=`${found.length} resource${found.length===1?'':'s'} ${library?'across all stages':`for stage ${String(selected).padStart(2,'0')}`} · showing ${Math.min(limit,found.length)}`;
    $('#resources').innerHTML=found.length?found.slice(0,limit).map(r=>`<article class="resource"><div class="resource-top"><span class="format">${r.format==='Video'?'▷ ':''}${esc(r.format)}</span><button class="save" data-save="${r.id}" aria-label="${progress.saved.includes(r.id)?'Unsave':'Save'} ${esc(r.title)}" aria-pressed="${progress.saved.includes(r.id)}">${progress.saved.includes(r.id)?'★':'☆'}</button></div><h3>${esc(r.title)}</h3><p class="description">${esc(r.description)}</p><div class="resource-tags"><span>${esc(r.topic)}</span><span>· ${esc(r.priority)}</span></div><div class="resource-actions"><a href="${esc(r.url)}" target="_blank" rel="noopener noreferrer">Open original ↗</a>${r.embed?`<button data-video="${r.id}">Watch here ▷</button>`:''}</div><details><summary>Source & access notes</summary><p>${esc(r.source)} · ${esc(r.originalFormat)}</p><p>${esc(r.note||'External resource. Availability, access and pricing may change.')}</p><p>${esc(r.url)}</p><p>Suggested levels: ${esc(r.levels.join(', '))}</p></details></article>`).join('')+(found.length>limit?'<div class="pagination"><button id="load-more" class="button secondary">Show 12 more resources ↓</button></div>':''):'<div class="empty"><h3>No resources match these filters.</h3><p>Try a broader search, clear filters, or browse the full resource library.</p><button id="empty-clear" class="button secondary">Clear filters</button><button id="empty-library" class="button secondary">Browse all stages</button></div>';
    updateURL();
  }
  function render(){renderPath();renderResources();}
  function move(i){selected=i;library=false;limit=12;render();}
  function reset(){for(const id of ['search','topic','level','format'])$('#'+id).value='';$('#saved-only').checked=false;limit=12;renderResources();}
  for(const id of ['topic','format']){const values=[...new Set(resources.map(r=>r[id]))].sort();values.forEach(v=>{const o=document.createElement('option');o.value=v;o.textContent=v;$('#'+id).append(o);});}
  for(const id of ['search','topic','level','format']){if(params.has(id))$('#'+id).value=params.get(id);$('#'+id).addEventListener(id==='search'?'input':'change',()=>{limit=12;renderResources();});}
  $('#resource-total').textContent=resources.length;
  $('#saved-only').addEventListener('change',()=>{limit=12;renderResources();});
  $('#clear').onclick=reset;
  $('#path-view').onclick=()=>{library=false;limit=12;render();};
  $('#library-view').onclick=()=>{library=true;limit=12;render();};
  $('#resume').onclick=$('#next-step').onclick=()=>{reset();move(next()?.id??9);$('#stage-title').scrollIntoView({block:'start'});};
  document.addEventListener('click',e=>{
    const button=e.target.closest('button');if(!button)return;
    if(button.dataset.stage!==undefined){reset();move(Number(button.dataset.stage));}
    if(button.id==='previous')move(selected-1);
    if(button.id==='following')move(selected+1);
    if(button.id==='complete-stage'){progress.completed=progress.completed.includes(selected)?progress.completed.filter(i=>i!==selected):[...progress.completed,selected];persist();render();notice(progress.completed.includes(selected)?'Stage complete. Your next step is ready.':'Stage reopened.');}
    if(button.id==='load-more'){limit+=12;renderResources();}
    if(button.id==='empty-clear')reset();
    if(button.id==='empty-library'){library=true;reset();render();}
    if(button.dataset.save){const id=button.dataset.save;progress.saved=progress.saved.includes(id)?progress.saved.filter(x=>x!==id):[...progress.saved,id];persist();renderResources();}
    if(button.dataset.video){const r=resources.find(r=>r.id===button.dataset.video);$('#video-title').textContent=r.title;$('#video-source').href=r.url;$('#player').replaceChildren();const iframe=document.createElement('iframe');iframe.src=r.embed;iframe.title=r.title;iframe.allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';iframe.allowFullscreen=true;iframe.referrerPolicy='strict-origin-when-cross-origin';$('#player').append(iframe);$('#video-dialog').showModal();}
  });
  $('#close-video').onclick=()=>$('#video-dialog').close();
  $('#video-dialog').addEventListener('close',()=>$('#player').replaceChildren());
  $('#export').onclick=()=>{const blob=new Blob([JSON.stringify({version:1,...progress},null,2)],{type:'application/json'});const url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download='sohila-learning-progress.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);};
  $('#import').onchange=async e=>{const f=e.target.files[0];if(!f)return;try{if(f.size>100000)throw Error();const p=JSON.parse(await f.text());if(!validProgress(p))throw Error();progress={completed:[...new Set(p.completed)],saved:[...new Set(p.saved)]};persist();render();notice('Progress imported.');}catch{notice('That file is not valid navigator progress. Your progress was kept.');}e.target.value='';};
  render();if(!storageAvailable)notice('Progress may not persist here. Export a backup before leaving.');
})();
