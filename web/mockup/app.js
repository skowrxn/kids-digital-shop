(function(){
/* odsłony: rootMargin -12%, żeby reveal kończył się tam, gdzie zaprojektowany */
(function(){
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var targets = document.querySelectorAll('.rise,.rise-l,.rise-r,.rise-pop');
  if(reduce){ targets.forEach(function(el){el.classList.add('is-in');}); }
  else{
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('is-in'); io.unobserve(e.target);} });
    },{rootMargin:'-12% 0px -12% 0px'});
    targets.forEach(function(el){io.observe(el);});
  }

  /* scroll jest jedynym zegarem: warstwy heroa liczone od środka viewportu */
  var layers = document.querySelectorAll('[data-scrub]');
  if(layers.length && !reduce){
    var ticking=false;
    function frame(){
      var mid = window.innerHeight/2;
      layers.forEach(function(el){
        var r = el.getBoundingClientRect();
        var d = ((r.top + r.height/2) - mid) / window.innerHeight; /* -1..1 */
        var k = parseFloat(el.dataset.scrub);
        el.style.translate = '0 ' + (d*k).toFixed(2) + 'px';
      });
      ticking=false;
    }
    function onScroll(){ if(!ticking){ ticking=true; requestAnimationFrame(frame); } }
    window.addEventListener('scroll',onScroll,{passive:true});
    window.addEventListener('resize',onScroll);
    frame();
  }

  /* "chcę..." — router problemów */
  var wants = document.querySelectorAll('[data-want]');
  var ansBox = document.getElementById('want-answer');
  var ansData = document.getElementById('want-data');
  if(wants.length && ansBox && ansData){
    var data = JSON.parse(ansData.textContent);
    function pick(i){
      wants.forEach(function(w){
        w.setAttribute('aria-pressed', w.dataset.want === String(i) ? 'true' : 'false');
      });
      var d = data[i];
      var pickHtml = d.name
        ? '<div class="answer__pick"><span class="answer__cover">' + d.cover + '</span>' +
          '<span><span class="answer__name">' + d.name + '</span>' +
          '<span class="answer__price">' + d.price + '</span></span>' +
          '<a class="btn btn--primary" href="' + d.href + '">' + d.cta + '</a></div>'
        : '<div class="answer__pick"><a class="btn btn--primary" href="' + d.href + '">' + d.cta + '</a></div>';
      ansBox.innerHTML = '<p class="answer__line">' + d.line + '</p>' + pickHtml;
    }
    wants.forEach(function(w){
      w.addEventListener('click', function(){ pick(Number(w.dataset.want)); });
    });
    pick(0);
  }

  /* podglad materialu */
  var pth = document.querySelectorAll('[data-preview]');
  var pstage = document.getElementById('preview-stage');
  if(pth.length && pstage){
    pth.forEach(function(t){
      t.addEventListener('click', function(){
        pth.forEach(function(x){ x.setAttribute('aria-selected','false'); });
        t.setAttribute('aria-selected','true');
        pstage.innerHTML = t.querySelector('svg').outerHTML;
      });
    });
  }

  /* mega menu na hover + klawiatura */
  var wrap = document.querySelector('.catwrap');
  if(wrap){
    var mega = wrap.querySelector('.mega');
    var links = wrap.querySelectorAll('[data-mega]');
    var closeT;
    function open(key){
      clearTimeout(closeT);
      links.forEach(function(l){
        if(l.dataset.mega===key){ l.setAttribute('data-open',''); } else { l.removeAttribute('data-open'); }
      });
      mega.querySelectorAll('.mega__panel').forEach(function(p){
        if(p.dataset.cat===key){ p.setAttribute('data-active',''); } else { p.removeAttribute('data-active'); }
      });
      mega.setAttribute('data-show','');
    }
    function close(){
      closeT = setTimeout(function(){
        mega.removeAttribute('data-show');
        links.forEach(function(l){ l.removeAttribute('data-open'); });
      }, 140);
    }
    links.forEach(function(l){
      l.addEventListener('mouseenter', function(){ open(l.dataset.mega); });
      l.addEventListener('focus', function(){ open(l.dataset.mega); });
      l.addEventListener('mouseleave', close);
    });
    mega.addEventListener('mouseenter', function(){ clearTimeout(closeT); });
    mega.addEventListener('mouseleave', close);
    wrap.addEventListener('keydown', function(e){ if(e.key==='Escape'){ clearTimeout(closeT); 
      mega.removeAttribute('data-show'); links.forEach(function(l){l.removeAttribute('data-open');}); } });
  }

  /* zakladki wieku */
  var tabs = document.querySelectorAll('[data-tab]');
  if(tabs.length){
    tabs.forEach(function(t){
      t.addEventListener('click', function(){
        var group = t.closest('[data-tabs]');
        group.querySelectorAll('[data-tab]').forEach(function(x){
          x.setAttribute('aria-selected', x === t ? 'true' : 'false');
        });
        group.parentNode.querySelectorAll('.tabpanel').forEach(function(p){
          p.hidden = (p.dataset.panel !== t.dataset.tab);
        });
      });
    });
  }

  /* galeria produktu */
  var thumbs = document.querySelectorAll('[data-shot]');
  var stage  = document.getElementById('shot-stage');
  if(thumbs.length && stage){
    thumbs.forEach(function(t){
      t.addEventListener('click',function(){
        thumbs.forEach(function(x){x.setAttribute('aria-selected','false');});
        t.setAttribute('aria-selected','true');
        stage.innerHTML = t.querySelector('svg').outerHTML;
      });
    });
  }
})();
})();