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

async def send_tcp_message_async(message: dict, timeout: float = 60.0) -> tuple[bool, str, str] | None:
    # print(f"message={message}")
    # message = {"hand":"01746062515855485355395137","simpleRoot":{"Abstraction":"Small","Board":"9sQsKs","PlayersInfo":[{"Bet":16.0,"BetSizingObject":{"Around":0.01,"DeleteDonkBet":False,"FisrsAllIn":False,"Flop":{"Bets":[0.666667],"Raises":[1.0]},"IsAround":False,"LastAllIn":False,"NumberOfBets":4,"OnlyPreflopFoldAllAfterCallAnd2Raise":False,"Preflop":{"Bets":[0.666667],"Raises":[1.0]},"PreflopWay":0,"River":{"Bets":[0.666667],"Raises":[1.0]},"ThresholdAllIn":80,"Turn":{"Bets":[0.666667],"Raises":[1.0]},"WithoutPreflopCall":False,"WithoutPreflopColdCall":False,"WithoutPreflopLimp":False,"WithoutPreflopRaiseAfterCall":False},"Name":"Seat1","Range":"[21.16]A8o[/21.16], [61.77]A7o[/61.77], [82.73]A6o[/82.73], [0.01]A5o[/0.01], [0.06]A4o[/0.06], [0.19]A3o[/0.19], [0.05]A2o[/0.05], [99.85]K8o[/99.85], [97.35]K7o[/97.35], [12.94]K6o[/12.94], [51.85]K5o[/51.85], [82.98]K4o[/82.98], [98.12]K3o[/98.12], [96.94]K2o[/96.94], [99.79]Q8o[/99.79], [99.99]Q7o[/99.99], [97.15]Q6o[/97.15], [99.97]Q5o[/99.97], [98.46]Q4o[/98.46], [96.33]Q3o[/96.33], [100.00]Q2o[/100.00], [100.00]J8o[/100.00], [100.00]J7o[/100.00], [100.00]J6o[/100.00], [100.00]J5o[/100.00], [100.00]J4o[/100.00], [100.00]J3o[/100.00], [100.00]J2o[/100.00], [11.20]T8o[/11.20], [100.00]T7o[/100.00], [100.00]T6o[/100.00], [100.00]T5o[/100.00], [100.00]T4o[/100.00], [100.00]T3o[/100.00], [100.00]T2o[/100.00], [10.47]98o[/10.47], [100.00]97o[/100.00], [100.00]96o[/100.00], [100.00]95o[/100.00], [100.00]94o[/100.00], [100.00]93o[/100.00], [100.00]92o[/100.00], [100.00]87o[/100.00], [100.00]86o[/100.00], [100.00]85o[/100.00], [100.00]84o[/100.00], [100.00]83o[/100.00], [100.00]82o[/100.00], [43.92]76o[/43.92], [100.00]75o[/100.00], [100.00]74o[/100.00], [100.00]73o[/100.00], [100.00]72o[/100.00], [0.02]J6s[/0.02], [0.02]96s[/0.02], [8.21]65o[/8.21], [100.00]64o[/100.00], [100.00]63o[/100.00], [100.00]62o[/100.00], [0.07]J5s[/0.07], [0.36]T5s[/0.36], [0.23]95s[/0.23], [0.07]85s[/0.07], [2.42]54o[/2.42], [100.00]53o[/100.00], [100.00]52o[/100.00], [0.01]Q4s[/0.01], [0.01]J4s[/0.01], [0.07]T4s[/0.07], [100.00]94s[/100.00], [14.96]84s[/14.96], [0.04]74s[/0.04], [100.00]43o[/100.00], [100.00]42o[/100.00], [0.03]J3s[/0.03], [0.02]T3s[/0.02], [100.00]93s[/100.00], [100.00]83s[/100.00], [3.07]73s[/3.07], [0.01]63s[/0.01], [0.01]43s[/0.01], [100.00]32o[/100.00], [0.01]Q2s[/0.01], [0.09]J2s[/0.09], [2.47]T2s[/2.47], [100.00]92s[/100.00], [100.00]82s[/100.00], [100.00]72s[/100.00], [22.82]62s[/22.82], [0.01]52s[/0.01], [0.05]42s[/0.05], [0.56]32s[/0.56], [100.00]Q6s[/100.00]","Stack":512.5,"isFold":False,"isOOP":True},{"Bet":16.0,"BetSizingObject":{"Around":0.01,"DeleteDonkBet":False,"FisrsAllIn":False,"Flop":{"Bets":[0.666667],"Raises":[1.0]},"IsAround":False,"LastAllIn":False,"NumberOfBets":4,"OnlyPreflopFoldAllAfterCallAnd2Raise":False,"Preflop":{"Bets":[0.666667],"Raises":[1.0]},"PreflopWay":0,"River":{"Bets":[0.666667],"Raises":[1.0]},"ThresholdAllIn":80,"Turn":{"Bets":[0.666667],"Raises":[1.0]},"WithoutPreflopCall":False,"WithoutPreflopColdCall":False,"WithoutPreflopLimp":False,"WithoutPreflopRaiseAfterCall":False},"Name":"Seat2","Range":"[100.00]AA[/100.00], [99.99]AKo[/99.99], [100.00]AQo[/100.00], [99.96]AJo[/99.96], [90.72]ATo[/90.72], [60.89]A9o[/60.89], [17.37]A8o[/17.37], [0.24]A7o[/0.24], [8.22]A6o[/8.22], [12.83]A5o[/12.83], [11.63]A4o[/11.63], [0.01]A3o[/0.01], [100.00]AKs[/100.00], [100.00]KK[/100.00], [97.19]KQo[/97.19], [49.01]KJo[/49.01], [46.22]KTo[/46.22], [34.30]K9o[/34.30], [0.17]K8o[/0.17], [0.02]K7o[/0.02], [0.02]K6o[/0.02], [100.00]AQs[/100.00], [99.98]KQs[/99.98], [100.00]QQ[/100.00], [5.84]QJo[/5.84], [16.14]QTo[/16.14], [4.76]Q9o[/4.76], [99.98]AJs[/99.98], [98.11]KJs[/98.11], [37.80]QJs[/37.80], [100.00]JJ[/100.00], [14.36]JTo[/14.36], [22.38]J9o[/22.38], [9.64]J8o[/9.64], [99.74]ATs[/99.74], [94.78]KTs[/94.78], [30.16]QTs[/30.16], [19.71]JTs[/19.71], [99.51]TT[/99.51], [27.58]T9o[/27.58], [25.93]T8o[/25.93], [84.29]A9s[/84.29], [53.63]K9s[/53.63], [47.00]Q9s[/47.00], [6.22]J9s[/6.22], [36.19]T9s[/36.19], [99.92]99[/99.92], [14.50]98o[/14.50], [9.34]97o[/9.34], [48.35]A8s[/48.35], [36.81]K8s[/36.81], [35.02]Q8s[/35.02], [62.48]J8s[/62.48], [39.01]T8s[/39.01], [39.35]98s[/39.35], [70.39]88[/70.39], [19.33]87o[/19.33], [13.79]A7s[/13.79], [36.19]K7s[/36.19], [0.27]Q7s[/0.27], [29.99]J7s[/29.99], [36.95]T7s[/36.95], [38.80]97s[/38.80], [44.29]87s[/44.29], [35.09]77[/35.09], [22.16]76o[/22.16], [40.02]A6s[/40.02], [18.52]K6s[/18.52], [0.85]Q6s[/0.85], [0.35]J6s[/0.35], [35.74]T6s[/35.74], [50.83]96s[/50.83], [42.29]86s[/42.29], [41.25]76s[/41.25], [30.64]66[/30.64], [1.47]65o[/1.47], [68.73]A5s[/68.73], [0.20]K5s[/0.20], [0.33]Q5s[/0.33], [0.12]J5s[/0.12], [21.36]T5s[/21.36], [26.68]95s[/26.68], [35.37]85s[/35.37], [13.23]75s[/13.23], [58.44]65s[/58.44], [0.48]55[/0.48], [48.50]A4s[/48.50], [19.80]K4s[/19.80], [0.01]Q4s[/0.01], [5.10]J4s[/5.10], [2.71]T4s[/2.71], [10.36]84s[/10.36], [2.58]74s[/2.58], [28.44]64s[/28.44], [37.42]54s[/37.42], [21.74]A3s[/21.74], [0.52]K3s[/0.52], [0.05]Q3s[/0.05], [17.54]63s[/17.54], [28.30]53s[/28.30], [32.70]43s[/32.70], [28.33]A2s[/28.33], [0.01]K2s[/0.01], [0.04]Q2s[/0.04], [0.01]J2s[/0.01], [0.05]52s[/0.05]","Stack":406.5,"isFold":False,"isOOP":False}],"Version":105,"numPlayers":2},"site":9}
    logging.info(f"message: {message}")
    try:
        host = os.getenv("HOST_QS", "127.0.0.1")
        port = int(os.getenv("PORT_QS", "12345"))
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port), timeout=timeout
        )
        logging.info(f"Connected to {host}:{port} with timeout={timeout}")
    except Exception as conn_error:
        logging.info(f"Failed on Connecting to QSolver Bridge: {conn_error}")
        return False, '', f"[连接失败] {conn_error}"

    try:
        seq = get_seq()
        logging.info(f"Seq {seq}")
        logging.info(f"Request {message}")
        raw_json = (json.dumps(message, separators=(',', ':'), ensure_ascii=False)+"\n").encode('utf-8')

        # 添加序列号到前4字节
        data_with_seq = struct.pack('>I', seq) + raw_json
        compressed = compress_data(data_with_seq)

        # 包装成 size(int32) + 数据格式
        data_to_send = struct.pack('>I', len(compressed)) + compressed

        print(f"[INFO] Sending message with seq={seq}, size={len(data_to_send)}")
        writer.write(data_to_send)
        await writer.drain()

        print(f"[INFO] Waiting for response")
        size_data = await asyncio.wait_for(reader.readexactly(4), timeout=timeout)
        size = struct.unpack('>I', size_data)[0]
        compressed_reply = await asyncio.wait_for(reader.readexactly(size), timeout=timeout)
        decompressed = decompress_data(compressed_reply)

        reply_seq = struct.unpack('>I', decompressed[:4])[0]
        reply_json = decompressed[4:].decode('utf-8')

        print(f"[INFO] Received response with seq={reply_seq}")

        if reply_seq != seq:
            return False, '', f"[序列号不匹配] 期待 {seq} 收到 {reply_seq}"
        logging.info(f"Reply {reply_seq}")
        return True, json.loads(reply_json), 'success'
    except Exception as read_error:
        return False, '', f"[读取失败] {read_error}"
    finally:
        writer.close()
        await writer.wait_closed()
        pass