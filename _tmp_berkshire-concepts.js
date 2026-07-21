
const grid=document.getElementById('grid');
const cards=[...grid.querySelectorAll('.card')];
const search=document.getElementById('search');
const catBtns=[...document.querySelectorAll('.cat-btn')];
let curCat='全部';
function applyFilter(){
  const q=search.value.trim().toLowerCase();
  cards.forEach(c=>{
    const name=c.dataset.name.toLowerCase();
    const en=c.dataset.cat.toLowerCase();
    const okCat=curCat==='全部'||c.dataset.cat===curCat;
    const okQ=!q||name.includes(q)||en.includes(q)||c.querySelector('.card-en').textContent.toLowerCase().includes(q);
    c.style.display=(okCat&&okQ)?'':'none';
  });
}
search.addEventListener('input',applyFilter);
catBtns.forEach(b=>b.addEventListener('click',()=>{
  catBtns.forEach(x=>x.classList.remove('active'));
  b.classList.add('active');curCat=b.dataset.cat;applyFilter();
}));
function openModal(id){
  const m=document.getElementById('m-'+id);
  if(!m)return;
  m.classList.add('open');m.setAttribute('aria-hidden','false');
  document.body.style.overflow='hidden';
}
function closeModal(m){m.classList.remove('open');m.setAttribute('aria-hidden','true');document.body.style.overflow='';}
cards.forEach(c=>c.addEventListener('click',()=>openModal(c.dataset.id)));
document.querySelectorAll('.modal').forEach(m=>{
  m.querySelectorAll('[data-close]').forEach(x=>x.addEventListener('click',()=>closeModal(m)));
  m.querySelectorAll('.chip').forEach(ch=>ch.addEventListener('click',e=>{e.stopPropagation();closeModal(m);openModal(ch.dataset.id);}));
});
document.addEventListener('keydown',e=>{if(e.key==='Escape'){document.querySelectorAll('.modal.open').forEach(closeModal);}});
