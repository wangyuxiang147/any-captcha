import pycapt
from PIL import Image

# dele_noise ：消除噪点方法，该方法使用的是八领域去噪点法，N 是领域异点个数，Z 是处理次数，处理次数越多 图形越圆滑。
# 原理是通过判断像素点与临近8个背景像素点的区别来去除噪点，当周围超过n个（一般设置5～7）与自身不同当像素时，则判断这个像素为噪点，
# 将噪点转化为与周围大多数像素一样的像素。这次实战感受非常深的一点 就是 从众法则：只要和大多数一样 那就看上去没有什么错。

# dele_line : 去除干扰线，删除连续的 N 个竖直像素。配合 dele_noise 方法使用效果更佳。
img = Image.open('./output/icp/11111.gif')

img = pycapt.tran_90(img)
img = pycapt.dele_line(img, 1)
img = pycapt.dele_noise(img, N=2, Z=2)
img = pycapt.tran_90(img)

# img.show()
img.save("./output/icp/11111_pycapt.gif")


"""
    去除图片噪点
"""
from io import BytesIO
from PIL import Image, ImageOps


class ReduceImgNoise:
    def sum_9_region_new(self, img, x, y):
        '''确定噪点 '''
        cur_pixel = img.getpixel((x, y))  # 当前像素点的值
        width = img.width
        height = img.height

        if cur_pixel == 1:  # 如果当前点为白色区域,则不统计邻域值
            return 0

        # 因当前图片的四周都有黑点，所以周围的黑点可以去除
        # if y < 3:  # 本例中，前两行的黑点都可以去除
        if y < 1:  #
            return 1
        elif y > height - 3:  # 最下面两行
            return 1
        else:  # y不在边界
            if x < 3:  # 前两列
                return 1
            elif x == width - 1:  # 右边非顶点
                return 1
            else:  # 具备9领域条件的
                sum = img.getpixel((x - 1, y - 1)) \
                      + img.getpixel((x - 1, y)) \
                      + img.getpixel((x - 1, y + 1)) \
                      + img.getpixel((x, y - 1)) \
                      + cur_pixel \
                      + img.getpixel((x, y + 1)) \
                      + img.getpixel((x + 1, y - 1)) \
                      + img.getpixel((x + 1, y)) \
                      + img.getpixel((x + 1, y + 1))
                return 9 - sum

    def collect_noise_point(self, img):
        '''收集所有的噪点'''
        noise_point_list = []
        for x in range(img.width):
            for y in range(img.height):
                res_9 = self.sum_9_region_new(img, x, y)
                if (0 < res_9 < 3) and img.getpixel((x, y)) == 0:  # 找到孤立点
                    pos = (x, y)
                    noise_point_list.append(pos)
        return noise_point_list

    def remove_noise_pixel(self, img, noise_point_list):
        '''根据噪点的位置信息，消除二值图片的黑点噪声'''
        for item in noise_point_list:
            img.putpixel((item[0], item[1]), 1)

    def get_bin_table(self, threshold=115):
        '''获取灰度转二值的映射table,0表示黑色,1表示白色'''
        table = []
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)
        return table

    def get_barry(self, content, threshold=115):
        '''
        降噪
        :param content:
        :return:
        '''
        image = Image.open(BytesIO(content))  # 读二进制
        # image = ImageOps.expand(image, border=5, fill=255)
        imgry = image.convert('L')

        table = self.get_bin_table(threshold)  # 75 0.3 | 115 0.4 | 80 0.22 0.32 | 78 0.24 0.26 nhc
        binary = imgry.point(table, '1')
        noise_point_list = self.collect_noise_point(binary)
        self.remove_noise_pixel(binary, noise_point_list)
        imgByteArr = BytesIO()

        binary.save(imgByteArr, format='JPEG')
        imgByteArr = imgByteArr.getvalue()  # 获取二进制
        return imgByteArr

if __name__ == '__main__':
    new_img = ReduceImgNoise().get_barry(open('./output/icp/11111.gif', 'rb').read())
    # Image.open(BytesIO(new_img)).show()
    Image.open(BytesIO(new_img)).save("./output/icp/11111_ReduceImgNoise.gif")
