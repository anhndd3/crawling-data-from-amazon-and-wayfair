import re
from typing import List

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By

from .data import WayFairProduct, AmazonProductDetail, AmazonProductRanking
from .interact_page import get_element, get_elements
from .log import logger, exception


@exception(logger)
def fetch_amazon_product_ranking(driver: WebDriver) -> List[AmazonProductRanking]:
    products: List[AmazonProductRanking] = []
    contents = get_elements(
        driver=driver,
        by=By.CSS_SELECTOR,
        value='div.a-column.a-span12.a-text-center._cDEzb_grid-column_2hIsc'
    )
    if (contents):
        logger.info('Amazon Product Ranking: Getting data')
        for content in contents:
            name = get_element(
                driver=content,
                by=By.XPATH,
                value='//div/div[2]/div/a[2]/span/div'
            )
            rank = get_element(
                driver=content,
                by=By.CLASS_NAME,
                value='zg-bdg-text'
            )
            url = get_element(
                driver=content,
                by=By.XPATH,
                value='//div/div[2]/div/a[2]'
            )
            price = get_element(
                driver=content,
                by=By.CLASS_NAME,
                value='p13n-sc-price'
            )
            if not price:
                price = get_element(
                    driver=content,
                    by=By.CLASS_NAME,
                    value='_cDEzb_p13n-sc-price_3mJ9Z'
                )
            products.append(AmazonProductRanking(
                rank=getattr(rank, 'text', None),
                name=getattr(name, 'text', None),
                price=getattr(price, 'text', None),
                url=url.get_attribute('href') if url else None
            ))
        logger.info(f'Amazon Product Ranking: {len(products)}')
    else:
        logger.warning(
            'Amazon Product Ranking: Not have any contents or change content elements')
        return []
    return products


@exception(logger)
def fetch_amazon_product_detail(driver: WebDriver) -> AmazonProductDetail | None:
    product: AmazonProductDetail
    left_content = get_element(
        driver=driver,
        by=By.CSS_SELECTOR,
        value='div#leftCol'
    )
    center_content = get_element(
        driver=driver,
        by=By.CSS_SELECTOR,
        value='div#centerCol'
    )

    if left_content and center_content:
        logger.info('Amazon Product Detail: Getting data')
        title = get_element(
            driver=center_content,
            by=By.CSS_SELECTOR,
            value='span.a-size-large.product-title-word-break'
        )
        rating = get_element(
            driver=center_content,
            by=By.CSS_SELECTOR,
            value='span.a-icon-alt'
        )
        rating_count = get_element(
            driver=center_content,
            by=By.CSS_SELECTOR,
            value='span.a-size-base'
        )
        list_price = get_element(
            driver=center_content,
            by=By.CSS_SELECTOR,
            value='span.a-offscreen'
        )
        int_price = get_element(
            driver=center_content,
            by=By.CSS_SELECTOR,
            value='span.a-price-whole'
        )
        fraction_price = get_element(
            driver=center_content,
            by=By.CSS_SELECTOR,
            value='span.a-price-fraction'
        )
        image_url = get_element(
            driver=left_content,
            by=By.CSS_SELECTOR,
            value='div.imgTagWrapper > img'
        )
        new_price = f'{getattr(int_price, "text", "")}.{getattr(fraction_price, "text", "")}'
        product = AmazonProductDetail(
            title=getattr(title, 'text', None),
            new_price=new_price,
            list_price=getattr(list_price, 'text', None),
            rating=getattr(rating, 'text', None),
            rating_count=getattr(rating_count, 'text', None),
            image_url=image_url.get_attribute('src') if image_url else None
        )
        logger.info(f'Amazon Product Detail: {product}')
    else:
        logger.warning(
            'Amazon Product Detail: Not have any contents or change content elements')
        return None

    return product


@exception(logger)
def fetch_wayfair_product_detail(driver: WebDriver) -> List[WayFairProduct]:
    def extract_rating(rating: str, pattern: str):
        rating = re.findall(rating, pattern)
        if rating:
            return rating[0]
        return ''

    products: List[WayFairProduct] = []
    contents = get_elements(
        driver=driver,
        by=By.CSS_SELECTOR,
        value='div.TrackedProductCardWrapper-inView > div > a'
    )

    if contents:
        logger.info('Wayfair Product Detail - Getting data')
        for content in contents:
            title = get_element(
                driver=content,
                by=By.CSS_SELECTOR,
                value='h2.kb51y90_6101.kb51y91_6101'
            )
            brand = get_element(
                driver=content,
                by=By.CSS_SELECTOR,
                value='p._1vgix4w0_6101._1vgix4w2_6101._1vgix4w6_6101'
            )
            rating = get_element(
                driver=content,
                by=By.CSS_SELECTOR,
                value='p.vdvxm0_6101'
            )
            rating_count = get_element(
                driver=content,
                by=By.CSS_SELECTOR,
                value='div._1xxktfua_6101.undefined'
            )
            list_price = get_element(
                driver=content,
                by=By.CSS_SELECTOR,
                value='s.oakhm627_6101.oakhm6y5_6101.oakhm610g_6101.oakhm6aj_6101'
            )
            shipping_fee = get_element(
                driver=content,
                by=By.CSS_SELECTOR,
                value='div > p.oakhm65j_6101.oakhm610g_6101.oakhm6b3_6101.nhya890_6101.nhya891_6101'
            )
            if not shipping_fee:
                shipping_fee = get_element(
                    driver=content,
                    by=By.CSS_SELECTOR,
                    value='span.ShippingBadge-text'
                )
            new_price = get_element(
                driver=content,
                by=By.CSS_SELECTOR,
                value='span.oakhm627_6101.oakhm6y5_6101.oakhm610g_6101.oakhm6aj_6101'
            )
            sponsored = get_element(
                driver=content,
                by=By.CSS_SELECTOR,
                value='div.FeaturedProductFlag'
            )

            products.append(WayFairProduct(
                title=getattr(title, 'text', None),
                brand=getattr(brand, 'text', None),
                new_price=getattr(new_price, 'text', None),
                list_price=getattr(list_price, 'text', None),
                rating=extract_rating(getattr(rating, 'text', ''), '\.(\d+)'),
                rating_count=getattr(rating_count, 'text', None),
                sponsored=True if getattr(sponsored, 'text', False) else False,
                shipping_fee=getattr(shipping_fee, 'text', None),
            ))
        logger.info(f'Wayfair Product Detail: {len(products)}')
    else:
        logger.warning(
            'Wayfair Product Detail: Not have any contents or change content elements')
        return []

    return products
