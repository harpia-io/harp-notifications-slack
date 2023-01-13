import slack
import ssl
from harp_notifications_slack.logic.get_bot_config import bot_config

ssl._create_default_https_context = ssl._create_unverified_context


class NotificationProcessor(object):
    def __init__(self, slack_channel):
        self.slack_channel = slack_channel
        self.bot_config = self.get_bot_config()
        self.slack_client = self.create_connector()

    def get_bot_config(self):
        config = self.bot_config = bot_config(bot_name='slack')

        return config

    def create_connector(self):
        slack_token = self.bot_config['SLACK_TOKEN']
        slack_client = slack.WebClient(token=slack_token)

        return slack_client

    def slack_content(self, title, text, button_url, facts, image_url):
        message_to_send = {"channel": self.slack_channel, "blocks": []}

        if title:
            content = {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": title,
                    "emoji": True
                }
            }

            message_to_send['blocks'].append(content)

        if text:
            content = {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": text,
                    "emoji": True
                }
            }

            message_to_send['blocks'].append(content)

        if facts:
            content = {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": facts
                }
            }

            message_to_send['blocks'].append(content)

        if button_url:
            content = {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "You can check more details inside Harp Platform"
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Open Alert",
                        "emoji": True
                    },
                    "value": "click_me_123",
                    "url": button_url,
                    "action_id": "button-action"
                }
            }

            message_to_send['blocks'].append(content)

        if image_url:
            image_content = {
                "type": "image",
                "image_url": image_url,
                "alt_text": "inspiration"
            }

            message_to_send['blocks'].append(image_content)

        return message_to_send

    @staticmethod
    def generate_facts(facts):
        message_section = []
        for key, value in facts.items():
            message_section.append(f"*{key}*: {value}")

        return '\n'.join(message_section)

    def send_notification(self, title, text, button_url, facts, image_url, image_body):
        result = self.slack_client.chat_postMessage(
            **self.slack_content(
                title=title,
                text=text,
                button_url=button_url,
                facts=self.generate_facts(facts),
                image_url=image_url
            )
        )

        return result
