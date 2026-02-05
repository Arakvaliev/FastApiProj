from fastapi import FastAPI
import uvicorn
import asyncio
import time

app = FastAPI()

async def calculate_square(num: int, delay: float):
    start_time = time.time()
    await asyncio.sleep(delay)
    square = num*num
    end_time = time.time() - start_time
    return {
        "number": num,
        "square": square,
        "delay": delay,
        "time": round(end_time, 2)
    }

@app.post('/calculate/')
async def calculate(request: dict):
    numbers = request.get("numbers", [])
    delays = request.get("delays", [])

    start_time = time.time()

    tasks = []
    for num, delay in zip(numbers, delays):
        task = calculate_square(num, delay)
        tasks.append(task)

    result = await asyncio.gather(*tasks)

    total_time = time.time() - start_time
    sequential_time = sum(delays)

    return {
            "results": result,
            "total_time": round(total_time, 2),
            "parallel_faster_than_sequential": total_time < sequential_time
        }
    

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port = 8000)
