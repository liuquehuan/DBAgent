from mcp.server import FastMCP # type: ignore
import base64
from openai import OpenAI
import time

## 初始化 FastMCP 服务器
app = FastMCP('image-analyzer')


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


@app.tool()
async def analyze_image(image_paths: list[str]) -> list[str]:
    """
    analyze images

    Args:
        image_paths: the list of paths of the images

    Returns:
        the list of descriptions of each image
    """
    start = time.time()
    results = []
    for image_path in image_paths:
        image_path = "/Users/liuquehuan/Downloads/research/Agent/DBAgent/" + image_path
        base64_image = encode_image(image_path)
        # client = OpenAI(
        #     api_key="83db886a9ca34175a97c31670216ef84.LHQrb8FovIxtIVLz",
        #     base_url="https://open.bigmodel.cn/api/paas/v4/"
        # )
        client = OpenAI(api_key="None", base_url="http://10.77.110.188:30000/v1/")
        # client = OpenAI(
        #     api_key="sk-ydWjHrxTcGAshMZRMkTdDWZ5MjRkuAXKGB40JKIMEPgbFqxl",
        #     base_url="https://api.ifopen.ai/v1/"
        # )

        response = client.chat.completions.create(
            # model="glm-4v-plus-0111",
            model="Qwen/Qwen2.5-VL-7B-Instruct",
            # model="gpt-4.1",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Provide a concise description of what is in the image, in English."},
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
        results.append(response.choices[0].message.content)
    end = time.time()
    # return end - start
    return results


if __name__ == "__main__":
    app.run(transport='stdio')
