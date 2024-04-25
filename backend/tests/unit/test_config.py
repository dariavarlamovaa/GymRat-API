import os
import dotenv

dotenv.load_dotenv('.env.test')


def test_read_config(test_settings):
    for key in [key for key, _ in test_settings.model_fields.items()]:
        assert str(getattr(test_settings, key)) == os.environ[key]