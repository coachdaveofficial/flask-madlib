# from django.shortcuts import render
from stories import Story

from flask import Flask, request, render_template

app = Flask(__name__)

story_1 = Story(
    ["place", "noun", "verb", "adjective", "plural_noun"],
    """Once upon a time in a long-ago {place}, there lived a
       large {adjective} {noun}. It loved to {verb} {plural_noun}."""
)
story_2 = Story(
    ["place", "adjective", "plural_noun", "verb", "noun"],
    """Most people don't know that {place} has many {adjective} {plural_noun}. 
       The best thing to do there is {verb} with the {noun}."""
)
story_3 = Story(
    ["place", "noun", "verb", "adjective", "plural_noun"],
    """Once upon a TEST in a long-ago {place}, there lived a
       large {adjective} {noun}. It loved to {verb} {plural_noun}."""
)

story_dict = {"First": story_1, "Second": story_2, "Third": story_3}


@app.route('/', methods=("GET", "POST"))
def home():
    if request.method == "GET":
        return render_template('story-form.html', stories=story_dict)
    elif request.method == "POST":
        choice = request.form['story-form']
        story = story_dict[choice]
        return render_template('form.html', prompts=story.prompts, story=choice)


# @app.route('/madlib/')
# def story_form():
    
#     return render_template('form.html', prompts=request.args)
    

@app.route('/result/<template>', methods=("GET", "POST"))
def show_story(template):
    story = story_dict[template]
    word_dict = {}
    for prompt in story.prompts:
        word_dict[prompt] = request.args[prompt]
    madlib = story.generate(word_dict)
    return f"""
    <h1>Finished Story</h1>
    <h3>
        {madlib}
    </h3>
    """