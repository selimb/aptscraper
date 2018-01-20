# from .database import get_jobs


def run_job(job_id):
# Setup logging -- threading.local
# Obtain job queries, hoods, to_email -- database.py
# Loop through queries
#   store = get_store(job_id, scraper)
#   crawl(base_url, hoods, to_email, store)

# call engine.run with queries, hoods, to_email, listing_store
# Loop through queries:
#    Collect listings
#       Request url -- REQUESTS
#       Run scraper for url

#    Filter data_id (exclude those in DB) -- DB
#    List of ad URLs to scrape
#    Scrape all URLs -- REQUESTS
#    Filter by geo
#    Send mail -- MAIL
    pass
