import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {escape as e,icon,intro,link,cta,about,resume,learn,contact,casePage} from './pages.mjs';
import {reportRoute, progressBadge, dashboardGallery, reportPage, inlineReport, homeReports, currentWork, toolkit, imageViewer} from './previews.mjs';
import {directoryCard, projectPage, projectPreview, caseExtras, studioHome, communityPage, credentialsPage, servicesPage, searchDialog} from './studio.mjs';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const read=async file=>JSON.parse(await fs.readFile(path.join(root,file),'utf8'));
const profile=await read('content/profile.json');
const cases={...await read('content/cases.json'),...await read('content/additional-cases.json')};
const catalog=await read('content/repositories.json');
const {reports}=await read('content/project-previews.json');
const projectStatus=await read('content/project-status.json');
const reportByRepo=new Map(reports.map(r=>[r.repo,r]));
const {projects:projectDetails}=await read('content/project-details.json');
const credentials=await read('content/credentials.json');
const community=await read('content/community.json');
const projectDetailsByRepo=new Map(projectDetails.map(p=>[p.repo,p]));
const rawHome=await fs.readFile(path.join(root,'src/home.html'),'utf8');
const symbols=rawHome.slice(rawHome.indexOf('<svg class="icon-library"'),rawHome.indexOf('</svg>')+6);
const title=profile.name;
const urlArg=process.argv.indexOf('--site-url');
const origin=(urlArg>=0?process.argv[urlArg+1]:process.env.SITE_URL||(process.env.VERCEL_PROJECT_PRODUCTION_URL?'https://'+process.env.VERCEL_PROJECT_PRODUCTION_URL:profile.website||''))?.replace(/\/$/,'');
if(origin&&!/^https?:\/\/[^\s]+$/.test(origin))throw new Error('SITE_URL must be an absolute HTTP(S) origin');
const out=path.join(root,'dist');
await fs.rm(out,{recursive:true,force:true});await fs.mkdir(out,{recursive:true});
await fs.cp(path.join(root,'src/assets'),out,{recursive:true});
const categories={all:'All work',analytics:'BI & analytics',engineering:'Data engineering',automation:'Automation & AI',apps:'Apps & tools',learning:'Learning & resources'};
function category(repo){const n=repo.name.toLowerCase();if(repo.fork||/roadmap|second.brain|course|fundamentals|workshop|^linux$|bootdev|awesome|tidytuesday|anshlamba/.test(n))return 'learning';if(/n8n|nl2sql|sentiment|gpt-oss/.test(n))return 'automation';if(/portfolio|website|showcase|deep.clean|local_data_aggregator|^the-data-tea$|hr-analytics-hub|data-career-roadmap-generator/.test(n))return 'apps';if(/pipeline|dwh|warehouse|etl|kafka|hadoop|streampulse|employee-directory|pixelfed|cosmetics|kickstarter|enterprise-hr|sql-server-data-platform|novatel/.test(n))return 'engineering';return 'analytics';}
const descriptions={
 'regional-sales-dashboard':'Power BI reporting for regional sales trends, profitability analysis, and growth opportunities.',
 'sohila-k-abbas-website':'A personal data portfolio website built with React and TypeScript.',
 'flyrank-ml-internship-starter':'Applied ML and search-intelligence notebooks, evaluation scripts, research writing, and an automation-agent showcase.',
 'fmcg-sales-churn-drop-analysis-powerbi':'Power BI portfolio exploring retailer lifecycle, delivery performance, and commercial metrics in an Egyptian B2B scenario.',
 'marketing_campaigns_analysis':'A data-engineering and analytics project connecting campaign inputs to modeled reporting and investment questions.',
 'ecommerce-flash-sale-analysis':'A data-engineering investigation of flash-sale behavior, margin questions, and potential bot-related patterns.',
 'apple-stock-market-analysis':'Historical AAPL market-data analysis with a Python and BI workflow.',
 'customer-360-banking-etl':'A diploma capstone using Informatica IICS to integrate banking data, apply exception rules, and produce a customer view.',
 'novatel-big-data-ecosystem':'A telecom data-engineering scenario exploring high-write-velocity architecture.',
 'enterprise-hr-analytics':'A multi-source HR and client-delivery portfolio scenario using a Kimball galaxy model.',
 'Sohila-Khaled-Abbas':'The source and assets behind my GitHub profile.',
 'Social-Media-Advertising-Dashboard':'A social-media advertising analysis and dashboard repository.',
 'airbnb-amsterdam-analysis':'An Airbnb Amsterdam exploratory analysis repository.',
 'Customer-Churn-Analysis':'A customer-churn analysis project.',
 'marketing-campaign-dashboard':'A marketing-campaign analytics and dashboard project.',
 'MaxAB_B2B_Retail_Wallet_Optimization':'A B2B retail wallet-optimization portfolio repository.',
 'Machine-Learning-and-Data-Science-Resourses':'A forked collection of machine-learning and data-science resources.',
 'data-engineering-roadmap':'A forked data-engineering learning roadmap.',
 'AnshLambaYoutube':'A forked collection of tutorial materials.',
 'AI_tools_nontechnical':'A forked collection of AI tools for nontechnical learners.',
 'Obsidian-Vault-Roadmap':'A forked learning-roadmap vault.',
 'tidytuesday':'A fork of the TidyTuesday data-practice resource repository.'
};
const byRepo=new Map(Object.values(cases).map(c=>[c.repo,c]));
const ordered=catalog.repositories.map(r=>({...r,category:category(r)})).sort((a,b)=>Number(byRepo.has(b.name))-Number(byRepo.has(a.name))||Date.parse(b.updated_at)-Date.parse(a.updated_at));
const repoCard=r=>directoryCard(r,projectDetailsByRepo.get(r.name),reportByRepo.get(r.name),projectStatus,categories,byRepo.has(r.name));
function work(){return `${intro('WORK / FROM QUESTION TO IMPLEMENTATION','A collection of<br><em>connected ideas.</em>','Dashboards, data pipelines, automation, and learning projects. Explore the case studies or search the full GitHub collection.')}<section class="wrap work-stats"><span><strong>${ordered.length}</strong> public repositories</span><span><strong>${projectDetails.length}</strong> project previews</span><span><strong>${Object.keys(cases).length}</strong> case studies</span><span><strong>${ordered.filter(r=>r.fork).length}</strong> clearly labeled forks</span><a href="https://github.com/Sohila-Khaled-Abbas" target="_blank" rel="noopener noreferrer">GitHub profile ${icon}</a></section><section id="repositories" class="wrap page-section repository-section"><div class="section-label"><span>GITHUB / THE FULL COLLECTION</span><span class="mono muted">UPDATED 30 OCT 2026</span></div><form class="repo-controls" role="search" onsubmit="return false"><label class="repo-search">Search repositories<span class="repo-search-field"><span aria-hidden="true">⌕</span><input id="repo-query" type="search" placeholder="Try Power BI, n8n, Python, or a project name…" autocomplete="off"></span></label><label>Repository type<select id="repo-kind"><option value="all">All repositories</option><option value="original">Original repositories</option><option value="fork">Forks & learning</option></select></label><label>Project status<select id="repo-status-filter"><option value="all">All projects</option><option value="progress">In progress</option></select></label><label>Sort by<select id="repo-sort"><option value="featured">Case studies first</option><option value="recent">Recently updated</option><option value="name">Name · A to Z</option></select></label></form><div class="repo-filters" role="group" aria-label="Filter repositories by subject">${Object.entries(categories).map(([key,label])=>`<button class="repo-filter${key==='all'?' active':''}" data-repo-filter="${key}" aria-pressed="${key==='all'}">${label}<span>${key==='all'?ordered.length:ordered.filter(r=>r.category===key).length}</span></button>`).join('')}</div><div class="repo-view-tools"><p>Open a project to explore its preview, toolkit, and available source files.</p><div class="project-view-buttons" role="group" aria-label="Project display"><button data-project-view="grid" aria-pressed="true">Gallery</button><button data-project-view="list" aria-pressed="false">List</button></div></div><div class="repo-results-bar"><p id="repo-status" role="status" aria-live="polite">${ordered.length} repositories</p><button id="repo-reset" class="text-link" hidden>Clear filters ×</button></div><div id="repo-grid" class="repo-grid">${ordered.map(repoCard).join('')}</div><div id="repo-empty" class="repo-empty" hidden><h3>No repositories match that search.</h3><p>Try a shorter name, a tool, or another subject.</p><button class="button primary" data-reset-repos>Show all repositories</button></div><div class="load-more-row"><button id="repo-more" class="button primary" hidden>Show more repositories <svg class="icon"><use href="#arrow"/></svg></button></div><p class="repo-footnote">A dated snapshot of accessible public repositories. Forks include upstream attribution. Repository language is GitHub’s primary detected language, not the complete project stack.</p><noscript><p>All repositories are shown below. Enable JavaScript to search, filter, and sort the collection.</p></noscript></section>${cta()}`;}
const navItems=[['/','Home'],['/work/','Work'],['/dashboards/','Dashboards'],['/about/','About'],['/resume/','Résumé'],['/learn/','Data Tea'],['/services/','Work with me'],['/community/','Community'],['/credentials/','Credentials']];
function header(route){const navLink=([url,label])=>`<a href="${url}"${route===url?' aria-current="page"':''}>${label}</a>`;return `<header class="header"><div class="nav-shell wrap"><a class="brand" href="/" aria-label="Sohila home"><span class="brand-mark"><i></i><i></i><i></i><i></i></span>sohila<span class="brand-dot">.</span></a><nav id="navigation" aria-label="Main navigation">${navItems.slice(0,4).map(navLink).join('')}<details class="nav-more"><summary>More</summary><div class="nav-more-menu">${navItems.slice(4).map(navLink).join('')}</div></details></nav><div class="nav-actions"><button class="project-search-button" data-open-finder aria-label="Search projects" aria-keyshortcuts="Control+K Meta+K" title="Search projects · Ctrl / ⌘ K"><svg class="icon" viewBox="0 0 24 24"><circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5"/></svg></button><button class="theme-toggle" aria-label="Switch to dark theme" title="Change theme"><svg class="icon"><use href="#sun"/></svg></button><a class="nav-contact" href="/contact/">Let’s connect ${icon}</a><button class="menu-toggle" aria-label="Open menu" aria-expanded="false" aria-controls="navigation"><span></span><span></span></button></div></div></header>`;}
function footer(){return `<footer class="site-footer"><div class="wrap"><div class="footer-main"><div><a class="brand" href="/">sohila<span class="brand-dot">.</span></a><p>Thoughtful data. Useful things.</p><span class="mono muted">DAMIETTA, EGYPT · OPEN TO REMOTE COLLABORATION</span></div><div class="footer-pages">${navItems.map(([url,label])=>`<a href="${url}">${label}</a>`).join('')}<a href="/contact/">Contact</a></div><div class="footer-social">${link(profile.github,'GitHub')}${link(profile.linkedin,'LinkedIn')}<a href="mailto:${e(profile.email)}">${e(profile.email)}</a></div></div><div class="footer-bottom"><span>© <span id="year">2026</span> ${e(profile.name)}</span><span>Built around questions worth answering.</span><a href="#main">Back to top ↑</a></div></div></footer><div id="toast" class="toast" role="status" aria-live="polite"></div>`;}
const pages=[];
async function write(route,pageTitle,description,body){
  const seoTitle=route==='/'?`${profile.name} | ${profile.seo_headline}`:`${pageTitle} | ${title}`;
  const entities=origin&&['/','/about/'].includes(route)?[
    {'@type':'WebSite','@id':origin+'/#website',url:origin+'/',name:profile.name,alternateName:'Sohila Data Studio',publisher:{'@id':origin+'/#person'}},
    {'@type':'Person','@id':origin+'/#person',name:profile.name,url:origin+'/',jobTitle:profile.role.split('|').map(x=>x.trim()),sameAs:[profile.linkedin,profile.github]},
    ...(route==='/about/'?[{'@type':'ProfilePage','@id':origin+route+'#profile',url:origin+route,name:'About '+profile.name,mainEntity:{'@id':origin+'/#person'}}]:[])
  ]:[];
  const jsonLd=entities.length?`<script type="application/ld+json">${JSON.stringify({'@context':'https://schema.org','@graph':entities}).replaceAll('<','\\u003c')}</script>`:'';
  const html=`<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#743348"><title>${e(seoTitle)}</title><meta name="description" content="${e(description)}">${route.includes('/Airbnb_Athens_Analysis/')?'<meta name="robots" content="noindex,follow">':''}<meta property="og:title" content="${e(seoTitle)}"><meta property="og:description" content="${e(description)}"><meta property="og:type" content="website"><meta property="og:site_name" content="${e(profile.name)}"><meta name="author" content="${e(profile.name)}">${jsonLd}${origin?`<link rel="canonical" href="${origin}${route}"><meta property="og:url" content="${origin}${route}"><meta property="og:image" content="${origin}/social-card.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Sohila Khaled Abbas — Data, analytics engineering and machine learning portfolio"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="${origin}/social-card.png">`:''}<link rel="icon" href="/favicon.ico?v=warm-grid-1" sizes="16x16 32x32 48x48"><link rel="icon" href="/favicon-32.png?v=warm-grid-1" type="image/png" sizes="32x32"><link rel="icon" href="/favicon.svg?v=warm-grid-1" type="image/svg+xml" sizes="any"><link rel="apple-touch-icon" href="/apple-touch-icon.png?v=warm-grid-1" sizes="180x180"><link rel="stylesheet" href="/styles.css"><link rel="stylesheet" href="/pages.css"><link rel="stylesheet" href="/enhancements.css"><link rel="stylesheet" href="/studio.css"><link rel="stylesheet" href="/theme.css"><script src="/app.js" defer></script><script src="/enhancements.js" defer></script><script src="/studio.js" defer></script></head><body><a class="skip" href="#main">Skip to content</a>${symbols}${header(route)}<main id="main">${body}</main>${footer()}${imageViewer()}${searchDialog(projectDetails.map(p=>({repo:p.repo,title:p.title,tags:p.technologies,url:'/projects/'+p.repo+'/'})).concat([{repo:'mobile-technical-support-analytics',title:'Mobile Technical Support Analytics',tags:['Power BI','DAX','Customer support'],url:'/dashboards/mobile-technical-support-analytics/'}]))}</body></html>`;const target=route==='/404.html'?path.join(out,'404.html'):path.join(out,route,'index.html');await fs.mkdir(path.dirname(target),{recursive:true});await fs.writeFile(target,html);if(route!=='/404.html')pages.push(route);}
let home=rawHome.slice(rawHome.indexOf('<main id="main">')+16,rawHome.indexOf('</main>'));
home=home.replace('<div class="work-footer"><span>Curious about the details? It’s all in the repositories.</span><a class="text-link" href="https://github.com/Sohila-Khaled-Abbas?tab=repositories" target="_blank" rel="noopener noreferrer">More on GitHub <svg class="icon small"><use href="#external"/></svg></a></div>',`<div class="work-footer"><span>${ordered.length} public repositories. ${Object.keys(cases).length} case studies. Plenty to explore.</span>${link('/work/','Browse all my work')}</div>`);
home=home.replace('My path into data is a career shift built through hands-on projects, structured study, and a lot of asking “why?”','My path into data connects hands-on projects, freelance BI work, internships, technical coaching, and a background in agricultural research.');
home=home.replace('Let’s connect on LinkedIn','More about my journey').replace('href="https://linkedin.com/in/sohilakabbas" target="_blank" rel="noopener noreferrer">More about my journey','href="/about/">More about my journey');
home=home.replace('I’m Sohila, a Data Analyst and BI Developer based in Egypt.','I’m Sohila, a Data & Analytics Engineer and Machine Learning Engineer based in Egypt.');
home=home.replace('My work spans BI and automation.','My work spans data engineering, machine learning, BI, and automation.');
home=home.replace('<span>Business intelligence</span><span>Analytics engineering</span><span>Workflow automation</span>','<span>Data & analytics engineering</span><span>Machine learning</span><span>Business intelligence</span>');
home=home.replace('I’m interested in remote opportunities and collaborations in data analytics, business intelligence, and automation.','I’m interested in remote opportunities and collaborations in data and analytics engineering, machine learning, business intelligence, and automation.');
home=home.replace(/<div class="toolstrip">[\s\S]*?<\/div><\/div>/,toolkit());
home=home.replace('<div class="sheet-top"><span class="file-symbol">≡</span>', '<div class="sheet-top"><img class="hero-logo" src="/logos/python.svg" alt="Python">');
home=home.replace('<div class="model-header"><span class="live-dot"></span>', '<div class="model-header"><img class="hero-logo" src="/logos/dbt.svg" alt="dbt">');
home=home.replace('<div class="insight-note"><span class="note-star">✳</span>', '<div class="insight-note"><img class="hero-logo" src="/logos/powerbi.svg" alt="Power BI">');
home=home.replace(/(<div class="hero-location">[^\n]+<\/div>)/,'$1<button class="hero-motion-toggle" data-motion-toggle aria-pressed="false">Pause animation</button>');
home=home.replace('  <section id="work"', currentWork(projectStatus,cases)+'<section id="work"');
home=home.replace('  <section id="approach"', homeReports(reports,projectStatus)+'<section id="approach"');
home=home.replace('<h3><button data-project="pixelfed">',progressBadge('pixelfed-analytics-engineering',projectStatus)+'<h3><button data-project="pixelfed">');
home=home.replace('<h3><button data-project="n8n">',progressBadge('n8n-production-queue-setup',projectStatus)+'<h3><button data-project="n8n">');
home=home.replace('<section id="about"',`<section class="home-path wrap"><div><span class="eyebrow">A BROADER VIEW</span><h2>There’s more<br><em>behind the work.</em></h2></div><div>${link('/resume/','Experience & education')}${link('/learn/','Learning hubs & labs')}${link('/work/','All GitHub repositories')}</div></section><section id="about"`);
home=studioHome(profile,cases,ordered,projectDetails,reports,projectStatus,home.match(/<section id="approach"[\s\S]*?<\/section>/)?.[0]);
await write('/','Data & Analytics Engineer | Machine Learning Engineer','Sohila Khaled Abbas: data and analytics engineering, machine learning, Python, SQL, Power BI, ETL/ELT and data warehousing. Explore projects and experience.',home);
await write('/work/','Work & GitHub repositories','Browse Sohila’s public GitHub repositories, detailed project case studies, BI dashboards, data pipelines, and automation workflows.',work());
await write('/dashboards/','Power BI dashboards & report previews','Explore Sohila’s Power BI reports, public interactive dashboards, repository screenshots, and report project files.',dashboardGallery(reports,projectStatus));
for(const r of reports)await write(reportRoute(r.repo),r.title+' — Dashboard',r.description,reportPage(r,projectStatus));
await write('/about/','About Sohila','Meet Sohila Khaled Abbas, a Data & Analytics Engineer and Machine Learning Engineer based in Egypt. Explore her background, technical skills, and experience.',about(profile));
await write('/resume/','Résumé & experience','Sohila’s professional experience, education, technical skills, projects, and selected training. Includes a print-friendly résumé.',resume(profile,cases));
await write('/learn/','The Data Tea','Explore Sohila’s learning hubs, Excel and VBA resources, data-engineering roadmap, networking labs, and operating-system practice.',learn(profile));
await write('/services/','Work with Sohila','Remote collaboration in Power BI reporting, data engineering, automation, and technical mentoring. Prepare a project brief.',servicesPage());
await write('/community/','Community & mentoring','The Data Tea, TechZone mentoring, and Notion community workshops by Sohila Khaled Abbas.',communityPage(community));
await write('/credentials/','Courses & credentials','Explore Sohila’s learning and credential collection across analytics, engineering, automation, AI, and SQL.',credentialsPage(credentials));
await write('/contact/','Contact','Connect with Sohila about remote analytics, BI, data engineering, and automation opportunities.',contact(profile));
for(const [key,c] of Object.entries(cases)){
 const p=projectDetailsByRepo.get(c.repo),report=reportByRepo.get(c.repo);
 let body=casePage(c,cases,null);
 body=body.replace(/<div class="wrap"><div class="generic-cover">[\s\S]*?<section class="wrap case-story">/,`${p?projectPreview(p,report)+caseExtras(p,report):''}<section class="wrap case-story">`);
 body=body.replace('<div class="eyebrow">'+e(c.type)+'</div>','<div class="eyebrow">'+e(c.type)+'</div>'+progressBadge(c.repo,projectStatus));
 if(report)body=body.replace('<section class="wrap case-story">',inlineReport(report)+'<section class="wrap case-story">');
 await write('/projects/'+c.repo+'/',c.title,c.intro,body);
}
for(const p of projectDetails){if(byRepo.has(p.repo))continue;const r=ordered.find(r=>r.name===p.repo);await write('/projects/'+p.repo+'/',p.title,p.summary,projectPage(p,r,reportByRepo.get(p.repo),projectStatus,categories));}
await write('/404.html','Page not found','This page could not be found.',`${intro('404 / LET’S FIND YOUR WAY BACK','A missing page.<br><em>A better next step.</em>','That address doesn’t point to a page here. Explore the project collection or head back home.')}<div class="wrap error-actions">${link('/work/','Explore my work','button primary')}${link('/','Back to home')}</div>`);
await fs.writeFile(path.join(out,'robots.txt'),'User-agent: *\nAllow: /\n'+(origin?'Sitemap: '+origin+'/sitemap.xml\n':''));
if(origin)await fs.writeFile(path.join(out,'sitemap.xml'),'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+pages.map(route=>'<url><loc>'+e(origin+route)+'</loc></url>').join('')+'</urlset>');
await fs.writeFile(path.join(out,'site-manifest.json'),JSON.stringify({pages,repositoryCount:ordered.length,caseStudyCount:Object.keys(cases).length,projectPreviewCount:projectDetails.length,reportCount:reports.length,updated:catalog.checked_on},null,2));
console.log(`Built ${pages.length} pages, ${ordered.length} repository entries, and ${Object.keys(cases).length} case studies.`);

// Copy the reviewed, prebuilt learning navigator into the portfolio output.
const navigatorBuild=path.join(root,"learning-navigator-dist");
if(await fs.stat(navigatorBuild).then(s=>s.isDirectory()).catch(()=>false)) await fs.cp(navigatorBuild,path.join(out,"learning-navigator"),{recursive:true});
