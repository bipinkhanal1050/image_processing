from paddleocr import PaddleOCR, draw_ocr
import cv2
# import matplotlib.pyplot as plt
import json
import itertools
from collections import Counter

class OCRProcessor:
    def __init__(self):
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en')

    def preprocess_image(self, image_path, alpha, beta):
        img = cv2.imread(image_path)
        if img is None:
            print(f"Error: Unable to read the image at {image_path}")
            return None, None, None

        img = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                       cv2.THRESH_BINARY, 11, 2)
        resize_scale = 2
        resized_thresh = cv2.resize(thresh, None, fx=resize_scale, fy=resize_scale, interpolation=cv2.INTER_CUBIC)
        return img, resized_thresh, resize_scale

    def run_ocr(self, image):
        result = self.ocr.ocr(image, cls=True)
        return result

    def process_detected_points(self, result, resize_scale, alpha, beta):
        detected_points = []
        if result and result != [None] and len(result) > 0:
            for line in result[0]:
                if line:
                    box = line[0]
                    text = line[1][0]
                    score = line[1][1]

                    top_left = [int(box[0][0] / resize_scale), int(box[0][1] / resize_scale)]
                    bottom_right = [int(box[2][0] / resize_scale), int(box[2][1] / resize_scale)]

                    detected_points.append({
                        "text": text,
                        "score": score,
                        "top_left": top_left,
                        "bottom_right": bottom_right,
                        "alpha": alpha,
                        "beta": beta
                    })
        return detected_points

    def filter_and_group_points(self, all_points):
        filtered_points = [
            point for point in all_points
            if point['score'] >= 0.55 and len(point['text'].replace('.', '')) <= 2 and point['text'].isdigit()
        ]

        def are_points_close(p1, p2):
            return (
                abs(p1['top_left'][0] - p2['top_left'][0]) <= 15 and
                abs(p1['top_left'][1] - p2['top_left'][1]) <= 15 and
                abs(p1['bottom_right'][0] - p2['bottom_right'][0]) <= 15 and
                abs(p1['bottom_right'][1] - p2['bottom_right'][1]) <= 15
            )

        grouped_points = []
        for point in filtered_points:
            added = False
            for group in grouped_points:
                if are_points_close(point, group[0]):
                    group.append(point)
                    added = True
                    break
            if not added:
                grouped_points.append([point])

        return grouped_points

    def process_image_with_params(self, image_path, alpha, beta):
        img, preprocessed_image, resize_scale = self.preprocess_image(image_path, alpha, beta)
        if preprocessed_image is not None:
            result = self.run_ocr(preprocessed_image)
            return self.process_detected_points(result, resize_scale, alpha, beta)
        return []

    def purify_data(self, grouped_points):
        purified_data = []
        
        for group in grouped_points:
            if not group:
                continue
            
            text_counter = Counter(point['text'] for point in group)
            most_common_text = text_counter.most_common(1)[0][0]
            
            best_points = [p for p in group if p['text'] == most_common_text]
            best_point = min(best_points, key=lambda x: x['alpha'])
            
            top_lefts = [point['top_left'] for point in group]
            bottom_rights = [point['bottom_right'] for point in group]
            avg_top_left = [sum(coord) // len(coord) for coord in zip(*top_lefts)]
            avg_bottom_right = [sum(coord) // len(coord) for coord in zip(*bottom_rights)]
            
            purified_point = {
                'text': most_common_text,
                'score': best_point['score'],
                'top_left': avg_top_left,
                'bottom_right': avg_bottom_right,
                'alpha': best_point['alpha'],
                'beta': best_point['beta']
            }
            purified_data.append(purified_point)
        
        return purified_data

def main():
    image_path = 'images/26.png'
    output_file = 'detected_points.json'
    purified_output_file = 'purified_points.json'
    
    alphas = [1, 1.1, 1.2, 1.3, 1.4]
    betas = [30, 40, 50, 60]

    ocr_processor = OCRProcessor()
    all_points = []

    for alpha, beta in itertools.product(alphas, betas):
        print(f"Processing with alpha={alpha}, beta={beta}")
        points = ocr_processor.process_image_with_params(image_path, alpha, beta)
        all_points.extend(points)

    grouped_points = ocr_processor.filter_and_group_points(all_points)

    with open(output_file, 'w') as f:
        json.dump(grouped_points, f, indent=4)

    print(f"Grouped and filtered points saved to {output_file}")

    purified_data = ocr_processor.purify_data(grouped_points)

    with open(purified_output_file, 'w') as f:
        json.dump(purified_data, f, indent=4)

    print(f"Purified points saved to {purified_output_file}")

if __name__ == '__main__':
    main()