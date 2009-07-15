from ragendja.settings_post import settings
settings.add_app_media('combined-%(LANGUAGE_CODE)s.js',
                       'challenge/quicksilver.js',
                       'challenge/jquery.quickselect.js'
                       )

settings.add_app_media('combined-en.css',
                       'challenge/jquery-quickselect.css'
                       )
