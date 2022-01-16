from __future__ import annotations

import asyncio
import pathlib
import shutil
from loguru import logger

from typing import TYPE_CHECKING

from abstract_execution_policy import (
	AbstractExecutionPolicy,
	AbstractAsyncWriter,
	AbstractAsyncReader,
)

from subprocess_async_pipes import (
	SubprocessAsyncReader,
	SubprocessAsyncWriter,
)

if TYPE_CHECKING:
	from .abstract_server_worker import AbstractServerWorker


class WineExecutionPolicy(AbstractExecutionPolicy):

	def __init__(
		self,
		context: AbstractServerWorker,
		wine_executable: str | pathlib.Path | None = None
	):
		self._context = context
		self._process: asyncio.subprocess.Process | None = None
		self.wine_executable = self._resolve_wine_path(wine_executable)
		self._environment: dict[str, str] = {}

	@classmethod
	def _resolve_wine_path(cls, wine_executable: str | pathlib.Path | None) -> pathlib.Path:
		if wine_executable is None:
			wine_executable = shutil.which('wine')
			if wine_executable is None:
				raise EnvironmentError(
					"Wine executable was not specified and "
					"was not found in path"
				)
			else:
				wine_executable = pathlib.Path(wine_executable).resolve()
				logger.warning(
					"Wine executable is not specified. Using wine from path."
				)
		else:
			wine_executable = pathlib.Path(wine_executable).resolve()

			if not wine_executable.exists():
				raise EnvironmentError(
					"Specified wine executable does not exists:"
				)

		logger.info(f'Using wine executable is: {wine_executable}')
		return wine_executable

	async def run(
		self,
		working_dir: pathlib.Path,
		environment: dict[str, str] = None,
		loop: asyncio.AbstractEventLoop = None
	):
		if loop is None:
			loop = asyncio.get_running_loop()

		self._environment = environment

		self._process = await asyncio.subprocess.create_subprocess_exec(
			program=self.wine_executable,

			stdin=asyncio.subprocess.PIPE,
			stdout=asyncio.subprocess.PIPE,
			env=environment,
			cwd=working_dir,
			loop=loop,
		)

	@property
	def stdin(self) -> SubprocessAsyncWriter | None:
		if self._process is not None:
			return SubprocessAsyncWriter(self._process.stdin)
		else:
			return None

	@property
	def stdout(self) -> SubprocessAsyncReader | None:
		if self._process is not None:
			return SubprocessAsyncReader(self._process.stdout)

	@property
	def environment(self) -> dict[str, str]:
		return dict(self._environment)

	def kill(self) -> None:
		self._process.kill()

	async def wait(self) -> None:
		await self._process.wait()
