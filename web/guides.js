'use strict';
const guideSearch=document.querySelector('#guide-search');
guideSearch?.addEventListener('input',()=>{
 const q=guideSearch.value.toLocaleLowerCase().trim();let count=0;
 document.querySelectorAll('.guide-card').forEach(card=>{card.hidden=!card.textContent.toLocaleLowerCase().includes(q);if(!card.hidden)count++;});
 document.querySelectorAll('.guide-group').forEach(group=>{if(group.querySelector('.guide-card'))group.hidden=![...group.querySelectorAll('.guide-card')].some(c=>!c.hidden);});
 document.querySelector('#guide-search-status').textContent=q?`${count} guide${count===1?'':'s'} found${count?'':'. Try another topic.'}`:'';
});
