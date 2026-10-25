import { readFile } from "node:fs/promises";
import { expect, test, type Page } from "@playwright/test";
const key = "craftsman-hairdressing-cbt:v1";
async function openMenu(page: Page) {
  await page.getByRole("button", { name: "메뉴 열기" }).click();
  await expect(page.locator(".sidebar")).toHaveClass(/open/);
  // Wait for the actual CSS transition, before calculating gesture coordinates.
  await page.locator(".sidebar").evaluate(el => Promise.all(el.getAnimations().map(a => a.finished)));
}
async function inViewport(page: Page, text: string) {
  const button=page.locator(".sidebar").getByRole("button",{name:text,exact:true});
  await expect(button).toBeInViewport({ratio:1});
}
for(const viewport of [{width:390,height:480},{width:740,height:360}]) {
  test(`작은 메뉴 실제 휠 아래·위 이동 ${viewport.width}×${viewport.height}·글자 확대`, async ({page})=>{
    await page.setViewportSize(viewport);
    await page.goto("");
    // Larger actual font dimensions in menu, not a programmatic scroll.
    await page.addStyleTag({content:'.sidebar nav button {font-size:18px; min-height:56px} .sidebar-bottom button {font-size:17px}'});
    await openMenu(page);
    const menu=page.locator('.sidebar');
    const metrics=await menu.evaluate(el=>({scroll:el.scrollHeight,height:el.clientHeight}));
    expect(metrics.scroll).toBeGreaterThan(metrics.height);
    const background=await page.evaluate(()=>scrollY);
    await page.mouse.move(120,viewport.height/2);
    await page.mouse.wheel(0,1800);
    await expect.poll(()=>menu.evaluate(el=>el.scrollTop)).toBeGreaterThan(0);
    await inViewport(page,'학습 기록 백업');
    await inViewport(page,'데이터 초기화');
    await page.mouse.wheel(0,1000);
    await page.waitForTimeout(150);
    expect(await page.evaluate(()=>scrollY)).toBe(background);
    await page.mouse.wheel(0,-3000);
    await expect.poll(()=>menu.evaluate(el=>el.scrollTop)).toBe(0);
    await inViewport(page,'학습 대시보드');
    await menu.getByRole('button',{name:'학습 대시보드',exact:true}).click();
    await expect(menu).not.toHaveClass(/open/);
    await expect(page.getByRole('heading',{name:'미용사(일반) 필기 CBT',exact:true})).toBeVisible();
  });
  test(`모바일 실제 터치 아래·위 이동 ${viewport.width}×${viewport.height}`, async ({page,isMobile})=>{
    test.skip(!isMobile,'터치 가능한 Pixel 7 에뮬레이션에서 실행');
    await page.setViewportSize(viewport);
    await page.goto('');
    await openMenu(page);
    const menu=page.locator('.sidebar');
    const cdp=await page.context().newCDPSession(page);
    const swipe=async (down:boolean)=>{
      const top=90, bottom=viewport.height-50;
      const start=down?bottom:top, end=down?top:bottom;
      await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:120,y:start}]});
      for(let i=1;i<=14;i++){
        await cdp.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x:120,y:start+(end-start)*i/14}]});
        await page.waitForTimeout(18);
      }
      await cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});
      await page.waitForTimeout(250);
    };
    const bg=await page.evaluate(()=>scrollY);
    for(let i=0;i<5;i++) await swipe(true);
    await expect.poll(()=>menu.evaluate(el=>el.scrollTop)).toBeGreaterThan(0);
    await inViewport(page,'학습 기록 백업');
    await inViewport(page,'데이터 초기화');
    expect(await page.evaluate(()=>scrollY)).toBe(bg);
    for(let i=0;i<5;i++) await swipe(false);
    await expect.poll(()=>menu.evaluate(el=>el.scrollTop)).toBe(0);
    await inViewport(page,'학습 대시보드');
    await menu.getByRole('button',{name:'학습 대시보드',exact:true}).tap();
    await expect(menu).not.toHaveClass(/open/);
  });
}
test('모든 학습 화면에 상단 상시 안내 없음·저장 실패 경고 보존',async({page})=>{
  await page.goto('');
  const check=async()=>{
    await expect(page.locator('main .criteria-note')).toHaveCount(0);
    for (const notice of await page.locator('main .notice:not([role="alert"])').all())
      await expect(notice).not.toContainText(/비공식|검증 대기|잠정|기출 미제공|출제기준 대조/);
    await expect(page.locator('main')).not.toContainText(/공식 출제기준 대조 대기|기출 미제공|잠정 규칙/);
  };
  for(const name of ['실전 모의시험','랜덤 문제풀이','오답노트','북마크','학습 통계','학습 대시보드']){
    if(await page.getByRole('button',{name:'메뉴 열기'}).isVisible())await openMenu(page);
    await page.getByRole('navigation').getByRole('button',{name,exact:true}).click();
    await check();
  }
  await page.getByRole('button',{name:'모의시험 시작하기',exact:true}).click();await check();
  await page.getByRole('button',{name:'시험 종료 및 제출'}).click();
  await page.getByRole('button',{name:'제출하고 결과 보기'}).click();await check();
  await page.addInitScript(()=>{
    Storage.prototype.setItem=function(){throw new DOMException('quota','QuotaExceededError')};
  });
  await page.reload();
  await expect(page.getByRole('alert')).toContainText('기록을 저장하지 못했습니다');
  await page.getByRole('button',{name:'문제풀이 시작하기'}).click();
  await page.locator('.choices button').first().click();
  await expect(page.locator('.explanation')).toBeVisible();
  await expect(page.getByRole('alert')).toContainText('백업');
});
test('기록 백업 다운로드와 초기화 취소·기본은행 유지',async({page},testInfo)=>{
  await page.goto('');
  if(await page.getByRole('button',{name:'메뉴 열기'}).isVisible()) await openMenu(page);
  const downloadPromise=page.waitForEvent('download');
  await page.getByRole('button',{name:'학습 기록 백업',exact:true}).click();
  const download=await downloadPromise;
  expect(download.suggestedFilename()).toBe('hairdressing-study-backup.json');
  const path=testInfo.outputPath('study-backup.json');
  await download.saveAs(path);
  const backup=JSON.parse(await readFile(path,'utf8'));
  expect(backup.schema).toBe(1);expect(backup.version).toBe('main');
  await page.getByRole('button',{name:'데이터 초기화',exact:true}).click();
  await page.getByRole('button',{name:'돌아가기',exact:true}).click();
  await expect(page.getByRole('dialog')).toHaveCount(0);
  if(await page.locator('.sidebar').evaluate(el=>el.classList.contains('open')))
    await page.getByRole('button',{name:'메뉴 닫기'}).click({position:{x:page.viewportSize()!.width-15,y:100}});
  await expect(page.locator('.bank-summary')).toContainText('등록 1000문항');
  expect(await page.evaluate(k=>JSON.parse(localStorage.getItem(k)!).imported.length,key)).toBe(0);
});
