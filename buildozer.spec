[app]
title = MyVoiceApp
package.name = myvoiceapp
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy==2.2.1,kivymd==1.1.1,edge-tts,asyncio,certifi,urllib3==1.26.15
orientation = portrait
android.permissions = INTERNET, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
android.accept_sdk_license = True
android.api = 31
android.minapi = 21
android.sdk = 31
android.ndk = 25b
[buildozer]
log_level = 2
warn_on_root = 0
