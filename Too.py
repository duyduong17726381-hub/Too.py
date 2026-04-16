import os, asyncio, random
from telethon import TelegramClient, events, errors

API_ID = 37371786
API_HASH = '29ad413d32ffcdd5fa6d799964e9dd66'
SESSION_NAME = 'vip_session'

active = True
spam_speed = 1.0
OWNER_ID = 6204301614
cam_targets = set()
running_tasks = []

VAN_MOI = [
    "th ngu đú:))", "ngôn ngữ tật ơi", "th ngu", "cn đĩ mẹ m", "kh gõ cả nhà m die",
    "bố th tộc", "phố bẩn đú à", "treo với cha đê", "alo e ei", "dit me m", "sua e ei",
    "delay a", "coi cha dit chet cn di me m", "cha dit cn gai me m tu trong nha ra toi duong hbt",
    "cha si nhuc cha doggy con gai me m nhu con cho", "m hieu canh do kh th mo coi",
    "cha choi cht cn di me m", "phố bẩn gặp cha no1 phải chết coăn ạ", "th ngu spam đi",
    "hw đú đòi ăn cha à", "thời cha còn on meta thì bọn đú m ở đâu",
    "thời cha còn bên meta cha dùng bot sĩ nhục bọn đua như m mà", "th ngu ei",
    "địt mẹ mi", "sủa cha coi", "hw đú à w", "bà già m die à.", "đú voiqs cha kh coăn ei",
    "con đĩ phố bẩn loạn ngôn chạy kìa", "rớt à em hw yếu v phố=))=))", "th yếu đuối ei=))=))",
    "đàn bà à w=))=))", "123 rớt à ngôn đâu e=))=))", "chó ngu 36 kìa=))=))", "chó ngu 🤪",
    "sủa nhiều lên", "đĩ cụ mày con chó", "não ngu + tật nguyền hả e", "cào chậm thế e cào nhanh lên",
    "tay cutk hay gid mà rặn ngôn lâu thế hả e", "chó ngu vậy", "não tật hả hay gì mà rặn ngôn lâu thế",
    "tật hả e", "não thối hả", "đĩ ma may ne con cho ngu", "đú với ai vậy e", "sao e tật ngôn thế",
    "cào phím gì lâu vậy hả e", "buồn cười vcl", "hahahahahhaha", "chó ngu 🐮"
]

def clear_tasks():
    global running_tasks
    for t in running_tasks:
        t.cancel()
    running_tasks = []

async def main():
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    try:
        await client.start()
        print("READY")
        
        @client.on(events.NewMessage)
        async def handler(event):
            global active, spam_speed, running_tasks
            if event.sender_id != OWNER_ID:
                return
            
            m = event.raw_text
            chat_id = event.chat_id
            
            if m == '/on':
                active = True
                await event.edit("✔")
                return
            
            if m == '/off':
                active = False
                clear_tasks()
                await event.edit("✘")
                return
                
            if m == '/dung':
                clear_tasks()
                await event.delete()
                return

            if not active: return

            if m.startswith('/tocdo'):
                try:
                    spam_speed = float(m.split()[1])
                    await event.delete()
                except: pass
                
            if m.startswith('/war'):
                try:
                    tid = int(m.split()[1])
                    await event.delete()
                    async def w_loop():
                        while True:
                            for cau in VAN_MOI:
                                await client.send_message(chat_id, f"[\u200b](tg://user?id={tid}){cau}")
                                await asyncio.sleep(spam_speed)
                    running_tasks.append(asyncio.create_task(w_loop()))
                except: pass
                
            if m.startswith('/cam'):
                try:
                    tid = int(m.split()[1])
                    cam_targets.add(tid)
                    await event.delete()
                except: pass
                
            if m.startswith('/uncam'):
                try:
                    tid = int(m.split()[1])
                    if tid in cam_targets: cam_targets.remove(tid)
                    await event.delete()
                except: pass

            if m.startswith('/di'):
                try:
                    text_di = m.split(maxsplit=1)[1]
                    await event.delete()
                    async def di_loop():
                        while True:
                            await client.send_message(chat_id, text_di)
                            await asyncio.sleep(spam_speed)
                    running_tasks.append(asyncio.create_task(di_loop()))
                except: pass

        @client.on(events.NewMessage)
        async def cam_handler(event):
            if active and event.sender_id in cam_targets:
                try:
                    await event.delete()
                except:
                    pass

        await client.run_until_disconnected()
    except Exception:
        await asyncio.sleep(5)
    finally:
        await client.disconnect()

if __name__ == "__main__":
    while True:
        try:
            asyncio.run(main())
        except KeyboardInterrupt:
            break
        except Exception:
            os.system("pkill -f python")
            continue
