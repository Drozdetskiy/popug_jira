import pika

from popug_sdk.conf.amqp import AMQPSettings


def get_connection_params(_config: AMQPSettings) -> pika.ConnectionParameters:
    credentials = pika.PlainCredentials(
        _config.username,
        _config.password,
    )
    return pika.ConnectionParameters(
        _config.host,
        _config.port,
        _config.virtual_host,
        credentials,
    )
