# flaretool

**flaretool** is flarebrow Library.

![License](https://img.shields.io/github/license/flarebrow/flaretool)
[![python](https://img.shields.io/badge/python-%3E%3D3.12-blue)](https://github.com/flarebrow/flaretool)
[![version](https://img.shields.io/github/v/release/flarebrow/flaretool?include_prereleases)](https://github.com/flarebrow/flaretool/releases/latest)
[![ReleaseDate](https://img.shields.io/github/release-date/flarebrow/flaretool)](https://github.com/flarebrow/flaretool/releases/latest)
![build](https://img.shields.io/github/actions/workflow/status/flarebrow/flaretool/auto_test.yml)
![Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/flarebrow/e31fc348a9dea0098de9540dc5961668/raw/pytest-coverage-3.12.json)
[![Downloads](https://static.pepy.tech/badge/flaretool)](https://pepy.tech/project/flaretool)

[Library Document](https://flarebrow.github.io/flaretool/)

> [!IMPORTANT]
> 
> This library is under development and may exhibit unexpected behavior. New features will be released soon. Please stay tuned.


> [!WARNING]
> 
> Please note that some formats have changed in version 0.2.7 and above, as well as in earlier versions, so be careful when updating.
>
> バージョン0.2.7以降のバージョンでいくつかのフォーマットが変更されているため、アップデート時には注意してください。



## install
```bash
pip install flaretool
```

## NetTool usage

[NetTool Usage Document](https://flarebrow.github.io/flaretool/flaretool.nettool.html)


### NetTool Examples of usage
```python
from flaretool import nettool

# 指定されたIPアドレスの情報を取得する例
ip_info = nettool.get_global_ipaddr_info("192.168.0.1")
print("ip:", ip_info.ipaddr)
print("hostname:", ip_info.hostname)
print("country:", ip_info.country)
# 出力例：
# ip: 192.168.0.1
# hostname: example.com
# country: earth

# ドメイン名からIPアドレスを取得する例
ip_address = nettool.lookup_ip("example.com")
print(ip_address)  # 123.456.789.001

# IPアドレスからドメイン名を取得する例
domain_name = nettool.lookup_domain("1.1.1.1")
print(domain_name)  # one.one.one.one

# 指定されたIPアドレスが指定されたネットワークに属しているかどうかを判定する例
allowed_networks = ["192.168.0.0/24", "10.0.0.0/16"]
is_allowed = nettool.is_ip_in_allowed_networks(
    "192.168.0.100", allowed_networks)
print(is_allowed)  # True

# 指定されたドメイン名が存在するかどうかを判定する例
domain_exists = nettool.domain_exists("example.com")
print(domain_exists)  # True

# 日本のIPアドレスのリストを取得する例
japan_ips = nettool.get_japanip_list()
print(japan_ips)

# 指定されたアドレスが日本のIPアドレスか確認する例
is_japan = nettool.is_japan_ip("203.0.113.1")
print(is_japan)  # False

# 日本語を含むドメインをpunycodeに変換する例
puny_info = nettool.get_puny_code("日本語ドメイン.jp")
print("originalvalue:", puny_info.originalvalue)
print("encodevalue:", puny_info.encodevalue)
print("decodevalue:", puny_info.decodevalue)
# 出力例：
# originalvalue: 日本語ドメイン.jp
# encodevalue: xn--eckwd4c7c5976acvb2w6i.jp
# decodevalue: 日本語ドメイン.jp

# robots.txtをもとに特定のユーザーエージェントでスクレイピング可否を確認する例
url = "http://example.com/page.html"
user_agent = "MyScraperBot"
allowed = nettool.is_scraping_allowed(url, user_agent) # user_agentはオプション引数
if not allowed:
    print(f"{url} はユーザーエージェント '{user_agent}' でのスクレイピングが禁止されています。")
```

### NetTool Command Examples of usage

```bash
flaretool nettool get_global_ipaddr_info
# usage
# flaretool nettool {FunctionName} [args...]
```

All methods within NetTool can be executed as commands.


### Help Command

```bash
flaretool nettool -h
```

## String utils usage

[String Utils Usage Document](https://flarebrow.github.io/flaretool/flaretool.html#module-flaretool.utils)

> [!NOTE]
> 旧モジュール名の `flaretool.utills` も引き続き利用できますが非推奨です（インポート時にDeprecationWarningが発生します）。新しいコードでは `flaretool.utils` を使用してください。

```python
from flaretool import utils
from flaretool.utils import ConversionMode

# 文字列変換
# 半角
value = "１２３４５６７８９６７８９"
result = utils.convert_value(value)
print(result)  # "1234567896789"

# 全角
value = "Hello"
result = utils.convert_value(value, ConversionMode.FULL_WIDTH)
print(result)  # "Ｈｅｌｌｏ"

# 文字列のみ半角
value = "ＡＢＣａｂｃ１２３"
result = utils.convert_value(
    value, ascii=True, digit=False, kana=False)
print(result)  # "ABCabc１２３"

# 小文字
value = "ABCabc"
result = utils.convert_value(
    value, ConversionMode.LOWER)
print(result)  # "abcabc"

# 大文字
value = "ABCabc"
result = utils.convert_value(
    value, ConversionMode.UPPER)
print(result)  # "ABCABC"
```

## JapaneseHoliday Examples of usage

[Holiday Usage Document](https://flarebrow.github.io/flaretool/flaretool.holiday.html#module-flaretool.holiday)

![online](https://img.shields.io/endpoint?url=https%3A%2F%2Fpublic.flarebrow.com%2Fjapanholiday-badge.json?ver=2025)

```python
# オフライン版
from flaretool.holiday import JapaneseHolidays
# オンライン版
from flaretool.holiday import JapaneseHolidaysOnline
import datetime

# JapaneseHolidaysクラスのインスタンスを作成
holidays = JapaneseHolidays()
# オンライン版を使う場合はこちら
# holidays = JapaneseHolidaysOnline()

# 特定の日付が祝日かどうかを判定(date型)
date = datetime.date(2023, 1, 1)
is_holiday = holidays.get_holiday_name(date)
print(is_holiday)  # "元日" が出力される

# 特定の日付が祝日かどうかを判定(str型)
date = "2023/1/1"
is_holiday = holidays.get_holiday_name(date)
print(is_holiday)  # "元日" が出力される

# 特定の日付が祝日かどうかを判定(祝日ではない場合)
date = "2023/1/3"
is_holiday = holidays.get_holiday_name(date)
print(is_holiday)  # None が出力される

# 特定の期間内の祝日一覧を取得
start_date = datetime.date(2023, 1, 1)
end_date = datetime.date(2023, 12, 31)
holiday_list = holidays.get_holidays_in_range(start_date, end_date)
for holiday in holiday_list:
    print(holiday)
# 出力例:
# (datetime.date(2023, 1, 1), "元日")
# (datetime.date(2023, 1, 2), "元日（振替休日）")
# (datetime.date(2023, 1, 9), "成人の日")
# (datetime.date(2023, 2, 11), "建国記念の日")
# ...

# 2023年の祝日を取得
holiday_list = holidays.get_holidays("2023")
for holiday in holiday_list:
    print(holiday)
# 出力例:
# (datetime.date(2023, 1, 1), "元日")
# (datetime.date(2023, 1, 2), "元日（振替休日）")
# (datetime.date(2023, 1, 9), "成人の日")
# (datetime.date(2023, 2, 11), "建国記念の日")
# ...

# 2023年5月の祝日を取得
holiday_list = holidays.get_holidays("202305")
for holiday in holiday_list:
    print(holiday)
# 出力例:
# (datetime.date(2023, 5, 3), '憲法記念日')
# (datetime.date(2023, 5, 4), 'みどりの日')
# (datetime.date(2023, 5, 5), 'こどもの日')

# 営業日を取得(7月)
date = datetime.date(2023, 7, 1)

## 第1営業日を取得
business_day = holidays.get_first_business_day(date)
print(business_day)  # "2023-07-03" が出力される

## 第4営業日を取得
business_day = holidays.get_first_business_day(date, 4)
print(business_day)  # "2023-07-06" が出力される

## 最終営業日を取得
business_day = holidays.get_last_business_day(date)
print(business_day)  # "2023-07-31" が出力される

# 特定期間内の営業日のリストを取得
business_days = holidays.get_business_date_range(start_date, end_date)
for business_day in business_days:
    print(business_day)
# 出力例:
# 2023-01-03
# 2023-01-04
# 2023-01-05
# ...
```

## BusinessDay and CustomHoliday Examples of usage

営業日の加算・カウントや、独自の休日（会社の休業日など）の登録ができます。

[Holiday Usage Document](https://flarebrow.github.io/flaretool/flaretool.holiday.html#module-flaretool.holiday)

```python
import datetime
from flaretool.holiday import JapaneseHolidays

holidays = JapaneseHolidays()

# 営業日の加算・減算（土日祝をスキップ）
holidays.add_business_days("2026/05/01", 1)   # datetime.date(2026, 5, 7) GWをスキップ
holidays.add_business_days("2026/05/07", -1)  # datetime.date(2026, 5, 1)

# 翌営業日・前営業日を取得
holidays.next_business_day("2026/05/03")      # 2026-05-07
holidays.previous_business_day("2026/05/06")  # 2026-05-01
# include_start=True で起点日が営業日ならその日を返す
holidays.next_business_day("2026/05/01", include_start=True)  # 2026-05-01

# 期間内の営業日数をカウント
holidays.count_business_days("2026/06/01", "2026/06/30")  # 22

# カスタム休日を登録（個別の日付指定）
holidays.add_custom_holidays("社休日", ["2026-06-15", "2026-06-16"])

# カスタム休日を毎年繰り返すルールとして登録
holidays.add_custom_holiday_rule("創立記念日", "8/15")
holidays.add_custom_holiday_rule("年末年始休業", "12/29-1/3")  # 年をまたぐ期間もOK
holidays.is_holiday("2026/01/02")  # True

# 週末の扱いを変更（営業日判定にのみ影響）
holidays.set_weekend(saturday=False)
holidays.is_business_day("2026/06/06")  # True（土曜日）

# カスタム休日をすべてクリア
holidays.clear_custom_holidays()
```

> [!NOTE]
> 法定祝日と重なる日は法定祝日名が優先され、ルール由来の休日は振替休日を発生させません。`set_weekend`は営業日判定にのみ影響します。

## Wareki Examples of usage

和暦（元号）と西暦の相互変換ができます（明治/大正/昭和/平成/令和対応）。

[Wareki Usage Document](https://flarebrow.github.io/flaretool/flaretool.html#module-flaretool.wareki)

```python
from flaretool.wareki import to_wareki, to_seireki, get_era, get_fiscal_year, today_wareki

# 西暦 → 和暦
to_wareki("2026-07-02")  # '令和8年7月2日'
to_wareki("2019-05-01")  # '令和元年5月1日'（gannen=Falseで'令和1年5月1日'）
to_wareki("2026-07-02", format="{era_short}{year}.{month}.{day}")  # 'R8.7.2'

# 和暦 → 西暦（漢数字・ローマ字表記などにも対応）
to_seireki("令和8年7月2日")    # datetime.date(2026, 7, 2)
to_seireki("R8.7.2")          # datetime.date(2026, 7, 2)
to_seireki("令和八年七月二日")  # datetime.date(2026, 7, 2)

# 元号の取得
get_era("1989-01-07").name  # '昭和'

# 年度（日本の会計年度）の取得
get_fiscal_year("2026-03-31")  # 2025

# 今日の日付を和暦で取得
today_wareki()  # '令和8年7月2日'
```

## Decorator Examples of usage

[Decorator Usage Document](https://flarebrow.github.io/flaretool/flaretool.html#module-flaretool.decorators)

```python
from flaretool.errors import FlareToolNetworkError
from flaretool.decorators import network_required, retry, repeat, timeout, timer

# ネットワーク接続を必須とするデコレーター
@network_required
def network_access(url):
    # ネットワークに接続されている場合に実行する処理
    response = requests.get(url)
    return response.json()

def main():
    try:
        network_access()
    except FlareToolNetworkError:
        # ネットワークに接続されていない場合の処理
        pass

# 例外が発生した場合にリトライを行うデコレーター
@retry(tries=3, delay=2) # 2秒毎に3回までリトライ
# @retry(3) # ←この場合は待機なし（delay=0）で3回までリトライ
def retry_function():
    pass

# 複数回実行を行うデコレーター
@repeat(tries=3, interval=2) # 2秒毎に3回メソッドを実行
# @repeat(2) # ←この場合は連続で2回実行
def repeat_function():
    # 強制的に実行を止めたい場合はStopIterationをraiseさせる
    print("repeat message")
    if 複数回の実行をとめたい条件:
        raise StopIteration("Stop the loop!")
    pass
## 出力例
# repeat message
# repeat message
# repeat message

# 制限時間をつけるデコレーター
@timeout(5)
def my_function():
    # Some time-consuming operation
    time.sleep(10)
    return "Operation completed"
try:
    result = my_function()
    print(result)
except TimeoutError:
    print("Operation timed out")
## 出力例
# Operation timed out

# メソッドの実行時間を計測するデコレーター
## Logger Setup
from flaretool.logger import setup_logger
logger = setup_logger(logging.DEBUG, console=True)
@timer
def example_function(x):
    time.sleep(x)
    return x

example_function(2)
## 出力例
# [2024-08-01 00:00:00,000] DEBUG : example_function took 2.0000 seconds to execute.
```

### Async support

すべてのデコレーターは非同期関数（`async def`）にもそのまま適用できます。

```python
import asyncio
from flaretool.decorators import retry

@retry(3)  # 非同期関数にも透過的に動作
async def fetch():
    ...

asyncio.run(fetch())
```

### More decorators

上記のほか、以下のデコレーターが利用できます。詳細は[Decorator Usage Document](https://flarebrow.github.io/flaretool/flaretool.html#module-flaretool.decorators)を参照してください。

- `rate_limit` : 呼び出し回数を制限（スライディングウィンドウ方式）
- `singleton` : クラスをシングルトンにする（スレッドセーフ）
- `suppress_errors` : 例外を抑制してデフォルト値を返す
- `run_in_thread` : 関数を別スレッドで実行し`Future`を返す
- `synchronized` : 関数の実行をロックで排他制御する
- `cache` : 結果をキャッシュする（TTL・サイズ上限指定可）
- `deprecate` : 非推奨警告（DeprecationWarning）を出す
- `type_check` : アノテーションに基づく実行時型チェック

```python
from flaretool.decorators import rate_limit, suppress_errors, singleton

# 1秒間に2回までに制限（超過分は空きが出るまで待機）
@rate_limit(calls=2, period=1.0)
def api_call():
    return "called"

# 例外発生時に例外を送出せずデフォルト値を返す
@suppress_errors(default=0)
def parse_number(text):
    return int(text)

parse_number("abc")  # 0

# 常に同一インスタンスを返すクラスにする
@singleton
class Config:
    def __init__(self):
        self.value = 42

Config() is Config()  # True
```

## Command Line Tool usage

祝日判定・営業日計算・和暦変換・文字列変換などをコマンドラインから実行できます。

```bash
flaretool holiday 2026-01-01          # => 元日
flaretool holiday 2026-01             # 年月を指定すると祝日一覧を表示
flaretool holiday 2026-01-01 --json   # => {"date": "2026-01-01", "name": "元日"}

flaretool business 2026-07-02                     # 営業日判定 => true / false
flaretool business 2026-07-02 --add 3             # 3営業日後 => 2026-07-07
flaretool business 2026-07-01 --count 2026-07-07  # 期間内の営業日数 => 5

flaretool wareki 2026-07-02      # 西暦→和暦 => 令和8年7月2日
flaretool seireki 令和8年7月2日   # 和暦→西暦 => 2026-07-02

flaretool convert ＡＢＣ１２３ --mode half  # 文字列変換 => ABC123
flaretool hash hello --mode sha256         # ハッシュ値の計算
flaretool base64 こんにちは                 # Base64エンコード（--decode でデコード）

flaretool track yamato 123456789012  # 荷物の配送状況を追跡
```

各サブコマンドは `--json` オプションでJSON形式の出力に切り替えられます。エラー時は終了コード1で終了します。nettoolの関数をコマンドとして実行する場合は[NetTool Command Examples of usage](#nettool-command-examples-of-usage)を参照してください。

# Flarebrow Service

There are the following services available:

1. Short URL service: This service allows you to shorten URLs.
2. DDNS (Dynamic DNS) service: This service provides Dynamic DNS functionality.

To use this class, you need to set up an API key.

## Configuration API Key

The library you are using relies on an API key to communicate with an external service. To securely store the API key, it needs to be defined either as an environment variable or in a `.env` file or script setting. Please follow the instructions below:

### Using an script setting:

```python
import flaretool
flaretool.api_key = "your_api_key_here"
```

### Using an environment variable:
   Set the API key as an environment variable using the following variable name:
   - API_KEY

   Example of defining an environment variable (Linux/macOS):
   ```bash
   export API_KEY=your_api_key_here
   ```

   Example of defining an environment variable (Windows):
   ```bat
   set API_KEY=your_api_key_here
   ```

### Using a `.env` file:
   Create a `.env` file in the root directory of your project and define the API key as follows:
   ```env
   API_KEY=your_api_key_here
   ```
   The library will read the API key from the `.env` file.

You need to log in to the external service's account to obtain an API key. Be careful not to share your API key with others, and avoid committing the `.env` file to a public version control system.

Please refer to the documentation of the library you are using to find the specific instructions for setting the API key and the exact name of the environment variable.

## ShortURL Service Usage

[ShortURL Usage Document](https://flarebrow.github.io/flaretool/flaretool.shorturl.html#module-flaretool.shorturl)

```python
from flaretool.shorturl import ShortUrlService
shorturl = ShortUrlService()

# 新規登録
result = shorturl.create("https://example.com")
print("ShortLink:", result.short_url)   # https://○○○/○○○
print("OriginalURL:", result.url)  # https://example.com

# 情報取得
result = shorturl.get(result.id)[0]
print("ShortLink:", result.short_url)   # https://○○○/○○○
print("OriginalURL:", result.url)  # https://example.com

# 更新
result.url = "https://example.com/sample"
result = shorturl.update(result)
print("ShortLink:", result.short_url)   # https://○○○/○○○
print("OriginalURL:", result.url)  # https://example.com/sample

# 削除
shorturl.delete(result)

# QRコード取得
image_data = shorturl.get_qr_code_raw_data(result)
image_path = "image.png"
with open(image_path, 'wb') as image_file:
    image_file.write(image_data) # image.png にQRコード画像が保存されます
# ※ QRコードは(株)デンソーウェーブの登録商標です
```

## Dynamic DNS Service Usage

[Dynamic DNS Usage Document](https://flarebrow.github.io/flaretool/flaretool.ddns.html#module-flaretool.ddns)

```python
from flaretool.ddns import DdnsService
service = DdnsService()
info = service.update_ddns("example", "192.168.0.100")
print(info.status)    # successful
print(info.currentIp) # 192.168.0.99
print(info.updateIp)  # 192.168.0.100
print(info.domain)    # example.○○○.○○
```

## Async API Examples of usage

ShortURL・DDNS・NetToolはasyncioに対応した非同期APIも提供しています。

```python
import asyncio
import flaretool
from flaretool.shorturl import AsyncShortUrlService
from flaretool.ddns import AsyncDdnsService

flaretool.api_key = "API-KEY"

async def main():
    # 非同期版ShortURLサービス
    async with AsyncShortUrlService() as svc:
        info = await svc.create("https://example.com")
        print(info.short_url)

    # 非同期版DDNSサービス
    async with AsyncDdnsService() as ddns:
        result = await ddns.update_ddns("example", "192.168.0.100")

asyncio.run(main())
```

nettoolは同期版と同名の関数のため、`from flaretool.nettool import aio` で明示的にインポートして使用します（`await aio.lookup_ip("example.com")` など）。`asyncio.gather`で並行実行も可能です。

```python
import asyncio
from flaretool.nettool import aio

async def main():
    ip, exists = await asyncio.gather(
        aio.lookup_ip("example.com"),
        aio.domain_exists("example.com"),
    )
    print(ip, exists)

asyncio.run(main())
```

