# TAIJI: MCP-based Multi-Modal Data Analytics on Data Lakes

The variety of data in data lakes presents significant challenges for data analytics, as data scientists must simultaneously analyze multi-modal data, including structured, semi-structured, and unstructured data. While Large Language Models (LLMs) have demonstrated promising capabilities, they still remain inadequate for multi-modal data analytics in terms of accuracy, efficiency, and freshness. First, current natural language (NL) or SQL-like query languages may struggle to precisely and comprehensively capture users' analytical intent. Second, relying on a single unified LLM to process diverse data modalities often leads to substantial inference overhead. Third, data stored in data lakes may be incomplete or outdated, making it essential to integrate external open-domain knowledge to generate timely and relevant analytics results.
In [this paper](https://arxiv.org/abs/2505.11270), we envision a new multi-modal data analytics system. Specifically, we propose a novel architecture built upon the Model Context Protocol (MCP), an emerging paradigm that enables LLMs to collaborate with knowledgeable agents.

# data preparation

```sql
CREATE TABLE furniture(
  aid bigint,
  time bigint,
  neighborhood text,
  title text,
  url text,
  price bigint,
	PRIMARY KEY (aid)
);

CREATE TABLE img(
  aid bigint,
  img text,
	FOREIGN KEY (aid) REFERENCES furniture(aid)
);

CREATE TABLE img_3000(
  aid bigint,
  img text,
	FOREIGN KEY (aid) REFERENCES furniture(aid)
);

CREATE UNIQUE INDEX furniture_aid_idx ON furniture (aid);

COPY furniture (time, neighborhood, title, url, price, aid) FROM 'furnitures.csv' CSV HEADER;
COPY img (img, aid) FROM 'imgs.csv' CSV HEADER;
COPY img_3000 (img, aid) FROM '3000_imgs.csv' CSV HEADER;
```

# build server

```bash
mkdir mcp_server
cd mcp_server
# python>=3.10
uv python pin 3.12
uv init
uv add "mcp[cli]"
uv venv
source .venv/bin/activate

# to test server
npx -y @modelcontextprotocol/inspector uv run image_analyzer.py
```

# run

```python
python dbagent.py
```
