import asyncio
import json

import aio_pika
import loguru
import pydantic

from server_manager.models import Task


class TaskAwaiter:

	def __init__(
		self,
		amqp_host: str = 'localhost',
		amqp_port: int = '5672',
		amqp_login: str = 'guest',
		amqp_password: str = 'guest',
		task_queue_name: str = 'tasks',
		loop: asyncio.AbstractEventLoop = None
	):
		if not loop:
			loop = asyncio.get_running_loop()

		self.task_queue_name = task_queue_name

		self.connection_coro = aio_pika.connect(
			login=amqp_login,
			password=amqp_password,
			host=amqp_host,
			port=amqp_port,
			loop=loop,
		)

		self.__stop_consuming = False

	async def process_task(self, message: aio_pika.IncomingMessage):
		async with message.process():
			loguru.logger.info('Begin processing incoming task')
			try:
				task: Task = Task.parse_raw(message.body, encoding='utf-8')
				loguru.logger.info('Processing task #{}'.format(task.id))
				return task
			except (json.JSONDecodeError, pydantic.ValidationError) as error:
				await self.process_invalid_message(message, error)

	async def process_invalid_message(
		self,
		message: aio_pika.IncomingMessage,
		exception: Exception
	):
		loguru.logger.error(f"Invalid message {exception}")

	async def listen(self) -> None:
		connection: aio_pika.Connection = await self.connection_coro
		channel = await connection.channel()
		queue = await channel.declare_queue(self.task_queue_name)
		exchange = await channel.declare_exchange("direct", auto_delete=True)
		await queue.bind(exchange=exchange, routing_key="tasks")
		loguru.logger.info("Listening tasks queue")
		async with queue.iterator() as queue_iter:
			async for message in queue_iter:
				task = await self.process_task(message)
				yield task


		await connection.close()
