import abc


class AbstractAsyncReader(abc.ABC):

	@abc.abstractmethod
	async def read(self, n: int = -1) -> bytes:
		pass

	@abc.abstractmethod
	async def read_until(self, stop: str):
		pass

	async def read_line(self):
		return await self.read_until('\n')

	@abc.abstractmethod
	async def close(self):
		pass

	@abc.abstractmethod
	@property
	def encoding(self) -> str:
		pass

	@abc.abstractmethod
	@property
	def eof(self) -> bool:
		pass

	@abc.abstractmethod
	@property
	def closed(self):
		pass


class AbstractAsyncWriter(abc.ABC):

	@abc.abstractmethod
	async def write(self, data: bytes) -> int:
		pass

	@abc.abstractmethod
	async def write_line(self, data: bytes) -> int:
		pass

	@abc.abstractmethod
	@property
	def encoding(self) -> str:
		pass

	@abc.abstractmethod
	@property
	def eof(self) -> bool:
		pass

	@abc.abstractmethod
	@property
	def closed(self):
		pass


class AbstractExecutionPolicy(abc.ABC):

	@abc.abstractmethod
	async def run(self, *args, **kwargs):
		pass

	@abc.abstractmethod
	@property
	def stdin(self) -> AbstractAsyncReader:
		pass

	@abc.abstractmethod
	@property
	def stdout(self) -> AbstractAsyncWriter:
		pass

	@abc.abstractmethod
	@property
	def environment(self) -> dict[str, str]:
		pass
	
