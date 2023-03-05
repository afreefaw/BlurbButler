# BlurbButler

chatGPT-based chatbot that reviews relevant local files before responding to your message.

## Setup

Simply clone, paste your openai API key into apikey.txt, and run:

```bash
python butler.py
```

## Examples
There are example txt files and associated topics provided. The example usage is a personal assistant with access to a few different notes files that the user keeps. Topics are in topics.json, txt files are in /blurbs/.

To try it out, take a look at the .txt files in the blurb files and ask related questions e.g.,
```
> Can you remind me how much salt is in my chili recipe?
> According to the recipe you provided, your chili recipe requires 1 1/2 teaspoons of salt.
```

Here, the user's query has been classified by chatGPT as most related to the topic 'recipes', out of the available topics ['recipes', 'graphics card options', 'finance thoughts', 'media recommendations', 'travel plans']

Another example:
```
> What books have been suggested to me recently?
> Some of the suggested books include "Where the Crawdads Sing" by Delia Owens, "The Four Winds" by Kristin Hannah, and "Becoming" by Michelle Obama.
```

## Further info

The idea of BlurbButler is to provide a lightweight way to ask questions about topics, context, documents, or any text that you wouldn't normally be able to easily ask chatGPT about, because chatGPT doesn't have access to the relevant information.

BlurbButler uses chatGPT to classify the topic of your message from within a **preset** set of topics, each associated with a file. If your message is relevant to a topic, the chatbot will review it as context prior to responding.