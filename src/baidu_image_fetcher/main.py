from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests
import os
import mimetypes

def download_image(url, folder_path, idx):
    """下载图片并保存到指定文件夹

    Args:
        url (str): 图片的URL
        folder_path (str): 保存图片的文件夹路径
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # 如果请求失败，则引发异常

        # 获取文件后缀名
        content_type = response.headers['content-type']
        extension = mimetypes.guess_extension(content_type)

        # 获取文件名
        file_name = os.path.join(folder_path, str(idx) + extension)

        with open(file_name, 'wb') as f:
            f.write(response.content)

        print(f"Downloaded {url} to {file_name}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading {url}: {e}")

def get_image_urls(keyword, num_images, driver):
    """使用Selenium获取百度图片搜索结果中的图片URL

    Args:
        keyword (str): 搜索关键词
        num_images (int): 要下载的图片数量
        driver (webdriver): Selenium WebDriver 对象

    Returns:
        list: 图片URL列表
    """
    image_urls = []
    url = f"https://image.baidu.com/search/index?tn=baiduimage&z=3&ie=utf-8&word={keyword}"
    driver.get(url)

    # 模拟滚动加载更多图片
    while len(image_urls) < num_images:
        # 获取当前页面高度
        last_height = driver.execute_script("return document.body.scrollHeight")

        # 滚动到底部
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # 等待页面加载
        time.sleep(2)

        # 获取新的页面高度
        new_height = driver.execute_script("return document.body.scrollHeight")

        # 如果高度没有变化，则说明已经加载完毕
        if new_height == last_height:
            break

        # 提取图片URL
        img_elements = driver.find_elements(By.CSS_SELECTOR, 'img.main_img')
        for img_element in img_elements:
            image_urls.append(img_element.get_attribute('src'))

    return image_urls[:num_images]

def main():
    keyword = input("请输入要搜索的关键词: ")
    num_images = int(input("请输入要下载的图片数量: "))

    # 创建保存图片的文件夹
    folder_path = f"images/{keyword}"
    os.makedirs(folder_path, exist_ok=True)

    # 初始化 Selenium WebDriver
    # 请根据你的浏览器类型选择合适的 WebDriver
    # 例如，使用 Chrome 浏览器：
    driver = webdriver.Chrome()
    # 或者使用 Firefox 浏览器：
    # driver = webdriver.Firefox()

    try:
        # 获取图片URL
        image_urls = get_image_urls(keyword, num_images, driver)

        print(f'已得到{len(image_urls)}张图片! 准备下载...')
        
        # 下载图片
        for idx, url in enumerate(image_urls):
            download_image(url, folder_path, idx)
    finally:
        # 关闭浏览器
        driver.quit()

if __name__ == "__main__":
    main()