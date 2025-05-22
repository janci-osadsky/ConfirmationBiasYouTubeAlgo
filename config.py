link = "https://www.youtube.com"

settings_btn = ('/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[1]/'
                'div[2]/div/div[2]/ytd-player/div/div/div[26]/div[2]/div[2]/button[4]')
settings_btn2 = ('/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[1]/'
                 'div[2]/div/div[2]/ytd-player/div/div/div[28]/div[2]/div[2]/button[4]')
consent = ('/html/body/ytd-app/ytd-consent-bump-v2-lightbox/tp-yt-paper-dialog/div[4]/div[2]/div[6]/'
           'div[1]/ytd-button-renderer[2]/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]')

recommended = "a.yt-simple-endpoint.style-scope.ytd-compact-video-renderer"
API_KEY = "YOUR API KEY"

long_delay = 5
short_delay = 2
click_delay = 0.5


# manuálne vytvorené vážené slovníky pre témy záujmu
search_query = ["crypto","steroids", "MRNA vakcína", "crypto"]

keyword_weights = [
    # Crypto (index 0)
    {
        "bitcoin": 5, "btc": 4, "candlestick": 4, "crypto": 5, "trading": 5, "cryptocurrency": 4, "blockchain": 3,
        "ethereum": 3, "eth": 3, "token": 2, "tokens": 2, "web3": 3, "defi": 3,
        "nft": 2, "staking": 2, "altcoin": 2, "altcoins": 2,
        "money": 1,
        "solana": 3, "cardano": 3, "binance": 3,
        "trading": 4, "trader": 3, "investing": 5, "investment": 4,
        "forex": 3, "stock market": 4, "financial": 2, "income": 2, "portfolio": 3
    },
    # Steroids (index 1)
    {
        "steroid": 5, "sermorelin": 5, "anabolic": 4, "anabolics": 4,
        "performance enhancing": 4, "doping": 3, "testosterone": 4,
        "trenbolone": 4, "growth hormone": 3, "muscle gain": 3,
        "growth": 3, "bodybuilding": 4, "supplements": 3,
        "performance drugs": 3, "peds": 4, "hormone therapy": 3,
        "androgen": 2, "cycle": 3, "pct": 3, "sarms": 4, "gh": 2, "hgh": 3
    },
    # Vaccines (index 2) – SLOVENSKÁ DEZINFORMAČNÁ SCÉNA
    {
        "vakcína": 5, "účinky": 3, "účinok": 3, "očkovanie": 4, "neočkujem": 5, "očkovaný": 4, "nežiaduce": 3,
        "vedľajšie": 3, "mrna": 4, "pfizer": 5, "moderna": 4, "astrazeneca": 4, "booster": 3, "svedectvo": 3,
        "dávka": 3, "poškodenie": 2, "experimentálna": 2, "pandémia": 5, "hoax": 3, "big pharma": 4, "konšpirácia": 3,
        "agenda": 3,  "globálny reset": 5, "covid": 4, "kovid": 4, "farmaceut": 3, "zabitý": 3, "genocída": 3,
        "centrá": 2, "totalita": 3, "biologická zbraň": 5, "tajomstvo" : 3,"nechcú povedať": 2, "antivax" : 5
    },
    # Crypto (index 3)
    {
        "bitcoin": 5, "btc": 4, "candlestick": 4, "crypto": 5, "trading": 5, "cryptocurrency": 4, "blockchain": 3,
        "ethereum": 3, "eth": 3, "token": 2, "tokens": 2, "web3": 3, "defi": 3,
        "nft": 2, "staking": 2, "altcoin": 2, "altcoins": 2,
        "money": 1,
        "solana": 3, "cardano": 3, "binance": 3,
        "trading": 4, "trader": 3, "investing": 5, "investment": 4,
        "forex": 3, "stock market": 4, "financial": 2, "income": 2, "portfolio": 3
    }
]

min_seed = 1
max_seed = 20
