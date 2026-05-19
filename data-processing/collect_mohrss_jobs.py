from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
OUTPUT_CSV = DATA_DIR / "mohrss_public_jobs.csv"
METADATA_JSON = DATA_DIR / "mohrss_public_jobs_metadata.json"

SOURCE_NAME = "中国公共招聘网"
SOURCE_HOME = "https://job.mohrss.gov.cn/"
SOURCE_LIST = "http://job.mohrss.gov.cn/cjobs/jobinfolist/listJobinfolist"

PROVINCES = {
    "110000": "北京",
    "120000": "天津",
    "130000": "河北",
    "140000": "山西",
    "150000": "内蒙古",
    "210000": "辽宁",
    "220000": "吉林",
    "230000": "黑龙江",
    "310000": "上海",
    "320000": "江苏",
    "330000": "浙江",
    "340000": "安徽",
    "350000": "福建",
    "360000": "江西",
    "370000": "山东",
    "410000": "河南",
    "420000": "湖北",
    "430000": "湖南",
    "440000": "广东",
    "450000": "广西",
    "460000": "海南",
    "500000": "重庆",
    "510000": "四川",
    "520000": "贵州",
    "530000": "云南",
    "540000": "西藏",
    "610000": "陕西",
    "620000": "甘肃",
    "630000": "青海",
    "640000": "宁夏",
    "650000": "新疆",
}

CITY_BY_PREFIX = {
    "1100": "北京",
    "1200": "天津",
    "1301": "石家庄",
    "1302": "唐山",
    "1303": "秦皇岛",
    "1304": "邯郸",
    "1305": "邢台",
    "1306": "保定",
    "1307": "张家口",
    "1308": "承德",
    "1309": "沧州",
    "1310": "廊坊",
    "1311": "衡水",
    "1401": "太原",
    "1402": "大同",
    "1403": "阳泉",
    "1404": "长治",
    "1405": "晋城",
    "1406": "朔州",
    "1407": "晋中",
    "1408": "运城",
    "1409": "忻州",
    "1410": "临汾",
    "1411": "吕梁",
    "1501": "呼和浩特",
    "1502": "包头",
    "1503": "乌海",
    "1504": "赤峰",
    "1505": "通辽",
    "1506": "鄂尔多斯",
    "1507": "呼伦贝尔",
    "1508": "巴彦淖尔",
    "1509": "乌兰察布",
    "2101": "沈阳",
    "2102": "大连",
    "2103": "鞍山",
    "2104": "抚顺",
    "2105": "本溪",
    "2106": "丹东",
    "2107": "锦州",
    "2108": "营口",
    "2109": "阜新",
    "2110": "辽阳",
    "2111": "盘锦",
    "2112": "铁岭",
    "2113": "朝阳",
    "2114": "葫芦岛",
    "2201": "长春",
    "2202": "吉林",
    "2203": "四平",
    "2204": "辽源",
    "2205": "通化",
    "2206": "白山",
    "2207": "松原",
    "2208": "白城",
    "2301": "哈尔滨",
    "2302": "齐齐哈尔",
    "2303": "鸡西",
    "2304": "鹤岗",
    "2305": "双鸭山",
    "2306": "大庆",
    "2307": "伊春",
    "2308": "佳木斯",
    "2309": "七台河",
    "2310": "牡丹江",
    "2311": "黑河",
    "2312": "绥化",
    "3100": "上海",
    "3201": "南京",
    "3202": "无锡",
    "3203": "徐州",
    "3204": "常州",
    "3205": "苏州",
    "3206": "南通",
    "3207": "连云港",
    "3208": "淮安",
    "3209": "盐城",
    "3210": "扬州",
    "3211": "镇江",
    "3212": "泰州",
    "3213": "宿迁",
    "3301": "杭州",
    "3302": "宁波",
    "3303": "温州",
    "3304": "嘉兴",
    "3305": "湖州",
    "3306": "绍兴",
    "3307": "金华",
    "3308": "衢州",
    "3309": "舟山",
    "3310": "台州",
    "3311": "丽水",
    "3401": "合肥",
    "3402": "芜湖",
    "3403": "蚌埠",
    "3404": "淮南",
    "3405": "马鞍山",
    "3406": "淮北",
    "3407": "铜陵",
    "3408": "安庆",
    "3410": "黄山",
    "3411": "滁州",
    "3412": "阜阳",
    "3413": "宿州",
    "3415": "六安",
    "3416": "亳州",
    "3417": "池州",
    "3418": "宣城",
    "3501": "福州",
    "3502": "厦门",
    "3503": "莆田",
    "3504": "三明",
    "3505": "泉州",
    "3506": "漳州",
    "3507": "南平",
    "3508": "龙岩",
    "3509": "宁德",
    "3601": "南昌",
    "3602": "景德镇",
    "3603": "萍乡",
    "3604": "九江",
    "3605": "新余",
    "3606": "鹰潭",
    "3607": "赣州",
    "3608": "吉安",
    "3609": "宜春",
    "3610": "抚州",
    "3611": "上饶",
    "3701": "济南",
    "3702": "青岛",
    "3703": "淄博",
    "3704": "枣庄",
    "3705": "东营",
    "3706": "烟台",
    "3707": "潍坊",
    "3708": "济宁",
    "3709": "泰安",
    "3710": "威海",
    "3711": "日照",
    "3713": "临沂",
    "3714": "德州",
    "3715": "聊城",
    "3716": "滨州",
    "3717": "菏泽",
    "4101": "郑州",
    "4102": "开封",
    "4103": "洛阳",
    "4104": "平顶山",
    "4105": "安阳",
    "4106": "鹤壁",
    "4107": "新乡",
    "4108": "焦作",
    "4109": "濮阳",
    "4110": "许昌",
    "4111": "漯河",
    "4112": "三门峡",
    "4113": "南阳",
    "4114": "商丘",
    "4115": "信阳",
    "4116": "周口",
    "4117": "驻马店",
    "4201": "武汉",
    "4202": "黄石",
    "4203": "十堰",
    "4205": "宜昌",
    "4206": "襄阳",
    "4207": "鄂州",
    "4208": "荆门",
    "4209": "孝感",
    "4210": "荆州",
    "4211": "黄冈",
    "4212": "咸宁",
    "4213": "随州",
    "4301": "长沙",
    "4302": "株洲",
    "4303": "湘潭",
    "4304": "衡阳",
    "4305": "邵阳",
    "4306": "岳阳",
    "4307": "常德",
    "4308": "张家界",
    "4309": "益阳",
    "4310": "郴州",
    "4311": "永州",
    "4312": "怀化",
    "4313": "娄底",
    "4401": "广州",
    "4402": "韶关",
    "4403": "深圳",
    "4404": "珠海",
    "4405": "汕头",
    "4406": "佛山",
    "4407": "江门",
    "4408": "湛江",
    "4409": "茂名",
    "4412": "肇庆",
    "4413": "惠州",
    "4414": "梅州",
    "4415": "汕尾",
    "4416": "河源",
    "4417": "阳江",
    "4418": "清远",
    "4419": "东莞",
    "4420": "中山",
    "4451": "潮州",
    "4452": "揭阳",
    "4453": "云浮",
    "4501": "南宁",
    "4502": "柳州",
    "4503": "桂林",
    "4504": "梧州",
    "4505": "北海",
    "4506": "防城港",
    "4507": "钦州",
    "4508": "贵港",
    "4509": "玉林",
    "4510": "百色",
    "4511": "贺州",
    "4512": "河池",
    "4513": "来宾",
    "4514": "崇左",
    "4601": "海口",
    "4602": "三亚",
    "4603": "三沙",
    "4604": "儋州",
    "5000": "重庆",
    "5101": "成都",
    "5103": "自贡",
    "5104": "攀枝花",
    "5105": "泸州",
    "5106": "德阳",
    "5107": "绵阳",
    "5108": "广元",
    "5109": "遂宁",
    "5110": "内江",
    "5111": "乐山",
    "5113": "南充",
    "5114": "眉山",
    "5115": "宜宾",
    "5116": "广安",
    "5117": "达州",
    "5118": "雅安",
    "5119": "巴中",
    "5120": "资阳",
    "5201": "贵阳",
    "5202": "六盘水",
    "5203": "遵义",
    "5204": "安顺",
    "5205": "毕节",
    "5206": "铜仁",
    "5301": "昆明",
    "5303": "曲靖",
    "5304": "玉溪",
    "5305": "保山",
    "5306": "昭通",
    "5307": "丽江",
    "5308": "普洱",
    "5309": "临沧",
    "5401": "拉萨",
    "5402": "日喀则",
    "5403": "昌都",
    "5404": "林芝",
    "5405": "山南",
    "5406": "那曲",
    "6101": "西安",
    "6102": "铜川",
    "6103": "宝鸡",
    "6104": "咸阳",
    "6105": "渭南",
    "6106": "延安",
    "6107": "汉中",
    "6108": "榆林",
    "6109": "安康",
    "6110": "商洛",
    "6201": "兰州",
    "6202": "嘉峪关",
    "6203": "金昌",
    "6204": "白银",
    "6205": "天水",
    "6206": "武威",
    "6207": "张掖",
    "6208": "平凉",
    "6209": "酒泉",
    "6210": "庆阳",
    "6211": "定西",
    "6212": "陇南",
    "6301": "西宁",
    "6302": "海东",
    "6401": "银川",
    "6402": "石嘴山",
    "6403": "吴忠",
    "6404": "固原",
    "6405": "中卫",
    "6501": "乌鲁木齐",
    "6502": "克拉玛依",
    "6504": "吐鲁番",
    "6505": "哈密",
}

EDUCATION_BY_CODE = {
    "11": "博士",
    "14": "硕士",
    "21": "本科",
    "31": "大专",
    "41": "中专",
    "44": "中专",
    "47": "技校",
    "61": "高中",
    "71": "初中",
    "90": "不限",
    "0": "不限",
    "00": "不限",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def fetch_page(area_code: str, page_no: int) -> str:
    params = urlencode({"AREA": area_code, "pageNo": page_no})
    request = Request(
        f"{SOURCE_LIST}?{params}",
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "http://job.mohrss.gov.cn/cjobs/jobinfolist/listJobinfolistIndex",
        },
    )
    last_error: Exception | None = None
    for attempt in range(1, 4):
        try:
            with urlopen(request, timeout=30) as response:
                return response.read().decode(response.headers.get_content_charset() or "utf-8", errors="replace")
        except Exception as exc:  # noqa: BLE001 - retry network and server-side transient failures.
            last_error = exc
            time.sleep(0.8 * attempt)
    raise RuntimeError(f"fetch failed area={area_code} page={page_no}: {last_error}") from last_error


def hidden_value(page: str, element_id: str) -> str:
    tag = re.search(rf"<input[^>]+id=[\"']{re.escape(element_id)}[\"'][^>]*>", page, flags=re.I | re.S)
    if not tag:
        return ""
    value = re.search(r"value=[\"'](.*?)[\"']", tag.group(0), flags=re.I | re.S)
    return html.unescape(value.group(1)) if value else ""


def parse_jobs(page: str) -> list[dict]:
    value = hidden_value(page, "findjoblist")
    if not value:
        return []
    try:
        data = json.loads(value)
    except json.JSONDecodeError:
        return []
    return data if isinstance(data, list) else []


def clean_text(value: object) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()


def province_from_area(area_code: str, fallback: str) -> str:
    code = clean_text(area_code)
    if len(code) >= 2 and f"{code[:2]}0000" in PROVINCES:
        return PROVINCES[f"{code[:2]}0000"]
    return fallback


def city_from_record(record: dict, province: str) -> str:
    area_code = clean_text(record.get("aab301") or record.get("area"))
    if len(area_code) >= 4 and area_code[:4] in CITY_BY_PREFIX:
        return CITY_BY_PREFIX[area_code[:4]]
    area_text = clean_text(record.get("area_"))
    if "·" in area_text:
        area_text = area_text.split("·", 1)[0]
    for suffix in ("省", "市", "自治区", "特别行政区"):
        area_text = area_text.replace(suffix, "")
    if area_text and area_text != province:
        return area_text
    district = clean_text(record.get("aab302"))
    for suffix in ("市本级", "本级", "新区", "区", "县", "市"):
        district = district.replace(suffix, "")
    return district or province


def salary_text(record: dict) -> str:
    low = clean_text(record.get("acb241"))
    high = clean_text(record.get("acb242"))
    if low and high and low != "0" and high != "0":
        return f"{low}-{high}元/月"
    if low and low != "0":
        return f"{low}元/月"
    return ""


def education_text(record: dict) -> str:
    code = clean_text(record.get("aac011"))
    return EDUCATION_BY_CODE.get(code, code or "不限")


def experience_text(record: dict) -> str:
    text = clean_text(record.get("acb22a"))
    if re.search(r"应届|毕业生|经验不限|无经验|不限", text):
        return "应届/不限"
    if re.search(r"5\s*年|五\s*年|8\s*年|10\s*年", text):
        return "5年以上"
    if re.search(r"3\s*年|三\s*年", text):
        return "3-5年"
    if "经验" in text:
        return "1-3年"
    return "不限"


def normalize_record(record: dict, province_fallback: str) -> dict[str, str]:
    area_code = clean_text(record.get("aab301") or record.get("area"))
    province = province_from_area(area_code, province_fallback)
    city = city_from_record(record, province)
    title = clean_text(record.get("aca112"))
    category = clean_text(record.get("aca111_") or record.get("aca111_Local_"))
    description = clean_text(record.get("acb22a"))
    publish_date = clean_text(record.get("s_aae397") or record.get("s_uptime"))
    source_url = clean_text(record.get("ace760")) or SOURCE_LIST
    return {
        "source_dataset": SOURCE_NAME,
        "source_ref": "job.mohrss.gov.cn",
        "job_id": clean_text(record.get("acb200")),
        "job_title": title,
        "company_name": clean_text(record.get("aab004")) or clean_text(record.get("org_")),
        "city": city,
        "province": province,
        "salary": salary_text(record),
        "education": education_text(record),
        "experience": experience_text(record),
        "industry": category or "未分类",
        "major": "",
        "company_size": "",
        "company_type": "",
        "publish_date": publish_date,
        "description": " ".join(part for part in [title, category, description] if part),
        "longitude": "",
        "latitude": "",
        "source_url": source_url,
    }


def write_csv(rows: list[dict[str, str]], output_path: Path) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "source_dataset",
        "source_ref",
        "job_id",
        "job_title",
        "company_name",
        "city",
        "province",
        "salary",
        "education",
        "experience",
        "industry",
        "major",
        "company_size",
        "company_type",
        "publish_date",
        "description",
        "longitude",
        "latitude",
        "source_url",
    ]
    with output_path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="采集中国公共招聘网公开岗位列表")
    parser.add_argument("--pages-per-province", type=int, default=1)
    parser.add_argument("--sleep", type=float, default=0.3)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--output", type=Path, default=OUTPUT_CSV)
    args = parser.parse_args()

    rows: list[dict[str, str]] = []
    seen: set[str] = set()
    province_counts: dict[str, int] = {}
    tasks = [(area_code, province, page_no) for area_code, province in PROVINCES.items() for page_no in range(1, args.pages_per_province + 1)]

    def ingest_page(area_code: str, province: str, page_no: int) -> tuple[str, int, list[dict[str, str]]]:
        page = fetch_page(area_code, page_no)
        page_rows = [normalize_record(record, province) for record in parse_jobs(page)]
        if args.sleep:
            time.sleep(args.sleep)
        return province, page_no, page_rows

    if args.workers <= 1:
        results = [ingest_page(area_code, province, page_no) for area_code, province, page_no in tasks]
    else:
        results = []
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            futures = [executor.submit(ingest_page, area_code, province, page_no) for area_code, province, page_no in tasks]
            for index, future in enumerate(as_completed(futures), start=1):
                results.append(future.result())
                if index % 100 == 0:
                    print(f"fetched pages: {index}/{len(futures)}")

    for province, _page_no, page_rows in sorted(results, key=lambda item: (item[0], item[1])):
        for normalized in page_rows:
            dedupe_key = normalized["job_id"] or hashlib.sha1(
                json.dumps(normalized, ensure_ascii=False, sort_keys=True).encode("utf-8")
            ).hexdigest()
            if dedupe_key in seen:
                continue
            seen.add(dedupe_key)
            rows.append(normalized)
            province_counts[province] = province_counts.get(province, 0) + 1

    for province in PROVINCES.values():
        province_counts.setdefault(province, 0)
        print(f"{province}: {province_counts[province]} rows")

    write_csv(rows, args.output)
    metadata = {
        "source_name": SOURCE_NAME,
        "source_home": SOURCE_HOME,
        "source_list": SOURCE_LIST,
        "collected_at": datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds"),
        "pages_per_province": args.pages_per_province,
        "rows": len(rows),
        "sha256": sha256(args.output),
        "province_counts": province_counts,
        "privacy_note": "Only public job fields used by this project are saved; contact names and phone numbers from the source page are intentionally not exported.",
    }
    METADATA_JSON.write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(metadata, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
