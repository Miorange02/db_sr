from DrissionPage import ChromiumPage, ChromiumOptions
import requests
import os
from concurrent.futures import ThreadPoolExecutor

# 创建页面对象
co = ChromiumOptions()
#无头模式
co.headless()
page = ChromiumPage(co)

def download_image(char_name, img_url):
    """下载单张图片"""
    try:
        # 下载图片
        response = requests.get(img_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        response.raise_for_status()

        # 用角色名字命名文件（替换非法字符，避免文件名错误）
        safe_name = char_name.replace("/", "-").replace("\\", "-")  # 替换可能引起路径问题的字符
        img_path = os.path.join('/illustration', f"{safe_name}.webp")
        # 保存图片
        with open(img_path, 'wb') as f:
            f.write(response.content)
        print(f"✅ 下载成功: {char_name}.webp")

    except requests.exceptions.RequestException as e:
        print(f"❌ 下载失败（{char_name}）: {e}")
    except Exception as e:
        print(f"❌ 处理 {char_name} 时出错: {e}")

try:
    # 访问目标网页
    url = "https://bbs.mihoyo.com/sr/wiki/channel/map/17/18?bbs_presentation_style=no_header"
    page.get(url)

    # 获取所有角色名字和图片元素
    name_elements = page.eles('.large-model-card__name')  # 名字元素
    icon_elements = page.eles('.large-model-card__icon')  # 图片元素

    # 确保名字和图片数量匹配,我不知道为什么匹配不上 /流汗
    # if len(name_elements) != len(icon_elements):
    #     print("⚠️ 名字和图片数量不匹配！")
    #     exit()

    # 创建目录保存图片
    os.makedirs('static/illustration', exist_ok=True)

    # 使用线程池并发下载图片
    with ThreadPoolExecutor(max_workers=5) as executor:  # 设置线程池大小
        for name_ele, icon in zip(name_elements, icon_elements):
            char_name = name_ele.text.strip()  # 获取角色名（去掉前后空格）
            img_url = icon.attr('data-src')   # 获取图片URL

            if not img_url:
                print(f"❌ {char_name} 未找到图片URL")
                continue

            # 提交下载任务到线程池
            executor.submit(download_image, char_name, img_url)

except Exception as e:
    print(f"❌ 页面访问或解析失败: {e}")

finally:
    page.close()
    print("爬取结束")