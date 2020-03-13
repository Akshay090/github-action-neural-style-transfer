import logging
import io
import os

import onnxruntime
from PIL import Image
import numpy as np


def run_inference(image):
    # See https://github.com/onnx/models/tree/master/vision/style_transfer/fast_neural_style
    # for implementation details
    model_path = f'./models/rain_princess.onnx'
    session = onnxruntime.InferenceSession(model_path)
    metadata = session.get_modelmeta()
    logging.info(f'Model metadata:\n' +
        f'    Graph name: {metadata.graph_name}\n' +
        f'    Model version: {metadata.version}\n' +
        f'    Producer: {metadata.producer_name}')

    # Preprocess image
    original_image_size = image.size[0], image.size[1]
    logging.info('Preprocessing image...')
    # Model expects a 224x224 shape input
    image = image.resize((224, 224), Image.LANCZOS)
    bands = image.getbands()
    if bands == ('R', 'G', 'B'):
        logging.info(f'Image is RGB. No conversion necessary.')
    else:
        logging.info(f'Image is {bands}, converting to RGB...')
        image = image.convert('RGB')

    x = np.array(image).astype('float32')
    x = np.transpose(x, [2, 0, 1])
    x = np.expand_dims(x, axis=0)

    output_name = session.get_outputs()[0].name
    input_name = session.get_inputs()[0].name
    logging.info('Running inference on ONNX model...')
    result = session.run([output_name], {input_name: x})[0][0]

    # Postprocess image
    result = np.clip(result, 0, 255)
    result = result.transpose(1,2,0).astype("uint8")
    img = Image.fromarray(result)
    max_width  = 800
    height = int(max_width * original_image_size[1] / original_image_size[0])
    # Upsample and correct aspect ratio for final image
    img = img.resize((max_width, height), Image.BICUBIC)
    
    # Store inferred image as in memory byte array
    img_byte_arr = io.BytesIO()
    # Convert composite to RGB so we can return JPEG
    img.convert('RGB').save(img_byte_arr, format='JPEG')
    final_image = img_byte_arr.getvalue()

    return final_image



def main():
    image_path = os.environ["INPUT_PATH"]
    image = Image.open(image_path)
    output_image = run_inference(image)
    output_image = Image.open(io.BytesIO(output_image))

    current_directory = os.getcwd()
    os.mkdir('styled_output')
    output_directory = os.path.join(current_directory, r'styled_output/styled_image.jpg')
    output_image.save(output_directory)

if __name__ == "__main__":
    main()
