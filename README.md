# 建表

```sql
CREATE TABLE furnitures(
  aid bigint,
  time bigint,
  neighborhood text,
  title text,
  url text,
  price bigint,
	PRIMARY KEY (aid)
);

CREATE TABLE imgs(
  aid bigint,
  img text,
	FOREIGN KEY (aid) REFERENCES furnitures(aid)
);

CREATE TABLE imgs_3000(
  aid bigint,
  img text,
	FOREIGN KEY (aid) REFERENCES furnitures(aid)
);

CREATE UNIQUE INDEX furniture_aid_idx ON furnitures (aid);

COPY furnitures (time, neighborhood, title, url, price, aid) FROM 'furnitures.csv' CSV HEADER;
COPY imgs (img, aid) FROM 'imgs.csv' CSV HEADER;
COPY imgs_3000 (img, aid) FROM '3000_imgs.csv' CSV HEADER;
```

# 构建server

```bash
mkdir mcp_server
cd mcp_server
# python>=3.10，否则不兼容mcp包
uv python pin 3.12
uv init
uv add "mcp[cli]"
uv venv
source .venv/bin/activate

# 测试server
npx -y @modelcontextprotocol/inspector uv run image_analyzer.py
```

servers_config.json的配置和image_analyzer.py的绝对路径要改一下

# 测试

```python
python dbagent.py
```

找出title中包含“wooden”且图片中包含粉色椅子的家具的最小价格。

prompt示例：

我需要你找出title中包含“wooden”且图片中包含粉色椅子的家具的最小价格。为此，你可能需要：1.找出title中包含“wooden”的所有家具，按价格升序排序；2.调用工具依次分析它们对应的图片，看看是否有粉色椅子。对于每个家具，你可以只查看它的一张图片。

任务比较复杂，需要进行多轮对话去引导llm。比如可以拆解成：

调用工具查看数据库中所有的表。

找出title中包含“wooden”的所有家具，按价格升序排序。

依次调用工具分析它们对应的图片，看看是否有粉色椅子。

# todo

1.解决cleanup的asyncio报错

2.分析图片的server换成本地小模型

3.完善system prompt