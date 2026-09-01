import httpx
import asyncio
import json

async def test_meeting_scenario():
    print("--- Testing Meeting Scenario ---")
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8000") as client:
        # Create Task
        resp = await client.post("/api/tasks", json={"goal": "Prepare me for tomorrow's meeting with Rahul"})
        print("Create Task:", resp.status_code, resp.json())
        task_id = resp.json()["task_id"]
        
        # Wait a bit
        await asyncio.sleep(2)
        
        # Check Task
        resp = await client.get(f"/api/tasks/{task_id}")
        print("Task State:", resp.status_code, resp.json()["status"])
        
async def test_finance_scenario():
    print("--- Testing Finance Scenario ---")
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8000") as client:
        # Create Task
        resp = await client.post("/api/tasks", json={"goal": "Handle the pending invoice if it is within my spending policy."})
        print("Create Task:", resp.status_code, resp.json())
        task_id = resp.json()["task_id"]
        
        # Wait for it to hit approval
        for _ in range(5):
            await asyncio.sleep(1)
            resp = await client.get(f"/api/tasks/{task_id}")
            if resp.json()["status"] == "waiting_approval":
                break
                
        task_data = resp.json()
        print("Task State:", task_data["status"])
        
        if task_data["status"] == "waiting_approval":
            approval_id = task_data["approval"]["approval_id"]
            print(f"Approving {approval_id}")
            resp = await client.post(f"/api/tasks/{task_id}/approve", json={"approval_id": approval_id})
            print("Approve response:", resp.status_code, resp.json())
            
        await asyncio.sleep(2)
        resp = await client.get(f"/api/tasks/{task_id}")
        print("Final Task State:", resp.json()["status"], "Result:", resp.json().get("result", {}).get("transaction_hash", "None"))

async def main():
    await test_meeting_scenario()
    await test_finance_scenario()

if __name__ == "__main__":
    asyncio.run(main())
