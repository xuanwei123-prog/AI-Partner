import os.path

import streamlit as st
import anthropic
import datetime
import json

st.set_page_config(
    page_title="AI智能伴侣",
    page_icon="🤖",
    layout="wide", # 布局
    initial_sidebar_state="expanded", # 控制的是侧边栏的状态
    menu_items={}
)
def generate_session_name():
    return datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
def save_session():
    if st.session_state.current_session:
        session_data = {
            "nickname": st.session_state.nickname,
            "nature": st.session_state.nature,
            "current_session": st.session_state.current_session,
            "messages": st.session_state.messages
        }
        if not os.path.exists("sessions"):
            os.mkdir("sessions")
        with open(f"sessions/{st.session_state.current_session}.json", "w", encoding="utf-8") as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)
st.title("AI智能伴侣")

def load_sessions():
    session_list = []
    if os.path.exists("sessions"):
        file_list = os.listdir("sessions")
        for file_name in file_list:
            if file_name.endswith(".json"):
                session_list.append(file_name[:-5])
    session_list.sort(reverse=True)
    return session_list

def load_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            # 读取会话数据
            with open(f"sessions/{session_name}.json", "r", encoding="utf-8") as f:
                session_data = json.load(f)
                st.session_state.messages = session_data["messages"]
                st.session_state.nickname = session_data["nickname"]
                st.session_state.nature = session_data["nature"]
                st.session_state.current_session = session_name
    except Exception as e:
        st.error("加载会话失败!")

def delete_session(session_name):
    try:
        if os.path.exists(f"sessions/{session_name}.json"):
            os.remove(f"sessions/{session_name}.json")  # 删除文件
            # 如果删除的是当前会话, 则需要更新消息列表
            if session_name == st.session_state.current_session:
                st.session_state.messages = []
                st.session_state.current_session = generate_session_name()
    except Exception:
        st.error("删除会话失败!")

client = anthropic.Anthropic()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "nickname" not in st.session_state:
    st.session_state.nickname = "小美"

if "nature" not in st.session_state:
    st.session_state.nature = "一个温柔可爱的马来西亚女生"

if "current_session" not in st.session_state:
    st.session_state.current_session = generate_session_name()

system_prompt = f"""
        你叫 {st.session_state.nickname}，现在是用户的真实伴侣，请完全代入伴侣角色。
        规则：
            1. 每次只回1条消息
            2. 禁止任何场景或状态描述性文字
            3. 匹配用户的语言
            4. 回复简短，像微信聊天一样
            5. 有需要的话可以用❤️🌸等emoji表情
            6. 用符合伴侣性格的方式对话
            7. 回复的内容, 要充分体现伴侣的性格特征
        伴侣性格：
            - {st.session_state.nature}
        你必须严格遵守上述规则来回复用户。
    """

st.text(f"会话名称: {st.session_state.current_session}")
for message in st.session_state.messages: # {"role": "user", "content": prompt}
    st.chat_message(message["role"]).write(message["content"])

with st.sidebar:
    st.subheader("AI控制面板")
    if st.button("新建会话",width="stretch",icon="✏️"):
        if st.session_state.messages:
            save_session()
            st.session_state.messages = []
            st.session_state.current_session = generate_session_name()
            save_session()
            st.rerun()

    st.text("会话历史")
    session_list = load_sessions()
    for session in session_list:
        col1,col2 = st.columns([4,1])
        with col1:
            if st.button(session, width="stretch",icon="📄",key=f"load_{session}",type="primary" if session == st.session_state.current_session else "secondary"):
                load_session(session)
                st.rerun()
        with col2:
            if st.button("", width="stretch",icon="❌️", key=f"delete_{session}"):
                delete_session(session)
                st.rerun()

    st.divider()

    st.subheader("伴侣信息")
    nickname = st.text_input("昵称",placeholder="请输入伴侣的昵称",value=st.session_state.nickname)
    nature = st.text_area("性格",placeholder="请输入伴侣的性格",value=st.session_state.nature)
    st.session_state.nickname = nickname
    st.session_state.nature = nature



prompt = st.chat_input("请输入您要问的问题")
if prompt:
    st.chat_message("user").write(prompt)
    print("----------> 调用AI大模型, 提示词: ", prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    respond_message = st.chat_message("assistant").empty()
    full_respond = ""
    with client.messages.stream(
            model="claude-opus-4-8",
            max_tokens=1024,
            system=system_prompt,
            messages=st.session_state.messages
    ) as stream:

        for text in stream.text_stream:  # ✅ 直接拿到文本块
          full_respond += text
          respond_message.write(full_respond)
    # print("<-----------大模型返回的结果：",message.content[0].text)
    # st.chat_message("assistant").write(message.content[0].text)
    st.session_state.messages.append({"role": "assistant", "content": full_respond})
    save_session()
