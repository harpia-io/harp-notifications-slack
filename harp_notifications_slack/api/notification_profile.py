from logger.logging import service_logger
import traceback
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
import harp_notifications_slack.settings as settings
from harp_notifications_slack.logic.notification_processor import NotificationProcessor
from typing import Optional

log = service_logger()

router = APIRouter(prefix=settings.URL_PREFIX)


class SlackNotification(BaseModel):
    slack_channel: str
    title: Optional[str]
    text: Optional[str]
    button_url: Optional[str]
    facts: Optional[dict]
    image_url: Optional[str]
    image_body: Optional[str]


@router.post('/notifications/slack')
async def create_notification(row_data: SlackNotification):
    """
    Create new notification
    """

    data = row_data.dict()

    log.info(msg=f"Received request to send notification to Slack\n{data}")

    try:
        processor = NotificationProcessor(slack_channel=data['slack_channel'])
        processor.send_notification(
            title=data['title'],
            text=data['text'],
            button_url=data['button_url'],
            facts=data['facts'],
            image_url=data['image_url'],
            image_body=data['image_body']
        )

        return 'Notification has been sent'
    except Exception as err:
        log.error(msg=f"Can`t process event\nERROR: {err}\nStack: {traceback.format_exc()}")

        raise HTTPException(status_code=500, detail=f"Backend error: {err}")
