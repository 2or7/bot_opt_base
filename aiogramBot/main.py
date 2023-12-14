import os
import math
import shutil
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageFilter


class ImageProcessingWindow:
    def __init__(self, master):
        self.master = master

        self.master.geometry("500x500")
        self.image_1_path = ""
        self.image_2_path = ""

        self.task_3_button = tk.Button(self.master, text="Task 3", command=self.select_image_task_3)
        self.task_3_button.pack()

    # Task 3

    def select_image_task_3(self):
        image_path = filedialog.askopenfilename()
        if image_path:
            destination_folder = os.path.join(os.path.expanduser("~"), "./", "image_processing", "task_3")
            os.makedirs(destination_folder, exist_ok=True)

            image_name = os.path.basename(image_path)
            destination_path = os.path.join(destination_folder, image_name)
            shutil.copy(image_path, destination_path)

            processed_image = self.apply_canny_filter(destination_path)

            processed_image_path = os.path.join(destination_folder, "processed_" + image_name)
            processed_image.save(processed_image_path)
            tk.messagebox.showinfo(" ", f"Done.")

            moments_file_path = os.path.join(destination_folder, "moments.txt")
            moments = self.calculate_moments(processed_image)
            with open(moments_file_path, "w") as moments_file:
                for i, moment in enumerate(moments, 1):
                    moments_file.write(f"Object {i} moments:\n")
                    for key, value in moment.items():
                        moments_file.write(f"{key}: {value}\n")
                    moments_file.write("\n")
            tk.messagebox.showinfo(" ", f"Done.")

    def apply_canny_filter(self, image_path):
        # Открытие изображения
        image = Image.open(image_path)

        # Преобразование изображения в оттенки серого
        gray_image = image.convert("L")

        # Размытие изображения для сглаживания шумов
        blurred_image = gray_image.filter(ImageFilter.GaussianBlur(3))

        # Получение градиентных значений и направлений
        gradient_values, gradient_directions = self.calculate_gradients(blurred_image)

        # Подавление не-максимумов
        suppressed_image = self.suppress_non_maximums(gradient_values, gradient_directions)

        # Применение порогового значения для обнаружения границ
        threshold_image = self.apply_threshold(suppressed_image, 20, 40)

        return threshold_image

    def calculate_gradients(self, image):
        sobel_x = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
        sobel_y = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]

        width, height = image.size
        gradient_values = [[0] * height for _ in range(width)]
        gradient_directions = [[0] * height for _ in range(width)]

        for x in range(1, width - 1):
            for y in range(1, height - 1):
                grad_x = 0
                grad_y = 0
                for i in range(3):
                    for j in range(3):
                        pixel_value = image.getpixel((x + i - 1, y + j - 1))
                        grad_x += pixel_value * sobel_x[i][j]
                        grad_y += pixel_value * sobel_y[i][j]

                gradient_value = int(math.sqrt(grad_x ** 2 + grad_y ** 2))
                gradient_direction = math.atan2(grad_y, grad_x)

                gradient_values[x][y] = gradient_value
                gradient_directions[x][y] = gradient_direction

        return gradient_values, gradient_directions

    def suppress_non_maximums(self, gradient_values, gradient_directions):
        width, height = len(gradient_values), len(gradient_values[0])
        suppressed_image = Image.new("L", (width, height))

        for x in range(1, width - 1):
            for y in range(1, height - 1):
                current_value = gradient_values[x][y]
                direction = gradient_directions[x][y]

                x1 = x + int(round(math.cos(direction)))
                y1 = y + int(round(math.sin(direction)))
                x2 = x - int(round(math.cos(direction)))
                y2 = y - int(round(math.sin(direction)))

                if current_value <= gradient_values[x1][y1] or current_value <= gradient_values[x2][y2]:
                    suppressed_image.putpixel((x, y), 0)
                else:
                    suppressed_image.putpixel((x, y), current_value)

        return suppressed_image

    def apply_threshold(self, image, low_threshold, high_threshold):
        width, height = image.size
        threshold_image = Image.new("L", (width, height))

        for x in range(width):
            for y in range(height):
                pixel_value = image.getpixel((x, y))

                if pixel_value >= high_threshold - 10:
                    threshold_image.putpixel((x, y), 255)
                elif pixel_value <= low_threshold + 10:
                    threshold_image.putpixel((x, y), 0)
                else:
                    above_threshold = False
                    for i in range(max(x - 1, 0), min(x + 2, width - 1)):
                        for j in range(max(y - 1, 0), min(y + 2, height - 1)):
                            if image.getpixel((i, j)) >= high_threshold:
                                above_threshold = True
                                break

                        if above_threshold:
                            break

                    if above_threshold:
                        threshold_image.putpixel((x, y), 255)
                    else:
                        threshold_image.putpixel((x, y), 0)

        return threshold_image

    def calculate_moments(self, image):
        width, height = image.size
        moments = []

        for x in range(width):
            for y in range(height):
                pixel_value = image.getpixel((x, y))
                if pixel_value == 255:
                    moment = {
                        "Общая масса": 1,
                        "Момент по X": x,
                        "Момент по Y": y,
                        "Второй момент по X": x ** 2,
                        "Второй момент по XY": x * y,
                        "Второй момент по Y": y ** 2,
                        "Третий момент по X": x ** 3,
                        "Третий момент по XY": x ** 2 * y,
                        "Третий момент по Y": x * y ** 2,
                        "Третий момент по Y": y ** 3,
                    }
                    moments.append(moment)

        return moments

    # Task 4

    def select_image_task_4(self):
        image = filedialog.askopenfilename()
        if image:
            destination_folder = os.path.join(os.path.expanduser("~"), "./", "image_processing", "task_4")
            os.makedirs(destination_folder, exist_ok=True)

            shutil.copy(image, os.path.join(destination_folder, os.path.basename(image)))

            tk.messagebox.showinfo(" ", "Done.")

    # Task 2

    def select_image_task_2(self):
        image = filedialog.askopenfilename()
        if image:
            destination_folder = os.path.join(os.path.expanduser("~"), "./", "image_processing", "task_2")
            os.makedirs(destination_folder, exist_ok=True)

            shutil.copy(image, os.path.join(destination_folder, os.path.basename(image)))

            tk.messagebox.showinfo("Image Copy Success", "Image successfully copied to task 2 folder.")

    # Task 1

    def select_images(self):
        if not self.image_1_path:
            image_1 = filedialog.askopenfilename()
            if image_1:
                self.image_1_path = image_1
                self.select_second_image()
        else:
            self.select_second_image()

    def select_second_image(self):
        image_2 = filedialog.askopenfilename()
        if image_2:
            self.image_2_path = image_2

        if self.image_1_path and self.image_2_path:
            old_mse = self.calculate_overall_mse()
            total_mse, avg_mse = self.calculate_mse_by_blocks()
            total_uiqi, avg_uiqi = self.calculate_uiqi_block_by_block()

            destination_folder = os.path.join(os.path.expanduser("~"), "./", "image_processing", "task_1")
            os.makedirs(destination_folder, exist_ok=True)

            shutil.copy(self.image_1_path, os.path.join(destination_folder, "image_1.jpg"))
            shutil.copy(self.image_2_path, os.path.join(destination_folder, "image_2.jpg"))

            comparison_file_path = os.path.join(destination_folder, "comparison.txt")
            with open(comparison_file_path, 'w') as comparison_file:
                comparison_file.write("Old Overall MSE: {}\n".format(old_mse))
                comparison_file.write("Average MSE by Blocks: {}\n".format(avg_mse))
                comparison_file.write("Old Overall UIQI: {}\n".format(self.calculate_uiqi()))
                comparison_file.write("Average UIQI by Blocks: {}\n".format(avg_uiqi))

            self.image_1_path, self.image_2_path = "", ""

            tk.messagebox.showinfo("Image Copy and Comparison Success", "Comparison metrics saved to comparison.txt")

    def get_image_pixels(self, image_path):
        image_pixels = []
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()

            for byte in image_data:
                image_pixels.append(byte)

        return image_pixels

    def calculate_overall_mse(self):
        image1_pixels = self.get_image_pixels(self.image_1_path)
        image2_pixels = self.get_image_pixels(self.image_2_path)

        min_len = min(len(image1_pixels), len(image2_pixels))
        mse = 0
        for i in range(min_len):
            mse += (image1_pixels[i] - image2_pixels[i]) ** 2

        mse /= min_len
        return mse

    def calculate_mse_by_blocks(self):
        image1_pixels = self.get_image_pixels(self.image_1_path)
        image2_pixels = self.get_image_pixels(self.image_2_path)

        block_size = 8

        total_mse = 0
        num_blocks = 0

        for i in range(0, len(image1_pixels), block_size):
            block_mse = 0
            for j in range(block_size):
                index = i + j
                if index < len(image1_pixels) and index < len(image2_pixels):
                    block_mse += (image1_pixels[index] - image2_pixels[index]) ** 2
            if block_mse > 0:
                num_blocks += 1
            total_mse += block_mse

        avg_mse = total_mse / num_blocks if num_blocks > 0 else 0

        return total_mse, avg_mse

    def calculate_uiqi(self):
        image1_pixels = self.get_image_pixels(self.image_1_path)
        image2_pixels = self.get_image_pixels(self.image_2_path)

        min_len = min(len(image1_pixels), len(image2_pixels))
        image1_pixels = image1_pixels[:min_len]
        image2_pixels = image2_pixels[:min_len]

        image1_mean = sum(image1_pixels) / len(image1_pixels)
        image2_mean = sum(image2_pixels) / len(image2_pixels)

        image1_variance = sum([(pixel - image1_mean) ** 2 for pixel in image1_pixels]) / len(image1_pixels)
        image2_variance = sum([(pixel - image2_mean) ** 2 for pixel in image2_pixels]) / len(image2_pixels)

        image_covariance = sum([(image1_pixels[i] - image1_mean) * (image2_pixels[i] - image2_mean) for i in
                                range(len(image1_pixels))]) / len(image1_pixels)

        c1 = (0.01 * 255) ** 2
        c2 = (0.03 * 255) ** 2

        numerator = (2 * image1_mean * image2_mean + c1) * (2 * image_covariance + c2)
        denominator = (image1_mean ** 2 + image2_mean ** 2 + c1) * (image1_variance + image2_variance + c2)

        uiqi = numerator / denominator

        return uiqi

    def calculate_uiqi_block_by_block(self):
        block_size = 8
        image1_pixels = self.get_image_pixels(self.image_1_path)
        image2_pixels = self.get_image_pixels(self.image_2_path)

        min_len = min(len(image1_pixels), len(image2_pixels))
        image1_pixels = image1_pixels[:min_len]
        image2_pixels = image2_pixels[:min_len]

        image1_blocks = [image1_pixels[i:i + block_size] for i in range(0, len(image1_pixels), block_size)]
        image2_blocks = [image2_pixels[i:i + block_size] for i in range(0, len(image2_pixels), block_size)]

        total_uiqi = 0

        for i in range(len(image1_blocks)):
            image1_block = image1_blocks[i]
            image2_block = image2_blocks[i]

            image1_mean = sum(image1_block) / len(image1_block)
            image2_mean = sum(image2_block) / len(image2_block)

            image1_variance = sum([(pixel - image1_mean) ** 2 for pixel in image1_block]) / len(image1_block)
            image2_variance = sum([(pixel - image2_mean) ** 2 for pixel in image2_block]) / len(image2_block)

            image_covariance = sum([(image1_block[j] - image1_mean) * (image2_block[j] - image2_mean) for j in
                                    range(len(image1_block))]) / len(image1_block)

            c1 = (0.01 * 255) ** 2
            c2 = (0.03 * 255) ** 2

            numerator = (2 * image1_mean * image2_mean + c1) * (2 * image_covariance + c2)
            denominator = (image1_mean ** 2 + image2_mean ** 2 + c1) * (image1_variance + image2_variance + c2)

            uiqi = numerator / denominator
            total_uiqi += uiqi

        avg_uiqi = total_uiqi / len(image1_blocks)

        return total_uiqi, avg_uiqi


def main():
    root = tk.Tk()
    app = ImageProcessingWindow(root)
    root.mainloop()


if __name__ == "__main__":
    main()