from flask import Flask, render_template, request, Response, jsonify
import requests
from flask_cors import CORS
import ssl
import pytesseract  # For OCR processing
from PIL import Image  # For image handling
import io
import base64
import re




# Initialize Flask app
app = Flask("Gurukul AI Chatbot", static_folder="static", static_url_path="/gurukulai/static")


app.secret_key = "secure_random_secret_key"
CORS(app) 


from datetime import timedelta

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
app.config['SESSION_COOKIE_SECURE'] = True  # Important for HTTPS
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # or 'Strict'/'None'


# Home Route to Render Chat UI
@app.route("/")
def home():
    return render_template("index.html")  # Renders the merged chatbot HTML template

@app.route('/home')
@app.route('/gurukulai/home') 
def index():
    return render_template('home.html')


PRACTICE_DATA = {
    "classes": {
        1: {
            "name": "Class 9",
            "subjects": {
                1: {
                    "name": "English",
                    "chapters": {
                        "eng_prose_03": {
                            "name": "Eng Prose 03",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for eng_prose_03.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "eng_prose_06": {
                            "name": "Eng Prose 06",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for eng_prose_06.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "eng_poem_07": {
                            "name": "Eng Poem 07",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for eng_poem_07.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "eng_prose_07": {
                            "name": "Eng Prose 07",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for eng_prose_07.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "eng_poem_05": {
                            "name": "Eng Poem 05",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for eng_poem_05.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "eng_poem_01": {
                            "name": "Eng Poem 01",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for eng_poem_01.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "eng_prose_09": {
                            "name": "Eng Prose 09",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for eng_prose_09.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "eng_poem_08": {
                            "name": "Eng Poem 08",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for eng_poem_08.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "eng_prose_04": {
                            "name": "Eng Prose 04",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for eng_prose_04.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "eng_prose_02": {
                            "name": "Eng Prose 02",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for eng_prose_02.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "eng_poem_02": {
                            "name": "Eng Poem 02",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for eng_poem_02.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "eng_prose_01": {
                            "name": "Eng Prose 01",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for eng_prose_01.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "eng_prose_08": {
                            "name": "Eng Prose 08",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for eng_prose_08.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "eng_poem_03": {
                            "name": "Eng Poem 03",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for eng_poem_03.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "eng_poem_06": {
                            "name": "Eng Poem 06",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for eng_poem_06.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "eng_prose_05": {
                            "name": "Eng Prose 05",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for eng_prose_05.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "eng_poem_04": {
                            "name": "Eng Poem 04",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for eng_poem_04.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        }
                    }
                },
                13: {
                    "name": "Maths",
                    "chapters": {
                        "maths_05": {
                            "name": "Maths 5",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for maths_05.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "maths_01": {
                            "name": "Maths 1",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for maths_01.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "maths_09": {
                            "name": "Maths 9",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for maths_09.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "maths_08": {
                            "name": "Maths 8",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for maths_08.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "maths_10": {
                            "name": "Maths 10",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for maths_10.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "maths_03": {
                            "name": "Maths 3",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for maths_03.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "maths_12": {
                            "name": "Maths 12",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for maths_12.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "maths_04": {
                            "name": "Maths 4",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for maths_04.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "maths_07": {
                            "name": "Maths 7",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for maths_07.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "maths_02": {
                            "name": "Maths 2",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for maths_02.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "maths_11": {
                            "name": "Maths 11",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for maths_11.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "maths_06": {
                            "name": "Maths 6",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for maths_06.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        }
                    }
                },
                14: {
                    "name": "Ss",
                    "chapters": {
                        "ss_eco_03": {
                            "name": "Ss Eco 03",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for ss_eco_03.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "ss_civics_04": {
                            "name": "Ss Civics 04",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for ss_civics_04.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "ss_geo_03": {
                            "name": "Ss Geo 03",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for ss_geo_03.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "ss_civics_03": {
                            "name": "Ss Civics 03",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for ss_civics_03.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "ss_history_04": {
                            "name": "Ss History 04",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for ss_history_04.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "ss_history_03": {
                            "name": "Ss History 03",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for ss_history_03.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "ss_civics_02": {
                            "name": "Ss Civics 02",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for ss_civics_02.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "ss_history_05": {
                            "name": "Ss History 05",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for ss_history_05.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "ss_geo_04": {
                            "name": "Ss Geo 04",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for ss_geo_04.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "ss_eco_04": {
                            "name": "Ss Eco 04",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for ss_eco_04.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "ss_eco_01": {
                            "name": "Ss Eco 01",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for ss_eco_01.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "ss_eco_02": {
                            "name": "Ss Eco 02",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for ss_eco_02.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "ss_geo_05": {
                            "name": "Ss Geo 05",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for ss_geo_05.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "ss_civics_05": {
                            "name": "Ss Civics 05",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for ss_civics_05.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "ss_history_02": {
                            "name": "Ss History 02",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for ss_history_02.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "ss_history_01": {
                            "name": "Ss History 01",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for ss_history_01.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "ss_civics_01": {
                            "name": "Ss Civics 01",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for ss_civics_01.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "ss_geo_02": {
                            "name": "Ss Geo 02",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for ss_geo_02.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "ss_geo_01": {
                            "name": "Ss Geo 01",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for ss_geo_01.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "ss_geo_06": {
                            "name": "Ss Geo 06",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for ss_geo_06.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        }
                    }
                },
                3: {
                    "name": "Science",
                    "chapters": {
                        "science_12": {
                            "name": "Science 12",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for science_12.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "science_09": {
                            "name": "Science 9",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for science_09.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "science_10": {
                            "name": "Science 10",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for science_10.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "science_01": {
                            "name": "Science 1",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for science_01.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "science_05": {
                            "name": "Science 5",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for science_05.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "science_11": {
                            "name": "Science 11",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for science_11.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "science_08": {
                            "name": "Science 8",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for science_08.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "science_07": {
                            "name": "Science 7",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for science_07.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "science_02": {
                            "name": "Science 2",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for science_02.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "science_03": {
                            "name": "Science 3",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for science_03.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "science_04": {
                            "name": "Science 4",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for science_04.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "science_06": {
                            "name": "Science 6",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for science_06.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        }
                    }
                }
            }
        },
        2: {
            "name": "Class 10",
            "subjects": {
                11: {
                    "name": "Civics",
                    "chapters": {
                        "civics_02": {
                            "name": "Civics 2",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for civics_02.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "civics_01": {
                            "name": "Civics 1",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for civics_01.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "civics_04": {
                            "name": "Civics 4",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for civics_04.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "civics_03": {
                            "name": "Civics 3",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for civics_03.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "civics_05": {
                            "name": "Civics 5",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for civics_05.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        }
                    }
                },
                9: {
                    "name": "History",
                    "chapters": {
                        "history_01": {
                            "name": "History 1",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for history_01.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "history_02": {
                            "name": "History 2",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for history_02.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "history_04": {
                            "name": "History 4",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for history_04.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "history_05": {
                            "name": "History 5",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for history_05.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "history_03": {
                            "name": "History 3",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for history_03.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        }
                    }
                },
                8: {
                    "name": "Economics",
                    "chapters": {
                        "economics_05": {
                            "name": "Economics 5",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for economics_05.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "economics_04": {
                            "name": "Economics 4",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for economics_04.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "economics_03": {
                            "name": "Economics 3",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for economics_03.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "economics_02": {
                            "name": "Economics 2",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for economics_02.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "economics_01": {
                            "name": "Economics 1",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for economics_01.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        }
                    }
                },
                1: {
                    "name": "English",
                    "chapters": {
                        "1_words": {
                            "name": "1 Words",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for 1_words.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "2_words": {
                            "name": "2 Words",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for 2_words.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "3_words": {
                            "name": "3 Words",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for 3_words.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "4_words": {
                            "name": "4 Words",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for 4_words.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "5_words": {
                            "name": "5 Words",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for 5_words.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "6_words": {
                            "name": "6 Words",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for 6_words.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "7_words": {
                            "name": "7 Words",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for 7_words.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "8_words": {
                            "name": "8 Words",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for 8_words.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "9_words": {
                            "name": "9 Words",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for 9_words.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "1_flight": {
                            "name": "1 Flight",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for 1_flight.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "2_flight": {
                            "name": "2 Flight",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for 2_flight.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "3_flight": {
                            "name": "3 Flight",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for 3_flight.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "4_flight": {
                            "name": "4 Flight",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for 4_flight.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "5_flight": {
                            "name": "5 Flight",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for 5_flight.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "6_flight": {
                            "name": "6 Flight",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for 6_flight.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "7_flight": {
                            "name": "7 Flight",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for 7_flight.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "8_flight": {
                            "name": "8 Flight",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for 8_flight.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "9_flight": {
                            "name": "9 Flight",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for 9_flight.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "1_footprint": {
                            "name": "1 Footprint",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for 1_footprint.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "2_footprint": {
                            "name": "2 Footprint",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for 2_footprint.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "3_footprint": {
                            "name": "3 Footprint",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for 3_footprint.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "4_footprint": {
                            "name": "4 Footprint",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for 4_footprint.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "5_footprint": {
                            "name": "5 Footprint",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for 5_footprint.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "6_footprint": {
                            "name": "6 Footprint",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for 6_footprint.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "7_footprint": {
                            "name": "7 Footprint",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for 7_footprint.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "8_footprint": {
                            "name": "8 Footprint",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for 8_footprint.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "9_footprint": {
                            "name": "9 Footprint",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for 9_footprint.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        }
                    }
                },
                10: {
                    "name": "Geography",
                    "chapters": {
                        "geography_04": {
                            "name": "Geography 4",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for geography_04.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "geography_06": {
                            "name": "Geography 6",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for geography_06.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "geography_05": {
                            "name": "Geography 5",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for geography_05.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "geography_07": {
                            "name": "Geography 7",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for geography_07.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "geography_03": {
                            "name": "Geography 3",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for geography_03.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "geography_01": {
                            "name": "Geography 1",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for geography_01.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "geography_02": {
                            "name": "Geography 2",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for geography_02.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        }
                    }
                },
                13: {
                    "name": "Maths",
                    "chapters": {
                        "maths_03": {
                            "name": "Maths 3",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for maths_03.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "maths_13": {
                            "name": "Maths 13",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for maths_13.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "maths_02": {
                            "name": "Maths 2",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for maths_02.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "maths_08": {
                            "name": "Maths 8",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for maths_08.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "maths_07": {
                            "name": "Maths 7",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for maths_07.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "maths_01": {
                            "name": "Maths 1",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for maths_01.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "maths_11": {
                            "name": "Maths 11",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for maths_11.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "maths_12": {
                            "name": "Maths 12",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for maths_12.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "maths_04": {
                            "name": "Maths 4",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for maths_04.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "maths_14": {
                            "name": "Maths 14",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for maths_14.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "maths_06": {
                            "name": "Maths 6",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for maths_06.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "maths_10": {
                            "name": "Maths 10",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for maths_10.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "maths_05": {
                            "name": "Maths 5",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for maths_05.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "maths_09": {
                            "name": "Maths 9",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for maths_09.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        }
                    }
                },
                14: {
                    "name": "Ss",
                    "chapters": {
                        "civics_02": {
                            "name": "Civics 2",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for civics_02.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "civics_01": {
                            "name": "Civics 1",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for civics_01.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "civics_04": {
                            "name": "Civics 4",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for civics_04.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "civics_03": {
                            "name": "Civics 3",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for civics_03.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "civics_05": {
                            "name": "Civics 5",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for civics_05.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "history_01": {
                            "name": "History 1",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for history_01.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "history_02": {
                            "name": "History 2",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for history_02.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "history_04": {
                            "name": "History 4",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for history_04.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "history_05": {
                            "name": "History 5",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for history_05.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "history_03": {
                            "name": "History 3",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for history_03.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "economics_05": {
                            "name": "Economics 5",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for economics_05.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "economics_04": {
                            "name": "Economics 4",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for economics_04.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "economics_03": {
                            "name": "Economics 3",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for economics_03.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "economics_02": {
                            "name": "Economics 2",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for economics_02.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "economics_01": {
                            "name": "Economics 1",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for economics_01.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "geography_04": {
                            "name": "Geography 4",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for geography_04.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "geography_06": {
                            "name": "Geography 6",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for geography_06.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "geography_05": {
                            "name": "Geography 5",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for geography_05.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "geography_07": {
                            "name": "Geography 7",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for geography_07.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "geography_03": {
                            "name": "Geography 3",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for geography_03.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "geography_01": {
                            "name": "Geography 1",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for geography_01.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "geography_02": {
                            "name": "Geography 2",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for geography_02.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        }
                    }
                },
                3: {
                    "name": "Science",
                    "chapters": {
                        "science_01": {
                            "name": "Science 1",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for science_01.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "science_09": {
                            "name": "Science 9",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for science_09.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "science_08": {
                            "name": "Science 8",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for science_08.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "science_02": {
                            "name": "Science 2",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for science_02.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "science_06": {
                            "name": "Science 6",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for science_06.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "science_03": {
                            "name": "Science 3",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for science_03.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "science_07": {
                            "name": "Science 7",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for science_07.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "science_05": {
                            "name": "Science 5",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for science_05.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "science_11": {
                            "name": "Science 11",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for science_11.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "science_10": {
                            "name": "Science 10",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for science_10.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "science_13": {
                            "name": "Science 13",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for science_13.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "science_04": {
                            "name": "Science 4",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for science_04.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "science_12": {
                            "name": "Science 12",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for science_12.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        }
                    }
                }
            }
        },
        3: {
            "name": "Class 11",
            "subjects": {
                7: {
                    "name": "Biology",
                    "chapters": {
                        "biology_09": {
                            "name": "Biology 9",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for biology_09.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "biology_15": {
                            "name": "Biology 15",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for biology_15.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "biology_07": {
                            "name": "Biology 7",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for biology_07.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "biology_11": {
                            "name": "Biology 11",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for biology_11.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "biology_04": {
                            "name": "Biology 4",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for biology_04.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "biology_02": {
                            "name": "Biology 2",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for biology_02.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "biology_05": {
                            "name": "Biology 5",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for biology_05.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "biology_03": {
                            "name": "Biology 3",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for biology_03.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "biology_14": {
                            "name": "Biology 14",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for biology_14.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "biology_12": {
                            "name": "Biology 12",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for biology_12.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "biology_13": {
                            "name": "Biology 13",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for biology_13.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "biology_06": {
                            "name": "Biology 6",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for biology_06.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "biology_08": {
                            "name": "Biology 8",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for biology_08.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "biology_17": {
                            "name": "Biology 17",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for biology_17.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "biology_19": {
                            "name": "Biology 19",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for biology_19.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "biology_18": {
                            "name": "Biology 18",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for biology_18.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "biology_10": {
                            "name": "Biology 10",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for biology_10.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "biology_16": {
                            "name": "Biology 16",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for biology_16.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "biology_01": {
                            "name": "Biology 1",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for biology_01.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        }
                    }
                },
                1: {
                    "name": "English",
                    "chapters": {
                        "english_ss_04": {
                            "name": "English Ss 04",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for english_ss_04.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "english_hb_01": {
                            "name": "English Hb 01",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for english_hb_01.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "english_hb_11": {
                            "name": "English Hb 11",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for english_hb_11.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "english_hb_07": {
                            "name": "English Hb 07",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for english_hb_07.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "english_hb_05": {
                            "name": "English Hb 05",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for english_hb_05.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "english_ss_01": {
                            "name": "English Ss 01",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for english_ss_01.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "english_ss_03": {
                            "name": "English Ss 03",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for english_ss_03.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "english_hb_08": {
                            "name": "English Hb 08",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for english_hb_08.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "english_hb_12": {
                            "name": "English Hb 12",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for english_hb_12.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "english_ss_05": {
                            "name": "English Ss 05",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for english_ss_05.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "english_hb_02": {
                            "name": "English Hb 02",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for english_hb_02.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "english_hb_10": {
                            "name": "English Hb 10",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for english_hb_10.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "english_hb_06": {
                            "name": "English Hb 06",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for english_hb_06.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "english_hb_09": {
                            "name": "English Hb 09",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for english_hb_09.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "english_hb_04": {
                            "name": "English Hb 04",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for english_hb_04.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "english_hb_03": {
                            "name": "English Hb 03",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for english_hb_03.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "english_ss_02": {
                            "name": "English Ss 02",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for english_ss_02.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        }
                    }
                },
                6: {
                    "name": "Chemistry",
                    "chapters": {
                        "chemistry-1_06": {
                            "name": "Chemistry-1 6",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for chemistry-1_06.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "chemistry-1_02": {
                            "name": "Chemistry-1 2",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for chemistry-1_02.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "chemistry-2_02": {
                            "name": "Chemistry-2 2",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for chemistry-2_02.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "chemistry-2_01": {
                            "name": "Chemistry-2 1",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for chemistry-2_01.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "chemistry-2_03": {
                            "name": "Chemistry-2 3",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for chemistry-2_03.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "chemistry-1_04": {
                            "name": "Chemistry-1 4",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for chemistry-1_04.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "chemistry-1_05": {
                            "name": "Chemistry-1 5",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for chemistry-1_05.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "chemistry-1_01": {
                            "name": "Chemistry-1 1",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for chemistry-1_01.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "chemistry-1_03": {
                            "name": "Chemistry-1 3",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for chemistry-1_03.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        }
                    }
                },
                13: {
                    "name": "Maths",
                    "chapters": {
                        "maths_13": {
                            "name": "Maths 13",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for maths_13.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "maths_10": {
                            "name": "Maths 10",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for maths_10.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "maths_12": {
                            "name": "Maths 12",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for maths_12.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "maths_03": {
                            "name": "Maths 3",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for maths_03.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "maths_08": {
                            "name": "Maths 8",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for maths_08.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "maths_02": {
                            "name": "Maths 2",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for maths_02.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "maths_04": {
                            "name": "Maths 4",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for maths_04.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "maths_01": {
                            "name": "Maths 1",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for maths_01.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "maths_07": {
                            "name": "Maths 7",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for maths_07.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "maths_05": {
                            "name": "Maths 5",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for maths_05.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "maths_06": {
                            "name": "Maths 6",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for maths_06.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "maths_11": {
                            "name": "Maths 11",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for maths_11.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "maths_14": {
                            "name": "Maths 14",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for maths_14.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "maths_09": {
                            "name": "Maths 9",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for maths_09.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        }
                    }
                },
                5: {
                    "name": "Physics",
                    "chapters": {
                        "physics-2_04": {
                            "name": "Physics-2 4",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for physics-2_04.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "physics-2_05": {
                            "name": "Physics-2 5",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for physics-2_05.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "physics-2_01": {
                            "name": "Physics-2 1",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for physics-2_01.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "physics-1_03": {
                            "name": "Physics-1 3",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for physics-1_03.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "physics-1_04": {
                            "name": "Physics-1 4",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for physics-1_04.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "physics-1_07": {
                            "name": "Physics-1 7",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for physics-1_07.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "physics-1_06": {
                            "name": "Physics-1 6",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for physics-1_06.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "physics-1_02": {
                            "name": "Physics-1 2",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for physics-1_02.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "physics-2_07": {
                            "name": "Physics-2 7",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for physics-2_07.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "physics-1_01": {
                            "name": "Physics-1 1",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for physics-1_01.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "physics-2_03": {
                            "name": "Physics-2 3",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for physics-2_03.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "physics-1_05": {
                            "name": "Physics-1 5",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for physics-1_05.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "physics-2_02": {
                            "name": "Physics-2 2",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for physics-2_02.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "physics-2_06": {
                            "name": "Physics-2 6",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for physics-2_06.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        }
                    }
                },
                15: {
                    "name": "Pe",
                    "chapters": {
                        "pe_02": {
                            "name": "Pe 2",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for pe_02.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "pe_11": {
                            "name": "Pe 11",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for pe_11.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "pe_09": {
                            "name": "Pe 9",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for pe_09.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "pe_03": {
                            "name": "Pe 3",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for pe_03.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "pe_10": {
                            "name": "Pe 10",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for pe_10.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "pe_07": {
                            "name": "Pe 7",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for pe_07.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "pe_05": {
                            "name": "Pe 5",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for pe_05.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "pe_06": {
                            "name": "Pe 6",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for pe_06.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "pe_08": {
                            "name": "Pe 8",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for pe_08.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "pe_01": {
                            "name": "Pe 1",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for pe_01.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "pe_04": {
                            "name": "Pe 4",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for pe_04.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        }
                    }
                }
            }
        },
        4: {
            "name": "Class 12",
            "subjects": {
                9: {
                    "name": "History",
                    "chapters": {
                        "history-1_04": {
                            "name": "History-1 4",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for history-1_04.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "history-1_03": {
                            "name": "History-1 3",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for history-1_03.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "history-2_03": {
                            "name": "History-2 3",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for history-2_03.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "history-1_02": {
                            "name": "History-1 2",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for history-1_02.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "history-2_04": {
                            "name": "History-2 4",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for history-2_04.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "history-3_04": {
                            "name": "History-3 4",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for history-3_04.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "history-2_01": {
                            "name": "History-2 1",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for history-2_01.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "history-1_01": {
                            "name": "History-1 1",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for history-1_01.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "history-3_02": {
                            "name": "History-3 2",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for history-3_02.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "history-3_03": {
                            "name": "History-3 3",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for history-3_03.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "history-2_02": {
                            "name": "History-2 2",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for history-2_02.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "history-3_01": {
                            "name": "History-3 1",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for history-3_01.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        }
                    }
                },
                7: {
                    "name": "Biology",
                    "chapters": {
                        "biology_09": {
                            "name": "Biology 9",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for biology_09.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "biology_07": {
                            "name": "Biology 7",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for biology_07.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "biology_11": {
                            "name": "Biology 11",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for biology_11.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "biology_04": {
                            "name": "Biology 4",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for biology_04.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "biology_02": {
                            "name": "Biology 2",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for biology_02.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "biology_05": {
                            "name": "Biology 5",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for biology_05.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "biology_03": {
                            "name": "Biology 3",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for biology_03.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "biology_12": {
                            "name": "Biology 12",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for biology_12.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "biology_13": {
                            "name": "Biology 13",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for biology_13.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "biology_06": {
                            "name": "Biology 6",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for biology_06.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "biology_08": {
                            "name": "Biology 8",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for biology_08.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "biology_10": {
                            "name": "Biology 10",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for biology_10.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "biology_01": {
                            "name": "Biology 1",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for biology_01.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        }
                    }
                },
                1: {
                    "name": "English",
                    "chapters": {
                        "english-fl_04": {
                            "name": "English-fl 4",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for english-fl_04.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "english-fl_12": {
                            "name": "English-fl 12",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for english-fl_12.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "english-fl_03": {
                            "name": "English-fl 3",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for english-fl_03.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "english-fl_09": {
                            "name": "English-fl 9",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for english-fl_09.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "english-fl_08": {
                            "name": "English-fl 8",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for english-fl_08.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "english-vs-06": {
                            "name": "English-Vs-06",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for english-vs-06.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "english-fl_01": {
                            "name": "English-fl 1",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for english-fl_01.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "english-fl_11": {
                            "name": "English-fl 11",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for english-fl_11.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "english-fl_06": {
                            "name": "English-fl 6",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for english-fl_06.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "english-vs-01": {
                            "name": "English-Vs-01",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for english-vs-01.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "english-vs-03": {
                            "name": "English-Vs-03",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for english-vs-03.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "english-fl_10": {
                            "name": "English-fl 10",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for english-fl_10.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "english-vs-05": {
                            "name": "English-Vs-05",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for english-vs-05.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "english-fl_07": {
                            "name": "English-fl 7",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for english-fl_07.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "english-fl_13": {
                            "name": "English-fl 13",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for english-fl_13.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "english-fl_05": {
                            "name": "English-fl 5",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for english-fl_05.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "english-vs-04": {
                            "name": "English-Vs-04",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for english-vs-04.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "english-fl_02": {
                            "name": "English-fl 2",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for english-fl_02.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "english-vs-02": {
                            "name": "English-Vs-02",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for english-vs-02.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        }
                    }
                },
                6: {
                    "name": "Chemistry",
                    "chapters": {
                        "chemistry-2_05": {
                            "name": "Chemistry-2 5",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for chemistry-2_05.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "chemistry-2_04": {
                            "name": "Chemistry-2 4",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for chemistry-2_04.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "chemistry-1_02": {
                            "name": "Chemistry-1 2",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for chemistry-1_02.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "chemistry-2_02": {
                            "name": "Chemistry-2 2",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for chemistry-2_02.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "chemistry-2_01": {
                            "name": "Chemistry-2 1",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for chemistry-2_01.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "chemistry-2_03": {
                            "name": "Chemistry-2 3",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for chemistry-2_03.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "chemistry-1_04": {
                            "name": "Chemistry-1 4",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for chemistry-1_04.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "chemistry-1_05": {
                            "name": "Chemistry-1 5",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for chemistry-1_05.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "chemistry-1_01": {
                            "name": "Chemistry-1 1",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for chemistry-1_01.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "chemistry-1_03": {
                            "name": "Chemistry-1 3",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for chemistry-1_03.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        }
                    }
                },
                13: {
                    "name": "Maths",
                    "chapters": {
                        "maths-2_02": {
                            "name": "Maths-2 2",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for maths-2_02.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "maths-1_05": {
                            "name": "Maths-1 5",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for maths-1_05.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "maths-2_01": {
                            "name": "Maths-2 1",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for maths-2_01.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "maths-1_06": {
                            "name": "Maths-1 6",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for maths-1_06.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "maths-1_01": {
                            "name": "Maths-1 1",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for maths-1_01.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "maths-1_04": {
                            "name": "Maths-1 4",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for maths-1_04.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "maths-2_07": {
                            "name": "Maths-2 7",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for maths-2_07.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "maths-1_03": {
                            "name": "Maths-1 3",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for maths-1_03.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "maths-2_06": {
                            "name": "Maths-2 6",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for maths-2_06.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "maths-2_04": {
                            "name": "Maths-2 4",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for maths-2_04.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "maths-2_05": {
                            "name": "Maths-2 5",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for maths-2_05.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "maths-2_03": {
                            "name": "Maths-2 3",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for maths-2_03.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "maths-1_02": {
                            "name": "Maths-1 2",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for maths-1_02.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        }
                    }
                },
                5: {
                    "name": "Physics",
                    "chapters": {
                        "physics-2_04": {
                            "name": "Physics-2 4",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for physics-2_04.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "physics-2_05": {
                            "name": "Physics-2 5",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for physics-2_05.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "physics-2_01": {
                            "name": "Physics-2 1",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for physics-2_01.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "physics-1_03": {
                            "name": "Physics-1 3",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for physics-1_03.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "physics-1_04": {
                            "name": "Physics-1 4",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for physics-1_04.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "physics-1_07": {
                            "name": "Physics-1 7",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for physics-1_07.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "physics-1_06": {
                            "name": "Physics-1 6",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for physics-1_06.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "physics-1_02": {
                            "name": "Physics-1 2",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for physics-1_02.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "physics-1_01": {
                            "name": "Physics-1 1",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for physics-1_01.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "physics-2_03": {
                            "name": "Physics-2 3",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for physics-2_03.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "physics-1_05": {
                            "name": "Physics-1 5",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for physics-1_05.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "physics-2_02": {
                            "name": "Physics-2 2",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for physics-2_02.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "physics-2_06": {
                            "name": "Physics-2 6",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for physics-2_06.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "physics-1_08": {
                            "name": "Physics-1 8",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for physics-1_08.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        }
                    }
                },
                15: {
                    "name": "Pe",
                    "chapters": {
                        "pe_02": {
                            "name": "Pe 2",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for pe_02.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "pe_11": {
                            "name": "Pe 11",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for pe_11.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "pe_09": {
                            "name": "Pe 9",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for pe_09.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "pe_03": {
                            "name": "Pe 3",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for pe_03.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "pe_10": {
                            "name": "Pe 10",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for pe_10.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "pe_07": {
                            "name": "Pe 7",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for pe_07.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "pe_05": {
                            "name": "Pe 5",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for pe_05.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "pe_06": {
                            "name": "Pe 6",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for pe_06.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "pe_08": {
                            "name": "Pe 8",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for pe_08.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "pe_01": {
                            "name": "Pe 1",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for pe_01.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        },
                        "pe_04": {
                            "name": "Pe 4",
                            "questions": [
                                {
                                    "id": 1,
                                    "text": "This is a sample MCQ for pe_04.",
                                    "options": [
                                        "Option A",
                                        "Option B",
                                        "Option C",
                                        "Option D"
                                    ],
                                    "correct": 0
                                }
                            ]
                        }
                    }
                }
            }
        }
    }
}

# PRACTICE_DATA = {
#     "classes": {
#         1: {
#             "name": "class-9",
#             "subjects": {
#                 1: {
#                     "name": "English",
#                     "chapters": {
#                         "eng_prose_03": {
#                             "name": "Eng Prose 03",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for eng_prose_03.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "eng_prose_06": {
#                             "name": "Eng Prose 06",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for eng_prose_06.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "eng_poem_07": {
#                             "name": "Eng Poem 07",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for eng_poem_07.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "eng_prose_07": {
#                             "name": "Eng Prose 07",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for eng_prose_07.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "eng_poem_05": {
#                             "name": "Eng Poem 05",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for eng_poem_05.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "eng_poem_01": {
#                             "name": "Eng Poem 01",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for eng_poem_01.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "eng_prose_09": {
#                             "name": "Eng Prose 09",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for eng_prose_09.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "eng_poem_08": {
#                             "name": "Eng Poem 08",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for eng_poem_08.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "eng_prose_04": {
#                             "name": "Eng Prose 04",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for eng_prose_04.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "eng_prose_02": {
#                             "name": "Eng Prose 02",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for eng_prose_02.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "eng_poem_02": {
#                             "name": "Eng Poem 02",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for eng_poem_02.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "eng_prose_01": {
#                             "name": "Eng Prose 01",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for eng_prose_01.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "eng_prose_08": {
#                             "name": "Eng Prose 08",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for eng_prose_08.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "eng_poem_03": {
#                             "name": "Eng Poem 03",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for eng_poem_03.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "eng_poem_06": {
#                             "name": "Eng Poem 06",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for eng_poem_06.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "eng_prose_05": {
#                             "name": "Eng Prose 05",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for eng_prose_05.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "eng_poem_04": {
#                             "name": "Eng Poem 04",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for eng_poem_04.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         }
#                     }
#                 },
#                 2: {
#                     "name": "Maths",
#                     "chapters": {
#                         "maths_05": {
#                             "name": "Maths 05",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for maths_05.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "maths_01": {
#                             "name": "Maths 01",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for maths_01.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "maths_09": {
#                             "name": "Maths 09",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for maths_09.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "maths_08": {
#                             "name": "Maths 08",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for maths_08.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "maths_10": {
#                             "name": "Maths 10",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for maths_10.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "maths_03": {
#                             "name": "Maths 03",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for maths_03.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "maths_12": {
#                             "name": "Maths 12",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for maths_12.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "maths_04": {
#                             "name": "Maths 04",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for maths_04.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "maths_07": {
#                             "name": "Maths 07",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for maths_07.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "maths_02": {
#                             "name": "Maths 02",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for maths_02.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "maths_11": {
#                             "name": "Maths 11",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for maths_11.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "maths_06": {
#                             "name": "Maths 06",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for maths_06.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         }
#                     }
#                 },
#                 3: {
#                     "name": "Ss",
#                     "chapters": {
#                         "ss_eco_03": {
#                             "name": "Ss Eco 03",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for ss_eco_03.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "ss_civics_04": {
#                             "name": "Ss Civics 04",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for ss_civics_04.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "ss_geo_03": {
#                             "name": "Ss Geo 03",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for ss_geo_03.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "ss_civics_03": {
#                             "name": "Ss Civics 03",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for ss_civics_03.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "ss_history_04": {
#                             "name": "Ss History 04",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for ss_history_04.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "ss_history_03": {
#                             "name": "Ss History 03",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for ss_history_03.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "ss_civics_02": {
#                             "name": "Ss Civics 02",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for ss_civics_02.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "ss_history_05": {
#                             "name": "Ss History 05",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for ss_history_05.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "ss_geo_04": {
#                             "name": "Ss Geo 04",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for ss_geo_04.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "ss_eco_04": {
#                             "name": "Ss Eco 04",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for ss_eco_04.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "ss_eco_01": {
#                             "name": "Ss Eco 01",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for ss_eco_01.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "ss_eco_02": {
#                             "name": "Ss Eco 02",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for ss_eco_02.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "ss_geo_05": {
#                             "name": "Ss Geo 05",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for ss_geo_05.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "ss_civics_05": {
#                             "name": "Ss Civics 05",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for ss_civics_05.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "ss_history_02": {
#                             "name": "Ss History 02",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for ss_history_02.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "ss_history_01": {
#                             "name": "Ss History 01",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for ss_history_01.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "ss_civics_01": {
#                             "name": "Ss Civics 01",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for ss_civics_01.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "ss_geo_02": {
#                             "name": "Ss Geo 02",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for ss_geo_02.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "ss_geo_01": {
#                             "name": "Ss Geo 01",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for ss_geo_01.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "ss_geo_06": {
#                             "name": "Ss Geo 06",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for ss_geo_06.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         }
#                     }
#                 },
#                 4: {
#                     "name": "Science",
#                     "chapters": {
#                         "science_12": {
#                             "name": "Science 12",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for science_12.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "science_09": {
#                             "name": "Science 09",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for science_09.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "science_10": {
#                             "name": "Science 10",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for science_10.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "science_01": {
#                             "name": "Science 01",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for science_01.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "science_05": {
#                             "name": "Science 05",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for science_05.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "science_11": {
#                             "name": "Science 11",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for science_11.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "science_08": {
#                             "name": "Science 08",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for science_08.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "science_07": {
#                             "name": "Science 07",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for science_07.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "science_02": {
#                             "name": "Science 02",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for science_02.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "science_03": {
#                             "name": "Science 03",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for science_03.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "science_04": {
#                             "name": "Science 04",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for science_04.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "science_06": {
#                             "name": "Science 06",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for science_06.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         }
#                     }
#                 }
#             }
#         },
#         2: {
#             "name": "class-10",
#             "subjects": {
#                 1: {
#                     "name": "Civics",
#                     "chapters": {
#                         "civics_02.pdf": {
#                             "name": "Civics 02.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for civics_02.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "civics_01.pdf": {
#                             "name": "Civics 01.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for civics_01.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "civics_04.pdf": {
#                             "name": "Civics 04.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for civics_04.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "civics_03.pdf": {
#                             "name": "Civics 03.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for civics_03.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "civics_05.pdf": {
#                             "name": "Civics 05.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for civics_05.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         }
#                     }
#                 },
#                 2: {
#                     "name": "History",
#                     "chapters": {
#                         "history_01.pdf": {
#                             "name": "History 01.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for history_01.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "history_02.pdf": {
#                             "name": "History 02.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for history_02.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "history_04.pdf": {
#                             "name": "History 04.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for history_04.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "history_05.pdf": {
#                             "name": "History 05.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for history_05.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "history_03.pdf": {
#                             "name": "History 03.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for history_03.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         }
#                     }
#                 },
#                 3: {
#                     "name": "Economics",
#                     "chapters": {
#                         "economics_05.pdf": {
#                             "name": "Economics 05.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for economics_05.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "economics_04.pdf": {
#                             "name": "Economics 04.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for economics_04.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "economics_03.pdf": {
#                             "name": "Economics 03.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for economics_03.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "economics_02.pdf": {
#                             "name": "Economics 02.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for economics_02.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "economics_01.pdf": {
#                             "name": "Economics 01.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for economics_01.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         }
#                     }
#                 },
#                 4: {
#                     "name": "English",
#                     "chapters": {
#                         "1_words": {
#                             "name": "1 Words",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for 1_words.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "2_words": {
#                             "name": "2 Words",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for 2_words.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "3_words": {
#                             "name": "3 Words",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for 3_words.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "4_words": {
#                             "name": "4 Words",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for 4_words.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "5_words": {
#                             "name": "5 Words",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for 5_words.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "6_words": {
#                             "name": "6 Words",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for 6_words.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "7_words": {
#                             "name": "7 Words",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for 7_words.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "8_words": {
#                             "name": "8 Words",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for 8_words.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "9_words": {
#                             "name": "9 Words",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for 9_words.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "1_flight": {
#                             "name": "1 Flight",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for 1_flight.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "2_flight": {
#                             "name": "2 Flight",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for 2_flight.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "3_flight": {
#                             "name": "3 Flight",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for 3_flight.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "4_flight": {
#                             "name": "4 Flight",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for 4_flight.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "5_flight": {
#                             "name": "5 Flight",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for 5_flight.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "6_flight": {
#                             "name": "6 Flight",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for 6_flight.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "7_flight": {
#                             "name": "7 Flight",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for 7_flight.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "8_flight": {
#                             "name": "8 Flight",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for 8_flight.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "9_flight": {
#                             "name": "9 Flight",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for 9_flight.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "1_footprint": {
#                             "name": "1 Footprint",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for 1_footprint.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "2_footprint": {
#                             "name": "2 Footprint",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for 2_footprint.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "3_footprint": {
#                             "name": "3 Footprint",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for 3_footprint.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "4_footprint": {
#                             "name": "4 Footprint",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for 4_footprint.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "5_footprint": {
#                             "name": "5 Footprint",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for 5_footprint.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "6_footprint": {
#                             "name": "6 Footprint",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for 6_footprint.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "7_footprint": {
#                             "name": "7 Footprint",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for 7_footprint.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "8_footprint": {
#                             "name": "8 Footprint",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for 8_footprint.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "9_footprint": {
#                             "name": "9 Footprint",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for 9_footprint.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         }
#                     }
#                 },
#                 5: {
#                     "name": "Geography",
#                     "chapters": {
#                         "geography_04.pdf": {
#                             "name": "Geography 04.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for geography_04.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "geography_06.pdf": {
#                             "name": "Geography 06.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for geography_06.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "geography_05.pdf": {
#                             "name": "Geography 05.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for geography_05.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "geography_07.pdf": {
#                             "name": "Geography 07.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for geography_07.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "geography_03.pdf": {
#                             "name": "Geography 03.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for geography_03.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "geography_01.pdf": {
#                             "name": "Geography 01.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for geography_01.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "geography_02.pdf": {
#                             "name": "Geography 02.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for geography_02.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         }
#                     }
#                 },
#                 6: {
#                     "name": "Maths",
#                     "chapters": {
#                         "maths_03.pdf": {
#                             "name": "Maths 03.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for maths_03.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "maths_13.pdf": {
#                             "name": "Maths 13.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for maths_13.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "maths_02.pdf": {
#                             "name": "Maths 02.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for maths_02.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "maths_08.pdf": {
#                             "name": "Maths 08.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for maths_08.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "maths_07.pdf": {
#                             "name": "Maths 07.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for maths_07.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "maths_01.pdf": {
#                             "name": "Maths 01.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for maths_01.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "maths_11.pdf": {
#                             "name": "Maths 11.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for maths_11.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "maths_12.pdf": {
#                             "name": "Maths 12.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for maths_12.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "maths_04.pdf": {
#                             "name": "Maths 04.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for maths_04.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "maths_14.pdf": {
#                             "name": "Maths 14.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for maths_14.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "maths_06.pdf": {
#                             "name": "Maths 06.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for maths_06.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "maths_10.pdf": {
#                             "name": "Maths 10.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for maths_10.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "maths_05.pdf": {
#                             "name": "Maths 05.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for maths_05.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "maths_09.pdf": {
#                             "name": "Maths 09.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for maths_09.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         }
#                     }
#                 },
#                 7: {
#                     "name": "Ss",
#                     "chapters": {
#                         "civics_02.pdf": {
#                             "name": "Civics 02.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for civics_02.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "civics_01.pdf": {
#                             "name": "Civics 01.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for civics_01.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "civics_04.pdf": {
#                             "name": "Civics 04.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for civics_04.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "civics_03.pdf": {
#                             "name": "Civics 03.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for civics_03.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "civics_05.pdf": {
#                             "name": "Civics 05.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for civics_05.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "history_01.pdf": {
#                             "name": "History 01.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for history_01.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "history_02.pdf": {
#                             "name": "History 02.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for history_02.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "history_04.pdf": {
#                             "name": "History 04.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for history_04.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "history_05.pdf": {
#                             "name": "History 05.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for history_05.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "history_03.pdf": {
#                             "name": "History 03.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for history_03.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "economics_05.pdf": {
#                             "name": "Economics 05.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for economics_05.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "economics_04.pdf": {
#                             "name": "Economics 04.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for economics_04.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "economics_03.pdf": {
#                             "name": "Economics 03.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for economics_03.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "economics_02.pdf": {
#                             "name": "Economics 02.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for economics_02.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "economics_01.pdf": {
#                             "name": "Economics 01.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for economics_01.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "geography_04.pdf": {
#                             "name": "Geography 04.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for geography_04.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "geography_06.pdf": {
#                             "name": "Geography 06.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for geography_06.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "geography_05.pdf": {
#                             "name": "Geography 05.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for geography_05.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "geography_07.pdf": {
#                             "name": "Geography 07.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for geography_07.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "geography_03.pdf": {
#                             "name": "Geography 03.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for geography_03.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "geography_01.pdf": {
#                             "name": "Geography 01.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for geography_01.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "geography_02.pdf": {
#                             "name": "Geography 02.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for geography_02.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         }
#                     }
#                 },
#                 8: {
#                     "name": "Science",
#                     "chapters": {
#                         "science_01.pdf": {
#                             "name": "Science 01.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for science_01.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "science_09.pdf": {
#                             "name": "Science 09.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for science_09.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "science_08.pdf": {
#                             "name": "Science 08.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for science_08.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "science_02.pdf": {
#                             "name": "Science 02.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for science_02.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "science_06.pdf": {
#                             "name": "Science 06.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for science_06.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "science_03.pdf": {
#                             "name": "Science 03.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for science_03.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "science_07.pdf": {
#                             "name": "Science 07.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for science_07.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "science_05.pdf": {
#                             "name": "Science 05.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for science_05.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "science_11.pdf": {
#                             "name": "Science 11.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for science_11.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "science_10.pdf": {
#                             "name": "Science 10.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for science_10.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "science_13.pdf": {
#                             "name": "Science 13.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for science_13.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "science_04.pdf": {
#                             "name": "Science 04.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for science_04.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "science_12.pdf": {
#                             "name": "Science 12.Pdf",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for science_12.pdf.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         }
#                     }
#                 }
#             }
#         },
#         3: {
#             "name": "class-11",
#             "subjects": {
#                 1: {
#                     "name": "Biology",
#                     "chapters": {
#                         "biology_09": {
#                             "name": "Biology 09",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for biology_09.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "biology_15": {
#                             "name": "Biology 15",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for biology_15.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "biology_07": {
#                             "name": "Biology 07",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for biology_07.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "biology_11": {
#                             "name": "Biology 11",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for biology_11.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "biology_04": {
#                             "name": "Biology 04",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for biology_04.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "biology_02": {
#                             "name": "Biology 02",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for biology_02.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "biology_05": {
#                             "name": "Biology 05",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for biology_05.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "biology_03": {
#                             "name": "Biology 03",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for biology_03.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "biology_14": {
#                             "name": "Biology 14",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for biology_14.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "biology_12": {
#                             "name": "Biology 12",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for biology_12.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "biology_13": {
#                             "name": "Biology 13",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for biology_13.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "biology_06": {
#                             "name": "Biology 06",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for biology_06.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "biology_08": {
#                             "name": "Biology 08",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for biology_08.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "biology_17": {
#                             "name": "Biology 17",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for biology_17.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "biology_19": {
#                             "name": "Biology 19",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for biology_19.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "biology_18": {
#                             "name": "Biology 18",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for biology_18.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "biology_10": {
#                             "name": "Biology 10",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for biology_10.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "biology_16": {
#                             "name": "Biology 16",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for biology_16.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "biology_01": {
#                             "name": "Biology 01",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for biology_01.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         }
#                     }
#                 },
#                 2: {
#                     "name": "English",
#                     "chapters": {
#                         "english_ss_04": {
#                             "name": "English Ss 04",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for english_ss_04.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "english_hb_01": {
#                             "name": "English Hb 01",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for english_hb_01.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "english_hb_11": {
#                             "name": "English Hb 11",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for english_hb_11.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "english_hb_07": {
#                             "name": "English Hb 07",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for english_hb_07.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "english_hb_05": {
#                             "name": "English Hb 05",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for english_hb_05.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "english_ss_01": {
#                             "name": "English Ss 01",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for english_ss_01.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "english_ss_03": {
#                             "name": "English Ss 03",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for english_ss_03.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "english_hb_08": {
#                             "name": "English Hb 08",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for english_hb_08.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "english_hb_12": {
#                             "name": "English Hb 12",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for english_hb_12.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "english_ss_05": {
#                             "name": "English Ss 05",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for english_ss_05.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "english_hb_02": {
#                             "name": "English Hb 02",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for english_hb_02.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "english_hb_10": {
#                             "name": "English Hb 10",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for english_hb_10.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "english_hb_06": {
#                             "name": "English Hb 06",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for english_hb_06.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "english_hb_09": {
#                             "name": "English Hb 09",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for english_hb_09.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "english_hb_04": {
#                             "name": "English Hb 04",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for english_hb_04.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "english_hb_03": {
#                             "name": "English Hb 03",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for english_hb_03.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "english_ss_02": {
#                             "name": "English Ss 02",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for english_ss_02.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         }
#                     }
#                 },
#                 3: {
#                     "name": "Chemistry",
#                     "chapters": {
#                         "chemistry-1_06": {
#                             "name": "Chemistry-1 06",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for chemistry-1_06.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "chemistry-1_02": {
#                             "name": "Chemistry-1 02",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for chemistry-1_02.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "chemistry-2_02": {
#                             "name": "Chemistry-2 02",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for chemistry-2_02.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "chemistry-2_01": {
#                             "name": "Chemistry-2 01",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for chemistry-2_01.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "chemistry-2_03": {
#                             "name": "Chemistry-2 03",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for chemistry-2_03.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "chemistry-1_04": {
#                             "name": "Chemistry-1 04",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for chemistry-1_04.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "chemistry-1_05": {
#                             "name": "Chemistry-1 05",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for chemistry-1_05.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "chemistry-1_01": {
#                             "name": "Chemistry-1 01",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for chemistry-1_01.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "chemistry-1_03": {
#                             "name": "Chemistry-1 03",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for chemistry-1_03.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         }
#                     }
#                 },
#                 4: {
#                     "name": "Maths",
#                     "chapters": {
#                         "maths_13": {
#                             "name": "Maths 13",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for maths_13.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "maths_10": {
#                             "name": "Maths 10",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for maths_10.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "maths_12": {
#                             "name": "Maths 12",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for maths_12.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "maths_03": {
#                             "name": "Maths 03",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for maths_03.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "maths_08": {
#                             "name": "Maths 08",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for maths_08.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "maths_02": {
#                             "name": "Maths 02",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for maths_02.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "maths_04": {
#                             "name": "Maths 04",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for maths_04.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "maths_01": {
#                             "name": "Maths 01",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for maths_01.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "maths_07": {
#                             "name": "Maths 07",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for maths_07.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "maths_05": {
#                             "name": "Maths 05",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for maths_05.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "maths_06": {
#                             "name": "Maths 06",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for maths_06.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "maths_11": {
#                             "name": "Maths 11",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for maths_11.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "maths_14": {
#                             "name": "Maths 14",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for maths_14.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "maths_09": {
#                             "name": "Maths 09",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for maths_09.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         }
#                     }
#                 },
#                 5: {
#                     "name": "Physics",
#                     "chapters": {
#                         "physics-2_04": {
#                             "name": "Physics-2 04",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for physics-2_04.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "physics-2_05": {
#                             "name": "Physics-2 05",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for physics-2_05.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "physics-2_01": {
#                             "name": "Physics-2 01",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for physics-2_01.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "physics-1_03": {
#                             "name": "Physics-1 03",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for physics-1_03.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "physics-1_04": {
#                             "name": "Physics-1 04",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for physics-1_04.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "physics-1_07": {
#                             "name": "Physics-1 07",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for physics-1_07.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "physics-1_06": {
#                             "name": "Physics-1 06",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for physics-1_06.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "physics-1_02": {
#                             "name": "Physics-1 02",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for physics-1_02.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "physics-2_07": {
#                             "name": "Physics-2 07",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for physics-2_07.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "physics-1_01": {
#                             "name": "Physics-1 01",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for physics-1_01.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "physics-2_03": {
#                             "name": "Physics-2 03",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for physics-2_03.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "physics-1_05": {
#                             "name": "Physics-1 05",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for physics-1_05.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "physics-2_02": {
#                             "name": "Physics-2 02",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for physics-2_02.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "physics-2_06": {
#                             "name": "Physics-2 06",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for physics-2_06.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         }
#                     }
#                 },
#                 6: {
#                     "name": "Pe",
#                     "chapters": {
#                         "pe_02": {
#                             "name": "Pe 02",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for pe_02.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "pe_11": {
#                             "name": "Pe 11",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for pe_11.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "pe_09": {
#                             "name": "Pe 09",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for pe_09.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "pe_03": {
#                             "name": "Pe 03",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for pe_03.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "pe_10": {
#                             "name": "Pe 10",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for pe_10.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "pe_07": {
#                             "name": "Pe 07",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for pe_07.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "pe_05": {
#                             "name": "Pe 05",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for pe_05.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "pe_06": {
#                             "name": "Pe 06",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for pe_06.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "pe_08": {
#                             "name": "Pe 08",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for pe_08.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "pe_01": {
#                             "name": "Pe 01",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for pe_01.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "pe_04": {
#                             "name": "Pe 04",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for pe_04.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         }
#                     }
#                 }
#             }
#         },
#         4: {
#             "name": "class-12",
#             "subjects": {
#                 1: {
#                     "name": "History",
#                     "chapters": {
#                         "history-1_04": {
#                             "name": "History-1 04",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for history-1_04.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "history-1_03": {
#                             "name": "History-1 03",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for history-1_03.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "history-2_03": {
#                             "name": "History-2 03",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for history-2_03.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "history-1_02": {
#                             "name": "History-1 02",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for history-1_02.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "history-2_04": {
#                             "name": "History-2 04",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for history-2_04.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "history-3_04": {
#                             "name": "History-3 04",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for history-3_04.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "history-2_01": {
#                             "name": "History-2 01",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for history-2_01.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "history-1_01": {
#                             "name": "History-1 01",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for history-1_01.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "history-3_02": {
#                             "name": "History-3 02",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for history-3_02.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "history-3_03": {
#                             "name": "History-3 03",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for history-3_03.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "history-2_02": {
#                             "name": "History-2 02",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for history-2_02.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "history-3_01": {
#                             "name": "History-3 01",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for history-3_01.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         }
#                     }
#                 },
#                 2: {
#                     "name": "Biology",
#                     "chapters": {
#                         "biology_09": {
#                             "name": "Biology 09",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for biology_09.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "biology_07": {
#                             "name": "Biology 07",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for biology_07.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "biology_11": {
#                             "name": "Biology 11",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for biology_11.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "biology_04": {
#                             "name": "Biology 04",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for biology_04.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "biology_02": {
#                             "name": "Biology 02",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for biology_02.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "biology_05": {
#                             "name": "Biology 05",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for biology_05.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "biology_03": {
#                             "name": "Biology 03",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for biology_03.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "biology_12": {
#                             "name": "Biology 12",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for biology_12.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "biology_13": {
#                             "name": "Biology 13",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for biology_13.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "biology_06": {
#                             "name": "Biology 06",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for biology_06.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "biology_08": {
#                             "name": "Biology 08",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for biology_08.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "biology_10": {
#                             "name": "Biology 10",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for biology_10.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "biology_01": {
#                             "name": "Biology 01",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for biology_01.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         }
#                     }
#                 },
#                 3: {
#                     "name": "English",
#                     "chapters": {
#                         "english-fl_04": {
#                             "name": "English-Fl 04",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for english-fl_04.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "english-fl_12": {
#                             "name": "English-Fl 12",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for english-fl_12.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "english-fl_03": {
#                             "name": "English-Fl 03",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for english-fl_03.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "english-fl_09": {
#                             "name": "English-Fl 09",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for english-fl_09.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "english-fl_08": {
#                             "name": "English-Fl 08",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for english-fl_08.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "english-vs-06": {
#                             "name": "English-Vs-06",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for english-vs-06.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "english-fl_01": {
#                             "name": "English-Fl 01",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for english-fl_01.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "english-fl_11": {
#                             "name": "English-Fl 11",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for english-fl_11.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "english-fl_06": {
#                             "name": "English-Fl 06",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for english-fl_06.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "english-vs-01": {
#                             "name": "English-Vs-01",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for english-vs-01.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "english-vs-03": {
#                             "name": "English-Vs-03",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for english-vs-03.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "english-fl_10": {
#                             "name": "English-Fl 10",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for english-fl_10.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "english-vs-05": {
#                             "name": "English-Vs-05",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for english-vs-05.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "english-fl_07": {
#                             "name": "English-Fl 07",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for english-fl_07.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "english-fl_13": {
#                             "name": "English-Fl 13",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for english-fl_13.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "english-fl_05": {
#                             "name": "English-Fl 05",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for english-fl_05.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "english-vs-04": {
#                             "name": "English-Vs-04",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for english-vs-04.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "english-fl_02": {
#                             "name": "English-Fl 02",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for english-fl_02.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "english-vs-02": {
#                             "name": "English-Vs-02",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for english-vs-02.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         }
#                     }
#                 },
#                 4: {
#                     "name": "Chemistry",
#                     "chapters": {
#                         "chemistry-2_05": {
#                             "name": "Chemistry-2 05",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for chemistry-2_05.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "chemistry-2_04": {
#                             "name": "Chemistry-2 04",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for chemistry-2_04.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "chemistry-1_02": {
#                             "name": "Chemistry-1 02",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for chemistry-1_02.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "chemistry-2_02": {
#                             "name": "Chemistry-2 02",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for chemistry-2_02.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "chemistry-2_01": {
#                             "name": "Chemistry-2 01",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for chemistry-2_01.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "chemistry-2_03": {
#                             "name": "Chemistry-2 03",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for chemistry-2_03.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "chemistry-1_04": {
#                             "name": "Chemistry-1 04",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for chemistry-1_04.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "chemistry-1_05": {
#                             "name": "Chemistry-1 05",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for chemistry-1_05.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "chemistry-1_01": {
#                             "name": "Chemistry-1 01",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for chemistry-1_01.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "chemistry-1_03": {
#                             "name": "Chemistry-1 03",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for chemistry-1_03.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         }
#                     }
#                 },
#                 5: {
#                     "name": "Maths",
#                     "chapters": {
#                         "maths-2_02": {
#                             "name": "Maths-2 02",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for maths-2_02.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "maths-1_05": {
#                             "name": "Maths-1 05",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for maths-1_05.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "maths-2_01": {
#                             "name": "Maths-2 01",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for maths-2_01.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "maths-1_06": {
#                             "name": "Maths-1 06",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for maths-1_06.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "maths-1_01": {
#                             "name": "Maths-1 01",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for maths-1_01.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "maths-1_04": {
#                             "name": "Maths-1 04",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for maths-1_04.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "maths-2_07": {
#                             "name": "Maths-2 07",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for maths-2_07.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "maths-1_03": {
#                             "name": "Maths-1 03",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for maths-1_03.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "maths-2_06": {
#                             "name": "Maths-2 06",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for maths-2_06.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "maths-2_04": {
#                             "name": "Maths-2 04",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for maths-2_04.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "maths-2_05": {
#                             "name": "Maths-2 05",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for maths-2_05.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "maths-2_03": {
#                             "name": "Maths-2 03",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for maths-2_03.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "maths-1_02": {
#                             "name": "Maths-1 02",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for maths-1_02.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         }
#                     }
#                 },
#                 6: {
#                     "name": "Physics",
#                     "chapters": {
#                         "physics-2_04": {
#                             "name": "Physics-2 04",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for physics-2_04.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "physics-2_05": {
#                             "name": "Physics-2 05",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for physics-2_05.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "physics-2_01": {
#                             "name": "Physics-2 01",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for physics-2_01.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "physics-1_03": {
#                             "name": "Physics-1 03",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for physics-1_03.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "physics-1_04": {
#                             "name": "Physics-1 04",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for physics-1_04.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "physics-1_07": {
#                             "name": "Physics-1 07",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for physics-1_07.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "physics-1_06": {
#                             "name": "Physics-1 06",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for physics-1_06.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "physics-1_02": {
#                             "name": "Physics-1 02",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for physics-1_02.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "physics-1_01": {
#                             "name": "Physics-1 01",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for physics-1_01.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "physics-2_03": {
#                             "name": "Physics-2 03",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for physics-2_03.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "physics-1_05": {
#                             "name": "Physics-1 05",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for physics-1_05.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "physics-2_02": {
#                             "name": "Physics-2 02",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for physics-2_02.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "physics-2_06": {
#                             "name": "Physics-2 06",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for physics-2_06.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "physics-1_08": {
#                             "name": "Physics-1 08",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for physics-1_08.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         }
#                     }
#                 },
#                 7: {
#                     "name": "Pe",
#                     "chapters": {
#                         "pe_02": {
#                             "name": "Pe 02",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for pe_02.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "pe_11": {
#                             "name": "Pe 11",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for pe_11.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "pe_09": {
#                             "name": "Pe 09",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for pe_09.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "pe_03": {
#                             "name": "Pe 03",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for pe_03.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "pe_10": {
#                             "name": "Pe 10",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for pe_10.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "pe_07": {
#                             "name": "Pe 07",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for pe_07.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "pe_05": {
#                             "name": "Pe 05",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for pe_05.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "pe_06": {
#                             "name": "Pe 06",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for pe_06.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "pe_08": {
#                             "name": "Pe 08",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for pe_08.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "pe_01": {
#                             "name": "Pe 01",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for pe_01.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         },
#                         "pe_04": {
#                             "name": "Pe 04",
#                             "questions": [
#                                 {
#                                     "id": 1,
#                                     "text": "This is a sample MCQ for pe_04.",
#                                     "options": [
#                                         "Option A",
#                                         "Option B",
#                                         "Option C",
#                                         "Option D"
#                                     ],
#                                     "correct": 0
#                                 }
#                             ]
#                         }
#                     }
#                 }
#             }
#         }
#     }
# }


@app.route('/practice')
@app.route('/gurukulai/practice')
def practice():
    classes = [{"id": k, "name": v["name"]} for k,v in PRACTICE_DATA["classes"].items()]
    return render_template('practice.html', classes=classes)

@app.route('/practice/get_subjects/<int:class_id>')
@app.route('/gurukulai/practice/get_subjects/<int:class_id>')
def get_subjects(class_id):
    try:
        print(f"ROUTE HIT: /practice/get_subjects/{class_id}")
        class_data = PRACTICE_DATA["classes"].get(class_id)
        if not class_data:
            return jsonify({"error": "Class not found"}), 404
            
        subjects = [{"id": k, "name": v["name"]} 
               for k,v in class_data.get("subjects", {}).items()]
        print(f"Returning subjects: {subjects}")
        return jsonify(subjects)
    except Exception as e:
        print(f"Error in get_subjects: {str(e)}")
        return jsonify([]), 500


@app.route('/practice/get_chapters/<int:subject_id>')
@app.route('/gurukulai/practice/get_chapters/<int:subject_id>')
def get_chapters(subject_id):
    # Find the subject in any class
    chapters = []
    for class_data in PRACTICE_DATA["classes"].values():
        if subject_id in class_data["subjects"]:
            chapters = [{"id": k, "name": v["name"]} 
                       for k,v in class_data["subjects"][subject_id]["chapters"].items()]
            break
    return jsonify(chapters)

# @app.route('/practice/get_questions/<int:chapter_id>')
# @app.route('/gurukulai/practice/get_questions/<int:chapter_id>')
# def get_questions(chapter_id):
#     # Find the chapter in any subject/class
#     questions = []
#     for class_data in PRACTICE_DATA["classes"].values():
#         for subject in class_data["subjects"].values():
#             if chapter_id in subject["chapters"]:
#                 questions = subject["chapters"][chapter_id]["questions"]
#                 break
#     return jsonify(questions)

@app.route("/list_routes")
def list_routes():
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            "endpoint": rule.endpoint,
            "methods": list(rule.methods),
            "path": str(rule)
        })
    return jsonify(routes)

@app.route("/process_ocr", methods=["POST"])
@app.route("/gurukulai/process_ocr", methods=["POST"])
def process_ocr():
    try:
        # Check if file is in request
        if 'image' in request.files:
            # Get the file from the request
            image_file = request.files['image']
            
            # Open and process the image
            image = Image.open(image_file)
            
            # Extract text using pytesseract
            extracted_text = pytesseract.image_to_string(image)
            
            # Clean up the text (remove excessive newlines, etc.)
            extracted_text = re.sub(r'\n+', '\n', extracted_text).strip()
            
            return jsonify({"success": True, "text": extracted_text})
        
        # Check if base64 image is in request (alternative method)
        elif 'imageData' in request.json:
            image_data = request.json['imageData']
            
            # Extract the base64 part (remove the data:image/*;base64, prefix)
            if ',' in image_data:
                image_data = image_data.split(',')[1]
            
            # Decode base64 to image
            image_bytes = base64.b64decode(image_data)
            image = Image.open(io.BytesIO(image_bytes))
            
            # Extract text using pytesseract
            extracted_text = pytesseract.image_to_string(image)
            
            # Clean up the text
            extracted_text = re.sub(r'\n+', '\n', extracted_text).strip()
            
            return jsonify({"success": True, "text": extracted_text})
        
        else:
            return jsonify({"error": "No image provided"}), 400
            
    except Exception as e:
        print(f"OCR Error: {str(e)}")
        return jsonify({"error": f"Failed to process image: {str(e)}"}), 500





@app.route("/generate_suggestions", methods=["POST"])
@app.route("/gurukulai/generate_suggestions", methods=["POST"])
def generate_suggestions():
    try:
        # Get the question, answer, class, and subject from the request
        data = request.json
        question = data.get("question")
        answer = data.get("answer")
        class_name = data.get("class")
        subject = data.get("subject")
        
        if not question or not answer:
            return jsonify({"error": "Missing question or answer"}), 400
        
        # Call the model API to generate suggestions
        api_url = "http://10.0.62.205:3223/generate_suggestions"  # Adjust to your backend API URL
        
        response = requests.post(api_url, json={
            "question": question,
            "answer": answer,
            "class": class_name,
            "subject": subject
        })
        
        if response.status_code != 200:
            print(f"API error: {response.status_code}, {response.text}")
            return jsonify({"suggestions": get_fallback_suggestions(question, subject)}), 200
            
        return jsonify(response.json())
        
    except Exception as e:
        print(f"Error generating suggestions: {e}")
        # Return some generic follow-up questions as fallback
        return jsonify({"suggestions": get_fallback_suggestions(question, subject)}), 200

# Function to generate fallback suggestions if the API fails
def get_fallback_suggestions(question, subject):
    # Simple fallback logic based on subject
    if "math" in subject.lower():
        return [
            "Can you explain this concept with an example?",
            "What's the application of this in real life?",
            "How do I solve more complex problems like this?"
        ]
    elif "science" in subject.lower():
        return [
            "What's the theory behind this?",
            "Can you explain related concepts?",
            "How is this applied in experiments?"
        ]
    elif "english" in subject.lower():
        return [
            "Can you provide more examples?",
            "How does this apply to literature?",
            "What are similar expressions or concepts?"
        ]
    else:
        return [
            "Can you explain this in more detail?",
            "What are related topics I should know?",
            "How can I learn more about this?"
        ]




@app.route("/upload_query", methods=["POST"])
@app.route("/gurukulai/upload_query", methods=["POST"])
def upload_query():
    print('hello from Isha')
    try:
        # Get the user's query from the POST request
        user_query = request.json.get("query", "")
        ocr_text = request.json.get("ocrText", "")
        is_ocr = request.json.get("isOcr", False)
        user_class = request.json.get("class")
        user_subject = request.json.get("subject")

        if not (user_query or ocr_text) or not user_class or not user_subject:
            return {"error": "Empty data received. Please provide a valid query or OCR text."}, 400

        # Combine query and OCR text if both are available
        combined_query = user_query
        if is_ocr and ocr_text:
            if user_query:
                combined_query = f"{user_query}\n\nText extracted from OCR: {ocr_text}"
            else:
                combined_query = ocr_text
        
        api_url = "http://10.0.62.205:3223/upload_query"

        # Prepare the data to send to the API
        data = {
            "query": combined_query,
            "class": user_class,
            "subject": user_subject,
            "isOcr": is_ocr
        }
        print('hello world!')
        # Send the POST request to the backend API
        response = requests.post(api_url, json=data)
        print('third print')
        # Return the API response back to the chatbox
        return jsonify(response.json())

    except Exception as e:
        print(f"Error: {e}")
        return {"error": "Request failed. Please try again."}, 500

# This snippet will extend your Flask app to integrate Google OAuth 2.0 login
# and store user info into a CSV file.

from flask import Flask, redirect, url_for, session, request, render_template
from authlib.integrations.flask_client import OAuth
import csv
import os

# Setup OAuth and user store
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id = os.getenv("GOOGLE_CLIENT_ID"),
    client_secret = os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

CSV_FILE = 'users.csv'

# Login route
@app.route('/login')
@app.route('/gurukulai/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
@app.route('/gurukulai/authorize')
def authorize():
    token = google.authorize_access_token()
    resp = google.get('https://openidconnect.googleapis.com/v1/userinfo')
    user_info = resp.json()

    session.permanent = True
    session['user'] = user_info


    # Save to CSV if new
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['email', 'name'])

    with open(CSV_FILE, mode='r', newline='') as f:
        existing_emails = [row[0] for row in csv.reader(f) if row]

    if user_info['email'] not in existing_emails:
        with open(CSV_FILE, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([user_info['email'], user_info.get('name', '')])

    return redirect('/gurukulai/home')


    

# Logout route
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')



@app.context_processor
def inject_user():
    return dict(user=session.get('user'))

#--


import os
import json
from flask import Flask, request, jsonify
from datetime import datetime

USER_RESPONSES_DIR = "user_responses"

# Ensure the directory exists
os.makedirs(USER_RESPONSES_DIR, exist_ok=True)

def get_user_file(user_name):
    """Get file path for a given user"""
    return os.path.join(USER_RESPONSES_DIR, f"{user_name}.json")

def save_user_answer(user_name, answer_data):
    """Save a user's answer to their JSON file"""
    file_path = get_user_file(user_name)
    
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            history = json.load(f)
    else:
        history = []

    answer_data['timestamp'] = datetime.utcnow().isoformat() + 'Z'
    history.append(answer_data)

    with open(file_path, "w") as f:
        json.dump(history, f, indent=2)

    return True

def load_user_history(user_name):
    """Load the user's answer history"""
    file_path = get_user_file(user_name)
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return []

import requests

from flask import Response, jsonify

@app.route('/practice/get_questions/<chapter_id>')
@app.route('/gurukulai/practice/get_questions/<chapter_id>')
def proxy_get_questions(chapter_id):
    user = request.args.get('user')
    class_id = request.args.get('class')
    subject_id = request.args.get('subject')

    backend_url = f"http://10.0.62.205:3223/practice/get_questions/{chapter_id}?user={user}&class={class_id}&subject={subject_id}"

    try:
        response = requests.get(backend_url, timeout=50)
        
        # Ensure the content is valid JSON and decoded
        json_data = response.json()  # <- Will raise if not valid JSON
        return jsonify(json_data), response.status_code

    except Exception as e:

        print(f"[proxy_get_questions] ERROR: {e}")
        return jsonify({"error": str(e)}), 500




@app.route("/practice/submit_answer", methods=["POST"])
def submit_answer():
    data = request.json
    user = data.get("user")
    answer = data.get("answer")

    if not user or not answer:
        return jsonify({"error": "Missing user or answer"}), 400

    save_user_answer(user, answer)
    return jsonify({"status": "saved"})

@app.route("/practice/get_user_history/<user_name>", methods=["GET"])
def get_user_history(user_name):
    history = load_user_history(user_name)
    return jsonify(history)
@app.route('/practice/get_theory_questions/<chapter_id>')
@app.route('/gurukulai/practice/get_theory_questions/<chapter_id>')
def proxy_get_theory_questions(chapter_id):
    user = request.args.get('user')
    class_name = request.args.get('class')
    subject_name = request.args.get('subject')

    # Validate required parameters
    if not all([user, class_name, subject_name]):
        return jsonify({"error": "Missing required parameters"}), 400

    # Forward the request to the backend service
    backend_url = f"http://10.0.62.205:3223/gurukulai/practice/get_theory_questions/{chapter_id}?user={user}&class={class_name}&subject={subject_name}"

    try:
        app.logger.info(f"Forwarding request to: {backend_url}")
        response = requests.get(backend_url, timeout=50)
        
        # Return the backend response
        return Response(
            response.content,
            status=response.status_code,
            content_type=response.headers.get('Content-Type', 'application/json')
        )

    except Exception as e:
        app.logger.error(f"Error proxying theory questions request: {str(e)}")
        return jsonify({
            "error": "Failed to retrieve theory questions",
            "details": str(e)
        }), 500

# Theory Questions Proxy Endpoints
# @app.route("/practice/get_theory_questions/<chapter_id>")
# @app.route("/gurukulai/practice/get_theory_questions/<chapter_id>")
# def proxy_get_theory_questions(chapter_id):
#     user = request.args.get('user')
#     class_name = request.args.get('class')
#     subject_name = request.args.get('subject')

#     # Validate required parameters
#     if not all([user, class_name, subject_name]):
#         return jsonify({"error": "Missing required parameters"}), 400

#     # Forward the request to the backend service
#     backend_url = f"http://10.0.62.205:3223/gurukulai/practice/get_theory_questions/{chapter_id}?user={user}&class={class_name}&subject={subject_name}"

#     try:
#         print(f"Forwarding theory questions request to: {backend_url}")
#         response = requests.get(backend_url, timeout=50)
        
#         # Ensure the content is valid JSON
#         return Response(
#             response.content,
#             status=response.status_code,
#             content_type=response.headers.get('Content-Type', 'application/json')
#         )

#     except Exception as e:
#         print(f"Error proxying theory questions request: {str(e)}")
#         return jsonify({
#             "error": "Failed to retrieve theory questions",
#             "details": str(e)
#         }), 500

@app.route("/practice/submit_theory_answer", methods=["POST"])
@app.route("/gurukulai/practice/submit_theory_answer", methods=["POST"])
def proxy_submit_theory_answer():
    try:
        data = request.json
        
        # Forward the request to the backend service
        backend_url = "http://10.0.62.205:3223/gurukulai/practice/submit_theory_answer"

        print(f"Forwarding theory answer submission to: {backend_url}")
        print(f"Data being sent: {data}")
        
        response = requests.post(
            backend_url, 
            json=data,
            timeout=50
        )
        
        # Print response for debugging
        print(f"Backend response status: {response.status_code}")
        print(f"Backend response content: {response.content[:200]}")  # First 200 chars for brevity
        
        # Return the backend response
        return Response(
            response.content,
            status=response.status_code,
            content_type=response.headers.get('Content-Type', 'application/json')
        )

    except Exception as e:
        print(f"Error proxying theory answer submission: {str(e)}")
        return jsonify({
            "error": "Failed to submit theory answer",
            "details": str(e)
        }), 500

# Add this to test if the route is working
@app.route("/test_theory_routes")
def test_theory_routes():
    routes = []
    for rule in app.url_map.iter_rules():
        if "theory" in str(rule):
            routes.append({
                "endpoint": rule.endpoint,
                "methods": list(rule.methods),
                "path": str(rule)
            })
    return jsonify(routes)

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3030, debug=True)