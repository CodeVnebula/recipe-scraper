from typing import Generator

from bs4 import BeautifulSoup, ResultSet, Tag
from config import KULINARIA_URL
from utils import ScraperHelper

import json

scraper_helper = ScraperHelper()


class MainPageParser:
    def __init__(self, html: str | bytes) -> None:
        self.__soup = BeautifulSoup(html, "lxml")
        more = self.__soup.select_one(".endless_more")
        self.__next_url = more.attrs.get('href') if more is not None else None
        self.__has_next = bool(more)

    @property
    def has_next(self) -> bool:
        return self.__has_next

    @property
    def next_url(self) -> str:
        return KULINARIA_URL + self.__next_url

    @staticmethod
    def scrape_post(post: Tag) -> dict:
        """Scrape post with specific bs4 pots TAG"""
        box_title = post.select_one('.box__title')

        recipe_title = box_title.text.strip()
        recipe_url = box_title.attrs.get('href')
        if recipe_url:
            recipe_url = KULINARIA_URL + recipe_url

        image_url = post.select_one('.box__img img').attrs.get('src')
        if image_url:
            image_url = KULINARIA_URL + image_url

        description = post.select_one('.box__desc').get_text().strip()

        author = post.select_one('.name a').text.strip()

        return dict(
                title=recipe_title,
                recipe_url=recipe_url,
                image_url=image_url,
                description=description,
                author=author,
            )

    def get_posts(self) -> ResultSet[Tag]:
        return self.__soup.select(".box")

    def get_posts_dict(self) -> Generator[dict[str, any], None, None]:
        for post in self.get_posts():
            yield self.scrape_post(post)

    def __str__(self) -> str:
        return self.__soup.prettify()

    def __repr__(self) -> str:
        return f"MainPageParser({self.__soup.__str__()})"


class RecipeParser:
    def __init__(self, html: str | bytes) -> None:
        self.__soup = BeautifulSoup(html, "lxml")

    def parse(self, return_all_data: bool = True) -> dict:
        """Parse the HTML content of a recipe page."""
        post_title = self.__soup.select_one(".post__title")
        if post_title is not None:
            post_title = post_title.text.strip()

        main_category = self.__soup.select_one('.pagination__item:nth-last-of-type(2)')
        main_category_name = main_category.text.strip()
        main_category_url = main_category.attrs.get('href')
        main_category_url = (KULINARIA_URL + main_category_url) if main_category_url else None

        sub_category = self.__soup.select_one('.pagination__item:last-child')
        sub_category_name = sub_category.text.strip()
        sub_category_url = KULINARIA_URL + sub_category.attrs.get('href')

        try:
            data = json.loads(self.__soup.select_one('head script[type*="json"]').text.strip())
        except json.decoder.JSONDecodeError:
            data = None

        if data:
            image = data.get('image')
            description = data.get('description')
            author = data.get('author')
            recipe_ingredients = scraper_helper.replace_numbers(data.get('recipeIngredient', []))
            recipe_instructions = scraper_helper.index_steps(data.get('recipeInstructions', ''))
            servings = data.get('recipeYield')
            if servings:
                servings = servings.split(' loaf')[0]
                servings = int(servings) if servings.isdigit() else None
        else:
            if image := self.__soup.select_one('.post__img img'):
                image = KULINARIA_URL + image.attrs.get('src')

            if description := self.__soup.select_one('.post__description'):
                description = description.text.strip()

            if author := self.__soup.select_one('.post__author'):
                author = author.text.strip()

            servings = None
            if desc_items := self.__soup.select('.lineDesc__item'):
                for desc_item in desc_items:
                    if 'ულუფა' in desc_item.text:
                        try:
                            servings = int(desc_item.text.strip().split()[0])
                        except (IndexError, ValueError):
                            servings = None

                        break

            recipe_ingredients = []
            if recipe_ingredient_tag := self.__soup.select('.list__item'):
                for ingredient in recipe_ingredient_tag:
                    recipe_ingredients.append(
                        ingredient.text.strip()
                    )

                recipe_ingredients = [x for x in scraper_helper.replace_numbers(recipe_ingredients) if x]

            recipe_instructions = []
            if line_list := self.__soup.select('.lineList > div'):
                for index, l in enumerate(line_list):
                    step = index + 1 if (count := l.select_one('.count')) is None else scraper_helper.replace_numbers(
                        count.text
                    )[0]

                    recipe_instructions.append(
                        (int(step), scraper_helper.replace_numbers(l.find('p').text)[0])
                    )

        if not return_all_data:
            metadata = dict(
                    main_category={'title': main_category_name, 'url': main_category_url},
                    sub_category={'title': sub_category_name, 'url': sub_category_url},
                )

            if post_title is not None:
                metadata['title'] = post_title
            if image:
                metadata['image'] = image
            if description is not None:
                metadata['description'] = description
            if author:
                author = author.replace('ავტორი:', '').strip()
                metadata['author'] = author

            metadata['servings'] = servings
            metadata['ingredients'] = recipe_ingredients
            metadata['steps'] = recipe_instructions

            return metadata

        else:
            recipe_url = self.__soup.select_one('meta[property="og:url"]')
            if recipe_url is not None:
                recipe_url = "https://" + recipe_url.attrs.get('content')

            author = author.replace('ავტორი:', '').strip()
            return dict(
                title=post_title,
                recipe_url=recipe_url,
                main_category={'title': main_category_name, 'url': main_category_url},
                sub_category={'title': sub_category_name, 'url': sub_category_url},
                image_url=image,
                description=description,
                author=author,
                servings=servings,
                ingredients=recipe_ingredients,
                steps=recipe_instructions
            )

    def __str__(self) -> str:
        return self.__soup.prettify()

    def __repr__(self) -> str:
        return f"RecipeParser({self.__soup.__str__()})"
