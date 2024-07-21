from DrissionPage import SessionOptions
so = SessionOptions()
so.set_a_header("user-agent","Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")
print(so.ini_path)
so.save()