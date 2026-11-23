"""cities-capitals: each city is its country's map with a pin where the city is, the country's
flag, and the city's name. Coordinates are typed by hand (good to about a tenth of a degree).
Run: python drawings/cities_capitals.py [ids...]
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import earth_geography as EG  # noqa: E402
import flags as FL  # noqa: E402
from _geo import Frame, ring_area  # noqa: E402
from _parts import A1, A1L, A2, DARK, LIGHT  # noqa: E402
from check_catalog import slug  # noqa: E402
from draw_lib import run  # noqa: E402
from text_tile import text_path  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

# id: (country id, lat, lon)
CITIES = """
kabul afghanistan 34.53 69.17|yerevan armenia 40.18 44.51|baku azerbaijan 40.41 49.87|manama bahrain 26.23 50.59
dhaka bangladesh 23.81 90.41|thimphu bhutan 27.47 89.64|bandar-seri-begawan brunei 4.90 114.94|phnom-penh cambodia 11.56 104.92
beijing china 39.90 116.40|nicosia cyprus 35.17 33.36|tbilisi georgia 41.72 44.79|new-delhi india 28.61 77.21
jakarta indonesia -6.21 106.85|tehran iran 35.69 51.39|baghdad iraq 33.31 44.36|jerusalem holy-land 31.78 35.22
tokyo japan 35.68 139.69|amman jordan 31.95 35.93|astana kazakhstan 51.17 71.45|kuwait-city kuwait 29.38 47.99
bishkek kyrgyzstan 42.87 74.59|vientiane laos 17.98 102.63|beirut lebanon 33.89 35.50|kuala-lumpur malaysia 3.14 101.69
male maldives 4.18 73.51|ulaanbaatar mongolia 47.89 106.91|naypyidaw myanmar 19.76 96.08|kathmandu nepal 27.72 85.32
pyongyang north-korea 39.04 125.76|muscat oman 23.59 58.41|islamabad pakistan 33.68 73.05|ramallah palestine 31.90 35.20
manila philippines 14.60 120.98|doha qatar 25.29 51.53|riyadh saudi-arabia 24.71 46.68|singapore-city singapore 1.29 103.85
seoul south-korea 37.57 126.98|sri-jayawardenepura-kotte sri-lanka 6.89 79.92|damascus syria 33.51 36.29|taipei taiwan 25.03 121.57
dushanbe tajikistan 38.56 68.79|bangkok thailand 13.76 100.50|dili timor-leste -8.56 125.57|ankara turkiye 39.93 32.86
ashgabat turkmenistan 37.96 58.33|abu-dhabi united-arab-emirates 24.45 54.38|tashkent uzbekistan 41.30 69.24|hanoi vietnam 21.03 105.85
sanaa yemen 15.37 44.19
algiers algeria 36.75 3.06|luanda angola -8.84 13.23|porto-novo benin 6.50 2.60|gaborone botswana -24.63 25.92
ouagadougou burkina-faso 12.37 -1.52|gitega burundi -3.43 29.92|praia cabo-verde 14.93 -23.51|yaounde cameroon 3.85 11.50
bangui central-african-republic 4.39 18.56|ndjamena chad 12.13 15.06|moroni comoros -11.70 43.26
kinshasa democratic-republic-of-the-congo -4.44 15.27|brazzaville republic-of-the-congo -4.27 15.28|yamoussoukro cote-divoire 6.83 -5.29
djibouti-city djibouti 11.59 43.15|cairo egypt 30.04 31.24|malabo equatorial-guinea 3.75 8.78|asmara eritrea 15.32 38.93
mbabane eswatini -26.31 31.14|addis-ababa ethiopia 9.03 38.74|libreville gabon 0.42 9.47|banjul gambia 13.45 -16.58
accra ghana 5.60 -0.19|conakry guinea 9.64 -13.58|bissau guinea-bissau 11.86 -15.60|nairobi kenya -1.29 36.82
maseru lesotho -29.31 27.48|monrovia liberia 6.30 -10.80|tripoli libya 32.89 13.19|antananarivo madagascar -18.88 47.51
lilongwe malawi -13.96 33.79|bamako mali 12.64 -8.00|nouakchott mauritania 18.08 -15.98|port-louis mauritius -20.16 57.50
rabat morocco 34.02 -6.83|maputo mozambique -25.97 32.57|windhoek namibia -22.56 17.08|niamey niger 13.51 2.11
abuja nigeria 9.08 7.40|kigali rwanda -1.94 30.06|sao-tome sao-tome-and-principe 0.34 6.73|dakar senegal 14.72 -17.47
victoria-seychelles seychelles -4.62 55.45|freetown sierra-leone 8.48 -13.23|mogadishu somalia 2.05 45.32|pretoria south-africa -25.75 28.19
juba south-sudan 4.85 31.58|khartoum sudan 15.50 32.56|dodoma tanzania -6.16 35.75|lome togo 6.14 1.21
tunis tunisia 36.81 10.18|kampala uganda 0.35 32.58|lusaka zambia -15.39 28.32|harare zimbabwe -17.83 31.05
tirana albania 41.33 19.82|andorra-la-vella andorra 42.51 1.52|vienna austria 48.21 16.37|minsk belarus 53.90 27.56
brussels belgium 50.85 4.35|sarajevo bosnia-and-herzegovina 43.86 18.41|sofia bulgaria 42.70 23.32|zagreb croatia 45.81 15.98
prague czechia 50.08 14.44|copenhagen denmark 55.68 12.57|tallinn estonia 59.44 24.75|helsinki finland 60.17 24.94
paris france 48.86 2.35|berlin germany 52.52 13.40|athens greece 37.98 23.73|budapest hungary 47.50 19.04
reykjavik iceland 64.15 -21.94|dublin ireland 53.35 -6.26|rome italy 41.90 12.50|pristina kosovo 42.66 21.17
riga latvia 56.95 24.11|vaduz liechtenstein 47.14 9.52|vilnius lithuania 54.69 25.28|luxembourg-city luxembourg 49.61 6.13
valletta malta 35.90 14.51|chisinau moldova 47.01 28.86|monaco-city monaco 43.73 7.42|podgorica montenegro 42.44 19.26
amsterdam netherlands 52.37 4.90|skopje north-macedonia 41.99 21.43|oslo norway 59.91 10.75|warsaw poland 52.23 21.01
lisbon portugal 38.72 -9.14|bucharest romania 44.43 26.10|moscow russia 55.76 37.62|city-of-san-marino san-marino 43.94 12.45
belgrade serbia 44.79 20.45|bratislava slovakia 48.15 17.11|ljubljana slovenia 46.06 14.51|madrid spain 40.42 -3.70
stockholm sweden 59.33 18.07|bern switzerland 46.95 7.45|kyiv ukraine 50.45 30.52|london united-kingdom 51.51 -0.13
saint-johns antigua-and-barbuda 17.12 -61.85|nassau bahamas 25.05 -77.35|bridgetown barbados 13.10 -59.62|belmopan belize 17.25 -88.77
ottawa canada 45.42 -75.70|san-jose-costa-rica costa-rica 9.93 -84.08|havana cuba 23.11 -82.37|roseau dominica 15.30 -61.39
santo-domingo dominican-republic 18.49 -69.93|san-salvador el-salvador 13.69 -89.22|st-georges grenada 12.06 -61.75
guatemala-city guatemala 14.63 -90.51|port-au-prince haiti 18.59 -72.31|tegucigalpa honduras 14.07 -87.19|kingston jamaica 18.02 -76.80
mexico-city mexico 19.43 -99.13|managua nicaragua 12.11 -86.24|panama-city panama 8.98 -79.52|basseterre saint-kitts-and-nevis 17.30 -62.72
castries saint-lucia 14.01 -60.99|kingstown saint-vincent-and-the-grenadines 13.16 -61.22|port-of-spain trinidad-and-tobago 10.65 -61.51
washington-dc united-states 38.90 -77.04|buenos-aires argentina -34.60 -58.38|la-paz bolivia -16.50 -68.15|sucre bolivia -19.04 -65.26
brasilia brazil -15.79 -47.88|santiago chile -33.45 -70.67|bogota colombia 4.71 -74.07|quito ecuador -0.18 -78.47
georgetown guyana 6.80 -58.16|asuncion paraguay -25.26 -57.58|lima peru -12.05 -77.04|paramaribo suriname 5.85 -55.20
montevideo uruguay -34.90 -56.16|caracas venezuela 10.48 -66.90
canberra australia -35.28 149.13|suva fiji -18.14 178.44|south-tarawa kiribati 1.33 172.98|majuro marshall-islands 7.09 171.38
palikir micronesia 6.92 158.16|yaren nauru -0.55 166.92|wellington new-zealand -41.29 174.78|ngerulmud palau 7.50 134.62
port-moresby papua-new-guinea -9.44 147.18|apia samoa -13.83 -171.76|honiara solomon-islands -9.43 159.95|nukualofa tonga -21.14 -175.20
funafuti tuvalu -8.52 179.20|port-vila vanuatu -17.73 168.32
mumbai india 19.08 72.88|delhi india 28.70 77.10|kolkata india 22.57 88.36|chennai india 13.08 80.27|bengaluru india 12.97 77.59
hyderabad india 17.39 78.49|ahmedabad india 23.02 72.57|pune india 18.52 73.86|jaipur india 26.91 75.79|lucknow india 26.85 80.95
varanasi india 25.32 82.97|agra india 27.18 78.01|amritsar india 31.63 74.87|kochi india 9.93 76.27|mysuru india 12.30 76.64
chandigarh india 30.73 76.78|srinagar india 34.08 74.80|shimla india 31.10 77.17|udaipur india 24.59 73.71|jodhpur india 26.24 73.02
bhopal india 23.26 77.41|indore india 22.72 75.86|patna india 25.59 85.14|guwahati india 26.14 91.74|bhubaneswar india 20.30 85.82
thiruvananthapuram india 8.52 76.94|surat india 21.17 72.83|nagpur india 21.15 79.09|visakhapatnam india 17.69 83.22
madurai india 9.93 78.12|puducherry india 11.94 79.81|kanpur india 26.45 80.33|rishikesh india 30.09 78.27|haridwar india 29.95 78.16
leh india 34.15 77.58|darjeeling india 27.04 88.26|ooty india 11.41 76.70|hyderabad-old-city india 17.36 78.47
makkah saudi-arabia 21.42 39.83|madinah saudi-arabia 24.47 39.61|jeddah saudi-arabia 21.49 39.19|taif saudi-arabia 21.27 40.42
dammam saudi-arabia 26.43 50.10|dubai united-arab-emirates 25.20 55.27|sharjah united-arab-emirates 25.35 55.42|istanbul turkiye 41.01 28.98
alexandria egypt 31.20 29.92|mashhad iran 36.30 59.61|isfahan iran 32.65 51.67|samarkand uzbekistan 39.65 66.96|bukhara uzbekistan 39.77 64.42
new-york-city united-states 40.71 -74.01|los-angeles united-states 34.05 -118.24|chicago united-states 41.88 -87.63
san-francisco united-states 37.77 -122.42|las-vegas united-states 36.17 -115.14|toronto canada 43.65 -79.38|vancouver canada 49.28 -123.12
rio-de-janeiro brazil -22.91 -43.17|sao-paulo brazil -23.55 -46.63|shanghai china 31.23 121.47|hong-kong china 22.32 114.17
osaka japan 34.69 135.50|kyoto japan 35.01 135.77|sydney australia -33.87 151.21|melbourne australia -37.81 144.96
karachi pakistan 24.86 67.01|lahore pakistan 31.55 74.34|colombo sri-lanka 6.93 79.86|lagos nigeria 6.52 3.38
johannesburg south-africa -26.20 28.05|cape-town south-africa -33.92 18.42|casablanca morocco 33.57 -7.59|marrakesh morocco 31.63 -7.98
barcelona spain 41.39 2.17|milan italy 45.46 9.19|venice italy 45.44 12.32|florence italy 43.77 11.26|munich germany 48.14 11.58
st-petersburg russia 59.93 30.34|granada spain 37.18 -3.60|cordoba spain 37.88 -4.78|abidjan cote-divoire 5.36 -4.01
dar-es-salaam tanzania -6.79 39.21
"""
TABLE = {}
for _row in CITIES.replace("\n", "|").split("|"):
    if _row.strip():
        _id, _c, _la, _lo = _row.split()
        TABLE[_id] = (_c, float(_la), float(_lo))

_names = {}
for _g in EG.CAT["groups"]:
    if _g["id"].startswith("countries-"):
        for _it in _g["items"]:
            _nm = _it["name"] if isinstance(_it, dict) else (_it if isinstance(_it, str) else _it[0])
            _iid = _it["id"] if isinstance(_it, dict) else slug(_nm)
            _names[_iid] = [_nm] + ([] if isinstance(_it, (str, dict)) else _it[1:])

_rings_cache = {}


def rings_for(country):
    if country in _rings_cache:
        return _rings_cache[country]
    if country == "india":
        r = EG.filter_far(EG.main_rings(EG.india_rings(), 0.004))
    elif country == "united-states":
        r = [x for v in EG.usa_lower48().values() for x in v]
    elif country == "holy-land":
        r = rings_for("israel") + rings_for("palestine")
    else:
        r = EG.filter_far(EG.main_rings(EG.country_rings(EG.SPECIAL.get(country) or _names[country]), 0.004))
    _rings_cache[country] = r
    return r


MAP_BOX = (60, 86, 452, 376)


def city(cid, name):
    country, lat, lon = TABLE[cid]

    def fn(s):
        rings = rings_for(country)
        f = Frame(rings, MAP_BOX)
        pts = [[f.pt(x, y) for x, y in r] for r in rings]
        if sum(ring_area(p) for p in pts) < 2500:     # scattered islands: a dot for each
            for p in pts:
                cx, cy = sum(q[0] for q in p) / len(p), sum(q[1] for q in p) / len(p)
                s.F("circle", cx=f"{cx:.0f}", cy=f"{cy:.0f}", r=14, fill=A1)
        else:
            EG.merged(s, f.path(rings, eps=1.2, min_area=4.0), A1)
        px, py = f.pt(lon, lat)
        s.F("path", d=f"M{px:.0f} {py:.0f} C{px - 6:.0f} {py - 18:.0f} {px - 26:.0f} {py - 30:.0f} {px - 26:.0f} {py - 48:.0f} "
                      f"A26 26 0 1 1 {px + 26:.0f} {py - 48:.0f} C{px + 26:.0f} {py - 30:.0f} {px + 6:.0f} {py - 18:.0f} {px:.0f} {py:.0f} Z", fill=A2)
        s.F("circle", outline=False, cx=f"{px:.0f}", cy=f"{py - 48:.0f}", r=10, fill=LIGHT)
        has_flag = country != "holy-land"
        x0 = 168 if has_flag else 40
        s.F("rect", x=x0, y=396, width=472 - x0, height=76, rx=38, fill=DARK)
        d, _ = text_path(name.upper(), "black", (x0 + 472) / 2, 434, 472 - x0 - 44, 40)
        s.F("path", outline=False, d=d, fill=LIGHT)
        if has_flag:
            k = 0.27
            s.open(transform=f"translate({40 - 36 * k:.1f} {400 - 109 * k:.1f}) scale({k})")
            FL.D["flag-" + country](s)
            s.close()
    return fn


D = {}
for _g in json.loads((ROOT / "catalog" / "cities-capitals.json").read_text(encoding="utf-8"))["groups"]:
    for _it in _g["items"]:
        _nm = _it["name"] if isinstance(_it, dict) else (_it if isinstance(_it, str) else _it[0])
        _iid = _it["id"] if isinstance(_it, dict) else slug(_nm)
        if _iid in TABLE:
            _label = {"hyderabad-old-city": "Hyderabad", "san-jose-costa-rica": "San José", "victoria-seychelles": "Victoria",
                      "singapore-city": "Singapore", "washington-dc": "Washington, D.C.", "city-of-san-marino": "San Marino",
                      "sri-jayawardenepura-kotte": "Kotte", "nukualofa": "Nuku'alofa"}.get(_iid, _nm.title().replace("'S", "'s"))
            D[_iid] = city(_iid, _label)

if __name__ == "__main__":
    missing = [i for g in json.loads((ROOT / "catalog" / "cities-capitals.json").read_text(encoding="utf-8"))["groups"]
               for i in ((x["id"] if isinstance(x, dict) else slug(x if isinstance(x, str) else x[0])) for x in g["items"]) if i not in TABLE]
    if missing:
        print("no coordinates for:", missing)
    run("cities-capitals", D, sys.argv[1:] or None)
