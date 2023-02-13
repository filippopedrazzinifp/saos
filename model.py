from langchain import OpenAI
from langchain.chains import ConversationChain, LLMChain
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate


def load_chatgpt_chain():
    template = """
        Assistant is a large language model trained by OpenAI.
        Assistant is designed to be able to assist with a wide range of tasks,
        from answering simple questions to providing in-depth explanations and
        discussions on a wide range of topics. As a language model, Assistant
        is able to generate human-like text based on the input it receives,
        allowing it to engage in natural-sounding conversations and provide
        responses that are coherent and relevant to the topic at hand.
        Assistant is constantly learning and improving, and its
        capabilities are constantly evolving. It is able to process and understand
        large amounts of text, and can use this knowledge to provide accurate and
        informative responses to a wide range of questions. Additionally, Assistant
        is able to generate its own text based on the input it receives, allowing it
        to engage in discussions and provide explanations and descriptions on a wide range of topics.
        Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide
        valuable insights and information on a wide range of topics. Whether you need help with a
        specific question or just want to have a conversation about a particular topic, Assistant is here to assist.

        {history}
        Human: {input}
        Assistant:
    """

    prompt = PromptTemplate(input_variables=["history", "input"], template=template)

    chain = LLMChain(
        llm=OpenAI(temperature=0),
        prompt=prompt,
        verbose=True,
        memory=ConversationBufferWindowMemory(k=2),
    )
    return chain


def load_conversation_chain():
    """Logic for loading the chain you want to use should go here."""
    llm = OpenAI(temperature=0)
    chain = ConversationChain(llm=llm)
    return chain


def generate_response(text):
    chain = load_chatgpt_chain()
    response = chain.run(input=text)
    return response


def summarize(text):
    llm = OpenAI(temperature=0)
    doc = Document(page_content=text)
    chain = load_summarize_chain(llm, chain_type="map_reduce")
    summary = chain.run([doc])
    return summary
