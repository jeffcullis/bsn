import wikipediaapi
import requests
import json

class PlantWiki:
    USER_AGENT = "PlantLookup/0.1 (https://jeffcullis.github.io jeffcullis@gmail.com)"
    WIKI_IMAGE_REQUEST = 'http://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles='

    def __init__(self):
        self._headers = {'User-Agent': self.USER_AGENT}
        self._wiki_api = wikipediaapi.Wikipedia('en', headers=self._headers)

    def _get_page(self, page_title):
        # Get the Wikipedia page
        page = self._wiki_api.page(page_title)
        if not page.exists():
            #raise ValueError(f"Wikipedia page '{page_title}' does not exist.")
            print(f"No Wikipedia page found for '{page_title}'")
            return None
        return page

    def _get_description(self, page):
        # Extract the summary (description) and add the source link
        description = page.summary
        description += f" [Source: {page.fullurl}]"
        return description

    def _get_image_url(self, page_title):
        # Use the Wikipedia API to fetch the main image URL
        response = requests.get(self.WIKI_IMAGE_REQUEST + page_title, headers=self._headers)
        if response.status_code != 200:
            raise ValueError(f"Failed to fetch image URL. HTTP status code: {response.status_code}")
        json_data = json.loads(response.text)
        img_link = list(json_data['query']['pages'].values())[0].get('original', {}).get('source')
        return img_link

    def get_wiki_data(self, page_title):
        # Fetch the page
        page = self._get_page(page_title)
        description = ''
        image_url = ''
        if page:
            # Get the description and image URL
            description = self._get_description(page)
            image_url = self._get_image_url(page_title)
        return description, image_url
