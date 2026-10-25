# 미용사(일반) 필기 CBT

전기기능사 CBT 표준 v1.4.0의 고정 기준 코드를 재사용한 한국어 React·TypeScript·Vite 정적 학습 앱입니다. 실전 모의시험, 랜덤 학습, 오답노트, 북마크, 통계, JSON/CSV 로컬 문제 등록과 기록 백업을 제공합니다. 모바일과 PC를 지원하며 두 모드에서 답안 선택 후 Space로 다음 문제에 이동합니다.

현재 **공식 시험 규칙 검증과 공개 배포는 미완료**입니다. Q-Net 접근은 네트워크 403, 최초 Pages 사전 조회는 HTTP 404로 막혔습니다. 실제 확인 범위와 남은 일은 아래 문서에 구분했습니다.

- [CBT 표준 스킬](.agents/skills/cbt-site-standard/SKILL.md), [개발 지침](AGENTS.md)
- [시험 규칙과 공식 확인 상태](docs/exam-rules.md)
- [문항 작성·내부 검토 범위](docs/question-review.md)
- [기준 코드·라이선스 출처](docs/provenance.md)
- [인수 검사와 배포 기록](docs/validation.md)

## 실행과 검증

Node.js 24.19.0을 `.node-version`에 고정했습니다. 이 클라우드의 기존 체크아웃을 사용하며 별도 worktree는 필요 없습니다.

```bash
cd /workspace/Craftsman-Hairdressing-CBT
npm ci --cache /tmp/cbt-npm-cache --no-audit --no-fund
npm run dev -- --port 5173 --strictPort
```

기본 경로는 `/Craftsman-Hairdressing-CBT/`입니다. 별도 서버·로그인·DB·유료 API·앱 비밀키는 필요 없습니다.

```bash
npm test
npm run build
npm run test:e2e
```

빌드는 TypeScript 검사를 포함합니다. Playwright는 명시한 `PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH`, 설치된 `/usr/bin/chromium`, Playwright Chromium 순으로 사용합니다. 이 클라우드에서는 기존 시스템 Chromium으로 검증했습니다. 새 로컬 환경에 브라우저가 없으면 `npx playwright install --with-deps chromium`을 실행합니다. CI는 이 설치를 수행합니다. PC Chromium과 Pixel 7 에뮬레이션이며 실기기 Safari 검증은 아닙니다.

## 문제은행과 시험 설정

현재 기본 JSON에는 ID·정규화 본문/보기 중복을 제거한 **1,000문항**이 있습니다. 모두 자체 제작으로 원문 기출·복원은 0개입니다. 구성은 개념 문항 200개와 **계산 8유형 × 조건 100개 = 800개 변형**입니다. 1,000개의 독립 개념이나 기출을 확보한 것이 아닙니다.

| 학습 영역 | 문항 수 |
| --- | ---: |
| 헤어스타일 연출 | 350 |
| 두피·모발 관리 | 50 |
| 피부·화장품 | 250 |
| 공중위생·안전 | 350 |

AI 일반지식 기반 작성과 저자 내부 문장·정답 검토, 별도 수학 재계산을 수행했습니다. 외부 전문가 검수와 공식 출제기준 대조는 미완료입니다. 계산 비중은 실제 필기시험 분포를 재현하지 않습니다. 약제·소독 농도는 문제의 가상 수학 조건이며 실제 사용 권장이 아닙니다. 문항 해설과 문제은행 관리에서 검토 범위를 볼 수 있습니다.

학습 설정은 `src/qualification-profile.json`에서 관리합니다. 잠정적으로 60문항·60분·4지선다·100점 만점 60점 합격·과락 없음이며 공식 원문 확인 대기 상태입니다. 학습 영역별 24/12/12/12 배분은 앱 자체 정책입니다. 미응답은 오답에 포함됩니다.

원고와 시드는 저장되어 있습니다. 의도적으로 데이터를 다시 만들 때만 `python3 scripts/generate-bank.py`를 실행합니다. 이 명령은 기본 JSON과 입력 양식을 재생성하므로 원고 변경과 기존 ID를 먼저 확인하세요.

## 기록과 개인정보

`craftsman-hairdressing-cbt:v1` 이름으로 이 브라우저의 localStorage에 기록합니다. 동일 소유자의 다른 Pages 프로젝트와 저장 키를 구분합니다. 시험은 시작·종료 절대 시각을 저장하므로 새로고침으로 시간이 늘지 않습니다. 최근 응답 5,000개·시험 30회까지 보관하고 통계도 이 보관 범위 기준입니다.

기록 백업은 JSON 다운로드입니다. 백업 복원 UI는 없습니다. 손상된 기록은 자동 덮어쓰지 않고 원본 백업을 제공합니다. 저장 공간 제한이나 차단 시 실제 경고를 표시합니다. 초기화는 확인 후 사용자 데이터만 지우며 기본 문제은행은 유지합니다. iframe·시크릿 모드·다른 기기·다른 origin에서는 저장 접근이나 기록 공유에 제한이 있을 수 있습니다.

가져오기는 현재 브라우저의 로컬 은행에만 등록합니다. 모든 문항은 검증 대기로 들어가며 사용자가 근거를 기록하고 승인하기 전에는 출제하지 않습니다. GitHub 공용 데이터에 자동 게시되지 않습니다.

## 배포

사용자는 처음 GitHub Pages 배포까지 요청했으나, 이후 GitHub 배포는 직접 처리한다고 지정했습니다. 구현은 `feat/hairdressing-cbt` 브랜치에 보존하며 에이전트는 main 반영·배포를 실행하지 않습니다. `.github/workflows/pages.yml`은 main push → 단위·빌드·PC/모바일 검사 → Pages 배포, PR은 검증만 수행하도록 준비했습니다. 첫 배포 사전 조회가 HTTP 404였으므로 표준의 첫 차단 시 중단 규칙에 따라 main 자동 배포를 시작하지 않았습니다. 재실행·우회 배포·배포 유발 추가 푸시도 하지 않습니다.

예상 기본 주소: `https://yunsangyeong.github.io/Craftsman-Hairdressing-CBT/` (게시·접속 확인한 주소가 아닙니다). 우선 저장소 **Settings → Pages → Source: GitHub Actions** 설정 상태를 확인해 주세요. Pages API 404는 미설정뿐 아니라 접근 권한 문제도 가능하므로 원인은 확정하지 않았습니다. 실제 CI·공개 게시 성공을 주장하지 않습니다.

애플리케이션의 원본 MIT 고지를 보존하고 새 자체 제작 데이터는 CC BY 4.0으로 구분했습니다. [LICENSE](LICENSE)를 확인하세요. 비공식 학습 서비스이며 Q-Net·한국산업인력공단과 무관합니다.
