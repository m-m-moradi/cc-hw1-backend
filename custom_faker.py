import os
import django
import datetime
from faker import Faker
from django.core.files import File

from tempfile import TemporaryFile
import decouple

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


DOTENV_FILE = os.environ.get("ENV_FILE", None)
if DOTENV_FILE:
    env_config = decouple.Config(decouple.RepositoryEnv(DOTENV_FILE))
else:
    env_config = decouple.Config(decouple.RepositoryEmpty())

faker = Faker()
Faker.seed(0)
deep_ai_key = env_config("DEEP_AI", default=None, cast=str)
print(deep_ai_key)
print({'api-key': deep_ai_key})

story_num = env_config("STORY_NUMBER", default=20, cast=int)
picture_num = env_config("PICTURE_NUMBER", default=20, cast=int)
fake_story = env_config("FAKE_STORY", default=True, cast=bool)
fake_picture = env_config("FAKE_PICTURE", default=True, cast=bool)

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
        with TemporaryFile('wb+') as picture_file:
            picture_file.write(response.content)
            picture = models.Picture(
                published_status=models.ACCEPTED,
                uploader=faker.name(),
                title=f'{rand_word()} is such a amazing {rand_word()}.',
            )
            picture.image.save(file_name, File(picture_file))
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
