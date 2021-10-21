import os
import django
import datetime
from faker import Faker
from django.core.files import File

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cc_hw1_backend.settings")
django.setup()

# placement of these imports are important ,don't change it
from bulletin import models
import requests
from random import randint

random_words = ['driver', 'philosophy', 'literature', 'inspection', 'shopping', 'topic',
                'cigarette', 'employee', 'music', 'software', 'advice', 'movie', 'bonus',
                'promotion', 'thanks', 'negotiation', 'nature', 'strategy', 'art', 'guest',
                'apartment', 'indication', 'awareness', 'computer', 'poet', 'city', 'psychology',
                'feedback', 'tension', 'thought', 'conclusion', 'cousin', 'recommendation',
                'county', 'intention', 'quantity', 'maintenance', 'photo', 'shirt', 'outcome',
                'replacement', 'gene', 'law', 'disaster', 'writer', 'discussion', 'effort',
                'cabinet', 'performance', 'ambition', 'camera', 'importance', 'death', 'depth',
                'obligation', 'independence', 'reflection', 'bird', 'possibility', 'hair',
                'statement', 'sister', 'bread', 'agreement', 'expression', 'area', 'priority',
                'error', 'disaster', 'percentage', 'storage', 'establishment', 'charity', 'diamond',
                'tradition', 'equipment', 'sympathy', 'consequence', 'history', 'politics', 'celebration',
                'hearing', 'world', 'physics', 'nation', 'goal', 'responsibility', 'protection', 'library',
                'drama', 'contract', 'activity', 'tension', 'event', 'initiative', 'manufacturer',
                'advertising', 'potato', 'story', 'effort']


def rand_word():
    return random_words[randint(0, len(random_words) - 1)]


# we also can use pytz package
class UTC0330(datetime.tzinfo):
    # can be configured here
    _offset = datetime.timedelta(seconds=12600)
    _dst = datetime.timedelta(0)
    _name = "+0330"

    def utcoffset(self, dt):
        return self.__class__._offset

    def dst(self, dt):
        return self.__class__._dst

    def tzname(self, dt):
        return self.__class__._name


faker = Faker()
Faker.seed(0)
deep_ai_key = os.getenv("DEEP_AI")
print(deep_ai_key)
print({'api-key': deep_ai_key})

story_num = 20
picture_num = 20
fake_story = True
fake_picture = True

if fake_story:
    for i in range(story_num):
        r = requests.post(
            "https://api.deepai.org/api/text-generator",
            data={
                'text': rand_word(),
            },
            headers={'api-key': deep_ai_key}
        )
        print(r.json())
        text = r.json()['output']

        story = models.Story(
            published_status=models.ACCEPTED,
            author=faker.name(),
            title=f'{rand_word()} is such a amazing {rand_word()}.',
            text=text,
        )
        story.save()
        for j in range(0, randint(1, 10)):
            comment = models.Comment(
                published_status=models.ACCEPTED,
                author=faker.name(),
                text=faker.paragraph(nb_sentences=7),
                content_object=story,
            )
            comment.save()
            print(f'comment #{j} done.')
        print(f'story #{i} done.')

if fake_picture:
    for i in range(picture_num):
        response = requests.get("https://picsum.photos/400/300")
        file_name = response.headers['Content-Disposition'].split(';')[1].strip().split("\"")[1]
        local_file = f'media/tmp/{file_name}'
        file = open(local_file, 'wb')
        file.write(response.content)
        file.close()
        picture = models.Picture(
            published_status=models.ACCEPTED,
            uploader=faker.name(),
            title=f'{rand_word()} is such a amazing {rand_word()}.',
        )
        picture.image.save(file_name, File(open(local_file, 'rb')))
        for j in range(0, randint(1, 10)):
            comment = models.Comment(
                published_status=models.ACCEPTED,
                author=faker.name(),
                text=faker.paragraph(nb_sentences=7),
                content_object=picture,
            )
            comment.save()
            print(f'comment #{j} done.')
        print(f'picture #{i} done.')
