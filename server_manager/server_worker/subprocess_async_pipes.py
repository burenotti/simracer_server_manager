import asyncio
import typing

from abstract_execution_policy import (
	AbstractAsyncReader,
	AbstractAsyncWriter,
)


class SubprocessAsyncReader(AbstractAsyncReader):

	def __init__(self, reader: asyncio.StreamReader):
		self._reader = reader

	async def read(self, n: int = -1) -> bytes:
		return await self._reader.read(n)

	async def read_until(self, stop: bytes):
		return await self._reader.readuntil(stop)

	async def close(self):
		pass

	@property
	def encoding(self) -> str:
		return 'utf-8'

	@property
	def at_eof(self) -> bool:
		return self._reader.at_eof()

	@property
	def closed(self):
		return self.at_eof


class SubprocessAsyncWriter(AbstractAsyncWriter):

	def __init__(self, writer: asyncio.StreamWriter):
		self._writer = writer

	async def write(self, data: bytes) -> None:
		self._writer.write(data)
		await self._writer.drain()

	async def write_lines(self, data: typing.Iterable[bytes]) -> None:
		self._writer.writelines(data)
		await self._writer.drain()

	async def close(self) -> None:
		return await self._writer.wait_closed()

	@property
	def encoding(self) -> str:
		return 'utf-8'

	@property
	def is_closed(self) -> bool:
		return self._writer.is_closing()
