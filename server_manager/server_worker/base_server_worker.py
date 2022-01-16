from typing import Callable

from .abstract_server_worker import (
	AbstractServerWorker,
	StreamType,
	AbstractExecutionPolicy
)


class BaseStreamHandler:

	def __init__(
		self,
		stream_type: StreamType,
		condition: Callable[[...], bool],
		callback: Callable[[...], None],
	):
		self.callback = callback
		self.condition = condition
		self.stream_type = stream_type

	def __call__(self, *args, **kwargs) -> bool:
		if self.condition(*args, **kwargs):
			self.callback(*args, **kwargs)
			return True
		else:
			return False


class BaseServerWorker(AbstractServerWorker):

	def __init__(
		self,
	):
		self.__handlers: list[BaseStreamHandler] = []
		self.__exec_policy: AbstractExecutionPolicy | None = None

	@property
	def execution_policy(self) -> AbstractExecutionPolicy:
		return self.__exec_policy

	@execution_policy.setter
	def execution_policy(self, value: AbstractExecutionPolicy) -> None:
		self.__exec_policy = value

	async def run(self, *args, **kwargs):
		await self.__exec_policy.run(*args, **kwargs)

	def set_stream_handler(
		self,
		stream: StreamType,
		condition: Callable[[...], bool],
		*args,
		**kwargs
	):
		def decorator(callback: Callable[[...], None]):
			handler = BaseStreamHandler(
				stream_type=stream,
				condition=condition,
				callback=callback,
			)
			self.__handlers.append(handler)
			return handler

		return decorator
