import mechanicalsoup
import re
import os


# Function to check for valid url.


def validate_url(url):
    regex = "^((http|https)://)[-a-zA-Z0-9@:%._\\+~#?&//=]{2,256}\\.[a-z]{2,6}\\b([-a-zA-Z0-9@:%._\\+~#?&//=]*)$"
    r = re.compile(regex)

    if r.match(url):
        return True
    else:
        return False


# WEB scraping utiltiy function to download files from a given url


def scrape(directory, url):
    # Init
    browser = mechanicalsoup.StatefulBrowser()
    log = {}
    browser.open(str(url))

    # Get course name for directory naming and mkdir
    course_name = url[url.rfind("/", 0, len(url) - 1) + 1 : url.rfind("/")]
    directory = f"{directory}/{course_name}"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Find course nav-links "Mobile used for ease of targeting"
    page_div = browser.page.find("div", id="mobile-course-nav")
    nav_links = page_div.find_all("a")
    for pg in nav_links:
        try:
            # Follow nav links
            browser.follow_link(pg)

            # Make new folders for each type of content
            pg_url = browser.url
            folder_names = pg_url[
                pg_url.rfind("/", 0, len(pg_url) - 1) + 1 : len(pg_url) - 1
            ]
            new_dir = f"{directory}/{folder_names}"
            if not os.path.exists(new_dir):
                os.makedirs(new_dir)

            # Follow links for each catagory
            for link in browser.page.find_all("a", href=re.compile("/resources/")):
                try:
                    # Follow each resource
                    browser.follow_link(link)

                    # Find download links only
                    download_link = browser.page.find(
                        "a", attrs={"class": "download-file"}
                    )

                    # Find video links only
                    video_link = browser.page.find(
                        "a", attrs={"aria-label": "Download video"}
                    )
                    # if video_link is not None:
                    #     video_link = video_link.get("href")
                    #     if video_link.endswith(".mp4"):
                    #         name = video_link[
                    #             video_link.rfind("/") + 1 : video_link.find(".mp4") + 4
                    #         ]
                    #     browser.download_link(link=video_link, file=f"{new_dir}/{name}")

                    # Check for materials
                    if download_link is not None:
                        download_link = download_link.get("href")
                        string_link = str(download_link)

                        # Handle Zip files
                        if string_link.endswith(".zip"):
                            name = string_link[
                                string_link.rfind("_")
                                + 1 : string_link.find(".zip")
                                + 4
                            ]

                        # Handle Pdf Files
                        elif string_link.endswith(".pdf"):
                            name = string_link[
                                string_link.rfind("_")
                                + 1 : string_link.find(".pdf")
                                + 4
                            ]

                        # Downloading...
                        browser.download_link(
                            link=download_link,
                            file=f"{new_dir}/{name}",
                        )

                        # log where it was taken from and name Success
                        log[string_link] = name
                    else:
                        continue
                except:
                    download_error = ("Download Link Error",)
                    return list(download_error)
            browser.open(url)
        except:
            navigation_error = ("Navigation Link Error",)
            return navigation_error

    browser.close()
    return list(log.items())
