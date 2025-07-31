import os
import json
import time
import random
import requests

# 数据文件夹路径
data_dir = "./data/"
# 接口url
pokemon_api_url = "https://www.pokemon.cn/play/pokedex/api/v1"
img_url_path = "https://www.pokemon.cn/play/resources/pokedex"
# 判断数据文件夹是否存在
if not os.path.exists(data_dir):
    os.mkdir(data_dir)


# 更新数据
def update_pokemon_data(data_dir):
    response = requests.get(pokemon_api_url, timeout=5)
    with open(f"{data_dir}pokemon.json", "w", encoding="utf-8") as f:
        f.write(response.text)

# 图片路径检查
def safe_filename(name):
    return str(name).replace("\\", "_").replace("/", "_")

# 图片下载保存
def image_download(url, path):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        with open(path, "wb") as f:
            f.write(response.content)
    except Exception as e:
        print(f"图片下载失败：{url} -> {path}\n错误信息：{e}")

# 宝可梦图片下载
def download_pokemon_images(json_file, download_path=""):
    # 创建图片保存目录
    img_folder = download_path if download_path else os.path.join(os.path.dirname(json_file), "images")
    os.makedirs(img_folder, exist_ok=True)
    # 读取Pokemon数据
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    # 遍历Pokemon数据
    for i in data["pokemons"]:
        # 解析拼接图片名称
        image_name = safe_filename(
            f"{i['zukan_id']}_{i['pokemon_name']}" +
            (f"_{i['pokemon_sub_name']}" if i["pokemon_sub_name"] else "") + ".png"
        )
        # 拼接图片保存路径
        img_save_path = os.path.join(img_folder, image_name).replace("\\", "/")
        # 已存在的图片跳过下载
        if os.path.exists(img_save_path):
            print(f"{img_save_path} 已存在，跳过下载。")
            continue
        # 拼接图片URL
        pokemon_image_url = img_url_path + i["file_name"]
        print(f"正在下载全国图鉴编号{i['zukan_id']}的精灵图片：{image_name}")
        # 下载图片
        image_download(pokemon_image_url, img_save_path)
        # 随机等待
        time_sleep = round(random.uniform(0.5, 2), 2)
        print(f"等待{time_sleep}秒后继续。")
        time.sleep(time_sleep)
    image_num = len(os.listdir(img_folder))
    print(f"图片下载完成！共{image_num}张图片。")

def main():
    if not os.path.exists(data_dir + "pokemon.json"):
        update_pokemon_data(data_dir)
    download_pokemon_images(data_dir + "pokemon.json", "./images")


if __name__ == "__main__":
    main()
