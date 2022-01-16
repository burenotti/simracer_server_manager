import abc

from asyncio import subprocess
from typing import Callable

from abstract_execution_policy import AbstractExecutionPolicy


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
	async def set_stdout_handler(self, *args, **kwargs) -> Callable[[], None]:
		pass

	@abc.abstractmethod
	async
