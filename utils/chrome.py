from fake_useragent  import UserAgent

def getUserAgent():
    ua = UserAgent(browsers=["chrome"], platforms=["pc"])
    return ua.random.replace("Chrome/122", "Chrome/126")