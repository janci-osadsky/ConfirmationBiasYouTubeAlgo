
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

import random
import time
import API_scratch
import config
import filter_program
import undetected_chromedriver as uc

''' 
    Inicializuje a pripraví YouTube na Chrome browseri
'''
def init():
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized") # spusti na maximalnej velkosti okna
    # options.add_argument("--headless") # spusti bez otvorenia okna
    options.add_argument(r"--user-data-dir=C:/uc_logged_profile") # ukazuje na vlastny priecinok s kopiou chrome
    options.add_argument("--profile-directory=Default") # nastavit pre prihlaseneho pouzivatela
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = uc.Chrome(options=options)
    driver.get(config.link)
    handle_consent(driver) # pri neprihlasenom pouzivatelovi odklikne suhlas so spracovanim udajov
    time.sleep(config.short_delay)
    return driver


def handle_consent(driver):
    try:
        time.sleep(config.short_delay)
        accept_button = driver.find_element(
            By.XPATH, config.consent)
        driver.execute_script("arguments[0].click();", accept_button)
        print("Consent clicked.")
    except Exception as e:
        print("Consent not clicked:")


''' 
    Vyhľadá zadanú tému relevancie a klikne náhodne na relevantné (dlhé) video
'''
def search_and_click(driver, query):
    search_box = driver.find_element(By.NAME, "search_query")
    search_box.clear()
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)
    time.sleep(config.short_delay)
    video_list = driver.find_elements(By.ID, "video-title")
    suitable_videos = []
    for video in video_list:
        try:
            href = video.get_attribute("href")
        except: continue
        if href and "/watch?v=" in href and "/shorts/" not in href:
            suitable_videos.append(video)
        if len(suitable_videos) == 10 : break
    if not suitable_videos:
        print("No suitable video found.")
        driver.navigate().refresh();
        suitable_videos = driver.find_elements(By.ID, "video-title")
    clicked = random.choice(suitable_videos)
    driver.execute_script("arguments[0].click();", clicked)
    href = clicked.get_attribute("href")
    print(f"Clicked video: {href}")
    # wait out the ads
    time.sleep(90)

''' 
    Na otvorenom videi v browseri zoberie linky na prvých ´max_links´ počet linkov, ktoré vráti ako zoznam     
'''
def collect_recommendation_links(driver, max_links=15):
    print(f"Collecting up to {max_links} recommendation links...")

    video_elements = driver.find_elements(By.CSS_SELECTOR, "#items ytd-compact-video-renderer a#thumbnail")

    seen = set()
    links = []

    for el in video_elements:
        href = el.get_attribute("href")
        if href and "/watch?v=" in href and href not in seen:
            links.append(href)
            seen.add(href)
            print(f"{href}")

        if len(links) >= max_links:
            break

    return links


''' 
    Preklikáva sa dopredu videom náhodný počet sekúnd
'''
def seek_video(driver):
    num_times = random.randint(config.min_seed, config.max_seed)
    times = 0
    while times < num_times:
        webdriver.ActionChains(driver).key_down(Keys.ARROW_RIGHT).perform()
        time.sleep(0.25)
        times += 1
    return num_times * 5.25


''' 
    Stlačí nastavenia videa
'''
def click_settings(driver):
    try:
        settings_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button.ytp-button.ytp-settings-button"))
        )
        driver.execute_script("arguments[0].click();", settings_button)
        print("Settings button clicked.")
    except Exception as e:
        print("Failed to click settings:", e)


''' 
    Nastaví video na dvojitú rýchlosť
'''
def double_speed(driver):
    click_settings(driver)
    webdriver.ActionChains(driver).key_down(Keys.DOWN).perform()
    time.sleep(0.25)
    webdriver.ActionChains(driver).key_down(Keys.DOWN).perform()
    time.sleep(0.25)
    webdriver.ActionChains(driver).key_down(Keys.DOWN).perform()
    time.sleep(0.25)
    webdriver.ActionChains(driver).key_down(Keys.DOWN).perform()
    time.sleep(0.25)
    webdriver.ActionChains(driver).key_down(Keys.DOWN).perform()
    time.sleep(0.25)
    webdriver.ActionChains(driver).key_down(Keys.RIGHT).perform()
    time.sleep(0.25)
    webdriver.ActionChains(driver).key_down(Keys.DOWN).perform()
    time.sleep(0.25)
    webdriver.ActionChains(driver).key_down(Keys.DOWN).perform()
    time.sleep(0.25)
    webdriver.ActionChains(driver).key_down(Keys.DOWN).perform()
    time.sleep(0.25)
    webdriver.ActionChains(driver).key_down(Keys.DOWN).perform()
    time.sleep(0.25)
    webdriver.ActionChains(driver).key_down(Keys.ENTER).perform()
    time.sleep(0.25)

''' 
    Náhodne pohybuje myšou po browseri
'''
def random_mouse_movements(driver, duration=60):
    from selenium.webdriver.common.action_chains import ActionChains
    import random
    import time

    start_time = time.time()

    try:
        ActionChains(driver).move_by_offset(0, 0).perform()
    except:
        pass

    while time.time() - start_time < duration:
        try:
            x_offset = random.randint(-50, 50)
            y_offset = random.randint(-50, 50)
            ActionChains(driver).move_by_offset(x_offset, y_offset).perform()
            ActionChains(driver).reset_actions()
            time.sleep(random.uniform(1.5, 4.0))
        except Exception as e:
            print(f"Mouse move error: {e}")
            break



''' 
    Náhodne scrolluje po browseri hore dole, čím pomáha načítať bočnú lištu
'''
def mouse_scroll(driver, duration=60):
    start_time = time.time()

    while time.time() - start_time < duration:
        try:
            direction = random.choice(["up", "down", "down", "down"])
            amount = random.randint(100, 300)  # koľko pixelov
            if direction == "down":
                driver.execute_script(f"window.scrollBy(0, {amount});")
            else:
                driver.execute_script(f"window.scrollBy(0, -{amount});")
            time.sleep(random.uniform(3.0, 6.0))  # počkaj náhodný čas
        except Exception as e:
            print(f"Scroll error: {e}")
            break


''' 
    Zistí dĺžku aktuálne prehrávaného videa
'''
def get_video_duration(driver):
    try:
        duration_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "ytp-time-duration"))
        )
        duration_text = duration_element.text.strip()
        parts = list(map(int, duration_text.split(':')))
        if len(parts) == 2:
            minutes, seconds = parts
            return minutes * 60 + seconds
        elif len(parts) == 3:
            hours, minutes, seconds = parts
            return hours * 3600 + minutes * 60 + seconds
        return 0
    except Exception as e:
        try:
            duration_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "display.notranslate > span.ytp - time - wrapper > div > span.ytp - time - duration")))
            duration_text = duration_element.text.strip()
            minutes, seconds = map(int, duration_text.split(':'))
            return minutes * 60 + seconds
        except Exception as ex:
            print(f"Duration fetch failed: {e}")
            return 0
        print(f"Duration fetch failed: {e}")
        return 0

''' 
    Pokúsi sa dať "páči sa mi" na aktuálne video. Funguje len pri prihlásenom používateľovi.
'''
def like_current_video(driver):
    try:
        like_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                "ytd-toggle-button-renderer:nth-of-type(1) button"))
        )
        driver.execute_script("arguments[0].click();", like_button)
        print("👍 Video lajknuté (fallback selektor).")
    except Exception as e:
        print(f"❌ Nepodarilo sa lajknúť video (fallback): {e}")


''' 
    Heuristický model správania, ktorý kliká len na videá, ktoré sú v téme relevancie, ak nenájde tak vyhľadá nové
    ---
    pozbiera videá z bočného panelu, vyhodnotí, ktoré sú relevantné, uloži dáta a iteruje ďalej
    ---
    driver: undetected chromedriver prehliadača spustený na videu súvisiacom s témou relevancie
    topic: téma relevancie
    iterations: koľkokrát opakuje na tej istej téme výber relevantnej témy a zber dát
    filter_type: spôsob filtrovania (využili sme vážený slovník)
'''
def watcher(driver, topic, iterations, filter_type):
    for step in range(iterations):
        mouse_scroll(driver, 5)
        links = collect_recommendation_links(driver)
        with open("links.txt", "w", encoding="utf-8") as l:
            for link in links:
                l.write(link + "\n")
        API_scratch.main()
        filter_topic = 0
        filtered = []
        while filter_topic <= topic:
            filtered = filter_program.run_filter(filter_type, filter_topic)
            with open("results.txt", "a", encoding="utf-8") as f:
                f.write(f"{len(filtered)}, ")
            filter_topic += 1
        if not filtered:
            print("No relevant videos found. Going back.")
            with open("results.txt", "a", encoding="utf-8") as f:
                f.write(f", going back, link return, watcher, \n")
            search_and_click(driver, config.search_query[topic])
            time.sleep(config.long_delay)
            continue
        index = 0
        # ak by sme chceli zmeniť 100% šancu, že sa rozhodne pokračovať v téme
        relevant = True
        video_elements = driver.find_elements(By.CSS_SELECTOR, config.recommended)
        if relevant:
            index = random.choice(filtered)
            watch_time = random.randint(60, 70)
        else:
            non_filtered = [i for i in range(len(video_elements)) if i not in filtered]
            if not non_filtered:
                driver.back()
                continue
            index = random.choice(non_filtered)
            watch_time = 7
        link_to_save = video_elements[index].get_attribute("href")
        with open("results.txt", "a", encoding="utf-8") as f:
            f.write(f"next relevant: {relevant}, index: {index}, URL: {link_to_save}, watcher, \n")

        driver.execute_script("arguments[0].click();", video_elements[index])
        print(f"Watching for {watch_time} seconds...")
        mouse_scroll(driver, watch_time)

''' 
    Heuristický model správania, ktorý kliká interaguje s videami, ktoré sú v téme relevancie, a rýchlo kliká preč ak vstúpi na video mimo témy záujmu.
    Ak chce pokračovať na relevantné video a nenájde tak vyhľadá znova tému záujmu.
    ---
    pozbiera videá z bočného panelu, vyhodnotí, ktoré sú relevantné, uloži dáta a iteruje ďalej
    ---
    driver: undetected chromedriver prehliadača spustený na videu súvisiacom s témou relevancie
    topic: téma relevancie
    iterations: koľkokrát opakuje na tej istej téme výber relevantnej témy a zber dát
    filter_type: spôsob filtrovania (využili sme vážený slovník)
'''
def interacter(driver, topic, iterations, filter_type):
    for step in range(iterations):
        links = collect_recommendation_links(driver)
        with open("links.txt", "w", encoding="utf-8") as l:
            for link in links:
                l.write(link + "\n")
        API_scratch.main()
        filter_topic = 0
        filtered = []
        while filter_topic <= topic:
            filtered = filter_program.run_filter(filter_type, filter_topic)
            with open("results.txt", "a", encoding="utf-8") as f:
                f.write(f"{len(filtered)}, ")
            filter_topic += 1
        # nastaviteľná 65% šanca, že je video relevantné
        relevant = True if random.random() <= 0.65 and filtered else False
        if not filtered:
            print("No filtered videos found. Going back.")
            with open("results.txt", "a", encoding="utf-8") as f:
                f.write(f"going back, interacter\n")
            search_and_click(driver, config.search_query[topic])
            time.sleep(5)
            continue
        video_elements = driver.find_elements(By.CSS_SELECTOR, config.recommended)
        if relevant and filtered:
            index = random.choice(filtered)
            link_to_save = video_elements[index].get_attribute("href")
            with open("results.txt", "a", encoding="utf-8") as f:
                f.write(f"next relevant: {relevant}, index: {index}, URL: {link_to_save}, interacter\n")
            driver.execute_script("arguments[0].click();", video_elements[index])
            seek_video(driver)
            like_current_video(driver)
            random_mouse_movements(driver, random.randint(15, 30))
            mouse_scroll(driver, random.randint(15, 30))
        else:
            non_filtered = [i for i in range(len(video_elements)) if i not in filtered]
            if non_filtered:
                index = random.choice(non_filtered)
                link_to_save = video_elements[index].get_attribute("href")
                with open("results.txt", "a", encoding="utf-8") as f:
                    f.write(f"next relevant: {relevant}, index: {index}, URL: {link_to_save}, interacter\n")
                driver.execute_script("arguments[0].click();", video_elements[index])
                time.sleep(random.randint(3, 7))
                driver.back()
            else: driver.back()

''' 
    Pre úspešné vykonanie simulácie je nevyhnutné mať v config.py nastavené správne všetky parametre a stabilný prístup na internet.
    Main vykoná simuláciu podľa nastavených príznakov:    
    ---
    watcherBot: či začína simuláciu watcher, alebo interacter
    iterations: koľkokrát opakuje na tej istej téme výber relevantnej témy a zber dát
    filter_type: typ filtra, ktorým sa rozhoduje relevancia
'''
def main():
    driver = init()
    muted = False
    watcherBOT = True
    iterations = 1
    filter_type = "weighted"  # "basic" "cosine" "weighted" "old"
    for k in range(2):
        for i in range(config.search_query.count()):
            search_and_click(driver, config.search_query[i])
            if (not muted):
                webdriver.ActionChains(driver).send_keys('m').perform()
                muted = True
            time.sleep(10)
            with open("results.txt", "a", encoding="utf-8") as f:
                if (i == 0):
                    f.write("First topic: Crypto \n")
                elif (i == 1):
                    f.write("Second topic: Steroids \n")
                elif (i == 2):
                    f.write("Third topic: Vaccine \n")
                else:
                    f.write("Fourth topic: Crypto again \n")
            if (watcherBOT):
                watcher(driver, i, iterations, filter_type)
            else:
                interacter(driver, i, iterations, filter_type)
        watcherBOT = not watcherBOT
    driver.quit()


if __name__ == '__main__':
    main()
