import sys
from confluent_kafka import KafkaError, KafkaException
from csle_common.dao.emulation_config.emulation_env_state import EmulationEnvState
import csle_collector.constants.constants as constants
from csle_common.metastore.metastore_facade import MetastoreFacade

if __name__ == '__main__':
    emulation_env_config = MetastoreFacade.get_emulation("csle-level9-001")
    emulation_env_config.create_consumer()
    consumer = emulation_env_config.consumer
    while True:
        msg = consumer.poll(timeout=2.0)
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
                print(f"received msg, topic:{msg.topic()}, partition: {msg.partition()}, offset: {msg.offset()}, "
                      f"key:{msg.key()}, value:{msg.value()}")
            # msg_count += 1
            # if msg_count % MIN_COMMIT_COUNT == 0:
            #     consumer.commit(asynchronous=False)