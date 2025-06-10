def hh_ids_from_urls(urls: list[str]) -> list[str]:
    hh_job_ids = []
    for url in urls:
        hh_job_ids.append(url.split("/")[-1])
    return hh_job_ids