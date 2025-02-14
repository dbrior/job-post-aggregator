from site_scrapers.hutchinson_and_bloodgood import hutchinson_and_bloodgood
from site_scrapers.cohn_reznick import cohn_reznick
from site_scrapers.gursey import gursey
from site_scrapers.eisner import eisner
from site_scrapers.eidebailly import eidebailly
from site_scrapers.armanino import armanino
from site_scrapers.kearny import kearny

from custom_selenium_utils import *

import os
import psycopg2

sites = [
    {
        "name": "hutchinson_and_bloodgood",
        "processor": hutchinson_and_bloodgood,
        "url": 'https://workforcenow.adp.com/mascsr/default/mdf/recruitment/recruitment.html?cid=f875368a-3030-4c9c-a17d-de78d91f27fc&ccId=19000101_000001&type=MP&lang=en_US'
    },
    {
        "name": "cohn_reznick",
        "processor": cohn_reznick,
        "url": 'https://www.cohnreznick.com/careers/experienced-professional-opportunities'
    },
    {
        "name": "gursey",
        "processor": gursey,
        "url": 'https://www.gursey.com/careers-at-gursey-schneider/openings/'
    },
    {
        "name": "eisner",
        "processor": eisner,
        "url": 'https://careers.eisneramper.com/en/career-opportunities/'
    },
    {
        "name": "eidebailly",
        "processor": eidebailly,
        "url": 'https://careers.eidebailly.com/experienced-careers/jobs'
    },
    {
        "name": "armanino",
        "processor": armanino,
        "url": 'https://armaninollp.wd1.myworkdayjobs.com/Armanino'
    },
    {
        "name": "kearny",
        "processor": kearny,
        "url": 'https://careers.kearneyco.com/jobs?page=1'
    },
]

print("Starting scrarping...")

if __name__ == '__main__':
    browser = create_chrome_stealth_browser(isHeadless=True)
    
    print("", flush=True)
    
    jobs = []
    for site in sites:
        name = site['name']
        url = site['url']
        processor_func = site['processor']
        
        print((('-'*10) + name + ('-'*10)), flush=True)
        try:
            job_postings = processor_func(browser, url)
            for job_posting in job_postings:
                job_posting.update({'firm': name})
            jobs += job_postings
            print((f"Got {len(job_postings)} jobs"), flush=True)
        except Exception as e:
            print(("FAILED"), flush=True)
            print((e), flush=True)
        print((('-'*10) + ('-'*len(name)) + ('-'*10)), flush=True)
        print("", flush=True)
        
    print((f"Pulled {len(jobs)} job postings in total"), flush=True)
    print("", flush=True)
    
    print(("Writing to databse"), flush=True)
    
    DATABASE_URL = os.getenv("DATABASE_URL")
    TABLE_NAME = 'listings'

    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    # Drop current table
    drop_table_query = f"DROP TABLE IF EXISTS {TABLE_NAME};"
    cur.execute(drop_table_query)

    # Create table if it doesn't exist
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        id SERIAL PRIMARY KEY,
        firm TEXT NOT NULL,
        title TEXT NOT NULL,
        location TEXT NOT NULL,
        url TEXT NOT NULL
    );
    """
    cur.execute(create_table_query)

    # Insert query
    query = f"INSERT INTO {TABLE_NAME} (firm, title, location, url) VALUES (%s, %s, %s, %s);"

    # Convert list of dicts to tuples
    values = [(d.get("firm", "unknown_firm"), d.get("title", "unknown_title"), d.get("location", "unknown_location"), d.get("url", "location_url")) for d in jobs]

    cur.executemany(query, values)

    conn.commit()
    cur.close()
    conn.close()
    
    print(("Complete"), flush=True)
    