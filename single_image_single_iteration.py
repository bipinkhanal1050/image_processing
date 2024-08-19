from paddleocr import PaddleOCR, draw_ocr
import cv2
import matplotlib.pyplot as plt
import json
import os

class OCRProcessor:
    def __init__(self):
        # Initialize PaddleOCR with English language
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en')

    def preprocess_image(self, image_path):
        # Read the image
        img = cv2.imread(image_path)

        # Check if the image was successfully loaded
        if img is None:
            print(f"Error: Unable to read the image at {image_path}")
            return None, None

        # Increase brightness and contrast
        # img = cv2.convertScaleAbs(img, alpha=1.4, beta=50)

        # Convert to grayscale
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # # Apply adaptive thresholding
        # thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        #                                cv2.THRESH_BINARY, 11, 2)

        # Resize image to double its original size for better detection
        resize_scale = 1.9
        resized_thresh = cv2.resize(img, None, fx=resize_scale, fy=resize_scale, interpolation=cv2.INTER_CUBIC)

        return img, resized_thresh, resize_scale

    def run_ocr(self, image):
        # Run OCR on the processed image
        result = self.ocr.ocr(image, cls=True)
        return result

    def save_detected_points(self, result, output_file, resize_scale):
        detected_points = []
        if result and result != [None] and len(result) > 0:
            for line in result[0]:
                if line:
                    box = line[0]
                    text = line[1][0]
                    score = line[1][1]

                    # Extract top-left and bottom-right coordinates
                    top_left = [int(box[0][0] / resize_scale), int(box[0][1] / resize_scale)]
                    bottom_right = [int(box[2][0] / resize_scale), int(box[2][1] / resize_scale)]

                    detected_points.append({
                        "text": text,
                        "score": score,
                        "top_left": top_left,
                        "bottom_right": bottom_right
                    })

        with open(output_file, 'w') as f:
            json.dump(detected_points, f, indent=4)

        print(f"Detected points saved to {output_file}")

    # def display_results(self, image, result):
    #     # Check if the image was successfully loaded
    #     if image is None:
    #         print("No image to display.")
    #         return

    #     # Convert to color for drawing
    #     image_color = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    #     if not result or not result[0]:
    #         print("No text detected in the image.")
    #         return

    #     # Print the number of text boxes detected
    #     num_text_boxes = len(result[0])
    #     print(f"Number of text boxes detected: {num_text_boxes}")

    #     # Process OCR results
    #     boxes = [line[0] for line in result[0] if line]
    #     texts = [line[1][0] for line in result[0] if line]
    #     scores = [line[1][1] for line in result[0] if line]

    #     # Provide a valid path to a TTF font file on your system
    #     font_path = 'C:/Windows/Fonts/arial.ttf'  # Change this to the path of an existing TTF font on your system

    #     # Draw OCR results on the image
    #     image_color = draw_ocr(image_color, boxes, texts, scores, font_path=font_path)
    #     plt.figure(figsize=(10, 10))
    #     plt.imshow(cv2.cvtColor(image_color, cv2.COLOR_BGR2RGB))
    #     plt.axis('off')
    #     plt.show()

    def display_results(self, image, result):
        # Check if the image was successfully loaded
        if image is None:
            print("No image to display.")
            return

        # Determine if the image is grayscale or color
        if len(image.shape) == 2:  # Grayscale image
            image_color = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        else:  # Color image
            image_color = image

        if not result or not result[0]:
            print("No text detected in the image.")
            return

        # Print the number of text boxes detected
        num_text_boxes = len(result[0])
        print(f"Number of text boxes detected: {num_text_boxes}")

        # Process OCR results
        boxes = [line[0] for line in result[0] if line]
        texts = [line[1][0] for line in result[0] if line]
        scores = [line[1][1] for line in result[0] if line]

        # Provide a valid path to a TTF font file on your system
        font_path = 'C:/Windows/Fonts/arial.ttf'  # Change this to the path of an existing TTF font on your system

        # Draw OCR results on the image
        image_color = draw_ocr(image_color, boxes, texts, scores, font_path=font_path)
        plt.figure(figsize=(10, 10))
        plt.imshow(cv2.cvtColor(image_color, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.show()


if __name__ == '__main__':
    # Replace with your image path
    image_path = 'images/5.png'
    output_file = 'detected_points.json'
    
    ocr_processor = OCRProcessor()
    img, preprocessed_image, resize_scale = ocr_processor.preprocess_image(image_path)
    
    if preprocessed_image is not None:
        result = ocr_processor.run_ocr(preprocessed_image)
        ocr_processor.save_detected_points(result, output_file, resize_scale)
        ocr_processor.display_results(preprocessed_image, result)
    else:
        print("Image preprocessing failed. Please check the image path and try again.")
