import re, hashlib

PATH = 'assets/app.js'
src = open(PATH, encoding='utf-8').read()
orig = src

def must(old, new, n=1):
    global src
    found = src.count(old)
    assert found == n, 'anchor x%d (expected %d): %r' % (found, n, old[:70])
    src = src.replace(old, new)

# ---- A1: engine state for flashes + drips -----------------------------------
must("var MAXD=220, intensity=0, target=0, bolt=0, boltNext=0;",
     "var MAXD=220, intensity=0, target=0, bolt=0, boltNext=0, flashes=[],flNext=2,drips=[];")

# ---- A2: blood blend factor + debug probe right after intensity telemetry ----
must("try{window.__monsoonIntensity=st;RumbleFX.setIntensity(st);}catch(e){}",
     "var bt=Math.max(0,(st-0.55)/0.45);/* blood tint 0..1 */\n      "
     "try{window.__monsoonIntensity=st;RumbleFX.setIntensity(st);}catch(e){}\n      "
     "window.__monsoonDbg=function(){return{st:intensity,fl:flashes.length,dr:drips.length};}")

# ---- A3: storm haze bottom shifts to blood-red as tint rises -----------------
must("hg.addColorStop(1,'rgba(30,10,10,'+(0.30*st)+')');",
     "hg.addColorStop(1,'rgba('+Math.round(30+46*bt)+',10,'+Math.round(10+8*bt)+','+(0.30*st)+')');")

# ---- A4: rain drops blend slate -> blood red ----------------------------------
must("        var a=d0.o*(0.75+0.45*st);\n"
     "        ctx.strokeStyle='rgba(203,213,225,'+a.toFixed(3)+')';",
     "        var a=d0.o*(0.75+0.45*st);\n"
     "        ctx.strokeStyle='rgba('+Math.round(203+22*bt)+','+Math.round(213-143*bt)+','+Math.round(225-145*bt)+','+a.toFixed(3)+')';")

# ---- A5: spawn/update gunfire each frame (before clearRect) -------------------
must("      bolt=Math.max(0,bolt-dt*2.2);\n      ctx.clearRect(0,0,W,H);",
     "      bolt=Math.max(0,bolt-dt*2.2);\n"
     "      /* distant gunfire: muzzle flashes + tracers, cadence scales with storm */\n"
     "      if(st>0.6){\n"
     "        flNext-=dt;\n"
     "        if(flNext<=0){\n"
     "          flNext=R(1.2,4)/(0.5+0.5*st);\n"
     "          var fx0=R(innerWidth*0.08,innerWidth*0.92),fy0=R(innerHeight*0.12,innerHeight*0.30);\n"
     "          flashes.push({x:fx0,y:fy0,ttl:0.11,max:0.11,r:R(26,64),tr:Math.random()<0.3?{x:fx0,y:fy0,vx:R(-1400,1400),vy:R(-260,260),ttl:0.2}:null});\n"
     "          try{RumbleFX.crack(fx0/innerWidth);}catch(e){}\n"
     "        }\n"
     "      }\n"
     "      for(var f8=flashes.length-1;f8>=0;f8--){var f9=flashes[f8];f9.ttl-=dt;\n"
     "        if(f9.tr){f9.tr.ttl-=dt;f9.tr.x+=f9.tr.vx*dt;f9.tr.y+=f9.tr.vy*dt;}\n"
     "        if(f9.ttl<=0)flashes.splice(f8,1);}\n"
     "      ctx.clearRect(0,0,W,H);")

# ---- A6: draw flashes + blood drips (before the embers block) -----------------
must("      /* embers only in gentle rain; storm hides them */",
     "      /* muzzle flash + tracer rendering */\n"
     "      for(i=0;i<flashes.length;i++){var f0=flashes[i];var fa=(f0.ttl/f0.max)*(0.55+0.45*Math.random());\n"
     "        var fg=ctx.createRadialGradient(f0.x,f0.y,0,f0.x,f0.y,f0.r);\n"
     "        fg.addColorStop(0,'rgba(254,243,199,'+(0.85*fa)+')');fg.addColorStop(0.35,'rgba(251,191,36,'+(0.35*fa)+')');fg.addColorStop(1,'rgba(251,191,36,0)');\n"
     "        ctx.fillStyle=fg;ctx.beginPath();ctx.arc(f0.x,f0.y,f0.r,0,6.283);ctx.fill();\n"
     "        ctx.fillStyle='rgba(255,255,255,'+(0.9*fa).toFixed(3)+')';ctx.beginPath();ctx.arc(f0.x,f0.y,2.5,0,6.283);ctx.fill();\n"
     "        if(f0.tr&&f0.tr.ttl>0){ctx.strokeStyle='rgba(253,230,138,'+(0.7*f0.tr.ttl/0.2).toFixed(3)+')';ctx.lineWidth=1.4;ctx.beginPath();ctx.moveTo(f0.tr.x,f0.tr.y);ctx.lineTo(f0.tr.x-f0.tr.vx*0.035,f0.tr.y-f0.tr.vy*0.035);ctx.stroke();}}\n"
     "      /* blood drips running down the glass at full storm */\n"
     "      if(st>0.75){while(drips.length<10)drips.push({x:R(0,innerWidth),y:R(-innerHeight,0),v:R(38,85),len:R(26,64),w:R(1.6,3),o:R(.4,.75)});}\n"
     "      else if(st<0.5)drips=[];\n"
     "      var da=Math.max(0,(st-0.75)/0.25);\n"
     "      for(i=0;i<drips.length;i++){var dp=drips[i];dp.y+=dp.v*dt;if(dp.y>innerHeight+70){dp.y=R(-120,-20);dp.x=R(0,innerWidth);}\n"
     "        if(da>0.01){var dca=da*dp.o;\n"
     "          ctx.strokeStyle='rgba(153,27,27,'+dca.toFixed(3)+')';ctx.lineWidth=dp.w;ctx.beginPath();ctx.moveTo(dp.x,dp.y-dp.len);ctx.lineTo(dp.x,dp.y);ctx.stroke();\n"
     "          ctx.fillStyle='rgba(127,29,29,'+(dca*0.9).toFixed(3)+')';ctx.beginPath();ctx.arc(dp.x,dp.y,dp.w*0.9,0,6.283);ctx.fill();}}\n"
     "      /* embers only in gentle rain; storm hides them */")

# ---- A7: RumbleFX.crack — synthesized distant gunshot --------------------------
must("    RumbleFX.dbg=function(){try{return {on:RumbleFX.on,ctx:actx?actx.state:null,gain:gain?+gain.gain.value.toFixed(4):null};}catch(e){return {err:String(e)};}};",
     "    RumbleFX.dbg=function(){try{return {on:RumbleFX.on,ctx:actx?actx.state:null,gain:gain?+gain.gain.value.toFixed(4):null};}catch(e){return {err:String(e)};}};\n"
     "    /* distant gunshot: filtered noise crack + low thump. Plays only while\n"
     "       the rumble toggle is on (same opt-in as the storm bed). */\n"
     "    RumbleFX.crack=function(pan){\n"
     "      try{\n"
     "        if(!RumbleFX.on||!actx||actx.state!=='running')return;\n"
     "        var t=actx.currentTime,dur=0.28;\n"
     "        var buf=actx.createBuffer(1,Math.floor(actx.sampleRate*dur),actx.sampleRate);\n"
     "        var ch=buf.getChannelData(0);\n"
     "        for(var i=0;i<ch.length;i++){ch[i]=(Math.random()*2-1)*Math.exp(-i/(actx.sampleRate*0.035));}\n"
     "        var src=actx.createBufferSource();src.buffer=buf;\n"
     "        var f=actx.createBiquadFilter();f.type='lowpass';f.frequency.value=900;f.Q.value=0.7;\n"
     "        var g=actx.createGain();g.gain.value=0.22+Math.random()*0.1;\n"
     "        src.connect(f);f.connect(g);\n"
     "        var p=actx.createStereoPanner?actx.createStereoPanner():null;\n"
     "        if(p){p.pan.value=Math.max(-1,Math.min(1,((pan||0.5)-0.5)*1.2));g.connect(p);p.connect(actx.destination);}\n"
     "        else{g.connect(actx.destination);}\n"
     "        src.start(t);\n"
     "        var o=actx.createOscillator(),og=actx.createGain();\n"
     "        o.type='sine';o.frequency.setValueAtTime(140,t);o.frequency.exponentialRampToValueAtTime(50,t+0.12);\n"
     "        og.gain.setValueAtTime(0.28,t);og.gain.exponentialRampToValueAtTime(0.001,t+0.18);\n"
     "        o.connect(og);og.connect(actx.destination);o.start(t);o.stop(t+0.2);\n"
     "      }catch(e){}\n"
     "    };")

# ---- A8: toggle labels now cover gunfire audio ---------------------------------
must("btn.setAttribute('aria-label','Toggle July monsoon rumble');",
     "btn.setAttribute('aria-label','Toggle July storm sound (rumble + distant gunfire)');")
must("btn.title='July monsoon rumble - click to enable';",
     "btn.title='July storm sound: rain rumble + distant gunfire - click to enable';", n=2)
must("btn.title='July monsoon rumble playing - click to stop';",
     "btn.title='July storm sound playing - click to stop';")

open(PATH, 'w', encoding='utf-8').write(src)
sha = hashlib.sha256(src.encode('utf-8')).hexdigest()
print('PATCH OK | new sha12:', sha[:12])
print('checks:', 'crack' in src, src.count('RumbleFX.crack'), src.count('flashes.push'))
