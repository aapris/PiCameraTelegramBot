import argparse
import datetime
import logging
import os
import time
from functools import wraps
from io import BytesIO

from telegram import ChatAction
from telegram.ext import CommandHandler
from telegram.ext import Updater

try:
    import picamera

    inpi = True
except ModuleNotFoundError:
    from PIL import Image, ImageDraw

    inpi = False


def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        def command_func(update, context, *args, **kwargs):
            context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return func(update, context, *args, **kwargs)

        return command_func

    return decorator


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--log", dest="log", choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                        default='ERROR', help="Set the logging level")
    parser.add_argument('-t', '--token', help='Telegram bot token')
    parser.add_argument('-d', '--delay', type=float, help='Warm up delay in seconds')
    args = parser.parse_args()
    if args.log:
        logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=getattr(logging, args.log))
    return args


@send_action(ChatAction.UPLOAD_PHOTO)
def photo(update, context):
    bio = BytesIO()
    bio.name = datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ.jpg')
    if inpi:
        with picamera.PiCamera() as camera:
            camera.start_preview()
            time.sleep(2)  # warm up delay
            camera.capture(bio, format='jpeg')
    else:  # Running in other system
        im = Image.new('RGB', (100, 30), color=(73, 109, 137))
        d = ImageDraw.Draw(im)
        d.text((10, 10), "Sample photo", fill=(255, 255, 0))
        im.save(bio, 'JPEG')
        time.sleep(2)  # pseudo warm up delay
    bio.seek(0)
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=bio)


def help(update, context):
    help_msg = '\n'.join([
        'Available commands:',
        '/photo Get photo from picamera',
        '/help This message'
    ])
    context.bot.send_message(chat_id=update.effective_chat.id, text=help_msg)


def main():
    args = get_args()
    if args.token is not None:
        token = args.token
    else:
        token = os.getenv('CAMBOT_TOKEN')
        if token is None:
            print('You must give bot token with --token argument or in CAMBOT_TOKEN environment variable')
            exit(1)

    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher

    photo_handler = CommandHandler('photo', photo)
    dispatcher.add_handler(photo_handler)

    help_handler = CommandHandler('help', help)
    dispatcher.add_handler(help_handler)

    updater.start_polling()


if __name__ == '__main__':
    main()
