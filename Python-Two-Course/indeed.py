import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://www.indeed.com/jobs?q=python&limit={LIMIT}"


def get_last_page():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    #indeed_result.text => html추출

    pagination = soup.find("div", {"class": "pagination"})
    #indeed_soup.find => 주요 정보 추출

    links = pagination.find_all('a')
    pages = []

    for link in links[:-1]:
        pages.append(int(
            link.find("span").string))  #span만 가져와 그 중 span의 글씨를 가져옴

    max_page = pages[-1]
    return max_page

    #for n in range(max_page):
    #range는 배열 만드는데 편리한 기능
    #print(f"start={n*50}")


def extract_job(html):
    title = html.find("h2", {"class": "title"}).find("a")["title"]
    company = html.find("span", {"class": "company"})
    company_anchor = company.find("a")
    if company:
        if company_anchor is not None:
            company = str(company_anchor.string)
        else:
            company = str(company.string)
    else:
        company = None
    company = company.strip()
    #strip()은 인자에 들어가는 값을 없애줌, 공백을 없앰
    location = html.find("div", {"class": "recJobLoc"})["data-rc-loc"]
    job_id = html["data-jk"]
    return {
        'title': title,
        'company': company,
        'location': location,
        "apply_link": f"https://www.indeed.com/viewjob?jk={job_id}"
    }


def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping Indeed: page: {page}")
        result = requests.get(f"{URL}&start={page*LIMIT}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
        #find_all은 여러개의 결과를 리스트로 가져오고 find는 첫번째 결과만 가져온다.
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs():
    last_pages = get_last_page()
    jobs = extract_jobs(last_pages)
    return jobs
