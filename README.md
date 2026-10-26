# HEX HAVEN PR 플레이 테스트

정식 저장소와 정식 Pages 설정을 변경하지 않는 별도 GitHub Pages 저장소용 패키지입니다.

- pr-3/는 nivesmik/hex-haven PR #3, 커밋 17dee39c954f88cab2715a168d316143d9f5b37a의 게임입니다.
- /pr-3/?fresh=1은 기본 모드·시드 202607의 새 실험을 시작합니다. /pr-3/는 해당 PR 저장을 계속합니다.
- 정식 페이지와 GitHub Pages의 호스트가 같아도 localStorage를 공유하지 않도록 모든 게임 저장 키에 hexhaven-preview:pr-3: 접두사를 붙였습니다. 일반 진행 전환도 테스트 전용 저장만 사용합니다.
- fresh=1은 이 PR의 실험 슬롯만 초기화하고 URL에서 제거하므로 이후 새로고침은 이어 하기가 됩니다. 정식 키는 읽거나 쓰거나 지우지 않습니다.
- 원본 지형·규칙 파일은 그대로이고, 배포 사본에만 저장 키와 진입 모듈을 변경했습니다.

## 최초 배포
이 패키지를 별도 공개 저장소의 main에 반영하고 Settings → Pages → Source를 GitHub Actions로 설정합니다.
Pages 워크플로 성공 후 공개 주소와 모든 게임 모듈의 HTTP 200을 확인해야 배포 완료입니다.

## 다음 PR 테스트
Actions → PR playtest Pages → Run workflow → source_pr에 HEX HAVEN의 PR 번호를 입력합니다.
그 PR의 head SHA로 고정해 필요한 정적 파일만 읽고 pr-N/ 경로를 생성합니다. 게임 코드를 빌드 서버에서 실행하지 않습니다.
기존 게임의 저장 키가 달라지면 자동 배포를 중단하므로 build-preview.py의 격리 규칙을 검토해야 합니다.
워크플로에서 만든 추가 PR 스냅샷은 그 배포 산출물에만 유지됩니다. 영구 보존하려면 생성된 pr-N/을 이 테스트 저장소에 커밋합니다.
정식 저장소의 main, PR 브랜치 및 정식 Pages는 변경하지 않습니다.
