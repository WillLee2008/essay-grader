import streamlit as st
from openai import OpenAI
from docx import Document
import io

st.set_page_config(page_title="文学作品评分", layout="centered")
st.title("文学作品评分")

client = OpenAI(
    api_key="7844b38cf9db446bb4522f1d8c4c2139.0MVYMANfxQj1AEr9",
    base_url="https://open.bigmodel.cn/api/paas/v4"
)

RUBRIC = """请对以下文学作品进行专业评分。评分维度：
1. 情感深度（25分）：情感是否真实、有层次
2. 语言表现力（25分）：用词是否精准、有文学质感
3. 意象与想象（25分）：意象是否独特、有感染力
4. 结构与节奏（25分）：整体结构是否完整、节奏是否得当

请先给出各维度得分，再给出总分（满分100），最后附上200字以内的总评。
作品内容如下："""

uploaded_file = st.file_uploader("上传 Word 文件 (.docx)", type=["docx"])

content = st.text_area("或者直接粘贴作品", height=300, placeholder="在这里输入或粘贴文学作品...")

if uploaded_file is not None:
    try:
        doc = Document(io.BytesIO(uploaded_file.getvalue()))
        content = "\n".join([para.text for para in doc.paragraphs])
        st.success(f"已读取：{uploaded_file.name}，共 {len(content)} 字符")
        st.text_area("文件内容预览", value=content, height=200, disabled=True)
    except Exception as e:
        st.error(f"读取 Word 文件失败：{e}")

if st.button("开始评分", type="primary"):
    if not content.strip():
        st.warning("请先输入作品内容或上传 Word 文件。")
    else:
        with st.spinner("正在评分..."):
            try:
                response = client.chat.completions.create(
                    model="glm-4-flash",
                    messages=[{"role": "user", "content": RUBRIC + "\n\n" + content}],
                    temperature=0.3
                )
                st.markdown("### 评分结果")
                st.write(response.choices[0].message.content)
            except Exception as e:
                st.error(f"评分失败：{e}")
