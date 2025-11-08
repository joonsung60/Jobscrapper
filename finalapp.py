from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup

def scrape_wanted(keyword):
    jobs = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"https://www.wanted.co.kr/search?query={keyword}&tab=position")
        for i in range(2):
            time.sleep(1.5)
            page.keyboard.down("End")
        soup = BeautifulSoup(page.content(), "html.parser")
        cards = soup.find_all("div", class_="JobCard_container__zQcZs")
        for card in cards:
            link = f"https://www.wanted.co.kr{card.find('a')['href']}"
            title = card.find("strong", class_="JobCard_title___kfvj").text
            company = card.find("span", class_="CompanyNameWithLocationPeriod_CompanyNameWithLocationPeriod__company__ByVLu").text
            jobs.append({"title": title, "company": company, "link": link, "source": "Wanted"})
        browser.close()
    return jobs


def scrape_berlin(keyword):
    jobs = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"https://berlinstartupjobs.com/skill-areas/{keyword}/")
        for i in range(2):
            time.sleep(1.5)
            page.keyboard.down("End")
        soup = BeautifulSoup(page.content(), "html.parser")
        cards = soup.find_all("li", class_="bjs-jlid")
        for card in cards:
            link = card.find("h4", class_="bjs-jlid__h").find("a")["href"]
            title = card.find("h4", class_="bjs-jlid__h").text
            company = card.find("a", class_="bjs-jlid__b").text
            jobs.append({"title": title, "company": company, "link": link , "source": "BerlinStartupJobs"})
        browser.close()
    return jobs


def scrape_wework(keyword):
    jobs = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term={keyword}")
        for i in range(2):
            time.sleep(1.5)
            page.keyboard.down("End")
        soup = BeautifulSoup(page.content(), "html.parser")
        cards = soup.find_all("li", class_="new-listing-container")
        for card in cards:
            a = card.find("a", class_="listing-link--unlocked")
            href = a["href"]
            link = "https://weworkremotely.com" + href
            title = card.find("h3", class_="new-listing__header__title").text
            company = card.find("p", class_="new-listing__company-name").text
            jobs.append({"title": title, "company": company, "link": link, "source": "WeWorkRemotely"})
        browser.close()
    return jobs


def scrape_web3(keyword):
    jobs = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f"https://web3.career/{keyword}-jobs")
        for i in range(2):
            time.sleep(1.5)
            page.keyboard.down("End")
        soup = BeautifulSoup(page.content(), "html.parser")
        cards = soup.select('tr.table_row[data-jobid]')
        for card in cards:
            link = f"https://web3.career{card.find('a')['href']}"
            title = card.find("h2").text
            company = card.find("h3").text
            jobs.append({"title": title, "company": company, "link": link, "source": "Web3.Career"})
        browser.close()
    return jobs


def extract_jobs(keyword):
    results = []
    results.extend(scrape_wanted(keyword))
    results.extend(scrape_berlin(keyword))
    results.extend(scrape_wework(keyword))
    results.extend(scrape_web3(keyword))
    return results
