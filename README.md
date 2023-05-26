# flaretool

**flaretool** is flarebrow Library.

[![python](https://img.shields.io/badge/python-%3E%3D3.9-blue)](https://github.com/flarebrow/flaretool)
[![Downloads](https://static.pepy.tech/badge/flaretool)](https://pepy.tech/project/flaretool)

[API Doc](https://flarebrow.github.io/flaretool/)

**Attention**

This library is under development and may exhibit unexpected behavior. New features will be released soon. Please stay tuned.

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
# hostname: sample.com
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

# 特定のユーザーエージェントでスクレイピング可否を確認する例
url = "http://example.com/page.html"
user_agent = "MyScraperBot"
allowed = nettool.is_scraping_allowed(url, user_agent) # user_agentはオプション引数
if allowed:
    print(f"{url} はユーザーエージェント '{user_agent}' でのスクレイピングが許可されています。")
else:
    print(f"{url} はユーザーエージェント '{user_agent}' でのスクレイピングが禁止されています。")
```

### NetTool Command Examples of usage

```bash
flaretool nettool get_global_ipaddr_info
# usage
# flaretool nettool {FunctionName} [args...]
```

All methods within Netttol can be executed as commands.


### Help Command

```bash
flaretool nettool -h
```

## JapaneseHoliday Examples of usage

[Holiday Usage Document](https://flarebrow.github.io/flaretool/flaretool.holiday.html#module-flaretool.holiday)

```python
from flaretool.holiday import JapaneseHolidays
import datetime

# JapaneseHolidaysクラスのインスタンスを作成
holidays = JapaneseHolidays()

# 特定の日付が祝日かどうかを判定
date = datetime.date(2023, 1, 1)
is_holiday = holidays.get_holiday_name(date)
print(is_holiday)  # "元日" が出力される

# 特定の期間内の祝日一覧を取得
start_date = datetime.date(2023, 1, 1)
end_date = datetime.date(2023, 12, 31)
holiday_list = holidays.get_holidays_in_range(start_date, end_date)
for holiday in holiday_list:
    print(holiday)
# 出力例:
# ("元日", datetime.date(2023, 1, 1))
# ("元日（振替休日）", datetime.date(2023, 1, 2))
# ("成人の日", datetime.date(2023, 1, 9))
# ("建国記念の日", datetime.date(2023, 2, 11))
# ...

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

# ShortURL Usage

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

## Usage

```python
from flaretool.shorturl import ShortUrlService
shorturl = ShortUrlService()

# 新規登録
result = shorturl.create_short_url("https://example.com")
print("ShortLink:", result.link)   # https://○○○/○○○
print("OriginalURL:", result.url)  # https://example.com

# 情報取得
result = shorturl.get_short_url_info(result.id)[0]
print("ShortLink:", result.link)   # https://○○○/○○○
print("OriginalURL:", result.url)  # https://example.com

# 更新
result.url = "https://example.com/sample"
result = shorturl.update_short_url(result)
print("ShortLink:", result.link)   # https://○○○/○○○
print("OriginalURL:", result.url)  # https://example.com/sample

# 削除
shorturl.delete_short_url(result)
```
