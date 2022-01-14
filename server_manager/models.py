import datetime
import os
import pathlib
from typing import Any

import aiofiles
from loguru import logger
from pydantic import BaseModel


class ConfigFile(BaseModel):
	path: pathlib.Path
	content: str
	encoding: str

	@logger.catch
	async def write(self, prefix: pathlib.Path):
		path = (prefix / self.path).resolve()

		if not str(path).startswith(str(prefix)):
			# Exception if result path is not in prefix dir
			raise ValueError(
				"All creating configuration files must be located in "
				"`prefix` dir or its sub-dirs."
			)

		path.mkdir(parents=True, exist_ok=True)

		async with aiofiles.open(path, mode='w', encoding=self.encoding) as cfg_file:
			await cfg_file.write(self.content)


class GameInfo(BaseModel):
	id: int
	label: str


class OwnerInfo(BaseModel):
	id: int
	first_name: str
	last_name: str


class TaskSchedule(BaseModel):
	startup_at: datetime.datetime
	startup_confirmation_deadline_s: int
	max_restart_count: int
	current_restart_tries: int
	hard_deadline_s: int


class TaskConfiguration(BaseModel):
	environment: dict[str, str]
	files: list[ConfigFile]


class TaskExecutionPolicy(BaseModel):
	type: str
	additional: dict[str, Any]


class Task(BaseModel):
	version: int
	id: int
	game: GameInfo
	owner: OwnerInfo
	schedule: TaskSchedule
	configuration: TaskConfiguration
	execution_policy: TaskExecutionPolicy


class TaskError(BaseModel):

	task: Task
