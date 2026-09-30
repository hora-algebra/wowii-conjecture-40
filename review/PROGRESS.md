# 投稿準備の状態

2026-09-30。目標は、Lemma A°の証明案を研究元の規範に沿って査読可能にし、適切な知見追記PRを作ること。Formal Conjectures本体のWOWII40をsolvedにすることではない。

完了：

- upstream main 290d1b28fd70038824fbba736e1bf47dd83aed01を取得。
- attempt/2026-09-30-codex-6e29を作成。mainは変更していない。
- 検証器と既存反例17ファイルのhashを照合。
- O-56/63/64をupstream oracleで再現。負の対照3件すべてで強制閉路と最小性仮定の不成立を検出。
- gauntletに対応する理解記録をCOMPREHENSION.mdに作成。ただし元の探索に先立つ記録ではなく、事後記録と明示。
- nauty2.8.9を作業ディレクトリ内でビルド。システムへのインストールはしていない。
- upstream gold a1_verify.py 7:143/143、失敗0、打切り0。forced_core.py 8:2186件、強制閉路0、最大道長6を再現。
- 次の検査計画・コードhashを実行前にcommit f2ba193に固定。
- scan_small.py完了、終了値0。2〜10頂点の連結二部グラフ5015個、最小FVSと残る辺158576組。tight集合94691件、共有隣接点2個以上のtight集合4650件、厳密隣接数検査5996件、carrier関係の検査14083件、直接選択列挙との照合1000件。失敗0。全定理の形式検証ではない。
- 日本語公開候補 proofs/LEMMA-A-ODD-EQUALITY-JA.md を作成。出典、CC BY4.0、AI探索・執筆・監査、査読や完全形式化を主張しない旨を追加。
- GitHub認証ユーザーhora-algebraを確認。push・PR作成はまだ行っていない。

残件：

- 先行attempt報告の全件読解を完了（review/prior-reports.txtへの取得は済み、全件を読み終えたとは主張しない）。依存しない先行監査の結果を借用しない。
- freshnessのMathOverflow・WOWII公式ページの直接取得はweb工具で失敗。別手段で再確認し、確認範囲を記録。
- 必要な補題の検証範囲を精査。現在のscanはshared U>=2の核心を重点検査し、偶数・奇数の一般補題自体の全域検査とは異なる。
- 英語の定理と証明要約、再現説明、ATTEMPT_REPORT、LESSONSを整備。
- 最終候補の引用・形式・描画を確認。自律的な研究試行として投稿し、人間が証明全体をレビュー済みとはしない。
- 試行ブランチをforkへpush、mainに対するPR差分はattempts/LESSONS.mdの追記だけとする。公開後はremote SHA・原稿取得・PRの内容と状態を読み戻す。

ローカルで完了した検査の記録であり、公開完了やPR作成の証拠ではない。
