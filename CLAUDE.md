# CLAUDE.md

flaretool は日本向けユーティリティの Python ライブラリ（祝日・営業日計算、和暦変換、全半角変換、短縮URL/DDNS/nettool クライアント、デコレーター集、CLI）。PyPI に公開中。**Python 3.12–3.14 対応（3.11以下は非対応）**。

## コマンド

```bash
# テスト（pyproject の pythonpath=["src"] で解決。PYTHONPATH 不要）
.venv12/bin/python -m pytest tests -q

# リリース前は 3バージョンすべてで実行
.venv13/bin/python -m pytest tests -q   # 3.13
.venv14/bin/python -m pytest tests -q   # 3.14

# lint / format（コミット前に必ず）
.venv12/bin/ruff format src tests
.venv12/bin/ruff check src tests

# wheel ビルド確認（build/ の残骸が混入するため先に削除）
rm -rf build/ && .venv12/bin/python -m build --wheel
```

実行はローカルの `.venv12` を使う（`.venv` は旧3.9なので使わない）。

## 構成

- パッケージ本体: `src/flaretool/`（src レイアウト、PEP 621 の pyproject.toml、py.typed 同梱）
- テスト: `tests/flaretool/`（pytest + pytest-asyncio、`asyncio_mode = "auto"`）
- `build/ dist/ .work*/ work/ htmlcov/` は生成物・ローカル作業場（gitignore 済み）。**調査・変更の対象にしない**

## アーキテクチャの要点

- **HTTP はすべて `flaretool.common.requests` を経由**（小文字の `requests` クラス。実体は共有 Session + デフォルトタイムアウト (5,30) + 冪等メソッドのみ Retry）。get/post/put/delete/head は必ず `requests.request` を通る —
  **テストはこの1点（`flaretool.common.requests.request`）をモックする**設計。ここを迂回する実装を書くと既存テストのモックが効かなくなる
- `flaretool.api_key` はモジュールグローバルで、実行時再代入がリクエストに反映される仕様（意図的に維持）
- holiday: 祝日定義は `holiday/algorithms.py` の宣言的ルールテーブル（`HOLIDAY_RULES`）+ `holidays_of_year(year)`（純粋・`functools.cache`）。
  インスタンス状態（追加休日・カスタムルール・週末設定）はキャッシュの外側でレイヤリングする。オンライン版（`online.py`）のオーバーライドポイントは `_statutory_holiday_name` のみ
- decorators: 全デコレーターが sync/async 透過（`inspect.iscoroutinefunction` で分岐、async 側は `asyncio.sleep` 等を使用）。新規デコレーターも両対応で書く
- 遅延 import 方針: `flaretool/__init__.py` は PEP 562 `__getattr__` で nettool を遅延、`whois` は関数内 import。import 時のネットワークアクセスは禁止（過去に PyPI チェックで問題化し除去済み）

## 互換契約（壊すと公開APIが崩れる）

- `flaretool.utills` は deprecation シム（実体は `utils.py`）。`holiday/JapaneseHolidays.py`・`JapaneseHolidaysOnline.py` はモジュールパス互換シム。削除しない
- タプル順: `get_holidays()` / `get_holidays_in_range()` / `get_rest_days_in_range()` はすべて **(date, 祝日名)**（v0.3.0 で統一済み。逆順に戻さない）
- shorturl の URL は送信前にハイフンを `%2D` エンコードする（サーバー側契約）。`_encode_url_for_api` を必ず経由
- `tests/flaretool/test_holiday.py` の 1980–2024 ゴールデンデータは祝日計算の回帰網。**アサーションを弱めない**
- docstring は日本語（Args/Returns/Raises/Examples 形式）。公開APIの docstring は sphinx-apidoc でそのままドキュメント化される

## リリース・CI

- バージョンは `src/flaretool/VERSION.py` の**手動更新のみ**（自動インクリメントは v0.3.0 で廃止済み。復活させない）
- リリース手順: develop に push → CI グリーン確認 → PR で main へ（レビュー必須）→ `gh workflow run auto_deploy.yml --ref main`（docs → PyPI 公開 → タグ → develop 再作成）。**auto_deploy 実行前に必ずユーザーの確認を取る**（PyPI 公開は取り消し不可）
- `merge-develop` ジョブが develop を再作成するため、リリース後はローカルを `git fetch` して確認すること
- CI のカバレッジバッジ（gist 更新）はマトリクスジョブが同時 PATCH すると 409 で落ちることがある。**テスト自体の失敗と混同しない**（ログで pytest の結果を確認）。失敗ジョブの再実行で解消する
- コミットは Conventional 形式でなく日本語の要約文。develop へ直接 push 可、main は PR 経由

## 秘密情報

- トークン・APIキーはコードやスクリプトにハードコードせず、環境変数または GitHub Secrets を使う。ハードコードを見つけたら環境変数化を提案する
