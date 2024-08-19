# Installation

- Clone the project

- Goto project directory

- Create virtual environment (recommended)

- Activate the virtual environment

- Install the requirements
 `pip install -r requirement.txt`

 - Run respective files as per requirement

    `single_image_single_iteration.py` to find and plot text from single image (single set of parameters)

    `multiple_image_multiple_iteration.py` to find the text from multiple images using multiple parameters (data stored in purified/file.json) 


## View the outputs

- serve the static files using python
    - run `python -m http.server` inside the project directory

- Visit `localhost:8000/index.html`