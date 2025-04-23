from mcp.server import FastMCP # type: ignore
import base64
from openai import OpenAI
from dotenv import load_dotenv # type: ignore

load_dotenv()

## 初始化 FastMCP 服务器
app = FastMCP('image-analyzer')


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


@app.tool()
async def analyze_image(image_path: str) -> str:
    """
    分析图片

    Args:
        path: 请求的图片路径

    Returns:
        图片内容
    """
    image_path = "/Users/liuquehuan/Downloads/科研/Agent/DBAgent/" + image_path
    base64_image = encode_image(image_path)
    client = OpenAI()

    response = client.chat.completions.create(
        model="o3",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "这张图片里有什么?请简单描述描述，不超过20字"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]
    )
    # print(response.choices[0].message.content)
    return response.choices[0].message.content


if __name__ == "__main__":
    app.run(transport='stdio')
