BOT_NAME = "dotrac"

SPIDER_MODULES = ["dotrac.spiders"]
NEWSPIDER_MODULE = "dotrac.spiders"

ROBOTSTXT_OBEY = False
DOWNLOAD_DELAY = 1

FEEDS = {
    "ket_qua_dot_rac.csv": {
        "format": "csv",
        "overwrite": True
    }
}