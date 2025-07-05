from seleniumwire import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time, os, json, re
from datetime import datetime

os.makedirs('screenshots', exist_ok=True)
os.makedirs('network_logs', exist_ok=True)

def clean_text(text):
    # Remove control and non-printable characters from text
    return re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)

def take_screenshot(driver, status, portal_name=""):
    # Save screenshot with timestamp and status in filename
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = portal_name.replace(" ", "_") if portal_name else "general"
    filename = f"screenshots/{safe_name}_{status}_{ts}.png"
    driver.save_screenshot(filename)
    print(f"📸 Screenshot saved: {filename}")

def save_network_log(driver, portal_name=""):
    # Save network requests with response bodies in JSON file
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = portal_name.replace(" ", "_") if portal_name else "general"
    filename = f"network_logs/network_log_{safe_name}_{ts}.json"
    log_data = []
    for req in driver.requests:
        if req.response:
            try:
                body = req.response.body.decode('utf-8', errors='replace')
                body = clean_text(body)
            except Exception:
                body = ""
            log_data.append({
                "url": req.url,
                "status_code": req.response.status_code,
                "body": body
            })
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(log_data, f, indent=2, ensure_ascii=False)
    print(f"🧞 Network log saved: {filename}")
    return log_data

def type_for_duration(driver, input_box, words, delay, word_delay, duration=30):
    # Type words continuously until duration (seconds) expires
    start_time = time.time()
    while True:
        for word in words:
            for letter in word:
                if time.time() - start_time >= duration:
                    return
                input_box.send_keys(letter)
                time.sleep(delay)
            input_box.send_keys(" ")
            time.sleep(word_delay)
            if time.time() - start_time >= duration:
                return

def monkeytype_typing_test(driver, speed="normal"):
    driver.requests.clear()
    driver.get("https://monkeytype.com/")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "words")))

    try:
        reject_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[10]/dialog/div[2]/div[2]/div[2]/button[2]"))
        )
        reject_btn.click()
        print("🍪 Cookies rejected.")
        time.sleep(1)
    except Exception:
        print("🍪 Cookie modal not found.")

    input_box = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "wordsInput")))
    ActionChains(driver).move_to_element(input_box).click().perform()
    input_box.send_keys(Keys.SPACE)
    time.sleep(0.5)

    words_wrapper = driver.find_element(By.ID, "wordsWrapper")
    words_line = words_wrapper.find_elements(By.CSS_SELECTOR, "#words .word")
    words = []

    for word in words_line:
        letters = word.find_elements(By.CSS_SELECTOR, "letter")
        word_text = ''.join([l.get_attribute("textContent") for l in letters])
        words.append(word_text)

    print(f"📝 Typing for 30 seconds at speed '{speed}'...")

    # Speed settings: delay per letter, delay per word
    # Slow remains unchanged, others are 40% faster (multiplied by 0.6)
    base_speeds = {
        "slow": (0.07, 0.12),
        "normal": (0.025, 0.04),
        "fast": (0.015, 0.025),
        "super_fast": (0.004, 0.005),
        "legend": (0.0001, 0.0001)
    }

    if speed.lower() == "slow":
        delay, word_delay = base_speeds["slow"]
    else:
        delay, word_delay = base_speeds.get(speed.lower(), (0.025, 0.04))
        delay *= 0.1      # 40% faster = 60% original delay
        word_delay *= 0.1

    typing_start = time.time()
    type_for_duration(driver, input_box, words * 50, delay=delay, word_delay=word_delay, duration=30)
    typing_end = time.time()

    elapsed = typing_end - typing_start
    remaining = max(0, 40 - elapsed)  # wait total 40 sec on page
    time.sleep(remaining)

    take_screenshot(driver, "typed", "monkeytype")
    logs = save_network_log(driver, "monkeytype_typing")
    return {"portal": "MonkeyType", "status": "success"}

# WebDriver setup
options = {
    'seleniumwire_options': {},
}
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=chrome_options, **options)

results = []

try:
    print("\n🚀 Starting MonkeyType automation...\n")
    # Use one of: slow, normal, fast, super_fast, legend (case-insensitive)
    result = monkeytype_typing_test(driver, speed="legend")
    results.append(result)

except Exception as e:
    print(f"❌ Fatal script error: {e}")
    take_screenshot(driver, "fatal_error", "monkeytype")
    save_network_log(driver, "fatal_error")

finally:
    driver.quit()
    print("\n📋 Final Summary:")
    for r in results:
        print(f"• Portal: {r['portal']} → Status: {r['status'].upper()}")
