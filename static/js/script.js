document.addEventListener('click', function(e){const el=e.target.closest('[data-confirm]');if(el&&!confirm(el.dataset.confirm)){e.preventDefault();}});
setTimeout(()=>document.querySelectorAll('.alert').forEach(a=>a.remove()),5000);
