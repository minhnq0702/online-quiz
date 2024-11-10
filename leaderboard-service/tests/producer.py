import asyncio
import json

from aiokafka import AIOKafkaProducer

# ! THIS IS SIMULATION FOR ANSWER SERVICE AFTER CACULATE SCORE AND PRODUCE SCORE TO KAFKA


async def send_score_update(producer, score_data):
    topic = 'score_updates'
    try:
        for i in range(10):
            await producer.send_and_wait(
                topic,
                key=str(score_data['user_id']).encode('utf-8'),
                value=json.dumps(score_data).encode('utf-8'),
            )
            print(f"Score update sent: {score_data}")
            await asyncio.sleep(0.5)
    except Exception as e:
        print(f"Failed to send score update: {e}")

# Example score update data
score_update_user2 = {
    "quiz_id": "1",
    "user_id": "2",
    'score': 300,
    'timestamp': '2023-10-01T12:34:56Z'
}

score_update_user_temp = {
    "quiz_id": "1",
    "user_id": None,
    'score': 10,
    'timestamp': '2023-10-01T12:34:56Z'
}


async def main():
    producer = AIOKafkaProducer(
        bootstrap_servers='localhost:9092'
    )
    await producer.start()
    try:
        jobs = [send_score_update(producer, score_update_user2)]
        for i in range(2000):
            update2 = send_score_update(producer, {
                **score_update_user_temp,
                "user_id": str(i),
            })
            jobs.append(update2)

        await asyncio.gather(*jobs)
    finally:
        await producer.stop()

# Run the main function
asyncio.run(main())
