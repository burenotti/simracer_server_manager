import abc
import enum

from asyncio import subprocess
from typing import Callable

from abstract_execution_policy import AbstractExecutionPolicy


class StreamType(enum.Enum):
	STDOUT = "stdout"
	STDERR = "stderr"
	STDIN = "stdin"


class AbstractServerWorker(abc.ABC):

	@abc.abstractmethod
	@property
	def execution_policy(self) -> AbstractExecutionPolicy:
		pass

	@abc.abstractmethod
	@execution_policy.setter
	def execution_policy(self, new_policy: AbstractExecutionPolicy) -> None:
		pass

	@abc.abstractmethod
	async def run(self, *args, **kwargs):
		pass

	@abc.abstractmethod
	def set_stream_handler(
		self,
		stream: StreamType,
		condition: Callable[[...], None],
		*args,
		**kwargs
	):
		pass
