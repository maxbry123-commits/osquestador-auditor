# SW-N45 EVIDENCE — HTML24 RECOVERY

schema: `sharck-input.swarm-node-evidence.v1`
node: `SW-N45` / agent: `SOL-6-GPT` / mode: `READ_ONLY_DESIGN`
claim: `0e87fb1c1384d774d236795aa5e6d5d621480330`
N33 blob: `d0e468828ac9303a988102352c1bcebe8d8e5d44`
N38 state: `BLOCKED_RELEASED`; reported manifest: `10f6cc61aa8e8a22c3725ef8b3e265bbeb8c198c7d895fa46caeb70a460079bc`.
N45 recovery manifest: `8b663d4332173ba9c18c7988c608493388f418a1749f98a3e1dfec9a81e9b659`.
Canonical/product mutation: `NO`; downloads/wiring: `0`.

## STEP 1 — deterministic reconstruction
Exactly 24 fixtures = languages `en,es,ar,zh-Hans` × classes `clean-semantic,boilerplate,malformed,multi-article,unicode,metadata-conflict`.
Every row contains N33-required fields: `fixture_id,language,class,html_sha256,gold_sha256,gold_title,gold_body,gold_authors[],gold_published_at,gold_canonical_url,selector_assertions[],forbidden_sentinels[]`.
Common rules: `fixture_id=<lang>__<class>`; published=`2026-01-01T00:00:00Z`; canonical URL=`https://fixtures.local/<fixture_id>`; HTML hash=SHA256 exact UTF-8; gold hash=SHA256 canonical compact sorted-key JSON; manifest hash=SHA256 canonical compact sorted-key JSON rows sorted by fixture_id.
Gold language bases: en=`Recovered English Story`/`The verified body is preserved exactly for the English fixture.`/`Alice Example`; es=`Historia española recuperada`/`El cuerpo verificado se conserva exactamente para la prueba en español.`/`Alicia Ejemplo`; ar=`قصة عربية مستعادة`/`يتم حفظ النص الموثق بدقة لاختبار اللغة العربية.`/`أليس مثال`; zh-Hans=`恢复的中文故事`/`已验证的正文被精确保留，用于简体中文测试。`/`爱丽丝示例`.
Class rules: boilerplate forbids `NAV_SENTINEL,AD_SENTINEL,FOOTER_SENTINEL,COMMENT_SENTINEL,RELATED_SENTINEL`; malformed uses unclosed/misnested tags + duplicate attr + entity and requires typed/no-uncaught result; multi-article forbids `RELATED_STORY_SENTINEL`; unicode contains decomposed `Café`, `🧪`, `中文`, `العربية`; metadata-conflict precedence=`JSON-LD > OpenGraph > HTML` and title suffix=` — canonical`.
N38 bytes were never persisted, so historical byte identity is not asserted; its digest is preserved separately and N45 independently materializes the N33 contract.

## STEP 2 — 24 fixture hashes
|id|html_sha256|gold_sha256|
|---|---|---|
|ar__boilerplate|37c9a20b57d81762021022b07d03ce657bade8fc16a08b54353fe97aee7710fb|ded6f7630bdd5dbc87ecfad322df498be9008c787b688d49f59cb0d5da4b4b13|
|ar__clean-semantic|51a46d9b6defd48cc6e1886be5e55b185e83e0eabf4b4f87c7ea5e999c8bcfc4|96913ff9b6983e0091971060027660934bf5b4d552af232a3dbf96113730fc10|
|ar__malformed|e5f54ede8f2c5a1330fa792e81ebcee2309da0d6424828fcd2fa24c4ee280092|9e226c7b1cc044ee453da518a252733f99d8cf9e33989df153cb8dbb4ada745b|
|ar__metadata-conflict|1798ba5f12e42df342aab106946a3c6b96aaf3f4abb5b303163737f4b6669599|9b3e027d9f3fe05e96948491f0df0084678a0528c4de3545ada2f58bf2187f36|
|ar__multi-article|27968178e156cba41b00e16e645dbdae0b30bcd2ef848ad89b1cc3b1e0391036|4fb06e991089efb69930fa5ccae838b95219a9c99c4fc6a7e6f3173e319de534|
|ar__unicode|362530a8e0f9a24bd56a62b3fb9411b66b5efc4203b5047b5a4e4960f4964c5d|e966e3380a8b343819c81173bba7a6cd6014c4bd228eac22153f977d0aacf27a|
|en__boilerplate|b9567ee04469642a615fbaea6a2b887ff1d51fb5084abf190e4adbdc7514025e|217c00ba2a69187f2d57f949ab107191fd18b24172cd732c7d065ec73bac3f86|
|en__clean-semantic|281a62a43ad21ae67dc1ebd811e4ca6204e354ad78389c16a6b8112143aed414|d9e0d6cbb9bfb635bb5bbd65364a4c25593a1af387d399790efaed4e10c83e26|
|en__malformed|b3126803210af1f73b3208601e6ab0a7d7d76ff2ca36b4da620d3438383773f8|17965dac4de887f014faaf587779c4157a38e7cb824333af77b1fa9b1a4601b8|
|en__metadata-conflict|ae23e144edc3c2d0bc7e5aeffbfbeb82bf613cc1f2c1387d51750a74679fcaa0|9d47693fa91f71be0714e87366825d7247f5888676234f30437d5668cfd01074|
|en__multi-article|6b0f687bab1f61dcd58f32997918527b8b919f514f26915f532cf94b94be23c3|a0982e9cc118033872fced96759ba6d0af8e35b258bff2050c745eb85bae60ea|
|en__unicode|bcf6ef449cf7f7ad681e7abbdaa830af18a1c4685430b1e581cd7df83491c6ef|67e9267c8357bf60922b781227c8bfb102aaf9b362ee82fb489d84a15726b302|
|es__boilerplate|1bf3a1a5e7b0e3ea0ac4cfdc2ddd45603dd989890f9b85346eafc6a1d35bd3ee|3a7c383cc9a21f8edab459d46a7812195e1f4f607d28082fe1ef0c426cb5a485|
|es__clean-semantic|ef5e481a7f169ad1d2f255f9fc9b8ce7c5609481ab6567829798bb7f6ec76e02|903b8dc08a355f55b0d91bea011182934ed08460d3a5a9fe5db5e63499898d99|
|es__malformed|91573a8b67eb665c897507d5584ff7c87d076a359d3b0fd26ead9ef54485f61b|a5af27f0d171cbdec42b0681b7fbb941d1ac6e1958b1a9e1fb9a9932554e785b|
|es__metadata-conflict|70a9065adc0838dd91295cbca7772699fd121141634bf60bbce2f62eb4f29cdb|8fdeae2ba0eebbed6a3dac41fcfcb830429adb7dd9057097ad56e5ba05170648|
|es__multi-article|5f54100c052fb27ad697eb97274a5d24bf3cb49553dffa4b5acccbdf33244608|f3a98e6e9dd1e848fcd85ffea365189084bd7ba12e8af8bc5a20d2446acbc6a1|
|es__unicode|356c38e5996f03ae327a1e46b70f46d291d942884a3dd790add9ce7785a42f17|004236bdb1668c377a8df497025c626f1209e87a5aeefcf1fe6a5d8698f34096|
|zh-Hans__boilerplate|da998045e3cfa2ae9a354ae504ffeba47c49b2f345744941086fdc5c4eadd328|f04d5889cfbf480dcef7d19e9f99cb3f6aa0a09c9cfd2e915cda150b174c157f|
|zh-Hans__clean-semantic|55be195d8eb12ab5336f1a1b92dd9cdd961975ac18d38f2b432b5e50cab24d16|2bf9eb28ad49e4a8eafba538b63c326fbc380778f85a45521d0d4e3e3685edc0|
|zh-Hans__malformed|aaf53528874dbed76eff9a7e67d1b2ad49139641aa5f51a2b5d1aab088ffe566|03872c9b36ce3fc92520539ac8589e185bac426b62dad9149f4c80b549372ece|
|zh-Hans__metadata-conflict|c24efe55d9a661e760bf0825a11c6906e6d34b0b37e03c76b48061de452cc453|fc322e49e8901544a58a292d179854f06c9d58ef7da0c7235f6d472acb7af5c7|
|zh-Hans__multi-article|96df5e961549a9dd08d465ed7c4bed3831bb18e0ef0865766f35a7627b2f3889|43920cbfaf2f6f5c39edba720de441632e3205e7a39487dfd03fea7f693fa581|
|zh-Hans__unicode|51be5e04e1ee59417ed0914d4fbc0de87e75eb0f147428f9097caf79cb62da9d|ef5359296b1216f825605b44707e51c32444ff1c7e0b701413240b7ddabbb5bf|

Validation: count 24 PASS; 4×6 coverage PASS; IDs unique PASS; required fields 24/24 PASS; SHA format PASS; HTML/gold recompute 24/24 PASS; boilerplate sentinels 4/4 PASS; unicode assertions 4/4 PASS; metadata precedence 4/4 PASS; canonical manifest rehash PASS.

## STEP 3 — 3 refutations
1. one HTML-byte drift => recorded hash mismatch: PASS.
2. remove one row => count 23 and digest `67d371f7768cfadc6720e2ec3848377a614a2b464a0e9ce3d867e63b28c7d12f`: PASS.
3. mutate one gold title => digest `1c4cf496c4fb74e101c64d60b8008fd2333117c42db5df7b7d55e2d205f14f0d`: PASS.

Verdict: `PASS_PENDING_REVIEW`. N38 evidence-persistence gap is recovered with an independently reproducible N33-compliant 24-fixture manifest. No claim of unavailable N38 byte identity; N38 digest preserved separately.
