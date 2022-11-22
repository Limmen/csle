from confluent_kafka import KafkaError, KafkaException
from csle_common.dao.emulation_config.emulation_env_state import EmulationEnvState


class DefenderUpdateStateMiddleware:
    """
    Class that implements update state actions for the defender.
    """

    @staticmethod
    def update_state(s: EmulationEnvState) -> EmulationEnvState:
        """
        Updates the defender's state by measuring the emulation

        :param s: the current state
        :return: s_prime
        """
        consumer = s.emulation_env_config.consumer
        msg = consumer.poll(timeout=10.0)
        if msg is None:
            print("msg is None, no more to consume?")
        else:
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    print(f"reached end of partition: {msg.topic(), msg.partition(), msg.offset()}")
                    # # End of partition event
                    # sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                    #                  (msg.topic(), msg.partition(), msg.offset()))
                elif msg.error():
                    raise KafkaException(msg.error())
            else:
                print(f"received msg, topic:{msg.topic()}, partition: {msg.partition()}, offset: {msg.offset()}")
                # msg_count += 1
                # if msg_count % MIN_COMMIT_COUNT == 0:
                #     consumer.commit(asynchronous=False)
            s_prime = s   # TODO
            return s_prime
