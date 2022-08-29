# coding: utf-8

"""
target captcha url: http://www.miitbeian.gov.cn/getVerifyCode?4
"""
import json
import time

from model.capthafactory import CaptchaFactory


def custom_fn(single_char):
    # do something
    # return single_char.filter(ImageFilter.GaussianBlur)
    return single_char


def bg_custom_fn(bg):
    # do something
    # return bg.filter(ImageFilter.GaussianBlur)
    return bg


def main():
    project_name = "icp"
    with open("configs/icp.json", encoding="utf-8") as fp:
        demo_config = json.load(fp)

    # with open("configs/char/specific_chars.json", encoding="utf-8") as fp:
    #     specific = json.load(fp)

    demo_factory = CaptchaFactory(char_custom_fns=[custom_fn], bg_custom_fns=[bg_custom_fn], **demo_config)
    number = 5
    while number:
        # captcha = demo_factory.generate_captcha(specific_chars=specific)
        captcha = demo_factory.generate_captcha()
        # captcha.save("output/%s/%s.jpg" % (project_name, captcha.text))
        # captcha.save(f"C:/Users/Ad/Desktop/verification_code/6_code/{captcha.text}_{int(time.time()*1000)}.jpg")
        # file_path = f"C:/Users/Ad/Desktop/verification_code/4_code/{captcha.text}_{int(time.time() * 1000)}.jpg"

        # captcha.save(file_path)

        # --add---
        img = captcha.captcha.convert("L")
        file_path = f"C:/Users/Ad/Desktop/verification_code/4_code/{captcha.text}_{int(time.time() * 1000)}.gif"
        captcha.captcha.save(file_path, format='GIF')
        # --add---

        print(captcha.text, captcha.num)
        number -= 1


if __name__ == "__main__":
    main()
