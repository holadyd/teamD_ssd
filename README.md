# Project teamD SSD: 가상 SSD 및 테스트 셸 개발

## 🌟 프로젝트 개요

[cite\_start]Digital Ninjas 팀이 진행하는 **teamD SSD 프로젝트**는 SSD(Solid State Drive)와 이를 검증하기 위한 **Test Shell**을 개발하는 프로젝트입니다[cite: 10, 11]. [cite\_start]실제 하드웨어(HW)가 아닌 소프트웨어(SW)로 가상 SSD를 구현하고 [cite: 13, 25, 48][cite\_start], 이 가상 SSD의 동작을 테스트하는 프로그램(Test Shell)을 제작합니다[cite: 14, 27, 95, 96].

## 🚀 주요 목표

  * [cite\_start]**가상 SSD 구현**: Read와 Write 명령어만을 수행하는 최소화된 기능의 가상 SSD를 SW로 구현합니다[cite: 51].

      * [cite\_start]LBA(Logical Block Address) 단위는 4 Byte이며 [cite: 52][cite\_start], LBA 0부터 99까지 총 100개의 공간에 데이터를 저장할 수 있습니다[cite: 53].
      * [cite\_start]SSD의 내부 저장소인 Nand에 기록되는 과정을 모사하여, `ssd_nand.txt` 파일에 데이터를 기록합니다[cite: 80, 81].

  * [cite\_start]**Test Shell 개발**: 가상 SSD에 명령을 내릴 수 있는 검증용 프로그램(Test Shell)을 제작합니다[cite: 95, 96].

      * [cite\_start]사용자는 `write`, `read`, `fullwrite`, `fullread`, `exit`, `help` 등 다양한 명령어를 사용하여 SSD의 동작을 테스트할 수 있습니다[cite: 97].
      * [cite\_start]Test Shell은 `write` 또는 `read` 명령을 수행할 때, 제작한 `ssd` 앱을 실행시켜 해당 작업을 수행합니다[cite: 97, 99].

  * [cite\_start]**Test Script 제작**: Test Shell 안에서 동작하는 자동화된 테스트 코드를 작성합니다[cite: 29, 108, 112].

      * [cite\_start]다양한 Test Scenario를 기반으로 `1_FullWriteAndReadCompare`, `2_PartialLBAWrite`, `3_WriteReadAging` 등의 Test Script를 구현합니다[cite: 119, 125, 129].
      * [cite\_start]테스트 결과는 "ReadCompare" 동작을 통해 **PASS / FAIL**로 결정되며 [cite: 114, 116][cite\_start], FAIL이 발생하면 즉시 테스트가 종료됩니다[cite: 116].
