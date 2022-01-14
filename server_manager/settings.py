from pydantic import BaseSettings


class Settings(BaseSettings):
	AMQP_HOST: str
	AMQP_PORT: int
	AMQP_LOGIN: str
	AMQP_PASSWORD: str
	AMQP_TASK_QUEUE: str
	AMQP_TASK_ROUTING: str
