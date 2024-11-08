﻿import os
import cv2
import json

class VisualTusimple:
    """
    VisualTusimple 是一个用于可视化 TuSimple 数据集中的车道线的类。
    
    Attributes:
        json_path (str): 存储 JSON 文件路径的字符串，该文件包含图像及车道线的注释。
        line_colors (list): 一个可选的颜色列表，用于绘制车道线。
        data (dict): 从 JSON 文件加载的数据，包括图像路径和车道线信息。
        image (numpy.ndarray): 加载的图像，使用 OpenCV 读取。
    """

    def __init__(self, json_path, line_colors=None) -> None:
        """
        初始化 VisualTusimple 类的实例。

        Args:
            json_path (str): JSON 文件的路径。
            line_colors (list, optional): 绘制车道线时使用的颜色列表。默认值为 None。
        """
        self.json_path = json_path
        self.line_colors = line_colors if line_colors is not None else [(255, 0, 0), (0, 255, 0), (0, 0, 255)]  # 默认颜色
        self.data = self._load_json(self.json_path)
        self.image = self._load_image()

    def _load_json(self):
        """
        从指定的 JSON 文件路径加载数据。

        Returns:
            dict: JSON 文件解析后的数据字典。
        """
        with open(self.json_path, 'r') as f:
            return json.load(f)
        
    def _load_image(self):
        """
        加载与 JSON 数据关联的图像。

        Returns:
            numpy.ndarray: 加载的图像数据。
        """
        return cv2.imread(self.data['raw_file'])
    
    def ensure_file_exists(self, *args, exist_ok=True):
        """
        确保指定路径的文件夹存在，如果不存在则创建。

        Args:
            *args: 一个或多个路径，检查其存在性并创建文件夹。
            exist_ok (bool): 如果为 True，则如果文件夹已存在则不抛出异常。默认为 True。
        """
        for path in args:
            if not os.path.exists(path):
                os.makedirs(path, exist_ok=exist_ok)
    
    def draw_lanes(self):
        """
        在图像上绘制车道线。根据 JSON 数据中的车道信息和高度样本，绘制每条车道。
        """
        lanes = self.data['lanes']
        h_samples = self.data['h_samples']
        for i, lane in enumerate(lanes):
            line_color = self.line_colors[i % len(self.line_colors)]
            lane_points = [(x, y) for x, y in zip(lane, h_samples) if x != -2]
            for point in lane_points:
                cv2.circle(self.image, point, 3, line_color, -1)

    def save_image(self, output_path):
        """
        保存绘制了车道线的图像到指定路径。

        Args:
            output_path (str): 输出图像的文件路径。
        """
        self.ensure_file_exists(output_path)
        cv2.imwrite(output_path, self.image)
    
    def visualize(self, output_path):
        """
        可视化车道线并保存图像到指定路径。

        Args:
            output_path (str): 输出图像的文件路径。
        """
        self.draw_lanes()
        self.save_image(output_path)


if __name__ == '__main__':
    json_path = ''
    output_path = '/path/to/your/***/tusimple/visual'
    visualizer = VisualTusimple(json_path)
    visualizer.visualize(output_path)
