import requests
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
from PIL import Image, ImageFilter, ImageDraw, ImageFont
from textblob import TextBlob
import random
import datetime
import time


class Content:
    def __init__(self, title, description, link):
        self.title = title
        self.description = description
        self.link = link
        self.caption = None
        self.image = None
        self.personalization = []

    def add_caption(self, text, sentiment):
        self.caption = {
            'text': text,
            'sentiment': sentiment
        }

    def add_image(self, image):
        self.image = image

    def add_personalization(self, preference):
        self.personalization.append(preference)


class ContentScheduler:
    def __init__(self, social_media_platforms):
        self.social_media_platforms = social_media_platforms
        self.content = []
        self.engagement_metrics = {}

    def collect_content(self, keywords):
        for keyword in keywords:
            # Collecting relevant content using BeautifulSoup
            url = f"https://example.com/search?q={keyword}"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.find_all('article')

            for article in articles:
                title = article.find('h2').text.strip()
                description = article.find('p').text.strip()
                link = article.find('a')['href']

                content = Content(title, description, link)
                self.content.append(content)

    def generate_captions(self):
        # Utilizing natural language processing libraries to generate captions
        for content in self.content:
            text = content.description

            # Removing stopwords
            stop_words = set(stopwords.words('english'))
            word_tokens = word_tokenize(text)
            filtered_text = [word for word in word_tokens if word.casefold() not in stop_words]

            # Sentiment analysis
            sentiment_score = SentimentIntensityAnalyzer().polarity_scores(text)['compound']
            sentiment = 'positive' if sentiment_score > 0 else 'negative' if sentiment_score < 0 else 'neutral'

            content.add_caption(' '.join(filtered_text), sentiment)

    def modify_images(self):
        image_paths = ['image1.jpg', 'image2.jpg', 'image3.jpg']

        for content in self.content:
            img_path = random.choice(image_paths)
            img = Image.open(img_path)
            draw = ImageDraw.Draw(img)

            # Adding text overlay
            caption = content.caption['text']
            font = ImageFont.truetype('arial.ttf', size=30)
            draw.text((10, 10), caption, fill='white', font=font)

            # Applying image filters
            img = img.filter(ImageFilter.BLUR)

            content.add_image(img)

    def schedule_content(self):
        now = datetime.datetime.now()

        for content in self.content:
            publish_time = now + datetime.timedelta(hours=1)

            for platform in self.social_media_platforms:
                platform.publish(content.title, content.caption, content.image, publish_time)

    def track_engagement(self):
        for platform in self.social_media_platforms:
            engagement = platform.get_engagement()
            self.engagement_metrics[platform] = engagement

    def personalize_content(self, user_preferences):
        for content in self.content:
            for preference in user_preferences:
                if preference in content.caption['text']:
                    content.add_personalization(preference)

    def generate_recommendations(self):
        recommendations = set()
        for content in self.content:
            if content.personalization:
                for preference in content.personalization:
                    recommendations.add(preference)

        return recommendations

    def collect_trending_topics(self):
        trending_topics = []
        for platform in self.social_media_platforms:
            topics = platform.get_trending_topics()
            trending_topics.extend(topics)

        return trending_topics


class SocialMediaPlatform:
    def __init__(self, name):
        self.name = name

    def publish(self, title, caption, image, publish_time):
        # Integration with social media APIs to publish content
        print(f"Publishing on {self.name}:")
        print(f"Title: {title}")
        print(f"Caption: {caption['text']}")
        print(f"Image: {image}")
        print(f"Scheduled time: {publish_time}")
        print()

    def get_engagement(self):
        # Tracking engagement metrics using social media APIs
        return random.randint(1, 1000)

    def get_trending_topics(self):
        # Collecting real-time trends and topics from social media platforms
        return ['trending1', 'trending2', 'trending3']


# Example usage
platform1 = SocialMediaPlatform('Facebook')
platform2 = SocialMediaPlatform('Instagram')
platform3 = SocialMediaPlatform('Twitter')
platform4 = SocialMediaPlatform('LinkedIn')

scheduler = ContentScheduler([platform1, platform2, platform3, platform4])

# Collecting relevant content
scheduler.collect_content(['python', 'programming'])
print('Collected Content:')
for content in scheduler.content:
    print(f"Title: {content.title}")
    print(f"Description: {content.description}")
    print(f"Link: {content.link}")
    print()

# Generating captions
scheduler.generate_captions()
print('Content with Captions:')
for content in scheduler.content:
    print(f"Title: {content.title}")
    print(f"Description: {content.description}")
    print(f"Link: {content.link}")
    print(f"Caption: {content.caption}")
    print()

# Modifying images
scheduler.modify_images()
print('Content with Modified Images:')
for content in scheduler.content:
    print(f"Title: {content.title}")
    print(f"Description: {content.description}")
    print(f"Link: {content.link}")
    print(f"Caption: {content.caption}")
    print(f"Image: {content.image}")
    print()

# Scheduling and publishing content
scheduler.schedule_content()

# Tracking engagement metrics
scheduler.track_engagement()
print('Engagement Metrics:')
for platform, engagement in scheduler.engagement_metrics.items():
    print(f"{platform.name}: {engagement}")
print()

# Personalizing content based on user preferences
user_preferences = ['python', 'AI']
scheduler.personalize_content(user_preferences)
print('Content with Personalization:')
for content in scheduler.content:
    print(f"Title: {content.title}")
    print(f"Description: {content.description}")
    print(f"Link: {content.link}")
    print(f"Caption: {content.caption}")
    print(f"Image: {content.image}")
    print(f"Personalization: {content.personalization}")
    print()

# Generating content recommendations
recommendations = scheduler.generate_recommendations()
print('Personalized Content Recommendations:')
print(recommendations)
print()

# Collecting trending topics
trending_topics = scheduler.collect_trending_topics()
print('Trending Topics:')
print(trending_topics)