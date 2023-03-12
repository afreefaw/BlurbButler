# BlurbButler

chatGPT-based chatbot that reviews relevant local files before responding to your message.

## Setup

Simply clone, [set your OpenAI API key is as an environment variable](https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety), e.g., for windows:
```
setx OPENAI_API_KEY “<yourkey>”
```
and run:

```bash
python butler.py
```
Please note as of Mar 5, 2023, unless you add a payment method to your openai account you will be rate limited and the bot may not work for more than a few messages at a time. At this time I have spent < $0.30 in all testing of BlurbButler.

## Examples
There are example txt files and associated topics provided. The example usage is a personal assistant with access to a few different notes files that the user keeps. Topics are in topics.json, txt files are in /blurbs/.

To try it out, take a look at the .txt files in the blurb files and ask related questions e.g.,
```
> Can you remind me how much salt is in my chili recipe?
> According to the recipe you provided, your chili recipe requires 1 1/2 teaspoons of salt.
```

Here, the user's query has been classified by chatGPT as most related to the topic 'recipes', out of the available topics
```python
['recipes', 'graphics card options', 'finance thoughts', 'media recommendations', 'travel plans']
```
Then, the text file associated with the selected topic has been included (unseen to the user) as context before the bot responds.

Another example:
```
> What books have been suggested to me recently?
> Some of the suggested books include "Where the Crawdads Sing" by Delia Owens, "The Four Winds" by Kristin Hannah, and "Becoming" by Michelle Obama.
```

## Further info

The idea of BlurbButler is to provide a lightweight way to ask questions about topics, context, documents, or any text that you wouldn't normally be able to easily ask chatGPT about, because chatGPT doesn't have access to the relevant information, and the total amount of information you want chatGPT to reference is greater than it can review at one time.

BlurbButler uses chatGPT to classify the topic of your message from within a **preset** set of topics, each associated with a file. If your message is relevant to a topic, the chatbot will review the associated file as context prior to responding. The user must configure the topic list and associated files in advance.

## Use Cases

- **Onboarding help:** A new employee can ask questions and have chatGPT respond, explaining organization specific context.

- **Personal assistant:** Keep some note files such as a todo list or meeting notes and ask questions about them.
