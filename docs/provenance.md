# 재사용 코드와 표준 출처

- 기준 앱: `YunSangYeong/electrician-cbt` 커밋 `b9a682ccff1b460334b78d5bfad9375b7ec4fbb6`.
- `src/App.tsx`, `src/styles.css`, `src/model.ts`, React 진입점, Vite·TypeScript·테스트 설정, package/lockfile, 기능 테스트와 Pages workflow를 해당 커밋에서 실제 복사해 수정했다.
- 표준 스킬 폴더: 원본 커밋 `76b990b8720adfa85c22a0a8f699b17094aa357b`의 `.agents/skills/cbt-site-standard/` 전체를 복사했다. 스킬 버전은 1.4.0이며 루트 AGENTS.md에서 연결한다. 계정 공통 스킬 설치를 의미하지 않는다.
- 원본 MIT 저작권 고지는 LICENSE에 보존했다. 전기기능사 문제 JSON·생성 스크립트·개인 기록·빌드 산출물은 복사하지 않았다. 새 문제 원고·생성기·검증은 대상 저장소 전용이다.
- 원본 저장소는 읽기용 `/tmp` 복사본으로만 접근했으며 수정·푸시·배포하지 않았다.

주요 변경은 자격증 설정 일원화, 고유 저장 namespace, 학습 영역과 출제량 분리, 신규 은행과 입력 양식, 상단 면책 배너 제거, 작은 메뉴의 독립 스크롤과 실제 터치·휠 회귀 검사이다. 실전·랜덤 Space 이동과 포커스, 저장 손상 보존, 시험 절대 시간·자동 제출, 오답과 북마크 기능은 기준 코드를 재사용했다.
