import json
import logging
import struct
import zlib
import asyncio
import os
logger = logging.getLogger(__name__)

def compress_data(data: bytes) -> bytes:
    return zlib.compress(data)

def decompress_data(data: bytes) -> bytes:
    return zlib.decompress(data)

def get_seq() -> int:
    poker_table_id = int(os.getenv("POKER_TABLE_ID", "1"))
    hands_played = int(os.getenv("HANDS_PLAYED", "0"))
    return poker_table_id * 100 + hands_played + 1 + 65535

async def send_tcp_message_async(message: dict, timeout: float = 15.0) -> tuple[bool, str, str] | None:
    try:
        host = os.getenv("HOST_QS", "127.0.0.1")
        port = int(os.getenv("PORT_QS", "12345"))

        print(f"[INFO] Connecting to {host}:{port} with timeout={timeout}")
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port), timeout=timeout
        )
    except Exception as conn_error:
        return False, '', f"[连接失败] {conn_error}"

    try:
        seq = get_seq()
        raw_json = json.dumps(message, separators=(',', ':'), ensure_ascii=False).encode('utf-8')

        # 添加序列号到前4字节
        data_with_seq = struct.pack('<I', seq) + raw_json
        compressed = compress_data(data_with_seq)

        # 包装成 size(int32) + 数据格式
        data_to_send = struct.pack('<I', len(compressed)) + compressed

        print(f"[INFO] Sending message with seq={seq}, size={len(data_to_send)}")
        writer.write(data_to_send)
        await writer.drain()

        print(f"[INFO] Waiting for response")
        size_data = await asyncio.wait_for(reader.readexactly(4), timeout=timeout)
        size = struct.unpack('<I', size_data)[0]

        compressed_reply = await asyncio.wait_for(reader.readexactly(size), timeout=timeout)
        decompressed = decompress_data(compressed_reply)

        reply_seq = struct.unpack('<I', decompressed[:4])[0]
        reply_json = decompressed[4:].decode('utf-8')

        print(f"[INFO] Received response with seq={reply_seq}")

        if reply_seq != seq:
            return False, '', f"[序列号不匹配] 期待 {seq} 收到 {reply_seq}"

        return True, reply_json, 'success'
    except Exception as read_error:
        return False, '', f"[读取失败] {read_error}"
    finally:
        writer.close()
        await writer.wait_closed()