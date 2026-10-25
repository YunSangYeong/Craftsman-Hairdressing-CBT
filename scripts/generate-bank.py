"""Deterministic original study bank. No third-party questions are copied.
800 numerical scenarios in 8 families are NOT 800 independent concepts.
Uses Decimal ROUND_HALF_UP; independent TypeScript evaluators test answers.
"""
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP
import json,random,csv,hashlib
ROOT=Path(__file__).resolve().parents[1]
rng=random.Random(20261025)
D=Decimal
URL='https://github.com/YunSangYeong/Craftsman-Hairdressing-CBT/blob/main/docs/question-review.md'
bank=[]
def fmt(n):return format(D(n).normalize(),'f')
def add(id,subject,topic,question,choices,correct,explanation,family=None,calculation=None):
 assert len(set(choices))==4 and correct in choices
 rng.shuffle(choices)
 q=dict(id=id,subject=subject,topic=topic,question=question,choices=choices,answer=choices.index(correct)+1,explanation=explanation,difficulty='중' if family else '하',year=None,session=None,type='original',sourceUrl=URL,verificationStatus='reviewed',reviewNote=('자체 제작 계산 조건 변형. 문제의 가정에 한정한 수학 연습이며 실제 약제·소독·시술 지침이 아님. Decimal 계산과 별도 TypeScript 식으로 재검산. ' if family else 'AI 일반지식 기반 자체 제작. 내부 문장·단일 정답 검토. ' )+'외부 전문가 검수 및 공식 출제기준 대조 미완료. 링크는 작성·검토 기록이며 외부 정답 증빙이 아님.',version='main',rights='이 프로젝트 자체 제작 · CC BY 4.0 · Craftsman-Hairdressing-CBT contributors')
 if family:q.update(family=family,calculation=calculation)
 bank.append(q)
subject='';counter={}
for line in (ROOT/'scripts/concepts.tsv').read_text().splitlines():
 if line.startswith('# '):subject=line[2:];continue
 if not line.strip():continue
 topic,question,correct,*rest=line.split('|');wrong=rest[:3];explanation=rest[3]
 counter[subject]=counter.get(subject,0)+1
 code=['헤어스타일 연출','두피·모발 관리','피부·화장품','공중위생·안전'].index(subject)+1
 add(f'HAIR-C{code}-{counter[subject]:03}',subject,topic,question,[correct,*wrong],correct,explanation)
def calc(family,subject,topic,inputs,result,unit,question,explanation):
 result=D(result).quantize(D('.01'),rounding=ROUND_HALF_UP)
 assert result>0
 # Multiplicative distractors remain positive and distinct, also at small values.
 options=[fmt(result)+unit]+[fmt(result*k)+unit for k in rng.sample([D('.25'),D('.5'),D('.75'),D('1.25'),D('1.5'),D('1.75'),D('2'),D('3')],3)]
 seq=sum(q.get('family')==family for q in bank)+1
 add(f'HAIR-{family}-{seq:03}',subject,topic,question,options,options[0],explanation+f' 최종 답: {fmt(result)}{unit}. 소수 셋째 자리에서 반올림하며 문제의 가정만 적용합니다.',family,dict(kind=family,values=[float(x) for x in inputs],result=float(result),unit=unit,precision=2))
for target in range(1,6):
 for total in range(20,401,20):
  stock=D(target)*total/10
  common=f'학습용 희석 계산에서 원액 10%(v/v)와 물을 사용해 {target}%(v/v) 용액 {total}mL를 만든다. 부피는 합산되고 손실은 없다고 가정한다. 실제 소독 농도 권장이 아니다. '
  calc('stock','공중위생·안전','희석 수학', [10,target,total],stock,'mL',common+'필요한 원액 부피는?',f'C₁V₁=C₂V₂이므로 원액은 {target}×{total}÷10={fmt(stock)}mL이다.')
  calc('water','공중위생·안전','희석 수학',[10,target,total],D(total)-stock,'mL',common+'첨가할 물의 부피는?',f'원액은 {target}×{total}÷10={fmt(stock)}mL. 물은 총량에서 원액을 뺀 {total}−{fmt(stock)}={fmt(D(total)-stock)}mL이다.')
for concentration in [10,20,30,40,50]:
 for total in range(100,2001,100):
  v=D(concentration)*10/total
  calc('final','공중위생·안전','농도 수학',[concentration,10,total],v,'%',f'학습용 부피 농도 계산이다. {concentration}%(v/v) 원액 10mL에 물을 넣어 최종 {total}mL로 만들었다. 부피 합산·용질 손실 없음 가정에서 최종 농도는? 실제 소독 기준이 아니다.',f'용질 상당 부피는 {concentration}÷100×10mL. 최종 백분율은 원액 농도×원액 부피÷최종 부피={concentration}×10÷{total}%.')
for concentration in range(1,11):
 for total in range(50,501,50):
  v=D(concentration)*total/100
  calc('solute','피부·화장품','질량 백분율',[concentration,total],v,'g',f'제형 계산 연습이다. 질량 백분율 {concentration}%(w/w)인 용액 {total}g에 포함된 용질 질량은? 다른 성분은 없고 손실도 없다고 가정한다.',f'질량%=용질 질량÷용액 전체 질량×100. 따라서 용질 질량은 {total}×{concentration}÷100={fmt(v)}g이다.')
for highmass in range(10,30):
 for lowmass in range(10,51,10):
  v=(D(6)*highmass+D(2)*lowmass)/(highmass+lowmass)
  calc('blend','피부·화장품','질량 혼합 수학',[6,highmass,2,lowmass],v,'%',f'제형 수학 연습으로 6%(w/w) 용액 {highmass}g과 2%(w/w) 용액 {lowmass}g을 섞는다. 반응·증발·손실이 없다면 혼합액의 질량 백분율은? 실제 제품 혼합 권장이 아니다.',f'총 용질 질량은 (6×{highmass}+2×{lowmass})÷100g이고 전체 질량은 {highmass+lowmass}g이다. 질량 백분율은 (6×{highmass}+2×{lowmass})÷{highmass+lowmass}%이다.')
for ratio in [D(1),D('1.5'),D(2),D('2.5')]:
 for mass in range(20,141,5):
  calc('developer','헤어스타일 연출','주어진 배합비 수학',[mass,ratio],D(mass)*ratio,'g',f'가상 제품의 지침이 염모제:산화제를 질량비 1:{fmt(ratio)}로 지정했다고 가정한다. 염모제 {mass}g에 필요한 산화제 질량은? 이 비율은 실제 제품의 권장치가 아니다.',f'문제에서 지정한 질량비를 적용한다. 산화제=염모제 질량×비율={mass}×{fmt(ratio)}={fmt(D(mass)*ratio)}g이다.')
  calc('batch','헤어스타일 연출','주어진 조제 총량',[mass,ratio],D(mass)*(1+ratio),'g',f'가상 지침에서 염모제:산화제 질량비를 1:{fmt(ratio)}로 정했다. 염모제 {mass}g과 필요한 산화제를 전량 혼합할 때 총 질량은? 손실이 없으며 실제 제품 혼합 권장은 아니다.',f'산화제={mass}×{fmt(ratio)}={fmt(D(mass)*ratio)}g. 총 질량={mass}+{fmt(D(mass)*ratio)}={fmt(D(mass)*(1+ratio))}g이다.')
for initial in range(20,40):
 for removed in range(1,6):
  calc('length','헤어스타일 연출','길이 측정 연습',[initial,removed],D(initial-removed),'cm',f'건조 상태가 일정하고 수축·신장은 없다고 가정한다. 기준점부터 길이가 {initial}cm인 한 가닥의 끝 {removed}cm를 잘랐다. 남은 길이는?',f'길이 변화 조건이 없으므로 남은 길이=원래 길이−잘라낸 길이={initial}−{removed}={initial-removed}cm이다. 실제 커트에서는 수분과 곱슬 수축 등을 별도로 고려한다.')
assert len(bank)==1000,len(bank)
assert len({q['id'] for q in bank})==1000
(ROOT/'src/data/questions.json').write_text(json.dumps(bank,ensure_ascii=False,indent=2)+'\n')
# The template remains pending even though copied from an internally reviewed example.
example=dict(bank[0],id='IMPORT-EXAMPLE-001',question='양식 예제: '+bank[0]['question'],verificationStatus='pending',reviewNote='양식 예제. 실제 등록 전 정답·해설·권한을 검토하세요.')
(ROOT/'public/templates/questions.json').write_text(json.dumps([example],ensure_ascii=False,indent=2)+'\n')
flat={k:v for k,v in example.items() if k!='choices'}
flat.update({f'choice{i+1}':v for i,v in enumerate(example['choices'])})
with (ROOT/'public/templates/questions.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(flat),lineterminator="\n");w.writeheader();w.writerow(flat)
print('Generated:',len(bank),'concepts:',len([q for q in bank if not q.get('family')]),'families:',len({q['family'] for q in bank if q.get('family')}))
print('SHA256',hashlib.sha256((ROOT/'src/data/questions.json').read_bytes()).hexdigest())
