import aio_pika
import msgpack
from aio_pika import ExchangeType
from sqlalchemy import insert
from config.settings import settings
from ..actions import REGISTER_USER
from ..schema.registration import RegistrationData
from ..model.models import User, UserStatus
from src.storage.db import async_session
from src.storage.rabbit import channel_pool
from src.apps.consumer.logger import correlation_id_ctx
from datetime import datetime

async def handle_event_registration(message: RegistrationData):
    if message['action'] == REGISTER_USER:
        async with async_session() as db:
            success=False
            try:
                await db.execute(insert(User).values(
                    name=message['name'],
                    description=message['description'],
                    image=message['image'],
                    dateOfBirth=datetime.date(),
                    telegram_id=1231,
                    status=UserStatus.NO_ACTIVE
                ))
            except:
                success = False
            else:
                success = True

            async with channel_pool.acquire() as channel:  # type: aio_pika.Channel
                exchange = await channel.declare_exchange("registration", ExchangeType.TOPIC, durable=True)

                await exchange.publish(
                    aio_pika.Message(
                        msgpack.packb({
                            'register_status': success
                        }),
                        correlation_id=correlation_id_ctx.get(),
                    ),
                    routing_key=settings.USER_REGISTRATION_QUEUE_TEMPLATE.format(user_id=message['user_id']),
                )