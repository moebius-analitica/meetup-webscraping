import pytesseract as tess
from PIL import Image
import re
from chromeConfig import driver
import tessConfig
import config 

def captchatext(image):
    captcha_txt = tess.image_to_string(
        image = image,
        config = tessConfig.config_tesseract
    )
    captcha_txt = captcha_txt.upper().strip()
    captcha_txt = re.sub('[^A-Z]','',captcha_txt)
    return captcha_txt

driver = driver()
driver.get(config.url_tess)

driver.find_element_by_name('imagen').screenshot(tessConfig.captcha_name)
resolved_captcha = captchatext(tessConfig.captcha_name)

print(resolved_captcha)
