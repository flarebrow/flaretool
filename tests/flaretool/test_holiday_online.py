import os
import pytest
import csv
import requests
from datetime import datetime, date, timedelta
from flaretool.holiday import JapaneseHolidays, JapaneseHolidaysOnline


@pytest.mark.skipif('HOLIDAY_TEST_URL' not in os.environ, reason="skip external api call during CI")
def test_syukujitsu():
    url = os.environ["HOLIDAY_TEST_URL"]
    try:
        response = requests.get(url)
        response.encoding = response.apparent_encoding
        response.raise_for_status()
    except Exception as e:
        raise AssertionError("date unknown")
    csv_data = response.text.splitlines()
    reader = csv.reader(csv_data[1:])
    holiday_list = {}
    for date_value, name in reader:
        date_value = datetime.strptime(date_value, "%Y/%m/%d").date()
        holiday_list[date_value] = name
    jh = JapaneseHolidays()
    jho = JapaneseHolidaysOnline()

    year = int(datetime.now().strftime("%Y")) + 1
    start_date = date(1980, 1, 1)
    end_date = date(year, 12, 31)
    current_date = start_date
    while current_date <= end_date:
        holiday_name = jh.get_holiday_name(current_date)
        holidayo_name = jho.get_holiday_name(current_date)
        syukujitsu_name = holiday_list.get(current_date, None)
        if holiday_name or syukujitsu_name:
            try:
                if "休日" == syukujitsu_name or "祝日扱い" in syukujitsu_name:
                    assert "振替" in holiday_name or "休日" in holiday_name
                    assert "振替" in holidayo_name or "休日" in holidayo_name
                elif "礼" in syukujitsu_name or "儀" in syukujitsu_name:
                    assert "休日" in holiday_name
                    assert holidayo_name == syukujitsu_name
                else:
                    assert holiday_name in syukujitsu_name
                    assert holidayo_name == syukujitsu_name
            except:
                print(current_date.strftime("%Y/%m/%d"),
                      holiday_name, syukujitsu_name)
                raise
        current_date += timedelta(days=1)
