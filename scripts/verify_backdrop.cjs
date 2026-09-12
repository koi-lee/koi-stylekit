// Real pointer interactions against a static gallery; mobile is an emulated viewport.
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const output=process.env.OUTPUT_DIR||'outputs/backdrop';
(async()=>{
 fs.mkdirSync(output,{recursive:true});
 const browser=await chromium.launch({channel:'chrome'});
 const results=[];
 try{
  for(const width of [1280,390]){
   const context=await browser.newContext({viewport:{width,height:900},hasTouch:width===390});
   const page=await context.newPage();const errors=[];
   page.on('pageerror',e=>errors.push(e.message));
   await page.goto(process.env.GALLERY_URL||'http://127.0.0.1:4347/dist/');
   const card=page.locator('#cards .card').nth(3);
   const detailOpener=card.getByRole('button',{name:/^查看.+详情$/});
   async function check(dialogId,opener,contentSelector){
    const dialog=page.locator('#'+dialogId);
    await opener.scrollIntoViewIfNeeded();
    const before=await page.evaluate(()=>({x:scrollX,y:scrollY,style:document.body.style.cssText}));
    await opener.click();await page.locator('#'+dialogId+'[open]').waitFor();
    const box=await dialog.boundingBox();const outside={x:2,y:450};
    assert(box.x>outside.x,'outside point is on the backdrop');
    assert.equal(await page.evaluate(()=>document.body.style.position),'fixed');
    // Internal padding and text/image must not dismiss.
    await page.mouse.click(box.x+2,box.y+box.height/2);
    assert(await dialog.evaluate(e=>e.open));
    const content=page.locator(contentSelector);await content.click();
    assert(await dialog.evaluate(e=>e.open));
    const inside=await content.boundingBox();
    await page.mouse.move(inside.x+10,inside.y+10);await page.mouse.down();
    await page.mouse.move(outside.x,outside.y,{steps:10});await page.mouse.up();
    assert(await dialog.evaluate(e=>e.open),'inside-to-outside drag must not dismiss');
    await page.mouse.move(outside.x,outside.y);await page.mouse.down();
    await page.mouse.move(box.x+5,box.y+box.height/2,{steps:10});await page.mouse.up();
    assert(await dialog.evaluate(e=>e.open),'outside-to-inside drag must not dismiss');
    await page.mouse.click(outside.x,outside.y,{button:'right'});
    assert(await dialog.evaluate(e=>e.open),'secondary click must not dismiss');
    await page.screenshot({path:`${output}/${dialogId}-${width}.png`});
    if(width===390)await page.touchscreen.tap(outside.x,outside.y);
    else await page.mouse.click(outside.x,outside.y);
    assert.equal(await dialog.evaluate(e=>e.open),false,'backdrop click dismisses');
    assert.deepEqual(await page.evaluate(()=>({x:scrollX,y:scrollY,style:document.body.style.cssText})),before);
    assert(await opener.evaluate(e=>document.activeElement===e));
    for(const method of ['outside','Escape','close']){
     await opener.click();await page.locator('#'+dialogId+'[open]').waitFor();
     if(method==='outside')await page.mouse.click(2,450);
     else if(method==='Escape')await page.keyboard.press('Escape');
     else await page.click(dialogId==='detail'?'#closeDetail':'#closePreview');
     assert.equal(await dialog.evaluate(e=>e.open),false);
     assert(await opener.evaluate(e=>document.activeElement===e));
     assert.equal(await page.evaluate(()=>document.body.style.position),'');
    }
    results.push({width,dialogId,passed:true});
   }
   await check('detail',detailOpener,'#detailBody img');
   await page.getByRole('button',{name:'选择双色孔版',exact:true}).click();
   await page.fill('#subject','绿色的书与猫');await page.fill('#caption','阅读时光');
   await page.selectOption('#colorPolicy','style');
   await check('preview',page.locator('#previewTrigger'),'#promptText');
   assert.equal(await page.inputValue('#subject'),'绿色的书与猫');
   assert.equal(await page.inputValue('#caption'),'阅读时光');
   assert.equal(await page.inputValue('#colorPolicy'),'style');
   assert.deepEqual(errors,[]);
   console.log(width,'detail/preview backdrop, internal clicks, drags, touch, repeat, focus/scroll/form preservation passed');
   await context.close();
  }
  fs.writeFileSync(`${output}/report.json`,JSON.stringify({url:process.env.GALLERY_URL||'http://127.0.0.1:4347/dist/',results},null,2)+'\n');
 }finally{await browser.close();}
})().catch(error=>{console.error(error);process.exit(1)});
